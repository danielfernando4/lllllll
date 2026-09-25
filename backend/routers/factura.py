from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/factura/", response_model=None, tags=["Factura"])
def get_all_factura(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Factura)
        query = query.options(joinedload(Factura.cliente_1))
        factura_list = query.all()

        # Serialize with relationships included
        result = []
        for factura_item in factura_list:
            item_dict = factura_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if factura_item.cliente_1:
                related_obj = factura_item.cliente_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['cliente_1'] = related_dict
            else:
                item_dict['cliente_1'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            itemfactura_list = database.query(ItemFactura).filter(ItemFactura.factura_id == factura_item.id).all()
            item_dict['facturaItems'] = []
            for itemfactura_obj in itemfactura_list:
                itemfactura_dict = itemfactura_obj.__dict__.copy()
                itemfactura_dict.pop('_sa_instance_state', None)
                item_dict['facturaItems'].append(itemfactura_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Factura).all()


@router.get("/factura/count/", response_model=None, tags=["Factura"])
def get_count_factura(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Factura entities"""
    count = database.query(Factura).count()
    return {"count": count}


@router.get("/factura/paginated/", response_model=None, tags=["Factura"])
def get_paginated_factura(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Factura entities"""
    total = database.query(Factura).count()
    factura_list = database.query(Factura).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": factura_list
        }

    result = []
    for factura_item in factura_list:
        facturaItems_ids = database.query(ItemFactura.id).filter(ItemFactura.factura_id == factura_item.id).all()
        item_data = {
            "factura": factura_item,
            "facturaItems_ids": [x[0] for x in facturaItems_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/factura/search/", response_model=None, tags=["Factura"])
def search_factura(
    idFactura: str = None,
    total: float = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Factura entities by attributes"""
    query = database.query(Factura)

    if idFactura is not None:
        query = query.filter(Factura.idFactura.ilike(f"%{idFactura}%"))
    if total is not None:
        query = query.filter(Factura.total == total)

    results = query.all()
    return results


@router.get("/factura/{factura_id}/", response_model=None, tags=["Factura"])
async def get_factura(factura_id: int, database: Session = Depends(get_db)) -> Factura:
    db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura not found")

    facturaItems_ids = database.query(ItemFactura.id).filter(ItemFactura.factura_id == db_factura.id).all()
    response_data = {
        "factura": db_factura,
        "facturaItems_ids": [x[0] for x in facturaItems_ids]}
    return response_data



@router.post("/factura/", response_model=None, tags=["Factura"])
async def create_factura(factura_data: FacturaCreate, database: Session = Depends(get_db)) -> Factura:

    if factura_data.cliente_1 is not None:
        db_cliente_1 = database.query(Cliente).filter(Cliente.id == factura_data.cliente_1).first()
        if not db_cliente_1:
            raise HTTPException(status_code=400, detail="Cliente not found")
    else:
        raise HTTPException(status_code=400, detail="Cliente ID is required")

    db_factura = Factura(
        fechaEmision=factura_data.fechaEmision,        total=factura_data.total,        idFactura=factura_data.idFactura,        estadoPago=factura_data.estadoPago.value,        cliente_1_id=factura_data.cliente_1        )

    database.add(db_factura)
    database.commit()
    database.refresh(db_factura)

    if factura_data.facturaItems:
        # Validate that all ItemFactura IDs exist
        for itemfactura_id in factura_data.facturaItems:
            db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
            if not db_itemfactura:
                raise HTTPException(status_code=400, detail=f"ItemFactura with id {itemfactura_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemFactura).filter(ItemFactura.id.in_(factura_data.facturaItems)).update(
            {ItemFactura.factura_id: db_factura.id}, synchronize_session=False
        )
        database.commit()



    facturaItems_ids = database.query(ItemFactura.id).filter(ItemFactura.factura_id == db_factura.id).all()
    response_data = {
        "factura": db_factura,
        "facturaItems_ids": [x[0] for x in facturaItems_ids]    }
    return response_data


@router.post("/factura/bulk/", response_model=None, tags=["Factura"])
async def bulk_create_factura(items: list[FacturaCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Factura entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.cliente_1:
                raise ValueError("Cliente ID is required")

            db_factura = Factura(
                fechaEmision=item_data.fechaEmision,                total=item_data.total,                idFactura=item_data.idFactura,                estadoPago=item_data.estadoPago.value,                cliente_1_id=item_data.cliente_1            )
            database.add(db_factura)
            database.flush()  # Get ID without committing
            created_items.append(db_factura.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Factura entities"
    }


@router.delete("/factura/bulk/", response_model=None, tags=["Factura"])
async def bulk_delete_factura(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Factura entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_factura = database.query(Factura).filter(Factura.id == item_id).first()
        if db_factura:
            database.delete(db_factura)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Factura entities"
    }

@router.put("/factura/{factura_id}/", response_model=None, tags=["Factura"])
async def update_factura(factura_id: int, factura_data: FacturaCreate, database: Session = Depends(get_db)) -> Factura:
    db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura not found")

    setattr(db_factura, 'fechaEmision', factura_data.fechaEmision)
    setattr(db_factura, 'total', factura_data.total)
    setattr(db_factura, 'idFactura', factura_data.idFactura)
    setattr(db_factura, 'estadoPago', factura_data.estadoPago.value)
    if factura_data.cliente_1 is not None:
        db_cliente_1 = database.query(Cliente).filter(Cliente.id == factura_data.cliente_1).first()
        if not db_cliente_1:
            raise HTTPException(status_code=400, detail="Cliente not found")
        setattr(db_factura, 'cliente_1_id', factura_data.cliente_1)
    if factura_data.facturaItems is not None:
        requested_facturaItems = set(factura_data.facturaItems)
        current_facturaItems = {
            getattr(item, 'id')
            for item in database.query(ItemFactura).filter(ItemFactura.factura_id == db_factura.id).all()
        }
        facturaItems_to_detach = current_facturaItems - requested_facturaItems
        if facturaItems_to_detach:
            raise HTTPException(status_code=409, detail="ItemFactura " + ", ".join(str(item) for item in sorted(facturaItems_to_detach)) + " requires a factura: reassign it instead of removing it")
        facturaItems_to_attach = requested_facturaItems - current_facturaItems
        for itemfactura_id in facturaItems_to_attach:
            db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
            if not db_itemfactura:
                raise HTTPException(status_code=400, detail="ItemFactura with id " + str(itemfactura_id) + " not found")
        if facturaItems_to_attach:
            database.query(ItemFactura).filter(ItemFactura.id.in_(facturaItems_to_attach)).update(
                {ItemFactura.factura_id: db_factura.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_factura)

    facturaItems_ids = database.query(ItemFactura.id).filter(ItemFactura.factura_id == db_factura.id).all()
    response_data = {
        "factura": db_factura,
        "facturaItems_ids": [x[0] for x in facturaItems_ids]    }
    return response_data


@router.delete("/factura/{factura_id}/", response_model=None, tags=["Factura"])
async def delete_factura(factura_id: int, database: Session = Depends(get_db)):
    db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura not found")
    related_facturaItems = db_factura.facturaItems
    for related in (list(related_facturaItems) if isinstance(related_facturaItems, list) else [item for item in [related_facturaItems] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Factura " + str(factura_id) + ": ItemFactura " + str(getattr(related, 'id')) + " requires at least 1 factura")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_factura = {
        attr.key: getattr(db_factura, attr.key)
        for attr in db_factura.__mapper__.column_attrs
    }
    database.delete(db_factura)
    database.commit()
    return deleted_factura


@router.get("/factura/{factura_id}/facturaItems/", response_model=None, tags=["Factura Relationships"])
async def get_facturaItems_of_factura(factura_id: int, database: Session = Depends(get_db)):
    """Get all ItemFactura entities related to this Factura through facturaItems"""
    db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
    if db_factura is None:
        raise HTTPException(status_code=404, detail="Factura not found")

    facturaItems_list = database.query(ItemFactura).filter(ItemFactura.factura_id == factura_id).all()

    return {
        "factura_id": factura_id,
        "facturaItems_count": len(facturaItems_list),
        "facturaItems": facturaItems_list
    }




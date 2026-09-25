from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/ordendecompra/", response_model=None, tags=["OrdenDeCompra"])
def get_all_ordendecompra(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(OrdenDeCompra)
        query = query.options(joinedload(OrdenDeCompra.proveedor))
        ordendecompra_list = query.all()

        # Serialize with relationships included
        result = []
        for ordendecompra_item in ordendecompra_list:
            item_dict = ordendecompra_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if ordendecompra_item.proveedor:
                related_obj = ordendecompra_item.proveedor
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['proveedor'] = related_dict
            else:
                item_dict['proveedor'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            itemordendecompra_list = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.ordendecompra_id == ordendecompra_item.id).all()
            item_dict['ordenCompraItems'] = []
            for itemordendecompra_obj in itemordendecompra_list:
                itemordendecompra_dict = itemordendecompra_obj.__dict__.copy()
                itemordendecompra_dict.pop('_sa_instance_state', None)
                item_dict['ordenCompraItems'].append(itemordendecompra_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(OrdenDeCompra).all()


@router.get("/ordendecompra/count/", response_model=None, tags=["OrdenDeCompra"])
def get_count_ordendecompra(database: Session = Depends(get_db)) -> dict:
    """Get the total count of OrdenDeCompra entities"""
    count = database.query(OrdenDeCompra).count()
    return {"count": count}


@router.get("/ordendecompra/paginated/", response_model=None, tags=["OrdenDeCompra"])
def get_paginated_ordendecompra(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of OrdenDeCompra entities"""
    total = database.query(OrdenDeCompra).count()
    ordendecompra_list = database.query(OrdenDeCompra).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": ordendecompra_list
        }

    result = []
    for ordendecompra_item in ordendecompra_list:
        ordenCompraItems_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.ordendecompra_id == ordendecompra_item.id).all()
        item_data = {
            "ordendecompra": ordendecompra_item,
            "ordenCompraItems_ids": [x[0] for x in ordenCompraItems_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/ordendecompra/search/", response_model=None, tags=["OrdenDeCompra"])
def search_ordendecompra(
    idOrdenCompra: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search OrdenDeCompra entities by attributes"""
    query = database.query(OrdenDeCompra)

    if idOrdenCompra is not None:
        query = query.filter(OrdenDeCompra.idOrdenCompra.ilike(f"%{idOrdenCompra}%"))

    results = query.all()
    return results


@router.get("/ordendecompra/{ordendecompra_id}/", response_model=None, tags=["OrdenDeCompra"])
async def get_ordendecompra(ordendecompra_id: int, database: Session = Depends(get_db)) -> OrdenDeCompra:
    db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
    if db_ordendecompra is None:
        raise HTTPException(status_code=404, detail="OrdenDeCompra not found")

    ordenCompraItems_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.ordendecompra_id == db_ordendecompra.id).all()
    response_data = {
        "ordendecompra": db_ordendecompra,
        "ordenCompraItems_ids": [x[0] for x in ordenCompraItems_ids]}
    return response_data



@router.post("/ordendecompra/", response_model=None, tags=["OrdenDeCompra"])
async def create_ordendecompra(ordendecompra_data: OrdenDeCompraCreate, database: Session = Depends(get_db)) -> OrdenDeCompra:

    if ordendecompra_data.proveedor is not None:
        db_proveedor = database.query(Proveedor).filter(Proveedor.id == ordendecompra_data.proveedor).first()
        if not db_proveedor:
            raise HTTPException(status_code=400, detail="Proveedor not found")
    else:
        raise HTTPException(status_code=400, detail="Proveedor ID is required")

    db_ordendecompra = OrdenDeCompra(
        estado=ordendecompra_data.estado.value,        fechaRecepcionEsperada=ordendecompra_data.fechaRecepcionEsperada,        idOrdenCompra=ordendecompra_data.idOrdenCompra,        fechaCreacion=ordendecompra_data.fechaCreacion,        proveedor_id=ordendecompra_data.proveedor        )

    database.add(db_ordendecompra)
    database.commit()
    database.refresh(db_ordendecompra)

    if ordendecompra_data.ordenCompraItems:
        # Validate that all ItemOrdenDeCompra IDs exist
        for itemordendecompra_id in ordendecompra_data.ordenCompraItems:
            db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
            if not db_itemordendecompra:
                raise HTTPException(status_code=400, detail=f"ItemOrdenDeCompra with id {itemordendecompra_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id.in_(ordendecompra_data.ordenCompraItems)).update(
            {ItemOrdenDeCompra.ordendecompra_id: db_ordendecompra.id}, synchronize_session=False
        )
        database.commit()



    ordenCompraItems_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.ordendecompra_id == db_ordendecompra.id).all()
    response_data = {
        "ordendecompra": db_ordendecompra,
        "ordenCompraItems_ids": [x[0] for x in ordenCompraItems_ids]    }
    return response_data


@router.post("/ordendecompra/bulk/", response_model=None, tags=["OrdenDeCompra"])
async def bulk_create_ordendecompra(items: list[OrdenDeCompraCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple OrdenDeCompra entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.proveedor:
                raise ValueError("Proveedor ID is required")

            db_ordendecompra = OrdenDeCompra(
                estado=item_data.estado.value,                fechaRecepcionEsperada=item_data.fechaRecepcionEsperada,                idOrdenCompra=item_data.idOrdenCompra,                fechaCreacion=item_data.fechaCreacion,                proveedor_id=item_data.proveedor            )
            database.add(db_ordendecompra)
            database.flush()  # Get ID without committing
            created_items.append(db_ordendecompra.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} OrdenDeCompra entities"
    }


@router.delete("/ordendecompra/bulk/", response_model=None, tags=["OrdenDeCompra"])
async def bulk_delete_ordendecompra(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple OrdenDeCompra entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == item_id).first()
        if db_ordendecompra:
            database.delete(db_ordendecompra)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} OrdenDeCompra entities"
    }

@router.put("/ordendecompra/{ordendecompra_id}/", response_model=None, tags=["OrdenDeCompra"])
async def update_ordendecompra(ordendecompra_id: int, ordendecompra_data: OrdenDeCompraCreate, database: Session = Depends(get_db)) -> OrdenDeCompra:
    db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
    if db_ordendecompra is None:
        raise HTTPException(status_code=404, detail="OrdenDeCompra not found")

    setattr(db_ordendecompra, 'estado', ordendecompra_data.estado.value)
    setattr(db_ordendecompra, 'fechaRecepcionEsperada', ordendecompra_data.fechaRecepcionEsperada)
    setattr(db_ordendecompra, 'idOrdenCompra', ordendecompra_data.idOrdenCompra)
    setattr(db_ordendecompra, 'fechaCreacion', ordendecompra_data.fechaCreacion)
    if ordendecompra_data.proveedor is not None:
        db_proveedor = database.query(Proveedor).filter(Proveedor.id == ordendecompra_data.proveedor).first()
        if not db_proveedor:
            raise HTTPException(status_code=400, detail="Proveedor not found")
        setattr(db_ordendecompra, 'proveedor_id', ordendecompra_data.proveedor)
    if ordendecompra_data.ordenCompraItems is not None:
        requested_ordenCompraItems = set(ordendecompra_data.ordenCompraItems)
        current_ordenCompraItems = {
            getattr(item, 'id')
            for item in database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.ordendecompra_id == db_ordendecompra.id).all()
        }
        ordenCompraItems_to_detach = current_ordenCompraItems - requested_ordenCompraItems
        if ordenCompraItems_to_detach:
            raise HTTPException(status_code=409, detail="ItemOrdenDeCompra " + ", ".join(str(item) for item in sorted(ordenCompraItems_to_detach)) + " requires a ordendecompra: reassign it instead of removing it")
        ordenCompraItems_to_attach = requested_ordenCompraItems - current_ordenCompraItems
        for itemordendecompra_id in ordenCompraItems_to_attach:
            db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
            if not db_itemordendecompra:
                raise HTTPException(status_code=400, detail="ItemOrdenDeCompra with id " + str(itemordendecompra_id) + " not found")
        if ordenCompraItems_to_attach:
            database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id.in_(ordenCompraItems_to_attach)).update(
                {ItemOrdenDeCompra.ordendecompra_id: db_ordendecompra.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_ordendecompra)

    ordenCompraItems_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.ordendecompra_id == db_ordendecompra.id).all()
    response_data = {
        "ordendecompra": db_ordendecompra,
        "ordenCompraItems_ids": [x[0] for x in ordenCompraItems_ids]    }
    return response_data


@router.delete("/ordendecompra/{ordendecompra_id}/", response_model=None, tags=["OrdenDeCompra"])
async def delete_ordendecompra(ordendecompra_id: int, database: Session = Depends(get_db)):
    db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
    if db_ordendecompra is None:
        raise HTTPException(status_code=404, detail="OrdenDeCompra not found")
    related_ordenCompraItems = db_ordendecompra.ordenCompraItems
    for related in (list(related_ordenCompraItems) if isinstance(related_ordenCompraItems, list) else [item for item in [related_ordenCompraItems] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete OrdenDeCompra " + str(ordendecompra_id) + ": ItemOrdenDeCompra " + str(getattr(related, 'id')) + " requires at least 1 ordendecompra")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_ordendecompra = {
        attr.key: getattr(db_ordendecompra, attr.key)
        for attr in db_ordendecompra.__mapper__.column_attrs
    }
    database.delete(db_ordendecompra)
    database.commit()
    return deleted_ordendecompra


@router.get("/ordendecompra/{ordendecompra_id}/ordenCompraItems/", response_model=None, tags=["OrdenDeCompra Relationships"])
async def get_ordenCompraItems_of_ordendecompra(ordendecompra_id: int, database: Session = Depends(get_db)):
    """Get all ItemOrdenDeCompra entities related to this OrdenDeCompra through ordenCompraItems"""
    db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
    if db_ordendecompra is None:
        raise HTTPException(status_code=404, detail="OrdenDeCompra not found")

    ordenCompraItems_list = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.ordendecompra_id == ordendecompra_id).all()

    return {
        "ordendecompra_id": ordendecompra_id,
        "ordenCompraItems_count": len(ordenCompraItems_list),
        "ordenCompraItems": ordenCompraItems_list
    }




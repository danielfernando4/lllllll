from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/ordendeproduccion/", response_model=None, tags=["OrdenDeProduccion"])
def get_all_ordendeproduccion(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(OrdenDeProduccion)
        query = query.options(joinedload(OrdenDeProduccion.cliente))
        ordendeproduccion_list = query.all()

        # Serialize with relationships included
        result = []
        for ordendeproduccion_item in ordendeproduccion_list:
            item_dict = ordendeproduccion_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if ordendeproduccion_item.cliente:
                related_obj = ordendeproduccion_item.cliente
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['cliente'] = related_dict
            else:
                item_dict['cliente'] = None

            # Add many-to-many and one-to-many relationship objects (full details)
            itemordendeproduccion_list = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.ordendeproduccion_id == ordendeproduccion_item.id).all()
            item_dict['ordenItems'] = []
            for itemordendeproduccion_obj in itemordendeproduccion_list:
                itemordendeproduccion_dict = itemordendeproduccion_obj.__dict__.copy()
                itemordendeproduccion_dict.pop('_sa_instance_state', None)
                item_dict['ordenItems'].append(itemordendeproduccion_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(OrdenDeProduccion).all()


@router.get("/ordendeproduccion/count/", response_model=None, tags=["OrdenDeProduccion"])
def get_count_ordendeproduccion(database: Session = Depends(get_db)) -> dict:
    """Get the total count of OrdenDeProduccion entities"""
    count = database.query(OrdenDeProduccion).count()
    return {"count": count}


@router.get("/ordendeproduccion/paginated/", response_model=None, tags=["OrdenDeProduccion"])
def get_paginated_ordendeproduccion(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of OrdenDeProduccion entities"""
    total = database.query(OrdenDeProduccion).count()
    ordendeproduccion_list = database.query(OrdenDeProduccion).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": ordendeproduccion_list
        }

    result = []
    for ordendeproduccion_item in ordendeproduccion_list:
        ordenItems_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.ordendeproduccion_id == ordendeproduccion_item.id).all()
        item_data = {
            "ordendeproduccion": ordendeproduccion_item,
            "ordenItems_ids": [x[0] for x in ordenItems_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/ordendeproduccion/search/", response_model=None, tags=["OrdenDeProduccion"])
def search_ordendeproduccion(
    idOrdenProd: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search OrdenDeProduccion entities by attributes"""
    query = database.query(OrdenDeProduccion)

    if idOrdenProd is not None:
        query = query.filter(OrdenDeProduccion.idOrdenProd.ilike(f"%{idOrdenProd}%"))

    results = query.all()
    return results


@router.get("/ordendeproduccion/{ordendeproduccion_id}/", response_model=None, tags=["OrdenDeProduccion"])
async def get_ordendeproduccion(ordendeproduccion_id: int, database: Session = Depends(get_db)) -> OrdenDeProduccion:
    db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
    if db_ordendeproduccion is None:
        raise HTTPException(status_code=404, detail="OrdenDeProduccion not found")

    ordenItems_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.ordendeproduccion_id == db_ordendeproduccion.id).all()
    response_data = {
        "ordendeproduccion": db_ordendeproduccion,
        "ordenItems_ids": [x[0] for x in ordenItems_ids]}
    return response_data



@router.post("/ordendeproduccion/", response_model=None, tags=["OrdenDeProduccion"])
async def create_ordendeproduccion(ordendeproduccion_data: OrdenDeProduccionCreate, database: Session = Depends(get_db)) -> OrdenDeProduccion:

    if ordendeproduccion_data.cliente is not None:
        db_cliente = database.query(Cliente).filter(Cliente.id == ordendeproduccion_data.cliente).first()
        if not db_cliente:
            raise HTTPException(status_code=400, detail="Cliente not found")
    else:
        raise HTTPException(status_code=400, detail="Cliente ID is required")

    db_ordendeproduccion = OrdenDeProduccion(
        estado=ordendeproduccion_data.estado.value,        fechaEntrega=ordendeproduccion_data.fechaEntrega,        idOrdenProd=ordendeproduccion_data.idOrdenProd,        fechaCreacion=ordendeproduccion_data.fechaCreacion,        cliente_id=ordendeproduccion_data.cliente        )

    database.add(db_ordendeproduccion)
    database.commit()
    database.refresh(db_ordendeproduccion)

    if ordendeproduccion_data.ordenItems:
        # Validate that all ItemOrdenDeProduccion IDs exist
        for itemordendeproduccion_id in ordendeproduccion_data.ordenItems:
            db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
            if not db_itemordendeproduccion:
                raise HTTPException(status_code=400, detail=f"ItemOrdenDeProduccion with id {itemordendeproduccion_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id.in_(ordendeproduccion_data.ordenItems)).update(
            {ItemOrdenDeProduccion.ordendeproduccion_id: db_ordendeproduccion.id}, synchronize_session=False
        )
        database.commit()



    ordenItems_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.ordendeproduccion_id == db_ordendeproduccion.id).all()
    response_data = {
        "ordendeproduccion": db_ordendeproduccion,
        "ordenItems_ids": [x[0] for x in ordenItems_ids]    }
    return response_data


@router.post("/ordendeproduccion/bulk/", response_model=None, tags=["OrdenDeProduccion"])
async def bulk_create_ordendeproduccion(items: list[OrdenDeProduccionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple OrdenDeProduccion entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.cliente:
                raise ValueError("Cliente ID is required")

            db_ordendeproduccion = OrdenDeProduccion(
                estado=item_data.estado.value,                fechaEntrega=item_data.fechaEntrega,                idOrdenProd=item_data.idOrdenProd,                fechaCreacion=item_data.fechaCreacion,                cliente_id=item_data.cliente            )
            database.add(db_ordendeproduccion)
            database.flush()  # Get ID without committing
            created_items.append(db_ordendeproduccion.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} OrdenDeProduccion entities"
    }


@router.delete("/ordendeproduccion/bulk/", response_model=None, tags=["OrdenDeProduccion"])
async def bulk_delete_ordendeproduccion(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple OrdenDeProduccion entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == item_id).first()
        if db_ordendeproduccion:
            database.delete(db_ordendeproduccion)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} OrdenDeProduccion entities"
    }

@router.put("/ordendeproduccion/{ordendeproduccion_id}/", response_model=None, tags=["OrdenDeProduccion"])
async def update_ordendeproduccion(ordendeproduccion_id: int, ordendeproduccion_data: OrdenDeProduccionCreate, database: Session = Depends(get_db)) -> OrdenDeProduccion:
    db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
    if db_ordendeproduccion is None:
        raise HTTPException(status_code=404, detail="OrdenDeProduccion not found")

    setattr(db_ordendeproduccion, 'estado', ordendeproduccion_data.estado.value)
    setattr(db_ordendeproduccion, 'fechaEntrega', ordendeproduccion_data.fechaEntrega)
    setattr(db_ordendeproduccion, 'idOrdenProd', ordendeproduccion_data.idOrdenProd)
    setattr(db_ordendeproduccion, 'fechaCreacion', ordendeproduccion_data.fechaCreacion)
    if ordendeproduccion_data.cliente is not None:
        db_cliente = database.query(Cliente).filter(Cliente.id == ordendeproduccion_data.cliente).first()
        if not db_cliente:
            raise HTTPException(status_code=400, detail="Cliente not found")
        setattr(db_ordendeproduccion, 'cliente_id', ordendeproduccion_data.cliente)
    if ordendeproduccion_data.ordenItems is not None:
        requested_ordenItems = set(ordendeproduccion_data.ordenItems)
        current_ordenItems = {
            getattr(item, 'id')
            for item in database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.ordendeproduccion_id == db_ordendeproduccion.id).all()
        }
        ordenItems_to_detach = current_ordenItems - requested_ordenItems
        if ordenItems_to_detach:
            raise HTTPException(status_code=409, detail="ItemOrdenDeProduccion " + ", ".join(str(item) for item in sorted(ordenItems_to_detach)) + " requires a ordendeproduccion: reassign it instead of removing it")
        ordenItems_to_attach = requested_ordenItems - current_ordenItems
        for itemordendeproduccion_id in ordenItems_to_attach:
            db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
            if not db_itemordendeproduccion:
                raise HTTPException(status_code=400, detail="ItemOrdenDeProduccion with id " + str(itemordendeproduccion_id) + " not found")
        if ordenItems_to_attach:
            database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id.in_(ordenItems_to_attach)).update(
                {ItemOrdenDeProduccion.ordendeproduccion_id: db_ordendeproduccion.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_ordendeproduccion)

    ordenItems_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.ordendeproduccion_id == db_ordendeproduccion.id).all()
    response_data = {
        "ordendeproduccion": db_ordendeproduccion,
        "ordenItems_ids": [x[0] for x in ordenItems_ids]    }
    return response_data


@router.delete("/ordendeproduccion/{ordendeproduccion_id}/", response_model=None, tags=["OrdenDeProduccion"])
async def delete_ordendeproduccion(ordendeproduccion_id: int, database: Session = Depends(get_db)):
    db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
    if db_ordendeproduccion is None:
        raise HTTPException(status_code=404, detail="OrdenDeProduccion not found")
    related_ordenItems = db_ordendeproduccion.ordenItems
    for related in (list(related_ordenItems) if isinstance(related_ordenItems, list) else [item for item in [related_ordenItems] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete OrdenDeProduccion " + str(ordendeproduccion_id) + ": ItemOrdenDeProduccion " + str(getattr(related, 'id')) + " requires at least 1 ordendeproduccion")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_ordendeproduccion = {
        attr.key: getattr(db_ordendeproduccion, attr.key)
        for attr in db_ordendeproduccion.__mapper__.column_attrs
    }
    database.delete(db_ordendeproduccion)
    database.commit()
    return deleted_ordendeproduccion


@router.get("/ordendeproduccion/{ordendeproduccion_id}/ordenItems/", response_model=None, tags=["OrdenDeProduccion Relationships"])
async def get_ordenItems_of_ordendeproduccion(ordendeproduccion_id: int, database: Session = Depends(get_db)):
    """Get all ItemOrdenDeProduccion entities related to this OrdenDeProduccion through ordenItems"""
    db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
    if db_ordendeproduccion is None:
        raise HTTPException(status_code=404, detail="OrdenDeProduccion not found")

    ordenItems_list = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.ordendeproduccion_id == ordendeproduccion_id).all()

    return {
        "ordendeproduccion_id": ordendeproduccion_id,
        "ordenItems_count": len(ordenItems_list),
        "ordenItems": ordenItems_list
    }




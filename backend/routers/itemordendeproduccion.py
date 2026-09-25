from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/itemordendeproduccion/", response_model=None, tags=["ItemOrdenDeProduccion"])
def get_all_itemordendeproduccion(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ItemOrdenDeProduccion)
        query = query.options(joinedload(ItemOrdenDeProduccion.ordendeproduccion))
        query = query.options(joinedload(ItemOrdenDeProduccion.producto))
        itemordendeproduccion_list = query.all()

        # Serialize with relationships included
        result = []
        for itemordendeproduccion_item in itemordendeproduccion_list:
            item_dict = itemordendeproduccion_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if itemordendeproduccion_item.ordendeproduccion:
                related_obj = itemordendeproduccion_item.ordendeproduccion
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['ordendeproduccion'] = related_dict
            else:
                item_dict['ordendeproduccion'] = None
            if itemordendeproduccion_item.producto:
                related_obj = itemordendeproduccion_item.producto
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['producto'] = related_dict
            else:
                item_dict['producto'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ItemOrdenDeProduccion).all()


@router.get("/itemordendeproduccion/count/", response_model=None, tags=["ItemOrdenDeProduccion"])
def get_count_itemordendeproduccion(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ItemOrdenDeProduccion entities"""
    count = database.query(ItemOrdenDeProduccion).count()
    return {"count": count}


@router.get("/itemordendeproduccion/paginated/", response_model=None, tags=["ItemOrdenDeProduccion"])
def get_paginated_itemordendeproduccion(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ItemOrdenDeProduccion entities"""
    total = database.query(ItemOrdenDeProduccion).count()
    itemordendeproduccion_list = database.query(ItemOrdenDeProduccion).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": itemordendeproduccion_list
    }
@router.get("/itemordendeproduccion/search/", response_model=None, tags=["ItemOrdenDeProduccion"])
def search_itemordendeproduccion(
    cantidad: int = None,
    idItem: str = None,
    observaciones: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search ItemOrdenDeProduccion entities by attributes"""
    query = database.query(ItemOrdenDeProduccion)

    if cantidad is not None:
        query = query.filter(ItemOrdenDeProduccion.cantidad == cantidad)
    if idItem is not None:
        query = query.filter(ItemOrdenDeProduccion.idItem.ilike(f"%{idItem}%"))
    if observaciones is not None:
        query = query.filter(ItemOrdenDeProduccion.observaciones.ilike(f"%{observaciones}%"))

    results = query.all()
    return results


@router.get("/itemordendeproduccion/{itemordendeproduccion_id}/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def get_itemordendeproduccion(itemordendeproduccion_id: int, database: Session = Depends(get_db)) -> ItemOrdenDeProduccion:
    db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
    if db_itemordendeproduccion is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeProduccion not found")

    response_data = {
        "itemordendeproduccion": db_itemordendeproduccion,
}
    return response_data



@router.post("/itemordendeproduccion/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def create_itemordendeproduccion(itemordendeproduccion_data: ItemOrdenDeProduccionCreate, database: Session = Depends(get_db)) -> ItemOrdenDeProduccion:

    if itemordendeproduccion_data.ordendeproduccion is not None:
        db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == itemordendeproduccion_data.ordendeproduccion).first()
        if not db_ordendeproduccion:
            raise HTTPException(status_code=400, detail="OrdenDeProduccion not found")
    else:
        raise HTTPException(status_code=400, detail="OrdenDeProduccion ID is required")
    if itemordendeproduccion_data.producto is not None:
        db_producto = database.query(Producto).filter(Producto.id == itemordendeproduccion_data.producto).first()
        if not db_producto:
            raise HTTPException(status_code=400, detail="Producto not found")
    else:
        raise HTTPException(status_code=400, detail="Producto ID is required")

    db_itemordendeproduccion = ItemOrdenDeProduccion(
        observaciones=itemordendeproduccion_data.observaciones,        idItem=itemordendeproduccion_data.idItem,        cantidad=itemordendeproduccion_data.cantidad,        ordendeproduccion_id=itemordendeproduccion_data.ordendeproduccion,        producto_id=itemordendeproduccion_data.producto        )

    database.add(db_itemordendeproduccion)
    database.commit()
    database.refresh(db_itemordendeproduccion)




    return db_itemordendeproduccion


@router.post("/itemordendeproduccion/bulk/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def bulk_create_itemordendeproduccion(items: list[ItemOrdenDeProduccionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ItemOrdenDeProduccion entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.ordendeproduccion:
                raise ValueError("OrdenDeProduccion ID is required")
            if not item_data.producto:
                raise ValueError("Producto ID is required")

            db_itemordendeproduccion = ItemOrdenDeProduccion(
                observaciones=item_data.observaciones,                idItem=item_data.idItem,                cantidad=item_data.cantidad,                ordendeproduccion_id=item_data.ordendeproduccion,                producto_id=item_data.producto            )
            database.add(db_itemordendeproduccion)
            database.flush()  # Get ID without committing
            created_items.append(db_itemordendeproduccion.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ItemOrdenDeProduccion entities"
    }


@router.delete("/itemordendeproduccion/bulk/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def bulk_delete_itemordendeproduccion(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ItemOrdenDeProduccion entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == item_id).first()
        if db_itemordendeproduccion:
            database.delete(db_itemordendeproduccion)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ItemOrdenDeProduccion entities"
    }

@router.put("/itemordendeproduccion/{itemordendeproduccion_id}/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def update_itemordendeproduccion(itemordendeproduccion_id: int, itemordendeproduccion_data: ItemOrdenDeProduccionCreate, database: Session = Depends(get_db)) -> ItemOrdenDeProduccion:
    db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
    if db_itemordendeproduccion is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeProduccion not found")

    setattr(db_itemordendeproduccion, 'observaciones', itemordendeproduccion_data.observaciones)
    setattr(db_itemordendeproduccion, 'idItem', itemordendeproduccion_data.idItem)
    setattr(db_itemordendeproduccion, 'cantidad', itemordendeproduccion_data.cantidad)
    if itemordendeproduccion_data.ordendeproduccion is not None:
        db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == itemordendeproduccion_data.ordendeproduccion).first()
        if not db_ordendeproduccion:
            raise HTTPException(status_code=400, detail="OrdenDeProduccion not found")
        setattr(db_itemordendeproduccion, 'ordendeproduccion_id', itemordendeproduccion_data.ordendeproduccion)
    if itemordendeproduccion_data.producto is not None:
        db_producto = database.query(Producto).filter(Producto.id == itemordendeproduccion_data.producto).first()
        if not db_producto:
            raise HTTPException(status_code=400, detail="Producto not found")
        setattr(db_itemordendeproduccion, 'producto_id', itemordendeproduccion_data.producto)
    database.commit()
    database.refresh(db_itemordendeproduccion)

    return db_itemordendeproduccion


@router.delete("/itemordendeproduccion/{itemordendeproduccion_id}/", response_model=None, tags=["ItemOrdenDeProduccion"])
async def delete_itemordendeproduccion(itemordendeproduccion_id: int, database: Session = Depends(get_db)):
    db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
    if db_itemordendeproduccion is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeProduccion not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_itemordendeproduccion = {
        attr.key: getattr(db_itemordendeproduccion, attr.key)
        for attr in db_itemordendeproduccion.__mapper__.column_attrs
    }
    database.delete(db_itemordendeproduccion)
    database.commit()
    return deleted_itemordendeproduccion





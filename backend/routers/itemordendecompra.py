from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/itemordendecompra/", response_model=None, tags=["ItemOrdenDeCompra"])
def get_all_itemordendecompra(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ItemOrdenDeCompra)
        query = query.options(joinedload(ItemOrdenDeCompra.ordendecompra))
        query = query.options(joinedload(ItemOrdenDeCompra.producto_1))
        itemordendecompra_list = query.all()

        # Serialize with relationships included
        result = []
        for itemordendecompra_item in itemordendecompra_list:
            item_dict = itemordendecompra_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if itemordendecompra_item.ordendecompra:
                related_obj = itemordendecompra_item.ordendecompra
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['ordendecompra'] = related_dict
            else:
                item_dict['ordendecompra'] = None
            if itemordendecompra_item.producto_1:
                related_obj = itemordendecompra_item.producto_1
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['producto_1'] = related_dict
            else:
                item_dict['producto_1'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ItemOrdenDeCompra).all()


@router.get("/itemordendecompra/count/", response_model=None, tags=["ItemOrdenDeCompra"])
def get_count_itemordendecompra(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ItemOrdenDeCompra entities"""
    count = database.query(ItemOrdenDeCompra).count()
    return {"count": count}


@router.get("/itemordendecompra/paginated/", response_model=None, tags=["ItemOrdenDeCompra"])
def get_paginated_itemordendecompra(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ItemOrdenDeCompra entities"""
    total = database.query(ItemOrdenDeCompra).count()
    itemordendecompra_list = database.query(ItemOrdenDeCompra).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": itemordendecompra_list
    }
@router.get("/itemordendecompra/search/", response_model=None, tags=["ItemOrdenDeCompra"])
def search_itemordendecompra(
    cantidad: int = None,
    idItem: str = None,
    precioUnitario: float = None,
    database: Session = Depends(get_db)
) -> list:
    """Search ItemOrdenDeCompra entities by attributes"""
    query = database.query(ItemOrdenDeCompra)

    if cantidad is not None:
        query = query.filter(ItemOrdenDeCompra.cantidad == cantidad)
    if idItem is not None:
        query = query.filter(ItemOrdenDeCompra.idItem.ilike(f"%{idItem}%"))
    if precioUnitario is not None:
        query = query.filter(ItemOrdenDeCompra.precioUnitario == precioUnitario)

    results = query.all()
    return results


@router.get("/itemordendecompra/{itemordendecompra_id}/", response_model=None, tags=["ItemOrdenDeCompra"])
async def get_itemordendecompra(itemordendecompra_id: int, database: Session = Depends(get_db)) -> ItemOrdenDeCompra:
    db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
    if db_itemordendecompra is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeCompra not found")

    response_data = {
        "itemordendecompra": db_itemordendecompra,
}
    return response_data



@router.post("/itemordendecompra/", response_model=None, tags=["ItemOrdenDeCompra"])
async def create_itemordendecompra(itemordendecompra_data: ItemOrdenDeCompraCreate, database: Session = Depends(get_db)) -> ItemOrdenDeCompra:

    if itemordendecompra_data.ordendecompra is not None:
        db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == itemordendecompra_data.ordendecompra).first()
        if not db_ordendecompra:
            raise HTTPException(status_code=400, detail="OrdenDeCompra not found")
    else:
        raise HTTPException(status_code=400, detail="OrdenDeCompra ID is required")
    if itemordendecompra_data.producto_1 is not None:
        db_producto_1 = database.query(Producto).filter(Producto.id == itemordendecompra_data.producto_1).first()
        if not db_producto_1:
            raise HTTPException(status_code=400, detail="Producto not found")
    else:
        raise HTTPException(status_code=400, detail="Producto ID is required")

    db_itemordendecompra = ItemOrdenDeCompra(
        precioUnitario=itemordendecompra_data.precioUnitario,        cantidad=itemordendecompra_data.cantidad,        idItem=itemordendecompra_data.idItem,        ordendecompra_id=itemordendecompra_data.ordendecompra,        producto_1_id=itemordendecompra_data.producto_1        )

    database.add(db_itemordendecompra)
    database.commit()
    database.refresh(db_itemordendecompra)




    return db_itemordendecompra


@router.post("/itemordendecompra/bulk/", response_model=None, tags=["ItemOrdenDeCompra"])
async def bulk_create_itemordendecompra(items: list[ItemOrdenDeCompraCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ItemOrdenDeCompra entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.ordendecompra:
                raise ValueError("OrdenDeCompra ID is required")
            if not item_data.producto_1:
                raise ValueError("Producto ID is required")

            db_itemordendecompra = ItemOrdenDeCompra(
                precioUnitario=item_data.precioUnitario,                cantidad=item_data.cantidad,                idItem=item_data.idItem,                ordendecompra_id=item_data.ordendecompra,                producto_1_id=item_data.producto_1            )
            database.add(db_itemordendecompra)
            database.flush()  # Get ID without committing
            created_items.append(db_itemordendecompra.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ItemOrdenDeCompra entities"
    }


@router.delete("/itemordendecompra/bulk/", response_model=None, tags=["ItemOrdenDeCompra"])
async def bulk_delete_itemordendecompra(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ItemOrdenDeCompra entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == item_id).first()
        if db_itemordendecompra:
            database.delete(db_itemordendecompra)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ItemOrdenDeCompra entities"
    }

@router.put("/itemordendecompra/{itemordendecompra_id}/", response_model=None, tags=["ItemOrdenDeCompra"])
async def update_itemordendecompra(itemordendecompra_id: int, itemordendecompra_data: ItemOrdenDeCompraCreate, database: Session = Depends(get_db)) -> ItemOrdenDeCompra:
    db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
    if db_itemordendecompra is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeCompra not found")

    setattr(db_itemordendecompra, 'precioUnitario', itemordendecompra_data.precioUnitario)
    setattr(db_itemordendecompra, 'cantidad', itemordendecompra_data.cantidad)
    setattr(db_itemordendecompra, 'idItem', itemordendecompra_data.idItem)
    if itemordendecompra_data.ordendecompra is not None:
        db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == itemordendecompra_data.ordendecompra).first()
        if not db_ordendecompra:
            raise HTTPException(status_code=400, detail="OrdenDeCompra not found")
        setattr(db_itemordendecompra, 'ordendecompra_id', itemordendecompra_data.ordendecompra)
    if itemordendecompra_data.producto_1 is not None:
        db_producto_1 = database.query(Producto).filter(Producto.id == itemordendecompra_data.producto_1).first()
        if not db_producto_1:
            raise HTTPException(status_code=400, detail="Producto not found")
        setattr(db_itemordendecompra, 'producto_1_id', itemordendecompra_data.producto_1)
    database.commit()
    database.refresh(db_itemordendecompra)

    return db_itemordendecompra


@router.delete("/itemordendecompra/{itemordendecompra_id}/", response_model=None, tags=["ItemOrdenDeCompra"])
async def delete_itemordendecompra(itemordendecompra_id: int, database: Session = Depends(get_db)):
    db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
    if db_itemordendecompra is None:
        raise HTTPException(status_code=404, detail="ItemOrdenDeCompra not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_itemordendecompra = {
        attr.key: getattr(db_itemordendecompra, attr.key)
        for attr in db_itemordendecompra.__mapper__.column_attrs
    }
    database.delete(db_itemordendecompra)
    database.commit()
    return deleted_itemordendecompra





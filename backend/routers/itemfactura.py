from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/itemfactura/", response_model=None, tags=["ItemFactura"])
def get_all_itemfactura(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ItemFactura)
        query = query.options(joinedload(ItemFactura.factura))
        query = query.options(joinedload(ItemFactura.producto_2))
        itemfactura_list = query.all()

        # Serialize with relationships included
        result = []
        for itemfactura_item in itemfactura_list:
            item_dict = itemfactura_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if itemfactura_item.factura:
                related_obj = itemfactura_item.factura
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['factura'] = related_dict
            else:
                item_dict['factura'] = None
            if itemfactura_item.producto_2:
                related_obj = itemfactura_item.producto_2
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['producto_2'] = related_dict
            else:
                item_dict['producto_2'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ItemFactura).all()


@router.get("/itemfactura/count/", response_model=None, tags=["ItemFactura"])
def get_count_itemfactura(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ItemFactura entities"""
    count = database.query(ItemFactura).count()
    return {"count": count}


@router.get("/itemfactura/paginated/", response_model=None, tags=["ItemFactura"])
def get_paginated_itemfactura(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ItemFactura entities"""
    total = database.query(ItemFactura).count()
    itemfactura_list = database.query(ItemFactura).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": itemfactura_list
    }
@router.get("/itemfactura/search/", response_model=None, tags=["ItemFactura"])
def search_itemfactura(
    cantidad: int = None,
    idItem: str = None,
    precioUnitario: float = None,
    subtotal: float = None,
    database: Session = Depends(get_db)
) -> list:
    """Search ItemFactura entities by attributes"""
    query = database.query(ItemFactura)

    if cantidad is not None:
        query = query.filter(ItemFactura.cantidad == cantidad)
    if idItem is not None:
        query = query.filter(ItemFactura.idItem.ilike(f"%{idItem}%"))
    if precioUnitario is not None:
        query = query.filter(ItemFactura.precioUnitario == precioUnitario)
    if subtotal is not None:
        query = query.filter(ItemFactura.subtotal == subtotal)

    results = query.all()
    return results


@router.get("/itemfactura/{itemfactura_id}/", response_model=None, tags=["ItemFactura"])
async def get_itemfactura(itemfactura_id: int, database: Session = Depends(get_db)) -> ItemFactura:
    db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
    if db_itemfactura is None:
        raise HTTPException(status_code=404, detail="ItemFactura not found")

    response_data = {
        "itemfactura": db_itemfactura,
}
    return response_data



@router.post("/itemfactura/", response_model=None, tags=["ItemFactura"])
async def create_itemfactura(itemfactura_data: ItemFacturaCreate, database: Session = Depends(get_db)) -> ItemFactura:

    if itemfactura_data.factura is not None:
        db_factura = database.query(Factura).filter(Factura.id == itemfactura_data.factura).first()
        if not db_factura:
            raise HTTPException(status_code=400, detail="Factura not found")
    else:
        raise HTTPException(status_code=400, detail="Factura ID is required")
    if itemfactura_data.producto_2 is not None:
        db_producto_2 = database.query(Producto).filter(Producto.id == itemfactura_data.producto_2).first()
        if not db_producto_2:
            raise HTTPException(status_code=400, detail="Producto not found")
    else:
        raise HTTPException(status_code=400, detail="Producto ID is required")

    db_itemfactura = ItemFactura(
        subtotal=itemfactura_data.subtotal,        cantidad=itemfactura_data.cantidad,        idItem=itemfactura_data.idItem,        precioUnitario=itemfactura_data.precioUnitario,        factura_id=itemfactura_data.factura,        producto_2_id=itemfactura_data.producto_2        )

    database.add(db_itemfactura)
    database.commit()
    database.refresh(db_itemfactura)




    return db_itemfactura


@router.post("/itemfactura/bulk/", response_model=None, tags=["ItemFactura"])
async def bulk_create_itemfactura(items: list[ItemFacturaCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ItemFactura entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.factura:
                raise ValueError("Factura ID is required")
            if not item_data.producto_2:
                raise ValueError("Producto ID is required")

            db_itemfactura = ItemFactura(
                subtotal=item_data.subtotal,                cantidad=item_data.cantidad,                idItem=item_data.idItem,                precioUnitario=item_data.precioUnitario,                factura_id=item_data.factura,                producto_2_id=item_data.producto_2            )
            database.add(db_itemfactura)
            database.flush()  # Get ID without committing
            created_items.append(db_itemfactura.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ItemFactura entities"
    }


@router.delete("/itemfactura/bulk/", response_model=None, tags=["ItemFactura"])
async def bulk_delete_itemfactura(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ItemFactura entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == item_id).first()
        if db_itemfactura:
            database.delete(db_itemfactura)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ItemFactura entities"
    }

@router.put("/itemfactura/{itemfactura_id}/", response_model=None, tags=["ItemFactura"])
async def update_itemfactura(itemfactura_id: int, itemfactura_data: ItemFacturaCreate, database: Session = Depends(get_db)) -> ItemFactura:
    db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
    if db_itemfactura is None:
        raise HTTPException(status_code=404, detail="ItemFactura not found")

    setattr(db_itemfactura, 'subtotal', itemfactura_data.subtotal)
    setattr(db_itemfactura, 'cantidad', itemfactura_data.cantidad)
    setattr(db_itemfactura, 'idItem', itemfactura_data.idItem)
    setattr(db_itemfactura, 'precioUnitario', itemfactura_data.precioUnitario)
    if itemfactura_data.factura is not None:
        db_factura = database.query(Factura).filter(Factura.id == itemfactura_data.factura).first()
        if not db_factura:
            raise HTTPException(status_code=400, detail="Factura not found")
        setattr(db_itemfactura, 'factura_id', itemfactura_data.factura)
    if itemfactura_data.producto_2 is not None:
        db_producto_2 = database.query(Producto).filter(Producto.id == itemfactura_data.producto_2).first()
        if not db_producto_2:
            raise HTTPException(status_code=400, detail="Producto not found")
        setattr(db_itemfactura, 'producto_2_id', itemfactura_data.producto_2)
    database.commit()
    database.refresh(db_itemfactura)

    return db_itemfactura


@router.delete("/itemfactura/{itemfactura_id}/", response_model=None, tags=["ItemFactura"])
async def delete_itemfactura(itemfactura_id: int, database: Session = Depends(get_db)):
    db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
    if db_itemfactura is None:
        raise HTTPException(status_code=404, detail="ItemFactura not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_itemfactura = {
        attr.key: getattr(db_itemfactura, attr.key)
        for attr in db_itemfactura.__mapper__.column_attrs
    }
    database.delete(db_itemfactura)
    database.commit()
    return deleted_itemfactura





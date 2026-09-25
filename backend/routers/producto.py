from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/producto/", response_model=None, tags=["Producto"])
def get_all_producto(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Producto)
        producto_list = query.all()

        # Serialize with relationships included
        result = []
        for producto_item in producto_list:
            item_dict = producto_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            itemfactura_list = database.query(ItemFactura).filter(ItemFactura.producto_2_id == producto_item.id).all()
            item_dict['productoItemsFactura'] = []
            for itemfactura_obj in itemfactura_list:
                itemfactura_dict = itemfactura_obj.__dict__.copy()
                itemfactura_dict.pop('_sa_instance_state', None)
                item_dict['productoItemsFactura'].append(itemfactura_dict)
            itemordendecompra_list = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.producto_1_id == producto_item.id).all()
            item_dict['productoItemsOrdenCompra'] = []
            for itemordendecompra_obj in itemordendecompra_list:
                itemordendecompra_dict = itemordendecompra_obj.__dict__.copy()
                itemordendecompra_dict.pop('_sa_instance_state', None)
                item_dict['productoItemsOrdenCompra'].append(itemordendecompra_dict)
            itemordendeproduccion_list = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.producto_id == producto_item.id).all()
            item_dict['productoItemsOrdenProd'] = []
            for itemordendeproduccion_obj in itemordendeproduccion_list:
                itemordendeproduccion_dict = itemordendeproduccion_obj.__dict__.copy()
                itemordendeproduccion_dict.pop('_sa_instance_state', None)
                item_dict['productoItemsOrdenProd'].append(itemordendeproduccion_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Producto).all()


@router.get("/producto/count/", response_model=None, tags=["Producto"])
def get_count_producto(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Producto entities"""
    count = database.query(Producto).count()
    return {"count": count}


@router.get("/producto/paginated/", response_model=None, tags=["Producto"])
def get_paginated_producto(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Producto entities"""
    total = database.query(Producto).count()
    producto_list = database.query(Producto).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": producto_list
        }

    result = []
    for producto_item in producto_list:
        productoItemsFactura_ids = database.query(ItemFactura.id).filter(ItemFactura.producto_2_id == producto_item.id).all()
        productoItemsOrdenCompra_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.producto_1_id == producto_item.id).all()
        productoItemsOrdenProd_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.producto_id == producto_item.id).all()
        item_data = {
            "producto": producto_item,
            "productoItemsFactura_ids": [x[0] for x in productoItemsFactura_ids],            "productoItemsOrdenCompra_ids": [x[0] for x in productoItemsOrdenCompra_ids],            "productoItemsOrdenProd_ids": [x[0] for x in productoItemsOrdenProd_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/producto/search/", response_model=None, tags=["Producto"])
def search_producto(
    descripcion: str = None,
    idProducto: str = None,
    nombre: str = None,
    precioUnitario: float = None,
    stockDisponible: int = None,
    unidadMedida: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Producto entities by attributes"""
    query = database.query(Producto)

    if descripcion is not None:
        query = query.filter(Producto.descripcion.ilike(f"%{descripcion}%"))
    if idProducto is not None:
        query = query.filter(Producto.idProducto.ilike(f"%{idProducto}%"))
    if nombre is not None:
        query = query.filter(Producto.nombre.ilike(f"%{nombre}%"))
    if precioUnitario is not None:
        query = query.filter(Producto.precioUnitario == precioUnitario)
    if stockDisponible is not None:
        query = query.filter(Producto.stockDisponible == stockDisponible)
    if unidadMedida is not None:
        query = query.filter(Producto.unidadMedida.ilike(f"%{unidadMedida}%"))

    results = query.all()
    return results


@router.get("/producto/{producto_id}/", response_model=None, tags=["Producto"])
async def get_producto(producto_id: int, database: Session = Depends(get_db)) -> Producto:
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")

    productoItemsFactura_ids = database.query(ItemFactura.id).filter(ItemFactura.producto_2_id == db_producto.id).all()
    productoItemsOrdenCompra_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.producto_1_id == db_producto.id).all()
    productoItemsOrdenProd_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.producto_id == db_producto.id).all()
    response_data = {
        "producto": db_producto,
        "productoItemsFactura_ids": [x[0] for x in productoItemsFactura_ids],        "productoItemsOrdenCompra_ids": [x[0] for x in productoItemsOrdenCompra_ids],        "productoItemsOrdenProd_ids": [x[0] for x in productoItemsOrdenProd_ids]}
    return response_data



@router.post("/producto/", response_model=None, tags=["Producto"])
async def create_producto(producto_data: ProductoCreate, database: Session = Depends(get_db)) -> Producto:


    db_producto = Producto(
        idProducto=producto_data.idProducto,        descripcion=producto_data.descripcion,        nombre=producto_data.nombre,        unidadMedida=producto_data.unidadMedida,        precioUnitario=producto_data.precioUnitario,        stockDisponible=producto_data.stockDisponible        )

    database.add(db_producto)
    database.commit()
    database.refresh(db_producto)

    if producto_data.productoItemsFactura:
        # Validate that all ItemFactura IDs exist
        for itemfactura_id in producto_data.productoItemsFactura:
            db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
            if not db_itemfactura:
                raise HTTPException(status_code=400, detail=f"ItemFactura with id {itemfactura_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemFactura).filter(ItemFactura.id.in_(producto_data.productoItemsFactura)).update(
            {ItemFactura.producto_2_id: db_producto.id}, synchronize_session=False
        )
        database.commit()
    if producto_data.productoItemsOrdenCompra:
        # Validate that all ItemOrdenDeCompra IDs exist
        for itemordendecompra_id in producto_data.productoItemsOrdenCompra:
            db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
            if not db_itemordendecompra:
                raise HTTPException(status_code=400, detail=f"ItemOrdenDeCompra with id {itemordendecompra_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id.in_(producto_data.productoItemsOrdenCompra)).update(
            {ItemOrdenDeCompra.producto_1_id: db_producto.id}, synchronize_session=False
        )
        database.commit()
    if producto_data.productoItemsOrdenProd:
        # Validate that all ItemOrdenDeProduccion IDs exist
        for itemordendeproduccion_id in producto_data.productoItemsOrdenProd:
            db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
            if not db_itemordendeproduccion:
                raise HTTPException(status_code=400, detail=f"ItemOrdenDeProduccion with id {itemordendeproduccion_id} not found")

        # Update the related entities with the new foreign key
        database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id.in_(producto_data.productoItemsOrdenProd)).update(
            {ItemOrdenDeProduccion.producto_id: db_producto.id}, synchronize_session=False
        )
        database.commit()



    productoItemsFactura_ids = database.query(ItemFactura.id).filter(ItemFactura.producto_2_id == db_producto.id).all()
    productoItemsOrdenCompra_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.producto_1_id == db_producto.id).all()
    productoItemsOrdenProd_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.producto_id == db_producto.id).all()
    response_data = {
        "producto": db_producto,
        "productoItemsFactura_ids": [x[0] for x in productoItemsFactura_ids],        "productoItemsOrdenCompra_ids": [x[0] for x in productoItemsOrdenCompra_ids],        "productoItemsOrdenProd_ids": [x[0] for x in productoItemsOrdenProd_ids]    }
    return response_data


@router.post("/producto/bulk/", response_model=None, tags=["Producto"])
async def bulk_create_producto(items: list[ProductoCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Producto entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_producto = Producto(
                idProducto=item_data.idProducto,                descripcion=item_data.descripcion,                nombre=item_data.nombre,                unidadMedida=item_data.unidadMedida,                precioUnitario=item_data.precioUnitario,                stockDisponible=item_data.stockDisponible            )
            database.add(db_producto)
            database.flush()  # Get ID without committing
            created_items.append(db_producto.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Producto entities"
    }


@router.delete("/producto/bulk/", response_model=None, tags=["Producto"])
async def bulk_delete_producto(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Producto entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_producto = database.query(Producto).filter(Producto.id == item_id).first()
        if db_producto:
            database.delete(db_producto)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Producto entities"
    }

@router.put("/producto/{producto_id}/", response_model=None, tags=["Producto"])
async def update_producto(producto_id: int, producto_data: ProductoCreate, database: Session = Depends(get_db)) -> Producto:
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")

    setattr(db_producto, 'idProducto', producto_data.idProducto)
    setattr(db_producto, 'descripcion', producto_data.descripcion)
    setattr(db_producto, 'nombre', producto_data.nombre)
    setattr(db_producto, 'unidadMedida', producto_data.unidadMedida)
    setattr(db_producto, 'precioUnitario', producto_data.precioUnitario)
    setattr(db_producto, 'stockDisponible', producto_data.stockDisponible)
    if producto_data.productoItemsFactura is not None:
        requested_productoItemsFactura = set(producto_data.productoItemsFactura)
        current_productoItemsFactura = {
            getattr(item, 'id')
            for item in database.query(ItemFactura).filter(ItemFactura.producto_2_id == db_producto.id).all()
        }
        productoItemsFactura_to_detach = current_productoItemsFactura - requested_productoItemsFactura
        if productoItemsFactura_to_detach:
            raise HTTPException(status_code=409, detail="ItemFactura " + ", ".join(str(item) for item in sorted(productoItemsFactura_to_detach)) + " requires a producto_2: reassign it instead of removing it")
        productoItemsFactura_to_attach = requested_productoItemsFactura - current_productoItemsFactura
        for itemfactura_id in productoItemsFactura_to_attach:
            db_itemfactura = database.query(ItemFactura).filter(ItemFactura.id == itemfactura_id).first()
            if not db_itemfactura:
                raise HTTPException(status_code=400, detail="ItemFactura with id " + str(itemfactura_id) + " not found")
        if productoItemsFactura_to_attach:
            database.query(ItemFactura).filter(ItemFactura.id.in_(productoItemsFactura_to_attach)).update(
                {ItemFactura.producto_2_id: db_producto.id}, synchronize_session=False
            )
    if producto_data.productoItemsOrdenCompra is not None:
        requested_productoItemsOrdenCompra = set(producto_data.productoItemsOrdenCompra)
        current_productoItemsOrdenCompra = {
            getattr(item, 'id')
            for item in database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.producto_1_id == db_producto.id).all()
        }
        productoItemsOrdenCompra_to_detach = current_productoItemsOrdenCompra - requested_productoItemsOrdenCompra
        if productoItemsOrdenCompra_to_detach:
            raise HTTPException(status_code=409, detail="ItemOrdenDeCompra " + ", ".join(str(item) for item in sorted(productoItemsOrdenCompra_to_detach)) + " requires a producto_1: reassign it instead of removing it")
        productoItemsOrdenCompra_to_attach = requested_productoItemsOrdenCompra - current_productoItemsOrdenCompra
        for itemordendecompra_id in productoItemsOrdenCompra_to_attach:
            db_itemordendecompra = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id == itemordendecompra_id).first()
            if not db_itemordendecompra:
                raise HTTPException(status_code=400, detail="ItemOrdenDeCompra with id " + str(itemordendecompra_id) + " not found")
        if productoItemsOrdenCompra_to_attach:
            database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.id.in_(productoItemsOrdenCompra_to_attach)).update(
                {ItemOrdenDeCompra.producto_1_id: db_producto.id}, synchronize_session=False
            )
    if producto_data.productoItemsOrdenProd is not None:
        requested_productoItemsOrdenProd = set(producto_data.productoItemsOrdenProd)
        current_productoItemsOrdenProd = {
            getattr(item, 'id')
            for item in database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.producto_id == db_producto.id).all()
        }
        productoItemsOrdenProd_to_detach = current_productoItemsOrdenProd - requested_productoItemsOrdenProd
        if productoItemsOrdenProd_to_detach:
            raise HTTPException(status_code=409, detail="ItemOrdenDeProduccion " + ", ".join(str(item) for item in sorted(productoItemsOrdenProd_to_detach)) + " requires a producto: reassign it instead of removing it")
        productoItemsOrdenProd_to_attach = requested_productoItemsOrdenProd - current_productoItemsOrdenProd
        for itemordendeproduccion_id in productoItemsOrdenProd_to_attach:
            db_itemordendeproduccion = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id == itemordendeproduccion_id).first()
            if not db_itemordendeproduccion:
                raise HTTPException(status_code=400, detail="ItemOrdenDeProduccion with id " + str(itemordendeproduccion_id) + " not found")
        if productoItemsOrdenProd_to_attach:
            database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.id.in_(productoItemsOrdenProd_to_attach)).update(
                {ItemOrdenDeProduccion.producto_id: db_producto.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_producto)

    productoItemsFactura_ids = database.query(ItemFactura.id).filter(ItemFactura.producto_2_id == db_producto.id).all()
    productoItemsOrdenCompra_ids = database.query(ItemOrdenDeCompra.id).filter(ItemOrdenDeCompra.producto_1_id == db_producto.id).all()
    productoItemsOrdenProd_ids = database.query(ItemOrdenDeProduccion.id).filter(ItemOrdenDeProduccion.producto_id == db_producto.id).all()
    response_data = {
        "producto": db_producto,
        "productoItemsFactura_ids": [x[0] for x in productoItemsFactura_ids],        "productoItemsOrdenCompra_ids": [x[0] for x in productoItemsOrdenCompra_ids],        "productoItemsOrdenProd_ids": [x[0] for x in productoItemsOrdenProd_ids]    }
    return response_data


@router.delete("/producto/{producto_id}/", response_model=None, tags=["Producto"])
async def delete_producto(producto_id: int, database: Session = Depends(get_db)):
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")
    related_productoItemsFactura = db_producto.productoItemsFactura
    for related in (list(related_productoItemsFactura) if isinstance(related_productoItemsFactura, list) else [item for item in [related_productoItemsFactura] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Producto " + str(producto_id) + ": ItemFactura " + str(getattr(related, 'id')) + " requires at least 1 producto_2")
    related_productoItemsOrdenCompra = db_producto.productoItemsOrdenCompra
    for related in (list(related_productoItemsOrdenCompra) if isinstance(related_productoItemsOrdenCompra, list) else [item for item in [related_productoItemsOrdenCompra] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Producto " + str(producto_id) + ": ItemOrdenDeCompra " + str(getattr(related, 'id')) + " requires at least 1 producto_1")
    related_productoItemsOrdenProd = db_producto.productoItemsOrdenProd
    for related in (list(related_productoItemsOrdenProd) if isinstance(related_productoItemsOrdenProd, list) else [item for item in [related_productoItemsOrdenProd] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Producto " + str(producto_id) + ": ItemOrdenDeProduccion " + str(getattr(related, 'id')) + " requires at least 1 producto")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_producto = {
        attr.key: getattr(db_producto, attr.key)
        for attr in db_producto.__mapper__.column_attrs
    }
    database.delete(db_producto)
    database.commit()
    return deleted_producto


@router.get("/producto/{producto_id}/productoItemsFactura/", response_model=None, tags=["Producto Relationships"])
async def get_productoItemsFactura_of_producto(producto_id: int, database: Session = Depends(get_db)):
    """Get all ItemFactura entities related to this Producto through productoItemsFactura"""
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")

    productoItemsFactura_list = database.query(ItemFactura).filter(ItemFactura.producto_2_id == producto_id).all()

    return {
        "producto_id": producto_id,
        "productoItemsFactura_count": len(productoItemsFactura_list),
        "productoItemsFactura": productoItemsFactura_list
    }

@router.get("/producto/{producto_id}/productoItemsOrdenCompra/", response_model=None, tags=["Producto Relationships"])
async def get_productoItemsOrdenCompra_of_producto(producto_id: int, database: Session = Depends(get_db)):
    """Get all ItemOrdenDeCompra entities related to this Producto through productoItemsOrdenCompra"""
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")

    productoItemsOrdenCompra_list = database.query(ItemOrdenDeCompra).filter(ItemOrdenDeCompra.producto_1_id == producto_id).all()

    return {
        "producto_id": producto_id,
        "productoItemsOrdenCompra_count": len(productoItemsOrdenCompra_list),
        "productoItemsOrdenCompra": productoItemsOrdenCompra_list
    }

@router.get("/producto/{producto_id}/productoItemsOrdenProd/", response_model=None, tags=["Producto Relationships"])
async def get_productoItemsOrdenProd_of_producto(producto_id: int, database: Session = Depends(get_db)):
    """Get all ItemOrdenDeProduccion entities related to this Producto through productoItemsOrdenProd"""
    db_producto = database.query(Producto).filter(Producto.id == producto_id).first()
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto not found")

    productoItemsOrdenProd_list = database.query(ItemOrdenDeProduccion).filter(ItemOrdenDeProduccion.producto_id == producto_id).all()

    return {
        "producto_id": producto_id,
        "productoItemsOrdenProd_count": len(productoItemsOrdenProd_list),
        "productoItemsOrdenProd": productoItemsOrdenProd_list
    }




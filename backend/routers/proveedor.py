from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/proveedor/", response_model=None, tags=["Proveedor"])
def get_all_proveedor(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Proveedor)
        proveedor_list = query.all()

        # Serialize with relationships included
        result = []
        for proveedor_item in proveedor_list:
            item_dict = proveedor_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            ordendecompra_list = database.query(OrdenDeCompra).filter(OrdenDeCompra.proveedor_id == proveedor_item.id).all()
            item_dict['proveedorOrdenesCompra'] = []
            for ordendecompra_obj in ordendecompra_list:
                ordendecompra_dict = ordendecompra_obj.__dict__.copy()
                ordendecompra_dict.pop('_sa_instance_state', None)
                item_dict['proveedorOrdenesCompra'].append(ordendecompra_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Proveedor).all()


@router.get("/proveedor/count/", response_model=None, tags=["Proveedor"])
def get_count_proveedor(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Proveedor entities"""
    count = database.query(Proveedor).count()
    return {"count": count}


@router.get("/proveedor/paginated/", response_model=None, tags=["Proveedor"])
def get_paginated_proveedor(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Proveedor entities"""
    total = database.query(Proveedor).count()
    proveedor_list = database.query(Proveedor).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": proveedor_list
        }

    result = []
    for proveedor_item in proveedor_list:
        proveedorOrdenesCompra_ids = database.query(OrdenDeCompra.id).filter(OrdenDeCompra.proveedor_id == proveedor_item.id).all()
        item_data = {
            "proveedor": proveedor_item,
            "proveedorOrdenesCompra_ids": [x[0] for x in proveedorOrdenesCompra_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/proveedor/search/", response_model=None, tags=["Proveedor"])
def search_proveedor(
    direccion: str = None,
    email: str = None,
    idProveedor: str = None,
    nombre: str = None,
    telefono: str = None,
    tipoProveedor: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Proveedor entities by attributes"""
    query = database.query(Proveedor)

    if direccion is not None:
        query = query.filter(Proveedor.direccion.ilike(f"%{direccion}%"))
    if email is not None:
        query = query.filter(Proveedor.email.ilike(f"%{email}%"))
    if idProveedor is not None:
        query = query.filter(Proveedor.idProveedor.ilike(f"%{idProveedor}%"))
    if nombre is not None:
        query = query.filter(Proveedor.nombre.ilike(f"%{nombre}%"))
    if telefono is not None:
        query = query.filter(Proveedor.telefono.ilike(f"%{telefono}%"))
    if tipoProveedor is not None:
        query = query.filter(Proveedor.tipoProveedor.ilike(f"%{tipoProveedor}%"))

    results = query.all()
    return results


@router.get("/proveedor/{proveedor_id}/", response_model=None, tags=["Proveedor"])
async def get_proveedor(proveedor_id: int, database: Session = Depends(get_db)) -> Proveedor:
    db_proveedor = database.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")

    proveedorOrdenesCompra_ids = database.query(OrdenDeCompra.id).filter(OrdenDeCompra.proveedor_id == db_proveedor.id).all()
    response_data = {
        "proveedor": db_proveedor,
        "proveedorOrdenesCompra_ids": [x[0] for x in proveedorOrdenesCompra_ids]}
    return response_data



@router.post("/proveedor/", response_model=None, tags=["Proveedor"])
async def create_proveedor(proveedor_data: ProveedorCreate, database: Session = Depends(get_db)) -> Proveedor:


    db_proveedor = Proveedor(
        tipoProveedor=proveedor_data.tipoProveedor,        email=proveedor_data.email,        nombre=proveedor_data.nombre,        telefono=proveedor_data.telefono,        idProveedor=proveedor_data.idProveedor,        direccion=proveedor_data.direccion        )

    database.add(db_proveedor)
    database.commit()
    database.refresh(db_proveedor)

    if proveedor_data.proveedorOrdenesCompra:
        # Validate that all OrdenDeCompra IDs exist
        for ordendecompra_id in proveedor_data.proveedorOrdenesCompra:
            db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
            if not db_ordendecompra:
                raise HTTPException(status_code=400, detail=f"OrdenDeCompra with id {ordendecompra_id} not found")

        # Update the related entities with the new foreign key
        database.query(OrdenDeCompra).filter(OrdenDeCompra.id.in_(proveedor_data.proveedorOrdenesCompra)).update(
            {OrdenDeCompra.proveedor_id: db_proveedor.id}, synchronize_session=False
        )
        database.commit()



    proveedorOrdenesCompra_ids = database.query(OrdenDeCompra.id).filter(OrdenDeCompra.proveedor_id == db_proveedor.id).all()
    response_data = {
        "proveedor": db_proveedor,
        "proveedorOrdenesCompra_ids": [x[0] for x in proveedorOrdenesCompra_ids]    }
    return response_data


@router.post("/proveedor/bulk/", response_model=None, tags=["Proveedor"])
async def bulk_create_proveedor(items: list[ProveedorCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Proveedor entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_proveedor = Proveedor(
                tipoProveedor=item_data.tipoProveedor,                email=item_data.email,                nombre=item_data.nombre,                telefono=item_data.telefono,                idProveedor=item_data.idProveedor,                direccion=item_data.direccion            )
            database.add(db_proveedor)
            database.flush()  # Get ID without committing
            created_items.append(db_proveedor.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Proveedor entities"
    }


@router.delete("/proveedor/bulk/", response_model=None, tags=["Proveedor"])
async def bulk_delete_proveedor(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Proveedor entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_proveedor = database.query(Proveedor).filter(Proveedor.id == item_id).first()
        if db_proveedor:
            database.delete(db_proveedor)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Proveedor entities"
    }

@router.put("/proveedor/{proveedor_id}/", response_model=None, tags=["Proveedor"])
async def update_proveedor(proveedor_id: int, proveedor_data: ProveedorCreate, database: Session = Depends(get_db)) -> Proveedor:
    db_proveedor = database.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")

    setattr(db_proveedor, 'tipoProveedor', proveedor_data.tipoProveedor)
    setattr(db_proveedor, 'email', proveedor_data.email)
    setattr(db_proveedor, 'nombre', proveedor_data.nombre)
    setattr(db_proveedor, 'telefono', proveedor_data.telefono)
    setattr(db_proveedor, 'idProveedor', proveedor_data.idProveedor)
    setattr(db_proveedor, 'direccion', proveedor_data.direccion)
    if proveedor_data.proveedorOrdenesCompra is not None:
        requested_proveedorOrdenesCompra = set(proveedor_data.proveedorOrdenesCompra)
        current_proveedorOrdenesCompra = {
            getattr(item, 'id')
            for item in database.query(OrdenDeCompra).filter(OrdenDeCompra.proveedor_id == db_proveedor.id).all()
        }
        proveedorOrdenesCompra_to_detach = current_proveedorOrdenesCompra - requested_proveedorOrdenesCompra
        if proveedorOrdenesCompra_to_detach:
            raise HTTPException(status_code=409, detail="OrdenDeCompra " + ", ".join(str(item) for item in sorted(proveedorOrdenesCompra_to_detach)) + " requires a proveedor: reassign it instead of removing it")
        proveedorOrdenesCompra_to_attach = requested_proveedorOrdenesCompra - current_proveedorOrdenesCompra
        for ordendecompra_id in proveedorOrdenesCompra_to_attach:
            db_ordendecompra = database.query(OrdenDeCompra).filter(OrdenDeCompra.id == ordendecompra_id).first()
            if not db_ordendecompra:
                raise HTTPException(status_code=400, detail="OrdenDeCompra with id " + str(ordendecompra_id) + " not found")
        if proveedorOrdenesCompra_to_attach:
            database.query(OrdenDeCompra).filter(OrdenDeCompra.id.in_(proveedorOrdenesCompra_to_attach)).update(
                {OrdenDeCompra.proveedor_id: db_proveedor.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_proveedor)

    proveedorOrdenesCompra_ids = database.query(OrdenDeCompra.id).filter(OrdenDeCompra.proveedor_id == db_proveedor.id).all()
    response_data = {
        "proveedor": db_proveedor,
        "proveedorOrdenesCompra_ids": [x[0] for x in proveedorOrdenesCompra_ids]    }
    return response_data


@router.delete("/proveedor/{proveedor_id}/", response_model=None, tags=["Proveedor"])
async def delete_proveedor(proveedor_id: int, database: Session = Depends(get_db)):
    db_proveedor = database.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")
    related_proveedorOrdenesCompra = db_proveedor.proveedorOrdenesCompra
    for related in (list(related_proveedorOrdenesCompra) if isinstance(related_proveedorOrdenesCompra, list) else [item for item in [related_proveedorOrdenesCompra] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Proveedor " + str(proveedor_id) + ": OrdenDeCompra " + str(getattr(related, 'id')) + " requires at least 1 proveedor")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_proveedor = {
        attr.key: getattr(db_proveedor, attr.key)
        for attr in db_proveedor.__mapper__.column_attrs
    }
    database.delete(db_proveedor)
    database.commit()
    return deleted_proveedor


@router.get("/proveedor/{proveedor_id}/proveedorOrdenesCompra/", response_model=None, tags=["Proveedor Relationships"])
async def get_proveedorOrdenesCompra_of_proveedor(proveedor_id: int, database: Session = Depends(get_db)):
    """Get all OrdenDeCompra entities related to this Proveedor through proveedorOrdenesCompra"""
    db_proveedor = database.query(Proveedor).filter(Proveedor.id == proveedor_id).first()
    if db_proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")

    proveedorOrdenesCompra_list = database.query(OrdenDeCompra).filter(OrdenDeCompra.proveedor_id == proveedor_id).all()

    return {
        "proveedor_id": proveedor_id,
        "proveedorOrdenesCompra_count": len(proveedorOrdenesCompra_list),
        "proveedorOrdenesCompra": proveedorOrdenesCompra_list
    }




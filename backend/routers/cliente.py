from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/cliente/", response_model=None, tags=["Cliente"])
def get_all_cliente(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Cliente)
        cliente_list = query.all()

        # Serialize with relationships included
        result = []
        for cliente_item in cliente_list:
            item_dict = cliente_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            ordendeproduccion_list = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.cliente_id == cliente_item.id).all()
            item_dict['clienteOrdenes'] = []
            for ordendeproduccion_obj in ordendeproduccion_list:
                ordendeproduccion_dict = ordendeproduccion_obj.__dict__.copy()
                ordendeproduccion_dict.pop('_sa_instance_state', None)
                item_dict['clienteOrdenes'].append(ordendeproduccion_dict)
            factura_list = database.query(Factura).filter(Factura.cliente_1_id == cliente_item.id).all()
            item_dict['clienteFacturas'] = []
            for factura_obj in factura_list:
                factura_dict = factura_obj.__dict__.copy()
                factura_dict.pop('_sa_instance_state', None)
                item_dict['clienteFacturas'].append(factura_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Cliente).all()


@router.get("/cliente/count/", response_model=None, tags=["Cliente"])
def get_count_cliente(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Cliente entities"""
    count = database.query(Cliente).count()
    return {"count": count}


@router.get("/cliente/paginated/", response_model=None, tags=["Cliente"])
def get_paginated_cliente(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Cliente entities"""
    total = database.query(Cliente).count()
    cliente_list = database.query(Cliente).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": cliente_list
        }

    result = []
    for cliente_item in cliente_list:
        clienteOrdenes_ids = database.query(OrdenDeProduccion.id).filter(OrdenDeProduccion.cliente_id == cliente_item.id).all()
        clienteFacturas_ids = database.query(Factura.id).filter(Factura.cliente_1_id == cliente_item.id).all()
        item_data = {
            "cliente": cliente_item,
            "clienteOrdenes_ids": [x[0] for x in clienteOrdenes_ids],            "clienteFacturas_ids": [x[0] for x in clienteFacturas_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/cliente/search/", response_model=None, tags=["Cliente"])
def search_cliente(
    direccion: str = None,
    email: str = None,
    idCliente: str = None,
    nombre: str = None,
    telefono: str = None,
    tipoCliente: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Cliente entities by attributes"""
    query = database.query(Cliente)

    if direccion is not None:
        query = query.filter(Cliente.direccion.ilike(f"%{direccion}%"))
    if email is not None:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))
    if idCliente is not None:
        query = query.filter(Cliente.idCliente.ilike(f"%{idCliente}%"))
    if nombre is not None:
        query = query.filter(Cliente.nombre.ilike(f"%{nombre}%"))
    if telefono is not None:
        query = query.filter(Cliente.telefono.ilike(f"%{telefono}%"))
    if tipoCliente is not None:
        query = query.filter(Cliente.tipoCliente.ilike(f"%{tipoCliente}%"))

    results = query.all()
    return results


@router.get("/cliente/{cliente_id}/", response_model=None, tags=["Cliente"])
async def get_cliente(cliente_id: int, database: Session = Depends(get_db)) -> Cliente:
    db_cliente = database.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    clienteOrdenes_ids = database.query(OrdenDeProduccion.id).filter(OrdenDeProduccion.cliente_id == db_cliente.id).all()
    clienteFacturas_ids = database.query(Factura.id).filter(Factura.cliente_1_id == db_cliente.id).all()
    response_data = {
        "cliente": db_cliente,
        "clienteOrdenes_ids": [x[0] for x in clienteOrdenes_ids],        "clienteFacturas_ids": [x[0] for x in clienteFacturas_ids]}
    return response_data



@router.post("/cliente/", response_model=None, tags=["Cliente"])
async def create_cliente(cliente_data: ClienteCreate, database: Session = Depends(get_db)) -> Cliente:


    db_cliente = Cliente(
        telefono=cliente_data.telefono,        email=cliente_data.email,        idCliente=cliente_data.idCliente,        nombre=cliente_data.nombre,        tipoCliente=cliente_data.tipoCliente,        direccion=cliente_data.direccion        )

    database.add(db_cliente)
    database.commit()
    database.refresh(db_cliente)

    if cliente_data.clienteOrdenes:
        # Validate that all OrdenDeProduccion IDs exist
        for ordendeproduccion_id in cliente_data.clienteOrdenes:
            db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
            if not db_ordendeproduccion:
                raise HTTPException(status_code=400, detail=f"OrdenDeProduccion with id {ordendeproduccion_id} not found")

        # Update the related entities with the new foreign key
        database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id.in_(cliente_data.clienteOrdenes)).update(
            {OrdenDeProduccion.cliente_id: db_cliente.id}, synchronize_session=False
        )
        database.commit()
    if cliente_data.clienteFacturas:
        # Validate that all Factura IDs exist
        for factura_id in cliente_data.clienteFacturas:
            db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
            if not db_factura:
                raise HTTPException(status_code=400, detail=f"Factura with id {factura_id} not found")

        # Update the related entities with the new foreign key
        database.query(Factura).filter(Factura.id.in_(cliente_data.clienteFacturas)).update(
            {Factura.cliente_1_id: db_cliente.id}, synchronize_session=False
        )
        database.commit()



    clienteOrdenes_ids = database.query(OrdenDeProduccion.id).filter(OrdenDeProduccion.cliente_id == db_cliente.id).all()
    clienteFacturas_ids = database.query(Factura.id).filter(Factura.cliente_1_id == db_cliente.id).all()
    response_data = {
        "cliente": db_cliente,
        "clienteOrdenes_ids": [x[0] for x in clienteOrdenes_ids],        "clienteFacturas_ids": [x[0] for x in clienteFacturas_ids]    }
    return response_data


@router.post("/cliente/bulk/", response_model=None, tags=["Cliente"])
async def bulk_create_cliente(items: list[ClienteCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Cliente entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_cliente = Cliente(
                telefono=item_data.telefono,                email=item_data.email,                idCliente=item_data.idCliente,                nombre=item_data.nombre,                tipoCliente=item_data.tipoCliente,                direccion=item_data.direccion            )
            database.add(db_cliente)
            database.flush()  # Get ID without committing
            created_items.append(db_cliente.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Cliente entities"
    }


@router.delete("/cliente/bulk/", response_model=None, tags=["Cliente"])
async def bulk_delete_cliente(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Cliente entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_cliente = database.query(Cliente).filter(Cliente.id == item_id).first()
        if db_cliente:
            database.delete(db_cliente)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Cliente entities"
    }

@router.put("/cliente/{cliente_id}/", response_model=None, tags=["Cliente"])
async def update_cliente(cliente_id: int, cliente_data: ClienteCreate, database: Session = Depends(get_db)) -> Cliente:
    db_cliente = database.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    setattr(db_cliente, 'telefono', cliente_data.telefono)
    setattr(db_cliente, 'email', cliente_data.email)
    setattr(db_cliente, 'idCliente', cliente_data.idCliente)
    setattr(db_cliente, 'nombre', cliente_data.nombre)
    setattr(db_cliente, 'tipoCliente', cliente_data.tipoCliente)
    setattr(db_cliente, 'direccion', cliente_data.direccion)
    if cliente_data.clienteOrdenes is not None:
        requested_clienteOrdenes = set(cliente_data.clienteOrdenes)
        current_clienteOrdenes = {
            getattr(item, 'id')
            for item in database.query(OrdenDeProduccion).filter(OrdenDeProduccion.cliente_id == db_cliente.id).all()
        }
        clienteOrdenes_to_detach = current_clienteOrdenes - requested_clienteOrdenes
        if clienteOrdenes_to_detach:
            raise HTTPException(status_code=409, detail="OrdenDeProduccion " + ", ".join(str(item) for item in sorted(clienteOrdenes_to_detach)) + " requires a cliente: reassign it instead of removing it")
        clienteOrdenes_to_attach = requested_clienteOrdenes - current_clienteOrdenes
        for ordendeproduccion_id in clienteOrdenes_to_attach:
            db_ordendeproduccion = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id == ordendeproduccion_id).first()
            if not db_ordendeproduccion:
                raise HTTPException(status_code=400, detail="OrdenDeProduccion with id " + str(ordendeproduccion_id) + " not found")
        if clienteOrdenes_to_attach:
            database.query(OrdenDeProduccion).filter(OrdenDeProduccion.id.in_(clienteOrdenes_to_attach)).update(
                {OrdenDeProduccion.cliente_id: db_cliente.id}, synchronize_session=False
            )
    if cliente_data.clienteFacturas is not None:
        requested_clienteFacturas = set(cliente_data.clienteFacturas)
        current_clienteFacturas = {
            getattr(item, 'id')
            for item in database.query(Factura).filter(Factura.cliente_1_id == db_cliente.id).all()
        }
        clienteFacturas_to_detach = current_clienteFacturas - requested_clienteFacturas
        if clienteFacturas_to_detach:
            raise HTTPException(status_code=409, detail="Factura " + ", ".join(str(item) for item in sorted(clienteFacturas_to_detach)) + " requires a cliente_1: reassign it instead of removing it")
        clienteFacturas_to_attach = requested_clienteFacturas - current_clienteFacturas
        for factura_id in clienteFacturas_to_attach:
            db_factura = database.query(Factura).filter(Factura.id == factura_id).first()
            if not db_factura:
                raise HTTPException(status_code=400, detail="Factura with id " + str(factura_id) + " not found")
        if clienteFacturas_to_attach:
            database.query(Factura).filter(Factura.id.in_(clienteFacturas_to_attach)).update(
                {Factura.cliente_1_id: db_cliente.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_cliente)

    clienteOrdenes_ids = database.query(OrdenDeProduccion.id).filter(OrdenDeProduccion.cliente_id == db_cliente.id).all()
    clienteFacturas_ids = database.query(Factura.id).filter(Factura.cliente_1_id == db_cliente.id).all()
    response_data = {
        "cliente": db_cliente,
        "clienteOrdenes_ids": [x[0] for x in clienteOrdenes_ids],        "clienteFacturas_ids": [x[0] for x in clienteFacturas_ids]    }
    return response_data


@router.delete("/cliente/{cliente_id}/", response_model=None, tags=["Cliente"])
async def delete_cliente(cliente_id: int, database: Session = Depends(get_db)):
    db_cliente = database.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    related_clienteOrdenes = db_cliente.clienteOrdenes
    for related in (list(related_clienteOrdenes) if isinstance(related_clienteOrdenes, list) else [item for item in [related_clienteOrdenes] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Cliente " + str(cliente_id) + ": OrdenDeProduccion " + str(getattr(related, 'id')) + " requires at least 1 cliente")
    related_clienteFacturas = db_cliente.clienteFacturas
    for related in (list(related_clienteFacturas) if isinstance(related_clienteFacturas, list) else [item for item in [related_clienteFacturas] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete Cliente " + str(cliente_id) + ": Factura " + str(getattr(related, 'id')) + " requires at least 1 cliente_1")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_cliente = {
        attr.key: getattr(db_cliente, attr.key)
        for attr in db_cliente.__mapper__.column_attrs
    }
    database.delete(db_cliente)
    database.commit()
    return deleted_cliente


@router.get("/cliente/{cliente_id}/clienteOrdenes/", response_model=None, tags=["Cliente Relationships"])
async def get_clienteOrdenes_of_cliente(cliente_id: int, database: Session = Depends(get_db)):
    """Get all OrdenDeProduccion entities related to this Cliente through clienteOrdenes"""
    db_cliente = database.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    clienteOrdenes_list = database.query(OrdenDeProduccion).filter(OrdenDeProduccion.cliente_id == cliente_id).all()

    return {
        "cliente_id": cliente_id,
        "clienteOrdenes_count": len(clienteOrdenes_list),
        "clienteOrdenes": clienteOrdenes_list
    }

@router.get("/cliente/{cliente_id}/clienteFacturas/", response_model=None, tags=["Cliente Relationships"])
async def get_clienteFacturas_of_cliente(cliente_id: int, database: Session = Depends(get_db)):
    """Get all Factura entities related to this Cliente through clienteFacturas"""
    db_cliente = database.query(Cliente).filter(Cliente.id == cliente_id).first()
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")

    clienteFacturas_list = database.query(Factura).filter(Factura.cliente_1_id == cliente_id).all()

    return {
        "cliente_id": cliente_id,
        "clienteFacturas_count": len(clienteFacturas_list),
        "clienteFacturas": clienteFacturas_list
    }




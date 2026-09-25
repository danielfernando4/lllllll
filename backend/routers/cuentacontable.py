from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/cuentacontable/", response_model=None, tags=["CuentaContable"])
def get_all_cuentacontable(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(CuentaContable)
        cuentacontable_list = query.all()

        # Serialize with relationships included
        result = []
        for cuentacontable_item in cuentacontable_list:
            item_dict = cuentacontable_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            movimientocontable_list = database.query(MovimientoContable).filter(MovimientoContable.cuentacontable_id == cuentacontable_item.id).all()
            item_dict['cuentaMovimientos'] = []
            for movimientocontable_obj in movimientocontable_list:
                movimientocontable_dict = movimientocontable_obj.__dict__.copy()
                movimientocontable_dict.pop('_sa_instance_state', None)
                item_dict['cuentaMovimientos'].append(movimientocontable_dict)
            movimientocontable_list = database.query(MovimientoContable).filter(MovimientoContable.movimientoCuenta_id == cuentacontable_item.id).all()
            item_dict['movimientocontable'] = []
            for movimientocontable_obj in movimientocontable_list:
                movimientocontable_dict = movimientocontable_obj.__dict__.copy()
                movimientocontable_dict.pop('_sa_instance_state', None)
                item_dict['movimientocontable'].append(movimientocontable_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(CuentaContable).all()


@router.get("/cuentacontable/count/", response_model=None, tags=["CuentaContable"])
def get_count_cuentacontable(database: Session = Depends(get_db)) -> dict:
    """Get the total count of CuentaContable entities"""
    count = database.query(CuentaContable).count()
    return {"count": count}


@router.get("/cuentacontable/paginated/", response_model=None, tags=["CuentaContable"])
def get_paginated_cuentacontable(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of CuentaContable entities"""
    total = database.query(CuentaContable).count()
    cuentacontable_list = database.query(CuentaContable).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": cuentacontable_list
        }

    result = []
    for cuentacontable_item in cuentacontable_list:
        cuentaMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.cuentacontable_id == cuentacontable_item.id).all()
        movimientocontable_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoCuenta_id == cuentacontable_item.id).all()
        item_data = {
            "cuentacontable": cuentacontable_item,
            "cuentaMovimientos_ids": [x[0] for x in cuentaMovimientos_ids],            "movimientocontable_ids": [x[0] for x in movimientocontable_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/cuentacontable/search/", response_model=None, tags=["CuentaContable"])
def search_cuentacontable(
    idCuenta: str = None,
    nombreCuenta: str = None,
    saldo: float = None,
    database: Session = Depends(get_db)
) -> list:
    """Search CuentaContable entities by attributes"""
    query = database.query(CuentaContable)

    if idCuenta is not None:
        query = query.filter(CuentaContable.idCuenta.ilike(f"%{idCuenta}%"))
    if nombreCuenta is not None:
        query = query.filter(CuentaContable.nombreCuenta.ilike(f"%{nombreCuenta}%"))
    if saldo is not None:
        query = query.filter(CuentaContable.saldo == saldo)

    results = query.all()
    return results


@router.get("/cuentacontable/{cuentacontable_id}/", response_model=None, tags=["CuentaContable"])
async def get_cuentacontable(cuentacontable_id: int, database: Session = Depends(get_db)) -> CuentaContable:
    db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == cuentacontable_id).first()
    if db_cuentacontable is None:
        raise HTTPException(status_code=404, detail="CuentaContable not found")

    cuentaMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.cuentacontable_id == db_cuentacontable.id).all()
    movimientocontable_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoCuenta_id == db_cuentacontable.id).all()
    response_data = {
        "cuentacontable": db_cuentacontable,
        "cuentaMovimientos_ids": [x[0] for x in cuentaMovimientos_ids],        "movimientocontable_ids": [x[0] for x in movimientocontable_ids]}
    return response_data



@router.post("/cuentacontable/", response_model=None, tags=["CuentaContable"])
async def create_cuentacontable(cuentacontable_data: CuentaContableCreate, database: Session = Depends(get_db)) -> CuentaContable:


    db_cuentacontable = CuentaContable(
        saldo=cuentacontable_data.saldo,        nombreCuenta=cuentacontable_data.nombreCuenta,        idCuenta=cuentacontable_data.idCuenta,        tipoCuenta=cuentacontable_data.tipoCuenta.value        )

    database.add(db_cuentacontable)
    database.commit()
    database.refresh(db_cuentacontable)

    if cuentacontable_data.cuentaMovimientos:
        # Validate that all MovimientoContable IDs exist
        for movimientocontable_id in cuentacontable_data.cuentaMovimientos:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail=f"MovimientoContable with id {movimientocontable_id} not found")

        # Update the related entities with the new foreign key
        database.query(MovimientoContable).filter(MovimientoContable.id.in_(cuentacontable_data.cuentaMovimientos)).update(
            {MovimientoContable.cuentacontable_id: db_cuentacontable.id}, synchronize_session=False
        )
        database.commit()
    if cuentacontable_data.movimientocontable:
        # Validate that all MovimientoContable IDs exist
        for movimientocontable_id in cuentacontable_data.movimientocontable:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail=f"MovimientoContable with id {movimientocontable_id} not found")

        # Update the related entities with the new foreign key
        database.query(MovimientoContable).filter(MovimientoContable.id.in_(cuentacontable_data.movimientocontable)).update(
            {MovimientoContable.movimientoCuenta_id: db_cuentacontable.id}, synchronize_session=False
        )
        database.commit()



    cuentaMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.cuentacontable_id == db_cuentacontable.id).all()
    movimientocontable_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoCuenta_id == db_cuentacontable.id).all()
    response_data = {
        "cuentacontable": db_cuentacontable,
        "cuentaMovimientos_ids": [x[0] for x in cuentaMovimientos_ids],        "movimientocontable_ids": [x[0] for x in movimientocontable_ids]    }
    return response_data


@router.post("/cuentacontable/bulk/", response_model=None, tags=["CuentaContable"])
async def bulk_create_cuentacontable(items: list[CuentaContableCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple CuentaContable entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_cuentacontable = CuentaContable(
                saldo=item_data.saldo,                nombreCuenta=item_data.nombreCuenta,                idCuenta=item_data.idCuenta,                tipoCuenta=item_data.tipoCuenta.value            )
            database.add(db_cuentacontable)
            database.flush()  # Get ID without committing
            created_items.append(db_cuentacontable.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} CuentaContable entities"
    }


@router.delete("/cuentacontable/bulk/", response_model=None, tags=["CuentaContable"])
async def bulk_delete_cuentacontable(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple CuentaContable entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == item_id).first()
        if db_cuentacontable:
            database.delete(db_cuentacontable)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} CuentaContable entities"
    }

@router.put("/cuentacontable/{cuentacontable_id}/", response_model=None, tags=["CuentaContable"])
async def update_cuentacontable(cuentacontable_id: int, cuentacontable_data: CuentaContableCreate, database: Session = Depends(get_db)) -> CuentaContable:
    db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == cuentacontable_id).first()
    if db_cuentacontable is None:
        raise HTTPException(status_code=404, detail="CuentaContable not found")

    setattr(db_cuentacontable, 'saldo', cuentacontable_data.saldo)
    setattr(db_cuentacontable, 'nombreCuenta', cuentacontable_data.nombreCuenta)
    setattr(db_cuentacontable, 'idCuenta', cuentacontable_data.idCuenta)
    setattr(db_cuentacontable, 'tipoCuenta', cuentacontable_data.tipoCuenta.value)
    if cuentacontable_data.cuentaMovimientos is not None:
        requested_cuentaMovimientos = set(cuentacontable_data.cuentaMovimientos)
        current_cuentaMovimientos = {
            getattr(item, 'id')
            for item in database.query(MovimientoContable).filter(MovimientoContable.cuentacontable_id == db_cuentacontable.id).all()
        }
        cuentaMovimientos_to_detach = current_cuentaMovimientos - requested_cuentaMovimientos
        if cuentaMovimientos_to_detach:
            raise HTTPException(status_code=409, detail="MovimientoContable " + ", ".join(str(item) for item in sorted(cuentaMovimientos_to_detach)) + " requires a cuentacontable: reassign it instead of removing it")
        cuentaMovimientos_to_attach = requested_cuentaMovimientos - current_cuentaMovimientos
        for movimientocontable_id in cuentaMovimientos_to_attach:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail="MovimientoContable with id " + str(movimientocontable_id) + " not found")
        if cuentaMovimientos_to_attach:
            database.query(MovimientoContable).filter(MovimientoContable.id.in_(cuentaMovimientos_to_attach)).update(
                {MovimientoContable.cuentacontable_id: db_cuentacontable.id}, synchronize_session=False
            )
    if cuentacontable_data.movimientocontable is not None:
        requested_movimientocontable = set(cuentacontable_data.movimientocontable)
        current_movimientocontable = {
            getattr(item, 'id')
            for item in database.query(MovimientoContable).filter(MovimientoContable.movimientoCuenta_id == db_cuentacontable.id).all()
        }
        movimientocontable_to_detach = current_movimientocontable - requested_movimientocontable
        if movimientocontable_to_detach:
            raise HTTPException(status_code=409, detail="MovimientoContable " + ", ".join(str(item) for item in sorted(movimientocontable_to_detach)) + " requires a movimientoCuenta: reassign it instead of removing it")
        movimientocontable_to_attach = requested_movimientocontable - current_movimientocontable
        for movimientocontable_id in movimientocontable_to_attach:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail="MovimientoContable with id " + str(movimientocontable_id) + " not found")
        if movimientocontable_to_attach:
            database.query(MovimientoContable).filter(MovimientoContable.id.in_(movimientocontable_to_attach)).update(
                {MovimientoContable.movimientoCuenta_id: db_cuentacontable.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_cuentacontable)

    cuentaMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.cuentacontable_id == db_cuentacontable.id).all()
    movimientocontable_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoCuenta_id == db_cuentacontable.id).all()
    response_data = {
        "cuentacontable": db_cuentacontable,
        "cuentaMovimientos_ids": [x[0] for x in cuentaMovimientos_ids],        "movimientocontable_ids": [x[0] for x in movimientocontable_ids]    }
    return response_data


@router.delete("/cuentacontable/{cuentacontable_id}/", response_model=None, tags=["CuentaContable"])
async def delete_cuentacontable(cuentacontable_id: int, database: Session = Depends(get_db)):
    db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == cuentacontable_id).first()
    if db_cuentacontable is None:
        raise HTTPException(status_code=404, detail="CuentaContable not found")
    related_cuentaMovimientos = db_cuentacontable.cuentaMovimientos
    for related in (list(related_cuentaMovimientos) if isinstance(related_cuentaMovimientos, list) else [item for item in [related_cuentaMovimientos] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete CuentaContable " + str(cuentacontable_id) + ": MovimientoContable " + str(getattr(related, 'id')) + " requires at least 1 cuentacontable")
    related_movimientocontable = db_cuentacontable.movimientocontable
    for related in (list(related_movimientocontable) if isinstance(related_movimientocontable, list) else [item for item in [related_movimientocontable] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete CuentaContable " + str(cuentacontable_id) + ": MovimientoContable " + str(getattr(related, 'id')) + " requires at least 1 movimientoCuenta")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_cuentacontable = {
        attr.key: getattr(db_cuentacontable, attr.key)
        for attr in db_cuentacontable.__mapper__.column_attrs
    }
    database.delete(db_cuentacontable)
    database.commit()
    return deleted_cuentacontable


@router.get("/cuentacontable/{cuentacontable_id}/cuentaMovimientos/", response_model=None, tags=["CuentaContable Relationships"])
async def get_cuentaMovimientos_of_cuentacontable(cuentacontable_id: int, database: Session = Depends(get_db)):
    """Get all MovimientoContable entities related to this CuentaContable through cuentaMovimientos"""
    db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == cuentacontable_id).first()
    if db_cuentacontable is None:
        raise HTTPException(status_code=404, detail="CuentaContable not found")

    cuentaMovimientos_list = database.query(MovimientoContable).filter(MovimientoContable.cuentacontable_id == cuentacontable_id).all()

    return {
        "cuentacontable_id": cuentacontable_id,
        "cuentaMovimientos_count": len(cuentaMovimientos_list),
        "cuentaMovimientos": cuentaMovimientos_list
    }

@router.get("/cuentacontable/{cuentacontable_id}/movimientocontable/", response_model=None, tags=["CuentaContable Relationships"])
async def get_movimientocontable_of_cuentacontable(cuentacontable_id: int, database: Session = Depends(get_db)):
    """Get all MovimientoContable entities related to this CuentaContable through movimientocontable"""
    db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == cuentacontable_id).first()
    if db_cuentacontable is None:
        raise HTTPException(status_code=404, detail="CuentaContable not found")

    movimientocontable_list = database.query(MovimientoContable).filter(MovimientoContable.movimientoCuenta_id == cuentacontable_id).all()

    return {
        "cuentacontable_id": cuentacontable_id,
        "movimientocontable_count": len(movimientocontable_list),
        "movimientocontable": movimientocontable_list
    }




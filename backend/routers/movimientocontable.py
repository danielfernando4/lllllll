from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/movimientocontable/", response_model=None, tags=["MovimientoContable"])
def get_all_movimientocontable(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(MovimientoContable)
        query = query.options(joinedload(MovimientoContable.cuentacontable))
        query = query.options(joinedload(MovimientoContable.asientocontable))
        query = query.options(joinedload(MovimientoContable.movimientoCuenta))
        query = query.options(joinedload(MovimientoContable.movimientoAsiento))
        movimientocontable_list = query.all()

        # Serialize with relationships included
        result = []
        for movimientocontable_item in movimientocontable_list:
            item_dict = movimientocontable_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if movimientocontable_item.cuentacontable:
                related_obj = movimientocontable_item.cuentacontable
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['cuentacontable'] = related_dict
            else:
                item_dict['cuentacontable'] = None
            if movimientocontable_item.asientocontable:
                related_obj = movimientocontable_item.asientocontable
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['asientocontable'] = related_dict
            else:
                item_dict['asientocontable'] = None
            if movimientocontable_item.movimientoCuenta:
                related_obj = movimientocontable_item.movimientoCuenta
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['movimientoCuenta'] = related_dict
            else:
                item_dict['movimientoCuenta'] = None
            if movimientocontable_item.movimientoAsiento:
                related_obj = movimientocontable_item.movimientoAsiento
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['movimientoAsiento'] = related_dict
            else:
                item_dict['movimientoAsiento'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(MovimientoContable).all()


@router.get("/movimientocontable/count/", response_model=None, tags=["MovimientoContable"])
def get_count_movimientocontable(database: Session = Depends(get_db)) -> dict:
    """Get the total count of MovimientoContable entities"""
    count = database.query(MovimientoContable).count()
    return {"count": count}


@router.get("/movimientocontable/paginated/", response_model=None, tags=["MovimientoContable"])
def get_paginated_movimientocontable(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of MovimientoContable entities"""
    total = database.query(MovimientoContable).count()
    movimientocontable_list = database.query(MovimientoContable).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": movimientocontable_list
    }
@router.get("/movimientocontable/search/", response_model=None, tags=["MovimientoContable"])
def search_movimientocontable(
    debe: float = None,
    haber: float = None,
    idMovimiento: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search MovimientoContable entities by attributes"""
    query = database.query(MovimientoContable)

    if debe is not None:
        query = query.filter(MovimientoContable.debe == debe)
    if haber is not None:
        query = query.filter(MovimientoContable.haber == haber)
    if idMovimiento is not None:
        query = query.filter(MovimientoContable.idMovimiento.ilike(f"%{idMovimiento}%"))

    results = query.all()
    return results


@router.get("/movimientocontable/{movimientocontable_id}/", response_model=None, tags=["MovimientoContable"])
async def get_movimientocontable(movimientocontable_id: int, database: Session = Depends(get_db)) -> MovimientoContable:
    db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
    if db_movimientocontable is None:
        raise HTTPException(status_code=404, detail="MovimientoContable not found")

    response_data = {
        "movimientocontable": db_movimientocontable,
}
    return response_data



@router.post("/movimientocontable/", response_model=None, tags=["MovimientoContable"])
async def create_movimientocontable(movimientocontable_data: MovimientoContableCreate, database: Session = Depends(get_db)) -> MovimientoContable:

    if movimientocontable_data.cuentacontable is not None:
        db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == movimientocontable_data.cuentacontable).first()
        if not db_cuentacontable:
            raise HTTPException(status_code=400, detail="CuentaContable not found")
    else:
        raise HTTPException(status_code=400, detail="CuentaContable ID is required")
    if movimientocontable_data.asientocontable is not None:
        db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == movimientocontable_data.asientocontable).first()
        if not db_asientocontable:
            raise HTTPException(status_code=400, detail="AsientoContable not found")
    else:
        raise HTTPException(status_code=400, detail="AsientoContable ID is required")
    if movimientocontable_data.movimientoCuenta is not None:
        db_movimientoCuenta = database.query(CuentaContable).filter(CuentaContable.id == movimientocontable_data.movimientoCuenta).first()
        if not db_movimientoCuenta:
            raise HTTPException(status_code=400, detail="CuentaContable not found")
    else:
        raise HTTPException(status_code=400, detail="CuentaContable ID is required")
    if movimientocontable_data.movimientoAsiento is not None:
        db_movimientoAsiento = database.query(AsientoContable).filter(AsientoContable.id == movimientocontable_data.movimientoAsiento).first()
        if not db_movimientoAsiento:
            raise HTTPException(status_code=400, detail="AsientoContable not found")
    else:
        raise HTTPException(status_code=400, detail="AsientoContable ID is required")

    db_movimientocontable = MovimientoContable(
        haber=movimientocontable_data.haber,        debe=movimientocontable_data.debe,        idMovimiento=movimientocontable_data.idMovimiento,        cuentacontable_id=movimientocontable_data.cuentacontable,        asientocontable_id=movimientocontable_data.asientocontable,        movimientoCuenta_id=movimientocontable_data.movimientoCuenta,        movimientoAsiento_id=movimientocontable_data.movimientoAsiento        )

    database.add(db_movimientocontable)
    database.commit()
    database.refresh(db_movimientocontable)




    return db_movimientocontable


@router.post("/movimientocontable/bulk/", response_model=None, tags=["MovimientoContable"])
async def bulk_create_movimientocontable(items: list[MovimientoContableCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple MovimientoContable entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.cuentacontable:
                raise ValueError("CuentaContable ID is required")
            if not item_data.asientocontable:
                raise ValueError("AsientoContable ID is required")
            if not item_data.movimientoCuenta:
                raise ValueError("CuentaContable ID is required")
            if not item_data.movimientoAsiento:
                raise ValueError("AsientoContable ID is required")

            db_movimientocontable = MovimientoContable(
                haber=item_data.haber,                debe=item_data.debe,                idMovimiento=item_data.idMovimiento,                cuentacontable_id=item_data.cuentacontable,                asientocontable_id=item_data.asientocontable,                movimientoCuenta_id=item_data.movimientoCuenta,                movimientoAsiento_id=item_data.movimientoAsiento            )
            database.add(db_movimientocontable)
            database.flush()  # Get ID without committing
            created_items.append(db_movimientocontable.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} MovimientoContable entities"
    }


@router.delete("/movimientocontable/bulk/", response_model=None, tags=["MovimientoContable"])
async def bulk_delete_movimientocontable(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple MovimientoContable entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == item_id).first()
        if db_movimientocontable:
            database.delete(db_movimientocontable)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} MovimientoContable entities"
    }

@router.put("/movimientocontable/{movimientocontable_id}/", response_model=None, tags=["MovimientoContable"])
async def update_movimientocontable(movimientocontable_id: int, movimientocontable_data: MovimientoContableCreate, database: Session = Depends(get_db)) -> MovimientoContable:
    db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
    if db_movimientocontable is None:
        raise HTTPException(status_code=404, detail="MovimientoContable not found")

    setattr(db_movimientocontable, 'haber', movimientocontable_data.haber)
    setattr(db_movimientocontable, 'debe', movimientocontable_data.debe)
    setattr(db_movimientocontable, 'idMovimiento', movimientocontable_data.idMovimiento)
    if movimientocontable_data.cuentacontable is not None:
        db_cuentacontable = database.query(CuentaContable).filter(CuentaContable.id == movimientocontable_data.cuentacontable).first()
        if not db_cuentacontable:
            raise HTTPException(status_code=400, detail="CuentaContable not found")
        setattr(db_movimientocontable, 'cuentacontable_id', movimientocontable_data.cuentacontable)
    if movimientocontable_data.asientocontable is not None:
        db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == movimientocontable_data.asientocontable).first()
        if not db_asientocontable:
            raise HTTPException(status_code=400, detail="AsientoContable not found")
        setattr(db_movimientocontable, 'asientocontable_id', movimientocontable_data.asientocontable)
    if movimientocontable_data.movimientoCuenta is not None:
        db_movimientoCuenta = database.query(CuentaContable).filter(CuentaContable.id == movimientocontable_data.movimientoCuenta).first()
        if not db_movimientoCuenta:
            raise HTTPException(status_code=400, detail="CuentaContable not found")
        setattr(db_movimientocontable, 'movimientoCuenta_id', movimientocontable_data.movimientoCuenta)
    if movimientocontable_data.movimientoAsiento is not None:
        db_movimientoAsiento = database.query(AsientoContable).filter(AsientoContable.id == movimientocontable_data.movimientoAsiento).first()
        if not db_movimientoAsiento:
            raise HTTPException(status_code=400, detail="AsientoContable not found")
        setattr(db_movimientocontable, 'movimientoAsiento_id', movimientocontable_data.movimientoAsiento)
    database.commit()
    database.refresh(db_movimientocontable)

    return db_movimientocontable


@router.delete("/movimientocontable/{movimientocontable_id}/", response_model=None, tags=["MovimientoContable"])
async def delete_movimientocontable(movimientocontable_id: int, database: Session = Depends(get_db)):
    db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
    if db_movimientocontable is None:
        raise HTTPException(status_code=404, detail="MovimientoContable not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_movimientocontable = {
        attr.key: getattr(db_movimientocontable, attr.key)
        for attr in db_movimientocontable.__mapper__.column_attrs
    }
    database.delete(db_movimientocontable)
    database.commit()
    return deleted_movimientocontable





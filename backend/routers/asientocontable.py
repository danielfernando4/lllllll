from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/asientocontable/", response_model=None, tags=["AsientoContable"])
def get_all_asientocontable(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(AsientoContable)
        asientocontable_list = query.all()

        # Serialize with relationships included
        result = []
        for asientocontable_item in asientocontable_list:
            item_dict = asientocontable_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            movimientocontable_list = database.query(MovimientoContable).filter(MovimientoContable.asientocontable_id == asientocontable_item.id).all()
            item_dict['asientoMovimientos'] = []
            for movimientocontable_obj in movimientocontable_list:
                movimientocontable_dict = movimientocontable_obj.__dict__.copy()
                movimientocontable_dict.pop('_sa_instance_state', None)
                item_dict['asientoMovimientos'].append(movimientocontable_dict)
            movimientocontable_list = database.query(MovimientoContable).filter(MovimientoContable.movimientoAsiento_id == asientocontable_item.id).all()
            item_dict['movimientocontable_1'] = []
            for movimientocontable_obj in movimientocontable_list:
                movimientocontable_dict = movimientocontable_obj.__dict__.copy()
                movimientocontable_dict.pop('_sa_instance_state', None)
                item_dict['movimientocontable_1'].append(movimientocontable_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(AsientoContable).all()


@router.get("/asientocontable/count/", response_model=None, tags=["AsientoContable"])
def get_count_asientocontable(database: Session = Depends(get_db)) -> dict:
    """Get the total count of AsientoContable entities"""
    count = database.query(AsientoContable).count()
    return {"count": count}


@router.get("/asientocontable/paginated/", response_model=None, tags=["AsientoContable"])
def get_paginated_asientocontable(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of AsientoContable entities"""
    total = database.query(AsientoContable).count()
    asientocontable_list = database.query(AsientoContable).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": asientocontable_list
        }

    result = []
    for asientocontable_item in asientocontable_list:
        asientoMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.asientocontable_id == asientocontable_item.id).all()
        movimientocontable_1_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoAsiento_id == asientocontable_item.id).all()
        item_data = {
            "asientocontable": asientocontable_item,
            "asientoMovimientos_ids": [x[0] for x in asientoMovimientos_ids],            "movimientocontable_1_ids": [x[0] for x in movimientocontable_1_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }
@router.get("/asientocontable/search/", response_model=None, tags=["AsientoContable"])
def search_asientocontable(
    descripcion: str = None,
    idAsiento: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search AsientoContable entities by attributes"""
    query = database.query(AsientoContable)

    if descripcion is not None:
        query = query.filter(AsientoContable.descripcion.ilike(f"%{descripcion}%"))
    if idAsiento is not None:
        query = query.filter(AsientoContable.idAsiento.ilike(f"%{idAsiento}%"))

    results = query.all()
    return results


@router.get("/asientocontable/{asientocontable_id}/", response_model=None, tags=["AsientoContable"])
async def get_asientocontable(asientocontable_id: int, database: Session = Depends(get_db)) -> AsientoContable:
    db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == asientocontable_id).first()
    if db_asientocontable is None:
        raise HTTPException(status_code=404, detail="AsientoContable not found")

    asientoMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.asientocontable_id == db_asientocontable.id).all()
    movimientocontable_1_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoAsiento_id == db_asientocontable.id).all()
    response_data = {
        "asientocontable": db_asientocontable,
        "asientoMovimientos_ids": [x[0] for x in asientoMovimientos_ids],        "movimientocontable_1_ids": [x[0] for x in movimientocontable_1_ids]}
    return response_data



@router.post("/asientocontable/", response_model=None, tags=["AsientoContable"])
async def create_asientocontable(asientocontable_data: AsientoContableCreate, database: Session = Depends(get_db)) -> AsientoContable:


    db_asientocontable = AsientoContable(
        idAsiento=asientocontable_data.idAsiento,        descripcion=asientocontable_data.descripcion,        fecha=asientocontable_data.fecha        )

    database.add(db_asientocontable)
    database.commit()
    database.refresh(db_asientocontable)

    if asientocontable_data.asientoMovimientos:
        # Validate that all MovimientoContable IDs exist
        for movimientocontable_id in asientocontable_data.asientoMovimientos:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail=f"MovimientoContable with id {movimientocontable_id} not found")

        # Update the related entities with the new foreign key
        database.query(MovimientoContable).filter(MovimientoContable.id.in_(asientocontable_data.asientoMovimientos)).update(
            {MovimientoContable.asientocontable_id: db_asientocontable.id}, synchronize_session=False
        )
        database.commit()
    if asientocontable_data.movimientocontable_1:
        # Validate that all MovimientoContable IDs exist
        for movimientocontable_id in asientocontable_data.movimientocontable_1:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail=f"MovimientoContable with id {movimientocontable_id} not found")

        # Update the related entities with the new foreign key
        database.query(MovimientoContable).filter(MovimientoContable.id.in_(asientocontable_data.movimientocontable_1)).update(
            {MovimientoContable.movimientoAsiento_id: db_asientocontable.id}, synchronize_session=False
        )
        database.commit()



    asientoMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.asientocontable_id == db_asientocontable.id).all()
    movimientocontable_1_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoAsiento_id == db_asientocontable.id).all()
    response_data = {
        "asientocontable": db_asientocontable,
        "asientoMovimientos_ids": [x[0] for x in asientoMovimientos_ids],        "movimientocontable_1_ids": [x[0] for x in movimientocontable_1_ids]    }
    return response_data


@router.post("/asientocontable/bulk/", response_model=None, tags=["AsientoContable"])
async def bulk_create_asientocontable(items: list[AsientoContableCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple AsientoContable entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_asientocontable = AsientoContable(
                idAsiento=item_data.idAsiento,                descripcion=item_data.descripcion,                fecha=item_data.fecha            )
            database.add(db_asientocontable)
            database.flush()  # Get ID without committing
            created_items.append(db_asientocontable.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} AsientoContable entities"
    }


@router.delete("/asientocontable/bulk/", response_model=None, tags=["AsientoContable"])
async def bulk_delete_asientocontable(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple AsientoContable entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == item_id).first()
        if db_asientocontable:
            database.delete(db_asientocontable)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} AsientoContable entities"
    }

@router.put("/asientocontable/{asientocontable_id}/", response_model=None, tags=["AsientoContable"])
async def update_asientocontable(asientocontable_id: int, asientocontable_data: AsientoContableCreate, database: Session = Depends(get_db)) -> AsientoContable:
    db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == asientocontable_id).first()
    if db_asientocontable is None:
        raise HTTPException(status_code=404, detail="AsientoContable not found")

    setattr(db_asientocontable, 'idAsiento', asientocontable_data.idAsiento)
    setattr(db_asientocontable, 'descripcion', asientocontable_data.descripcion)
    setattr(db_asientocontable, 'fecha', asientocontable_data.fecha)
    if asientocontable_data.asientoMovimientos is not None:
        requested_asientoMovimientos = set(asientocontable_data.asientoMovimientos)
        current_asientoMovimientos = {
            getattr(item, 'id')
            for item in database.query(MovimientoContable).filter(MovimientoContable.asientocontable_id == db_asientocontable.id).all()
        }
        asientoMovimientos_to_detach = current_asientoMovimientos - requested_asientoMovimientos
        if asientoMovimientos_to_detach:
            raise HTTPException(status_code=409, detail="MovimientoContable " + ", ".join(str(item) for item in sorted(asientoMovimientos_to_detach)) + " requires a asientocontable: reassign it instead of removing it")
        asientoMovimientos_to_attach = requested_asientoMovimientos - current_asientoMovimientos
        for movimientocontable_id in asientoMovimientos_to_attach:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail="MovimientoContable with id " + str(movimientocontable_id) + " not found")
        if asientoMovimientos_to_attach:
            database.query(MovimientoContable).filter(MovimientoContable.id.in_(asientoMovimientos_to_attach)).update(
                {MovimientoContable.asientocontable_id: db_asientocontable.id}, synchronize_session=False
            )
    if asientocontable_data.movimientocontable_1 is not None:
        requested_movimientocontable_1 = set(asientocontable_data.movimientocontable_1)
        current_movimientocontable_1 = {
            getattr(item, 'id')
            for item in database.query(MovimientoContable).filter(MovimientoContable.movimientoAsiento_id == db_asientocontable.id).all()
        }
        movimientocontable_1_to_detach = current_movimientocontable_1 - requested_movimientocontable_1
        if movimientocontable_1_to_detach:
            raise HTTPException(status_code=409, detail="MovimientoContable " + ", ".join(str(item) for item in sorted(movimientocontable_1_to_detach)) + " requires a movimientoAsiento: reassign it instead of removing it")
        movimientocontable_1_to_attach = requested_movimientocontable_1 - current_movimientocontable_1
        for movimientocontable_id in movimientocontable_1_to_attach:
            db_movimientocontable = database.query(MovimientoContable).filter(MovimientoContable.id == movimientocontable_id).first()
            if not db_movimientocontable:
                raise HTTPException(status_code=400, detail="MovimientoContable with id " + str(movimientocontable_id) + " not found")
        if movimientocontable_1_to_attach:
            database.query(MovimientoContable).filter(MovimientoContable.id.in_(movimientocontable_1_to_attach)).update(
                {MovimientoContable.movimientoAsiento_id: db_asientocontable.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_asientocontable)

    asientoMovimientos_ids = database.query(MovimientoContable.id).filter(MovimientoContable.asientocontable_id == db_asientocontable.id).all()
    movimientocontable_1_ids = database.query(MovimientoContable.id).filter(MovimientoContable.movimientoAsiento_id == db_asientocontable.id).all()
    response_data = {
        "asientocontable": db_asientocontable,
        "asientoMovimientos_ids": [x[0] for x in asientoMovimientos_ids],        "movimientocontable_1_ids": [x[0] for x in movimientocontable_1_ids]    }
    return response_data


@router.delete("/asientocontable/{asientocontable_id}/", response_model=None, tags=["AsientoContable"])
async def delete_asientocontable(asientocontable_id: int, database: Session = Depends(get_db)):
    db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == asientocontable_id).first()
    if db_asientocontable is None:
        raise HTTPException(status_code=404, detail="AsientoContable not found")
    related_asientoMovimientos = db_asientocontable.asientoMovimientos
    for related in (list(related_asientoMovimientos) if isinstance(related_asientoMovimientos, list) else [item for item in [related_asientoMovimientos] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete AsientoContable " + str(asientocontable_id) + ": MovimientoContable " + str(getattr(related, 'id')) + " requires at least 1 asientocontable")
    related_movimientocontable_1 = db_asientocontable.movimientocontable_1
    for related in (list(related_movimientocontable_1) if isinstance(related_movimientocontable_1, list) else [item for item in [related_movimientocontable_1] if item is not None]):
        remaining = 0
        if remaining < 1:
            raise HTTPException(status_code=409, detail="Cannot delete AsientoContable " + str(asientocontable_id) + ": MovimientoContable " + str(getattr(related, 'id')) + " requires at least 1 movimientoAsiento")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_asientocontable = {
        attr.key: getattr(db_asientocontable, attr.key)
        for attr in db_asientocontable.__mapper__.column_attrs
    }
    database.delete(db_asientocontable)
    database.commit()
    return deleted_asientocontable


@router.get("/asientocontable/{asientocontable_id}/asientoMovimientos/", response_model=None, tags=["AsientoContable Relationships"])
async def get_asientoMovimientos_of_asientocontable(asientocontable_id: int, database: Session = Depends(get_db)):
    """Get all MovimientoContable entities related to this AsientoContable through asientoMovimientos"""
    db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == asientocontable_id).first()
    if db_asientocontable is None:
        raise HTTPException(status_code=404, detail="AsientoContable not found")

    asientoMovimientos_list = database.query(MovimientoContable).filter(MovimientoContable.asientocontable_id == asientocontable_id).all()

    return {
        "asientocontable_id": asientocontable_id,
        "asientoMovimientos_count": len(asientoMovimientos_list),
        "asientoMovimientos": asientoMovimientos_list
    }

@router.get("/asientocontable/{asientocontable_id}/movimientocontable_1/", response_model=None, tags=["AsientoContable Relationships"])
async def get_movimientocontable_1_of_asientocontable(asientocontable_id: int, database: Session = Depends(get_db)):
    """Get all MovimientoContable entities related to this AsientoContable through movimientocontable_1"""
    db_asientocontable = database.query(AsientoContable).filter(AsientoContable.id == asientocontable_id).first()
    if db_asientocontable is None:
        raise HTTPException(status_code=404, detail="AsientoContable not found")

    movimientocontable_1_list = database.query(MovimientoContable).filter(MovimientoContable.movimientoAsiento_id == asientocontable_id).all()

    return {
        "asientocontable_id": asientocontable_id,
        "movimientocontable_1_count": len(movimientocontable_1_list),
        "movimientocontable_1": movimientocontable_1_list
    }




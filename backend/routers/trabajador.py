from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/trabajador/", response_model=None, tags=["Trabajador"])
def get_all_trabajador(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    return database.query(Trabajador).all()


@router.get("/trabajador/count/", response_model=None, tags=["Trabajador"])
def get_count_trabajador(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Trabajador entities"""
    count = database.query(Trabajador).count()
    return {"count": count}


@router.get("/trabajador/paginated/", response_model=None, tags=["Trabajador"])
def get_paginated_trabajador(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Trabajador entities"""
    total = database.query(Trabajador).count()
    trabajador_list = database.query(Trabajador).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": trabajador_list
    }
@router.get("/trabajador/search/", response_model=None, tags=["Trabajador"])
def search_trabajador(
    idTrabajador: str = None,
    nombre: str = None,
    puesto: str = None,
    sueldo: float = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Trabajador entities by attributes"""
    query = database.query(Trabajador)

    if idTrabajador is not None:
        query = query.filter(Trabajador.idTrabajador.ilike(f"%{idTrabajador}%"))
    if nombre is not None:
        query = query.filter(Trabajador.nombre.ilike(f"%{nombre}%"))
    if puesto is not None:
        query = query.filter(Trabajador.puesto.ilike(f"%{puesto}%"))
    if sueldo is not None:
        query = query.filter(Trabajador.sueldo == sueldo)

    results = query.all()
    return results


@router.get("/trabajador/{trabajador_id}/", response_model=None, tags=["Trabajador"])
async def get_trabajador(trabajador_id: int, database: Session = Depends(get_db)) -> Trabajador:
    db_trabajador = database.query(Trabajador).filter(Trabajador.id == trabajador_id).first()
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador not found")

    response_data = {
        "trabajador": db_trabajador,
}
    return response_data



@router.post("/trabajador/", response_model=None, tags=["Trabajador"])
async def create_trabajador(trabajador_data: TrabajadorCreate, database: Session = Depends(get_db)) -> Trabajador:


    db_trabajador = Trabajador(
        fechaIngreso=trabajador_data.fechaIngreso,        nombre=trabajador_data.nombre,        sueldo=trabajador_data.sueldo,        idTrabajador=trabajador_data.idTrabajador,        puesto=trabajador_data.puesto        )

    database.add(db_trabajador)
    database.commit()
    database.refresh(db_trabajador)




    return db_trabajador


@router.post("/trabajador/bulk/", response_model=None, tags=["Trabajador"])
async def bulk_create_trabajador(items: list[TrabajadorCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Trabajador entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_trabajador = Trabajador(
                fechaIngreso=item_data.fechaIngreso,                nombre=item_data.nombre,                sueldo=item_data.sueldo,                idTrabajador=item_data.idTrabajador,                puesto=item_data.puesto            )
            database.add(db_trabajador)
            database.flush()  # Get ID without committing
            created_items.append(db_trabajador.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Trabajador entities"
    }


@router.delete("/trabajador/bulk/", response_model=None, tags=["Trabajador"])
async def bulk_delete_trabajador(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Trabajador entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_trabajador = database.query(Trabajador).filter(Trabajador.id == item_id).first()
        if db_trabajador:
            database.delete(db_trabajador)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Trabajador entities"
    }

@router.put("/trabajador/{trabajador_id}/", response_model=None, tags=["Trabajador"])
async def update_trabajador(trabajador_id: int, trabajador_data: TrabajadorCreate, database: Session = Depends(get_db)) -> Trabajador:
    db_trabajador = database.query(Trabajador).filter(Trabajador.id == trabajador_id).first()
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador not found")

    setattr(db_trabajador, 'fechaIngreso', trabajador_data.fechaIngreso)
    setattr(db_trabajador, 'nombre', trabajador_data.nombre)
    setattr(db_trabajador, 'sueldo', trabajador_data.sueldo)
    setattr(db_trabajador, 'idTrabajador', trabajador_data.idTrabajador)
    setattr(db_trabajador, 'puesto', trabajador_data.puesto)
    database.commit()
    database.refresh(db_trabajador)

    return db_trabajador


@router.delete("/trabajador/{trabajador_id}/", response_model=None, tags=["Trabajador"])
async def delete_trabajador(trabajador_id: int, database: Session = Depends(get_db)):
    db_trabajador = database.query(Trabajador).filter(Trabajador.id == trabajador_id).first()
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_trabajador = {
        attr.key: getattr(db_trabajador, attr.key)
        for attr in db_trabajador.__mapper__.column_attrs
    }
    database.delete(db_trabajador)
    database.commit()
    return deleted_trabajador





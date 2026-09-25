import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from routers import ordendecompra as ordendecompra_router
from routers import itemordendeproduccion as itemordendeproduccion_router
from routers import ordendeproduccion as ordendeproduccion_router
from routers import producto as producto_router
from routers import trabajador as trabajador_router
from routers import proveedor as proveedor_router
from routers import movimientocontable as movimientocontable_router
from routers import cliente as cliente_router
from routers import asientocontable as asientocontable_router
from routers import cuentacontable as cuentacontable_router
from routers import itemfactura as itemfactura_router
from routers import factura as factura_router
from routers import itemordendecompra as itemordendecompra_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ERP_manufactura API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "OrdenDeCompra", "description": "Operations for OrdenDeCompra entities"},
        {"name": "OrdenDeCompra Relationships", "description": "Manage OrdenDeCompra relationships"},
        {"name": "ItemOrdenDeProduccion", "description": "Operations for ItemOrdenDeProduccion entities"},
        {"name": "ItemOrdenDeProduccion Relationships", "description": "Manage ItemOrdenDeProduccion relationships"},
        {"name": "OrdenDeProduccion", "description": "Operations for OrdenDeProduccion entities"},
        {"name": "OrdenDeProduccion Relationships", "description": "Manage OrdenDeProduccion relationships"},
        {"name": "Producto", "description": "Operations for Producto entities"},
        {"name": "Producto Relationships", "description": "Manage Producto relationships"},
        {"name": "Trabajador", "description": "Operations for Trabajador entities"},
        {"name": "Proveedor", "description": "Operations for Proveedor entities"},
        {"name": "Proveedor Relationships", "description": "Manage Proveedor relationships"},
        {"name": "MovimientoContable", "description": "Operations for MovimientoContable entities"},
        {"name": "MovimientoContable Relationships", "description": "Manage MovimientoContable relationships"},
        {"name": "Cliente", "description": "Operations for Cliente entities"},
        {"name": "Cliente Relationships", "description": "Manage Cliente relationships"},
        {"name": "AsientoContable", "description": "Operations for AsientoContable entities"},
        {"name": "AsientoContable Relationships", "description": "Manage AsientoContable relationships"},
        {"name": "CuentaContable", "description": "Operations for CuentaContable entities"},
        {"name": "CuentaContable Relationships", "description": "Manage CuentaContable relationships"},
        {"name": "ItemFactura", "description": "Operations for ItemFactura entities"},
        {"name": "ItemFactura Relationships", "description": "Manage ItemFactura relationships"},
        {"name": "Factura", "description": "Operations for Factura entities"},
        {"name": "Factura Relationships", "description": "Manage Factura relationships"},
        {"name": "ItemOrdenDeCompra", "description": "Operations for ItemOrdenDeCompra entities"},
        {"name": "ItemOrdenDeCompra Relationships", "description": "Manage ItemOrdenDeCompra relationships"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format.

    `detail` carries the endpoint's actual message — clients (including the
    generated frontend dialog) read it to show the user what went wrong.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": exc.detail
        }
    )

############################################
#
#   Routers
#
############################################

app.include_router(ordendecompra_router.router)
app.include_router(itemordendeproduccion_router.router)
app.include_router(ordendeproduccion_router.router)
app.include_router(producto_router.router)
app.include_router(trabajador_router.router)
app.include_router(proveedor_router.router)
app.include_router(movimientocontable_router.router)
app.include_router(cliente_router.router)
app.include_router(asientocontable_router.router)
app.include_router(cuentacontable_router.router)
app.include_router(itemfactura_router.router)
app.include_router(factura_router.router)
app.include_router(itemordendecompra_router.router)

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "ERP_manufactura API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check(database: Session = Depends(get_db)):
    """Health check endpoint for monitoring.

    Actually touches the database — a health check that hardcodes
    "connected" is worse than none.
    """
    from datetime import datetime
    from sqlalchemy import text as _sql_text
    try:
        database.execute(_sql_text("SELECT 1"))
        db_status = "connected"
    except Exception:
        raise HTTPException(status_code=503, detail={
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "database": "error",
        })
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["ordendecompra_count"] = database.query(OrdenDeCompra).count()
    stats["itemordendeproduccion_count"] = database.query(ItemOrdenDeProduccion).count()
    stats["ordendeproduccion_count"] = database.query(OrdenDeProduccion).count()
    stats["producto_count"] = database.query(Producto).count()
    stats["trabajador_count"] = database.query(Trabajador).count()
    stats["proveedor_count"] = database.query(Proveedor).count()
    stats["movimientocontable_count"] = database.query(MovimientoContable).count()
    stats["cliente_count"] = database.query(Cliente).count()
    stats["asientocontable_count"] = database.query(AsientoContable).count()
    stats["cuentacontable_count"] = database.query(CuentaContable).count()
    stats["itemfactura_count"] = database.query(ItemFactura).count()
    stats["factura_count"] = database.query(Factura).count()
    stats["itemordendecompra_count"] = database.query(ItemOrdenDeCompra).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
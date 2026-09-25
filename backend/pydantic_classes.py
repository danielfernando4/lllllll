from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

class FacturaEstado(Enum):
    Pendiente = "Pendiente"
    Vencido = "Vencido"
    Pagado = "Pagado"

class CuentaContableTipo(Enum):
    Pasivo = "Pasivo"
    Gasto = "Gasto"
    Patrimonio = "Patrimonio"
    Ingreso = "Ingreso"
    Activo = "Activo"

class OrdenDeProduccionEstado(Enum):
    Finalizada = "Finalizada"
    Pendiente = "Pendiente"
    Cancelada = "Cancelada"
    EnProceso = "EnProceso"

class OrdenDeCompraEstado(Enum):
    Pendiente = "Pendiente"
    Recibida = "Recibida"
    Cancelada = "Cancelada"

############################################
# Classes are defined here
############################################
class OrdenDeCompraCreate(BaseModel):
    estado: OrdenDeCompraEstado
    fechaRecepcionEsperada: date
    idOrdenCompra: str
    fechaCreacion: date
    proveedor: int  # N:1 Relationship (mandatory)
    ordenCompraItems: Optional[List[int]] = None  # 1:N Relationship


class ItemOrdenDeProduccionCreate(BaseModel):
    observaciones: Optional[str] = None
    idItem: str
    cantidad: int
    ordendeproduccion: int  # N:1 Relationship (mandatory)
    producto: int  # N:1 Relationship (mandatory)


class OrdenDeProduccionCreate(BaseModel):
    estado: OrdenDeProduccionEstado
    fechaEntrega: date
    idOrdenProd: str
    fechaCreacion: date
    cliente: int  # N:1 Relationship (mandatory)
    ordenItems: Optional[List[int]] = None  # 1:N Relationship


class ProductoCreate(BaseModel):
    idProducto: str
    descripcion: str
    nombre: str
    unidadMedida: str
    precioUnitario: float
    stockDisponible: Optional[int] = 0
    productoItemsFactura: Optional[List[int]] = None  # 1:N Relationship
    productoItemsOrdenCompra: Optional[List[int]] = None  # 1:N Relationship
    productoItemsOrdenProd: Optional[List[int]] = None  # 1:N Relationship


class TrabajadorCreate(BaseModel):
    fechaIngreso: date
    nombre: str
    sueldo: float
    idTrabajador: str
    puesto: str


class ProveedorCreate(BaseModel):
    tipoProveedor: Optional[str] = None
    email: str
    nombre: str
    telefono: str
    idProveedor: str
    direccion: str
    proveedorOrdenesCompra: Optional[List[int]] = None  # 1:N Relationship


class MovimientoContableCreate(BaseModel):
    haber: float = 0.0
    debe: float = 0.0
    idMovimiento: str
    cuentacontable: int  # N:1 Relationship (mandatory)
    asientocontable: int  # N:1 Relationship (mandatory)
    movimientoCuenta: int  # N:1 Relationship (mandatory)
    movimientoAsiento: int  # N:1 Relationship (mandatory)


class ClienteCreate(BaseModel):
    telefono: str
    email: str
    idCliente: str
    nombre: str
    tipoCliente: Optional[str] = None
    direccion: str
    clienteOrdenes: Optional[List[int]] = None  # 1:N Relationship
    clienteFacturas: Optional[List[int]] = None  # 1:N Relationship


class AsientoContableCreate(BaseModel):
    idAsiento: str
    descripcion: str
    fecha: date
    asientoMovimientos: Optional[List[int]] = None  # 1:N Relationship
    movimientocontable_1: Optional[List[int]] = None  # 1:N Relationship


class CuentaContableCreate(BaseModel):
    saldo: float = 0.0
    nombreCuenta: str
    idCuenta: str
    tipoCuenta: CuentaContableTipo
    cuentaMovimientos: Optional[List[int]] = None  # 1:N Relationship
    movimientocontable: Optional[List[int]] = None  # 1:N Relationship


class ItemFacturaCreate(BaseModel):
    subtotal: float = 0.0
    cantidad: int
    idItem: str
    precioUnitario: float
    factura: int  # N:1 Relationship (mandatory)
    producto_2: int  # N:1 Relationship (mandatory)


class FacturaCreate(BaseModel):
    fechaEmision: date
    total: float = 0.0
    idFactura: str
    estadoPago: FacturaEstado
    facturaItems: Optional[List[int]] = None  # 1:N Relationship
    cliente_1: int  # N:1 Relationship (mandatory)


class ItemOrdenDeCompraCreate(BaseModel):
    precioUnitario: float
    cantidad: int
    idItem: str
    ordendecompra: int  # N:1 Relationship (mandatory)
    producto_1: int  # N:1 Relationship (mandatory)



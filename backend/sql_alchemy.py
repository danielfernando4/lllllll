import enum
import os
from typing import List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Column as Column_, ForeignKey as ForeignKey_, Table as Table_,
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_,
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_,
    Interval as Interval_, PickleType as PickleType_, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped as Mapped_, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date, timedelta as dt_timedelta
from uuid import uuid4 as _uuid4


def _new_str_id() -> str:
    """Server-side surrogate for string primary keys named ``id``.

    A string PK has no autoincrement; without a default every INSERT dies
    on NOT NULL (the id is in nobody's hands: create schemas rightly
    exclude the server-owned ``id``, so the server must mint it).
    """
    return _uuid4().hex

class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class FacturaEstado(enum.Enum):
    Pendiente = "Pendiente"
    Vencido = "Vencido"
    Pagado = "Pagado"

class CuentaContableTipo(enum.Enum):
    Pasivo = "Pasivo"
    Gasto = "Gasto"
    Patrimonio = "Patrimonio"
    Ingreso = "Ingreso"
    Activo = "Activo"

class OrdenDeProduccionEstado(enum.Enum):
    Finalizada = "Finalizada"
    Pendiente = "Pendiente"
    Cancelada = "Cancelada"
    EnProceso = "EnProceso"

class OrdenDeCompraEstado(enum.Enum):
    Pendiente = "Pendiente"
    Recibida = "Recibida"
    Cancelada = "Cancelada"


# Tables definition for many-to-many relationships

# Tables definition
class OrdenDeCompra(Base):
    __tablename__ = "ordendecompra"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idOrdenCompra: Mapped_[str] = mapped_column(String_(100))
    fechaCreacion: Mapped_[dt_date] = mapped_column(Date_)
    fechaRecepcionEsperada: Mapped_[dt_date] = mapped_column(Date_)
    estado: Mapped_[OrdenDeCompraEstado] = mapped_column(Enum(OrdenDeCompraEstado))
    proveedor_id: Mapped_[int] = mapped_column(ForeignKey_("proveedor.id"))

class ItemOrdenDeProduccion(Base):
    __tablename__ = "itemordendeproduccion"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idItem: Mapped_[str] = mapped_column(String_(100))
    cantidad: Mapped_[int] = mapped_column(Integer_)
    observaciones: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    producto_id: Mapped_[int] = mapped_column(ForeignKey_("producto.id"))
    ordendeproduccion_id: Mapped_[int] = mapped_column(ForeignKey_("ordendeproduccion.id"))

class OrdenDeProduccion(Base):
    __tablename__ = "ordendeproduccion"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idOrdenProd: Mapped_[str] = mapped_column(String_(100))
    fechaCreacion: Mapped_[dt_date] = mapped_column(Date_)
    fechaEntrega: Mapped_[dt_date] = mapped_column(Date_)
    estado: Mapped_[OrdenDeProduccionEstado] = mapped_column(Enum(OrdenDeProduccionEstado))
    cliente_id: Mapped_[int] = mapped_column(ForeignKey_("cliente.id"))

class Producto(Base):
    __tablename__ = "producto"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idProducto: Mapped_[str] = mapped_column(String_(100))
    nombre: Mapped_[str] = mapped_column(String_(100))
    descripcion: Mapped_[str] = mapped_column(String_(100))
    precioUnitario: Mapped_[float] = mapped_column(Float_)
    unidadMedida: Mapped_[str] = mapped_column(String_(100))
    stockDisponible: Mapped_[Optional_[int]] = mapped_column(Integer_, nullable=True, default=0)

class Trabajador(Base):
    __tablename__ = "trabajador"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idTrabajador: Mapped_[str] = mapped_column(String_(100))
    nombre: Mapped_[str] = mapped_column(String_(100))
    puesto: Mapped_[str] = mapped_column(String_(100))
    sueldo: Mapped_[float] = mapped_column(Float_)
    fechaIngreso: Mapped_[dt_date] = mapped_column(Date_)

class Proveedor(Base):
    __tablename__ = "proveedor"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idProveedor: Mapped_[str] = mapped_column(String_(100))
    nombre: Mapped_[str] = mapped_column(String_(100))
    direccion: Mapped_[str] = mapped_column(String_(100))
    telefono: Mapped_[str] = mapped_column(String_(100))
    email: Mapped_[str] = mapped_column(String_(100))
    tipoProveedor: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)

class MovimientoContable(Base):
    __tablename__ = "movimientocontable"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idMovimiento: Mapped_[str] = mapped_column(String_(100))
    debe: Mapped_[float] = mapped_column(Float_, default=0.0)
    haber: Mapped_[float] = mapped_column(Float_, default=0.0)
    cuentacontable_id: Mapped_[int] = mapped_column(ForeignKey_("cuentacontable.id"))
    movimientoCuenta_id: Mapped_[int] = mapped_column(ForeignKey_("cuentacontable.id"))
    asientocontable_id: Mapped_[int] = mapped_column(ForeignKey_("asientocontable.id"))
    movimientoAsiento_id: Mapped_[int] = mapped_column(ForeignKey_("asientocontable.id"))

class Cliente(Base):
    __tablename__ = "cliente"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idCliente: Mapped_[str] = mapped_column(String_(100))
    nombre: Mapped_[str] = mapped_column(String_(100))
    direccion: Mapped_[str] = mapped_column(String_(100))
    telefono: Mapped_[str] = mapped_column(String_(100))
    email: Mapped_[str] = mapped_column(String_(100))
    tipoCliente: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)

class AsientoContable(Base):
    __tablename__ = "asientocontable"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idAsiento: Mapped_[str] = mapped_column(String_(100))
    fecha: Mapped_[dt_date] = mapped_column(Date_)
    descripcion: Mapped_[str] = mapped_column(String_(100))

class CuentaContable(Base):
    __tablename__ = "cuentacontable"
    id: Mapped_[int] = mapped_column(primary_key=True)
    saldo: Mapped_[float] = mapped_column(Float_, default=0.0)
    idCuenta: Mapped_[str] = mapped_column(String_(100))
    nombreCuenta: Mapped_[str] = mapped_column(String_(100))
    tipoCuenta: Mapped_[CuentaContableTipo] = mapped_column(Enum(CuentaContableTipo))

class ItemFactura(Base):
    __tablename__ = "itemfactura"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idItem: Mapped_[str] = mapped_column(String_(100))
    cantidad: Mapped_[int] = mapped_column(Integer_)
    precioUnitario: Mapped_[float] = mapped_column(Float_)
    subtotal: Mapped_[float] = mapped_column(Float_, default=0.0)
    producto_2_id: Mapped_[int] = mapped_column(ForeignKey_("producto.id"))
    factura_id: Mapped_[int] = mapped_column(ForeignKey_("factura.id"))

class Factura(Base):
    __tablename__ = "factura"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idFactura: Mapped_[str] = mapped_column(String_(100))
    fechaEmision: Mapped_[dt_date] = mapped_column(Date_)
    total: Mapped_[float] = mapped_column(Float_, default=0.0)
    estadoPago: Mapped_[FacturaEstado] = mapped_column(Enum(FacturaEstado))
    cliente_1_id: Mapped_[int] = mapped_column(ForeignKey_("cliente.id"))

class ItemOrdenDeCompra(Base):
    __tablename__ = "itemordendecompra"
    id: Mapped_[int] = mapped_column(primary_key=True)
    idItem: Mapped_[str] = mapped_column(String_(100))
    cantidad: Mapped_[int] = mapped_column(Integer_)
    precioUnitario: Mapped_[float] = mapped_column(Float_)
    producto_1_id: Mapped_[int] = mapped_column(ForeignKey_("producto.id"))
    ordendecompra_id: Mapped_[int] = mapped_column(ForeignKey_("ordendecompra.id"))


#--- Relationships of the ordendecompra table
OrdenDeCompra.ordenCompraItems: Mapped_[List_["ItemOrdenDeCompra"]] = relationship("ItemOrdenDeCompra", back_populates="ordendecompra", foreign_keys=[ItemOrdenDeCompra.ordendecompra_id])

OrdenDeCompra.proveedor: Mapped_["Proveedor"] = relationship("Proveedor", back_populates="proveedorOrdenesCompra", uselist=False, foreign_keys=[OrdenDeCompra.proveedor_id])

#--- Relationships of the itemordendeproduccion table

ItemOrdenDeProduccion.producto: Mapped_["Producto"] = relationship("Producto", back_populates="productoItemsOrdenProd", uselist=False, foreign_keys=[ItemOrdenDeProduccion.producto_id])

ItemOrdenDeProduccion.ordendeproduccion: Mapped_["OrdenDeProduccion"] = relationship("OrdenDeProduccion", back_populates="ordenItems", uselist=False, foreign_keys=[ItemOrdenDeProduccion.ordendeproduccion_id])

#--- Relationships of the ordendeproduccion table
OrdenDeProduccion.ordenItems: Mapped_[List_["ItemOrdenDeProduccion"]] = relationship("ItemOrdenDeProduccion", back_populates="ordendeproduccion", foreign_keys=[ItemOrdenDeProduccion.ordendeproduccion_id])

OrdenDeProduccion.cliente: Mapped_["Cliente"] = relationship("Cliente", back_populates="clienteOrdenes", uselist=False, foreign_keys=[OrdenDeProduccion.cliente_id])

#--- Relationships of the producto table
Producto.productoItemsOrdenCompra: Mapped_[List_["ItemOrdenDeCompra"]] = relationship("ItemOrdenDeCompra", back_populates="producto_1", foreign_keys=[ItemOrdenDeCompra.producto_1_id])
Producto.productoItemsOrdenProd: Mapped_[List_["ItemOrdenDeProduccion"]] = relationship("ItemOrdenDeProduccion", back_populates="producto", foreign_keys=[ItemOrdenDeProduccion.producto_id])
Producto.productoItemsFactura: Mapped_[List_["ItemFactura"]] = relationship("ItemFactura", back_populates="producto_2", foreign_keys=[ItemFactura.producto_2_id])

#--- Relationships of the proveedor table
Proveedor.proveedorOrdenesCompra: Mapped_[List_["OrdenDeCompra"]] = relationship("OrdenDeCompra", back_populates="proveedor", foreign_keys=[OrdenDeCompra.proveedor_id])

#--- Relationships of the movimientocontable table

MovimientoContable.cuentacontable: Mapped_["CuentaContable"] = relationship("CuentaContable", back_populates="cuentaMovimientos", uselist=False, foreign_keys=[MovimientoContable.cuentacontable_id])

MovimientoContable.movimientoCuenta: Mapped_["CuentaContable"] = relationship("CuentaContable", back_populates="movimientocontable", uselist=False, foreign_keys=[MovimientoContable.movimientoCuenta_id])

MovimientoContable.asientocontable: Mapped_["AsientoContable"] = relationship("AsientoContable", back_populates="asientoMovimientos", uselist=False, foreign_keys=[MovimientoContable.asientocontable_id])

MovimientoContable.movimientoAsiento: Mapped_["AsientoContable"] = relationship("AsientoContable", back_populates="movimientocontable_1", uselist=False, foreign_keys=[MovimientoContable.movimientoAsiento_id])

#--- Relationships of the cliente table
Cliente.clienteFacturas: Mapped_[List_["Factura"]] = relationship("Factura", back_populates="cliente_1", foreign_keys=[Factura.cliente_1_id])
Cliente.clienteOrdenes: Mapped_[List_["OrdenDeProduccion"]] = relationship("OrdenDeProduccion", back_populates="cliente", foreign_keys=[OrdenDeProduccion.cliente_id])

#--- Relationships of the asientocontable table
AsientoContable.asientoMovimientos: Mapped_[List_["MovimientoContable"]] = relationship("MovimientoContable", back_populates="asientocontable", foreign_keys=[MovimientoContable.asientocontable_id])
AsientoContable.movimientocontable_1: Mapped_[List_["MovimientoContable"]] = relationship("MovimientoContable", back_populates="movimientoAsiento", foreign_keys=[MovimientoContable.movimientoAsiento_id])

#--- Relationships of the cuentacontable table
CuentaContable.cuentaMovimientos: Mapped_[List_["MovimientoContable"]] = relationship("MovimientoContable", back_populates="cuentacontable", foreign_keys=[MovimientoContable.cuentacontable_id])
CuentaContable.movimientocontable: Mapped_[List_["MovimientoContable"]] = relationship("MovimientoContable", back_populates="movimientoCuenta", foreign_keys=[MovimientoContable.movimientoCuenta_id])

#--- Relationships of the itemfactura table

ItemFactura.producto_2: Mapped_["Producto"] = relationship("Producto", back_populates="productoItemsFactura", uselist=False, foreign_keys=[ItemFactura.producto_2_id])

ItemFactura.factura: Mapped_["Factura"] = relationship("Factura", back_populates="facturaItems", uselist=False, foreign_keys=[ItemFactura.factura_id])

#--- Relationships of the factura table

Factura.cliente_1: Mapped_["Cliente"] = relationship("Cliente", back_populates="clienteFacturas", uselist=False, foreign_keys=[Factura.cliente_1_id])
Factura.facturaItems: Mapped_[List_["ItemFactura"]] = relationship("ItemFactura", back_populates="factura", foreign_keys=[ItemFactura.factura_id])

#--- Relationships of the itemordendecompra table

ItemOrdenDeCompra.producto_1: Mapped_["Producto"] = relationship("Producto", back_populates="productoItemsOrdenCompra", uselist=False, foreign_keys=[ItemOrdenDeCompra.producto_1_id])

ItemOrdenDeCompra.ordendecompra: Mapped_["OrdenDeCompra"] = relationship("OrdenDeCompra", back_populates="ordenCompraItems", uselist=False, foreign_keys=[ItemOrdenDeCompra.ordendecompra_id])

# Database connection (override the default with the DATABASE_URL environment variable)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/ERP_manufactura.db")  # SQLite connection
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    # Create tables in the database only when this module is executed directly,
    # so importing it never touches the database as a side effect.
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)  # folder for the default SQLite database
    Base.metadata.create_all(engine, checkfirst=True)
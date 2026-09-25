####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Enumerations
OrdenDeProduccionEstado: Enumeration = Enumeration(
    name="OrdenDeProduccionEstado",
    literals={
            EnumerationLiteral(name="Pendiente"),
			EnumerationLiteral(name="EnProceso"),
			EnumerationLiteral(name="Finalizada"),
			EnumerationLiteral(name="Cancelada")
    }
)

OrdenDeCompraEstado: Enumeration = Enumeration(
    name="OrdenDeCompraEstado",
    literals={
            EnumerationLiteral(name="Pendiente"),
			EnumerationLiteral(name="Recibida"),
			EnumerationLiteral(name="Cancelada")
    }
)

FacturaEstado: Enumeration = Enumeration(
    name="FacturaEstado",
    literals={
            EnumerationLiteral(name="Pendiente"),
			EnumerationLiteral(name="Pagado"),
			EnumerationLiteral(name="Vencido")
    }
)

CuentaContableTipo: Enumeration = Enumeration(
    name="CuentaContableTipo",
    literals={
            EnumerationLiteral(name="Activo"),
			EnumerationLiteral(name="Pasivo"),
			EnumerationLiteral(name="Patrimonio"),
			EnumerationLiteral(name="Ingreso"),
			EnumerationLiteral(name="Gasto")
    }
)

# Classes
ItemOrdenDeCompra = Class(name="ItemOrdenDeCompra")
Factura = Class(name="Factura")
ItemFactura = Class(name="ItemFactura")
CuentaContable = Class(name="CuentaContable")
AsientoContable = Class(name="AsientoContable")
Cliente = Class(name="Cliente")
MovimientoContable = Class(name="MovimientoContable")
Proveedor = Class(name="Proveedor")
Trabajador = Class(name="Trabajador")
Producto = Class(name="Producto")
OrdenDeProduccion = Class(name="OrdenDeProduccion")
ItemOrdenDeProduccion = Class(name="ItemOrdenDeProduccion")
OrdenDeCompra = Class(name="OrdenDeCompra")

# ItemOrdenDeCompra class attributes and methods
ItemOrdenDeCompra_idItem: Property = Property(name="idItem", type=StringType, visibility="private")
ItemOrdenDeCompra_cantidad: Property = Property(name="cantidad", type=IntegerType, visibility="private")
ItemOrdenDeCompra_precioUnitario: Property = Property(name="precioUnitario", type=FloatType, visibility="private")
ItemOrdenDeCompra.attributes={ItemOrdenDeCompra_cantidad, ItemOrdenDeCompra_idItem, ItemOrdenDeCompra_precioUnitario}

# Factura class attributes and methods
Factura_idFactura: Property = Property(name="idFactura", type=StringType, visibility="private")
Factura_fechaEmision: Property = Property(name="fechaEmision", type=DateType, visibility="private")
Factura_total: Property = Property(name="total", type=FloatType, visibility="private", is_derived=True, default_value="0.0")
Factura_estadoPago: Property = Property(name="estadoPago", type=FacturaEstado, visibility="private")
Factura.attributes={Factura_estadoPago, Factura_fechaEmision, Factura_idFactura, Factura_total}

# ItemFactura class attributes and methods
ItemFactura_idItem: Property = Property(name="idItem", type=StringType, visibility="private")
ItemFactura_cantidad: Property = Property(name="cantidad", type=IntegerType, visibility="private")
ItemFactura_precioUnitario: Property = Property(name="precioUnitario", type=FloatType, visibility="private")
ItemFactura_subtotal: Property = Property(name="subtotal", type=FloatType, visibility="private", is_derived=True, default_value="0.0")
ItemFactura.attributes={ItemFactura_cantidad, ItemFactura_idItem, ItemFactura_precioUnitario, ItemFactura_subtotal}

# CuentaContable class attributes and methods
CuentaContable_saldo: Property = Property(name="saldo", type=FloatType, visibility="private", default_value="0.0")
CuentaContable_idCuenta: Property = Property(name="idCuenta", type=StringType, visibility="private")
CuentaContable_nombreCuenta: Property = Property(name="nombreCuenta", type=StringType, visibility="private")
CuentaContable_tipoCuenta: Property = Property(name="tipoCuenta", type=CuentaContableTipo, visibility="private")
CuentaContable.attributes={CuentaContable_idCuenta, CuentaContable_nombreCuenta, CuentaContable_saldo, CuentaContable_tipoCuenta}

# AsientoContable class attributes and methods
AsientoContable_idAsiento: Property = Property(name="idAsiento", type=StringType, visibility="private")
AsientoContable_fecha: Property = Property(name="fecha", type=DateType, visibility="private")
AsientoContable_descripcion: Property = Property(name="descripcion", type=StringType, visibility="private")
AsientoContable.attributes={AsientoContable_descripcion, AsientoContable_fecha, AsientoContable_idAsiento}

# Cliente class attributes and methods
Cliente_idCliente: Property = Property(name="idCliente", type=StringType, visibility="private")
Cliente_nombre: Property = Property(name="nombre", type=StringType, visibility="private")
Cliente_direccion: Property = Property(name="direccion", type=StringType, visibility="private")
Cliente_telefono: Property = Property(name="telefono", type=StringType, visibility="private")
Cliente_email: Property = Property(name="email", type=StringType, visibility="private")
Cliente_tipoCliente: Property = Property(name="tipoCliente", type=StringType, visibility="private", is_optional=True)
Cliente.attributes={Cliente_direccion, Cliente_email, Cliente_idCliente, Cliente_nombre, Cliente_telefono, Cliente_tipoCliente}

# MovimientoContable class attributes and methods
MovimientoContable_idMovimiento: Property = Property(name="idMovimiento", type=StringType, visibility="private")
MovimientoContable_debe: Property = Property(name="debe", type=FloatType, visibility="private", default_value="0.0")
MovimientoContable_haber: Property = Property(name="haber", type=FloatType, visibility="private", default_value="0.0")
MovimientoContable.attributes={MovimientoContable_debe, MovimientoContable_haber, MovimientoContable_idMovimiento}

# Proveedor class attributes and methods
Proveedor_idProveedor: Property = Property(name="idProveedor", type=StringType, visibility="private")
Proveedor_nombre: Property = Property(name="nombre", type=StringType, visibility="private")
Proveedor_direccion: Property = Property(name="direccion", type=StringType, visibility="private")
Proveedor_telefono: Property = Property(name="telefono", type=StringType, visibility="private")
Proveedor_email: Property = Property(name="email", type=StringType, visibility="private")
Proveedor_tipoProveedor: Property = Property(name="tipoProveedor", type=StringType, visibility="private", is_optional=True)
Proveedor.attributes={Proveedor_direccion, Proveedor_email, Proveedor_idProveedor, Proveedor_nombre, Proveedor_telefono, Proveedor_tipoProveedor}

# Trabajador class attributes and methods
Trabajador_idTrabajador: Property = Property(name="idTrabajador", type=StringType, visibility="private")
Trabajador_nombre: Property = Property(name="nombre", type=StringType, visibility="private")
Trabajador_puesto: Property = Property(name="puesto", type=StringType, visibility="private")
Trabajador_sueldo: Property = Property(name="sueldo", type=FloatType, visibility="private")
Trabajador_fechaIngreso: Property = Property(name="fechaIngreso", type=DateType, visibility="private")
Trabajador.attributes={Trabajador_fechaIngreso, Trabajador_idTrabajador, Trabajador_nombre, Trabajador_puesto, Trabajador_sueldo}

# Producto class attributes and methods
Producto_idProducto: Property = Property(name="idProducto", type=StringType, visibility="private")
Producto_nombre: Property = Property(name="nombre", type=StringType, visibility="private")
Producto_descripcion: Property = Property(name="descripcion", type=StringType, visibility="private")
Producto_precioUnitario: Property = Property(name="precioUnitario", type=FloatType, visibility="private")
Producto_unidadMedida: Property = Property(name="unidadMedida", type=StringType, visibility="private")
Producto_stockDisponible: Property = Property(name="stockDisponible", type=IntegerType, visibility="private", is_optional=True, default_value="0")
Producto.attributes={Producto_descripcion, Producto_idProducto, Producto_nombre, Producto_precioUnitario, Producto_stockDisponible, Producto_unidadMedida}

# OrdenDeProduccion class attributes and methods
OrdenDeProduccion_idOrdenProd: Property = Property(name="idOrdenProd", type=StringType, visibility="private")
OrdenDeProduccion_fechaCreacion: Property = Property(name="fechaCreacion", type=DateType, visibility="private")
OrdenDeProduccion_fechaEntrega: Property = Property(name="fechaEntrega", type=DateType, visibility="private")
OrdenDeProduccion_estado: Property = Property(name="estado", type=OrdenDeProduccionEstado, visibility="private")
OrdenDeProduccion.attributes={OrdenDeProduccion_estado, OrdenDeProduccion_fechaCreacion, OrdenDeProduccion_fechaEntrega, OrdenDeProduccion_idOrdenProd}

# ItemOrdenDeProduccion class attributes and methods
ItemOrdenDeProduccion_idItem: Property = Property(name="idItem", type=StringType, visibility="private")
ItemOrdenDeProduccion_cantidad: Property = Property(name="cantidad", type=IntegerType, visibility="private")
ItemOrdenDeProduccion_observaciones: Property = Property(name="observaciones", type=StringType, visibility="private", is_optional=True)
ItemOrdenDeProduccion.attributes={ItemOrdenDeProduccion_cantidad, ItemOrdenDeProduccion_idItem, ItemOrdenDeProduccion_observaciones}

# OrdenDeCompra class attributes and methods
OrdenDeCompra_idOrdenCompra: Property = Property(name="idOrdenCompra", type=StringType, visibility="private")
OrdenDeCompra_fechaCreacion: Property = Property(name="fechaCreacion", type=DateType, visibility="private")
OrdenDeCompra_fechaRecepcionEsperada: Property = Property(name="fechaRecepcionEsperada", type=DateType, visibility="private")
OrdenDeCompra_estado: Property = Property(name="estado", type=OrdenDeCompraEstado, visibility="private")
OrdenDeCompra.attributes={OrdenDeCompra_estado, OrdenDeCompra_fechaCreacion, OrdenDeCompra_fechaRecepcionEsperada, OrdenDeCompra_idOrdenCompra}

# Relationships
clienteFacturas: BinaryAssociation = BinaryAssociation(
    name="clienteFacturas",
    ends={
        Property(name="cliente_1", type=Cliente, multiplicity=Multiplicity(1, 1)),
        Property(name="clienteFacturas", type=Factura, multiplicity=Multiplicity(0, 9999))
    }
)
facturaItems: BinaryAssociation = BinaryAssociation(
    name="facturaItems",
    ends={
        Property(name="factura", type=Factura, multiplicity=Multiplicity(1, 1)),
        Property(name="facturaItems", type=ItemFactura, multiplicity=Multiplicity(0, 9999), is_composite=True)
    }
)
clienteOrdenes: BinaryAssociation = BinaryAssociation(
    name="clienteOrdenes",
    ends={
        Property(name="cliente", type=Cliente, multiplicity=Multiplicity(1, 1)),
        Property(name="clienteOrdenes", type=OrdenDeProduccion, multiplicity=Multiplicity(0, 9999))
    }
)
productoItemsFactura: BinaryAssociation = BinaryAssociation(
    name="productoItemsFactura",
    ends={
        Property(name="producto_2", type=Producto, multiplicity=Multiplicity(1, 1)),
        Property(name="productoItemsFactura", type=ItemFactura, multiplicity=Multiplicity(0, 9999))
    }
)
ordenItems: BinaryAssociation = BinaryAssociation(
    name="ordenItems",
    ends={
        Property(name="ordendeproduccion", type=OrdenDeProduccion, multiplicity=Multiplicity(1, 1)),
        Property(name="ordenItems", type=ItemOrdenDeProduccion, multiplicity=Multiplicity(0, 9999), is_composite=True)
    }
)
cuentaMovimientos: BinaryAssociation = BinaryAssociation(
    name="cuentaMovimientos",
    ends={
        Property(name="cuentacontable", type=CuentaContable, multiplicity=Multiplicity(1, 1)),
        Property(name="cuentaMovimientos", type=MovimientoContable, multiplicity=Multiplicity(0, 9999))
    }
)
asientoMovimientos: BinaryAssociation = BinaryAssociation(
    name="asientoMovimientos",
    ends={
        Property(name="asientocontable", type=AsientoContable, multiplicity=Multiplicity(1, 1)),
        Property(name="asientoMovimientos", type=MovimientoContable, multiplicity=Multiplicity(0, 9999), is_composite=True)
    }
)
productoItemsOrdenProd: BinaryAssociation = BinaryAssociation(
    name="productoItemsOrdenProd",
    ends={
        Property(name="producto", type=Producto, multiplicity=Multiplicity(1, 1)),
        Property(name="productoItemsOrdenProd", type=ItemOrdenDeProduccion, multiplicity=Multiplicity(0, 9999))
    }
)
movimientoCuenta: BinaryAssociation = BinaryAssociation(
    name="movimientoCuenta",
    ends={
        Property(name="movimientocontable", type=MovimientoContable, multiplicity=Multiplicity(0, 9999)),
        Property(name="movimientoCuenta", type=CuentaContable, multiplicity=Multiplicity(1, 1))
    }
)
proveedorOrdenesCompra: BinaryAssociation = BinaryAssociation(
    name="proveedorOrdenesCompra",
    ends={
        Property(name="proveedor", type=Proveedor, multiplicity=Multiplicity(1, 1)),
        Property(name="proveedorOrdenesCompra", type=OrdenDeCompra, multiplicity=Multiplicity(0, 9999))
    }
)
ordenCompraItems: BinaryAssociation = BinaryAssociation(
    name="ordenCompraItems",
    ends={
        Property(name="ordendecompra", type=OrdenDeCompra, multiplicity=Multiplicity(1, 1)),
        Property(name="ordenCompraItems", type=ItemOrdenDeCompra, multiplicity=Multiplicity(0, 9999), is_composite=True)
    }
)
movimientoAsiento: BinaryAssociation = BinaryAssociation(
    name="movimientoAsiento",
    ends={
        Property(name="movimientocontable_1", type=MovimientoContable, multiplicity=Multiplicity(0, 9999)),
        Property(name="movimientoAsiento", type=AsientoContable, multiplicity=Multiplicity(1, 1))
    }
)
productoItemsOrdenCompra: BinaryAssociation = BinaryAssociation(
    name="productoItemsOrdenCompra",
    ends={
        Property(name="producto_1", type=Producto, multiplicity=Multiplicity(1, 1)),
        Property(name="productoItemsOrdenCompra", type=ItemOrdenDeCompra, multiplicity=Multiplicity(0, 9999))
    }
)

# Domain Model
domain_model = DomainModel(
    name="ERP_manufactura",
    types={ItemOrdenDeCompra, Factura, ItemFactura, CuentaContable, AsientoContable, Cliente, MovimientoContable, Proveedor, Trabajador, Producto, OrdenDeProduccion, ItemOrdenDeProduccion, OrdenDeCompra, OrdenDeProduccionEstado, OrdenDeCompraEstado, FacturaEstado, CuentaContableTipo},
    associations={clienteFacturas, facturaItems, clienteOrdenes, productoItemsFactura, ordenItems, cuentaMovimientos, asientoMovimientos, productoItemsOrdenProd, movimientoCuenta, proveedorOrdenesCompra, ordenCompraItems, movimientoAsiento, productoItemsOrdenCompra},
    generalizations={},
    metadata=None
)

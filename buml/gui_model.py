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


###############
#  GUI MODEL  #
###############

from besser.BUML.metamodel.gui import (
    GUIModel, Module, Screen,
    ViewComponent, ViewContainer,
    Button, ButtonType, ButtonActionType,
    Text, Image, Link, InputField, InputFieldType, SelectOption,
    Alert, AlertSeverity,
    Form, Menu, MenuItem, DataList,
    DataSource, DataSourceElement, EmbeddedContent,
    Styling, Size, Position, Color, Layout, LayoutType,
    UnitSize, PositionType, Alignment
)
from besser.BUML.metamodel.gui.dashboard import (
    LineChart, BarChart, PieChart, RadarChart, RadialBarChart, Table, AgentComponent,
    Column, FieldColumn, LookupColumn, ExpressionColumn,
    Map, MapLayer, MapLayerType, WorldMap, LocationMap, MetricCard, Series
)
from besser.BUML.metamodel.gui.events_actions import (
    Event, EventType, Transition, Create, Read, Update, Delete, Parameter
)
from besser.BUML.metamodel.gui.binding import DataBinding

# Module: GUI_Module

# Screen: wrapper
wrapper = Screen(name="wrapper", description="Cliente", view_elements=set(), is_main_page=True, route_path="/cliente", screen_size="Medium")
wrapper.component_id = "page-cliente-0"
iykph = Text(
    name="iykph",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="iykph",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "iykph"}
)
iozx1 = Link(
    name="iozx1",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iozx1",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "iozx1"}
)
ih8hj = Link(
    name="ih8hj",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ih8hj",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "ih8hj"}
)
i1qkm = Link(
    name="i1qkm",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i1qkm",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "i1qkm"}
)
izkc8 = Link(
    name="izkc8",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="izkc8",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "izkc8"}
)
iph2r = Link(
    name="iph2r",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iph2r",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "iph2r"}
)
inf5e = Link(
    name="inf5e",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="inf5e",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "inf5e"}
)
imxyi = Link(
    name="imxyi",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imxyi",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "imxyi"}
)
iqsah = Link(
    name="iqsah",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iqsah",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "iqsah"}
)
iz831 = Link(
    name="iz831",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iz831",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "iz831"}
)
ikfsj = Link(
    name="ikfsj",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ikfsj",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "ikfsj"}
)
i5pui = Link(
    name="i5pui",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i5pui",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "i5pui"}
)
i12ao = Link(
    name="i12ao",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i12ao",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "i12ao"}
)
i7gfa = Link(
    name="i7gfa",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7gfa",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i7gfa"}
)
i9g3w = ViewContainer(
    name="i9g3w",
    description=" component",
    view_elements={iozx1, ih8hj, i1qkm, izkc8, iph2r, inf5e, imxyi, iqsah, iz831, ikfsj, i5pui, i12ao, i7gfa},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="i9g3w",
    display_order=1,
    custom_attributes={"id": "i9g3w"}
)
i9g3w_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
i9g3w.layout = i9g3w_layout
ixlpp = Text(
    name="ixlpp",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ixlpp",
    display_order=2,
    custom_attributes={"id": "ixlpp"}
)
imwws = ViewContainer(
    name="imwws",
    description="nav container",
    view_elements={iykph, i9g3w, ixlpp},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="imwws",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "imwws"}
)
imwws_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
imwws.layout = imwws_layout
i3cup = Text(
    name="i3cup",
    content="Cliente",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="i3cup",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "i3cup"}
)
ihvpy = Text(
    name="ihvpy",
    content="Manage Cliente data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ihvpy",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ihvpy"}
)
table_cliente_0_col_0 = FieldColumn(label="IdCliente", field=Cliente_idCliente)
table_cliente_0_col_1 = FieldColumn(label="Nombre", field=Cliente_nombre)
table_cliente_0_col_2 = FieldColumn(label="Direccion", field=Cliente_direccion)
table_cliente_0_col_3 = FieldColumn(label="Telefono", field=Cliente_telefono)
table_cliente_0_col_4 = FieldColumn(label="Email", field=Cliente_email)
table_cliente_0_col_5 = FieldColumn(label="TipoCliente", field=Cliente_tipoCliente)
table_cliente_0_col_6_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "clienteOrdenes")
table_cliente_0_col_6 = LookupColumn(label="ClienteOrdenes", path=table_cliente_0_col_6_path, field=OrdenDeProduccion_idOrdenProd)
table_cliente_0_col_7_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "clienteFacturas")
table_cliente_0_col_7 = LookupColumn(label="ClienteFacturas", path=table_cliente_0_col_7_path, field=Factura_idFactura)
table_cliente_0 = Table(
    name="table_cliente_0",
    title="Cliente List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_cliente_0_col_0, table_cliente_0_col_1, table_cliente_0_col_2, table_cliente_0_col_3, table_cliente_0_col_4, table_cliente_0_col_5, table_cliente_0_col_6, table_cliente_0_col_7],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-cliente-0",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Cliente List", "data-source": "class_a972xjff0_muhb7pxa_ci0", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idCliente', 'label': 'IdCliente', 'columnType': 'field', '_expanded': False}, {'field': 'nombre', 'label': 'Nombre', 'columnType': 'field', '_expanded': False}, {'field': 'direccion', 'label': 'Direccion', 'columnType': 'field', '_expanded': False}, {'field': 'telefono', 'label': 'Telefono', 'columnType': 'field', '_expanded': False}, {'field': 'email', 'label': 'Email', 'columnType': 'field', '_expanded': False}, {'field': 'tipoCliente', 'label': 'TipoCliente', 'columnType': 'field', '_expanded': False}, {'field': 'clienteOrdenes', 'label': 'ClienteOrdenes', 'columnType': 'lookup', 'lookupEntity': 'class_w54mwuy3g_muhb7pxa_xzj', 'lookupField': 'idOrdenProd', '_expanded': False}, {'field': 'clienteFacturas', 'label': 'ClienteFacturas', 'columnType': 'lookup', 'lookupEntity': 'class_78m7ywlbr_muhb7pxa_0b1', 'lookupField': 'idFactura', '_expanded': False}], "id": "table-cliente-0", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_cliente_0_binding_domain = None
if domain_model_ref is not None:
    table_cliente_0_binding_domain = domain_model_ref.get_class_by_name("Cliente")
if table_cliente_0_binding_domain:
    table_cliente_0_binding = DataBinding(domain_concept=table_cliente_0_binding_domain, name="ClienteDataBinding")
else:
    # Domain class 'Cliente' not resolved; data binding skipped.
    table_cliente_0_binding = None
if table_cliente_0_binding:
    table_cliente_0.data_binding = table_cliente_0_binding
itcdr = ViewContainer(
    name="itcdr",
    description="main container",
    view_elements={i3cup, ihvpy, table_cliente_0},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="itcdr",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "itcdr"}
)
itcdr_layout = Layout(flex="1")
itcdr.layout = itcdr_layout
i3a44 = ViewContainer(
    name="i3a44",
    description=" component",
    view_elements={imwws, itcdr},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i3a44",
    display_order=0,
    custom_attributes={"id": "i3a44"}
)
i3a44_layout = Layout(layout_type=LayoutType.FLEX)
i3a44.layout = i3a44_layout
wrapper.view_elements = {i3a44}


# Screen: wrapper_10
wrapper_10 = Screen(name="wrapper_10", description="CuentaContable", view_elements=set(), route_path="/cuentacontable", screen_size="Medium")
wrapper_10.component_id = "page-cuentacontable-9"
iu60cw = Text(
    name="iu60cw",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="iu60cw",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "iu60cw"}
)
inl5za = Link(
    name="inl5za",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="inl5za",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "inl5za"}
)
idt7qf = Link(
    name="idt7qf",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="idt7qf",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "idt7qf"}
)
i8i8tu = Link(
    name="i8i8tu",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8i8tu",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "i8i8tu"}
)
ik7kfz = Link(
    name="ik7kfz",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ik7kfz",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "ik7kfz"}
)
iazad9 = Link(
    name="iazad9",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iazad9",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "iazad9"}
)
iklboe = Link(
    name="iklboe",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iklboe",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "iklboe"}
)
irm0do = Link(
    name="irm0do",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="irm0do",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "irm0do"}
)
ii4oh8 = Link(
    name="ii4oh8",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ii4oh8",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "ii4oh8"}
)
ijurrd = Link(
    name="ijurrd",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ijurrd",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "ijurrd"}
)
i66r1l = Link(
    name="i66r1l",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i66r1l",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "i66r1l"}
)
irzdsh = Link(
    name="irzdsh",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="irzdsh",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "irzdsh"}
)
iborqc = Link(
    name="iborqc",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iborqc",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "iborqc"}
)
i6hk4k = Link(
    name="i6hk4k",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i6hk4k",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i6hk4k"}
)
iku7jq = ViewContainer(
    name="iku7jq",
    description=" component",
    view_elements={inl5za, idt7qf, i8i8tu, ik7kfz, iazad9, iklboe, irm0do, ii4oh8, ijurrd, i66r1l, irzdsh, iborqc, i6hk4k},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="iku7jq",
    display_order=1,
    custom_attributes={"id": "iku7jq"}
)
iku7jq_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
iku7jq.layout = iku7jq_layout
i3y418 = Text(
    name="i3y418",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="i3y418",
    display_order=2,
    custom_attributes={"id": "i3y418"}
)
izn0ch = ViewContainer(
    name="izn0ch",
    description="nav container",
    view_elements={iu60cw, iku7jq, i3y418},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="izn0ch",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "izn0ch"}
)
izn0ch_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
izn0ch.layout = izn0ch_layout
iecqpz = Text(
    name="iecqpz",
    content="CuentaContable",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="iecqpz",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "iecqpz"}
)
i8smlo = Text(
    name="i8smlo",
    content="Manage CuentaContable data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="i8smlo",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "i8smlo"}
)
table_cuentacontable_9_col_0 = FieldColumn(label="IdCuenta", field=CuentaContable_idCuenta)
table_cuentacontable_9_col_1 = FieldColumn(label="NombreCuenta", field=CuentaContable_nombreCuenta)
table_cuentacontable_9_col_2 = FieldColumn(label="TipoCuenta", field=CuentaContable_tipoCuenta)
table_cuentacontable_9_col_3 = FieldColumn(label="Saldo", field=CuentaContable_saldo)
table_cuentacontable_9_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "cuentaMovimientos")
table_cuentacontable_9_col_4 = LookupColumn(label="CuentaMovimientos", path=table_cuentacontable_9_col_4_path, field=MovimientoContable_idMovimiento)
table_cuentacontable_9 = Table(
    name="table_cuentacontable_9",
    title="CuentaContable List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_cuentacontable_9_col_0, table_cuentacontable_9_col_1, table_cuentacontable_9_col_2, table_cuentacontable_9_col_3, table_cuentacontable_9_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-cuentacontable-9",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "CuentaContable List", "data-source": "class_j1wo61blj_muhb7pxb_p14", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idCuenta', 'label': 'IdCuenta', 'columnType': 'field', '_expanded': False}, {'field': 'nombreCuenta', 'label': 'NombreCuenta', 'columnType': 'field', '_expanded': False}, {'field': 'tipoCuenta', 'label': 'TipoCuenta', 'columnType': 'field', '_expanded': False}, {'field': 'saldo', 'label': 'Saldo', 'columnType': 'field', '_expanded': False}, {'field': 'cuentaMovimientos', 'label': 'CuentaMovimientos', 'columnType': 'lookup', 'lookupEntity': 'class_wbhr7e3qa_muhb7pxb_nnr', 'lookupField': 'idMovimiento', '_expanded': False}, {'field': 'MovimientoContable', 'label': 'MovimientoContable', 'columnType': 'lookup', 'lookupEntity': 'class_wbhr7e3qa_muhb7pxb_nnr', 'lookupField': 'idMovimiento', '_expanded': False}], "id": "table-cuentacontable-9", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_cuentacontable_9_binding_domain = None
if domain_model_ref is not None:
    table_cuentacontable_9_binding_domain = domain_model_ref.get_class_by_name("CuentaContable")
if table_cuentacontable_9_binding_domain:
    table_cuentacontable_9_binding = DataBinding(domain_concept=table_cuentacontable_9_binding_domain, name="CuentaContableDataBinding")
else:
    # Domain class 'CuentaContable' not resolved; data binding skipped.
    table_cuentacontable_9_binding = None
if table_cuentacontable_9_binding:
    table_cuentacontable_9.data_binding = table_cuentacontable_9_binding
i7hr0v = ViewContainer(
    name="i7hr0v",
    description="main container",
    view_elements={iecqpz, i8smlo, table_cuentacontable_9},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i7hr0v",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i7hr0v"}
)
i7hr0v_layout = Layout(flex="1")
i7hr0v.layout = i7hr0v_layout
iq851p = ViewContainer(
    name="iq851p",
    description=" component",
    view_elements={izn0ch, i7hr0v},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="iq851p",
    display_order=0,
    custom_attributes={"id": "iq851p"}
)
iq851p_layout = Layout(layout_type=LayoutType.FLEX)
iq851p.layout = iq851p_layout
wrapper_10.view_elements = {iq851p}


# Screen: wrapper_11
wrapper_11 = Screen(name="wrapper_11", description="AsientoContable", view_elements=set(), route_path="/asientocontable", screen_size="Medium")
wrapper_11.component_id = "page-asientocontable-10"
i67vai = Text(
    name="i67vai",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i67vai",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i67vai"}
)
i2uq3l = Link(
    name="i2uq3l",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2uq3l",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i2uq3l"}
)
ixzyx4 = Link(
    name="ixzyx4",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ixzyx4",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "ixzyx4"}
)
iikuvg = Link(
    name="iikuvg",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iikuvg",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "iikuvg"}
)
ihw23j = Link(
    name="ihw23j",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihw23j",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "ihw23j"}
)
iqwmw4 = Link(
    name="iqwmw4",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iqwmw4",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "iqwmw4"}
)
ibj105 = Link(
    name="ibj105",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ibj105",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "ibj105"}
)
imwbvg = Link(
    name="imwbvg",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imwbvg",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "imwbvg"}
)
ilh72j = Link(
    name="ilh72j",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ilh72j",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "ilh72j"}
)
ich1vq = Link(
    name="ich1vq",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ich1vq",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "ich1vq"}
)
ix3trg = Link(
    name="ix3trg",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ix3trg",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "ix3trg"}
)
i12u7j = Link(
    name="i12u7j",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i12u7j",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "i12u7j"}
)
ii0hkh = Link(
    name="ii0hkh",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ii0hkh",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "ii0hkh"}
)
i5pc4j = Link(
    name="i5pc4j",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i5pc4j",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i5pc4j"}
)
ipsubl = ViewContainer(
    name="ipsubl",
    description=" component",
    view_elements={i2uq3l, ixzyx4, iikuvg, ihw23j, iqwmw4, ibj105, imwbvg, ilh72j, ich1vq, ix3trg, i12u7j, ii0hkh, i5pc4j},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ipsubl",
    display_order=1,
    custom_attributes={"id": "ipsubl"}
)
ipsubl_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ipsubl.layout = ipsubl_layout
ildaru = Text(
    name="ildaru",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ildaru",
    display_order=2,
    custom_attributes={"id": "ildaru"}
)
icsvl9 = ViewContainer(
    name="icsvl9",
    description="nav container",
    view_elements={i67vai, ipsubl, ildaru},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="icsvl9",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "icsvl9"}
)
icsvl9_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
icsvl9.layout = icsvl9_layout
ibd5r3 = Text(
    name="ibd5r3",
    content="AsientoContable",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ibd5r3",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ibd5r3"}
)
ivpvtd = Text(
    name="ivpvtd",
    content="Manage AsientoContable data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ivpvtd",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ivpvtd"}
)
table_asientocontable_10_col_0 = FieldColumn(label="IdAsiento", field=AsientoContable_idAsiento)
table_asientocontable_10_col_1 = FieldColumn(label="Fecha", field=AsientoContable_fecha)
table_asientocontable_10_col_2 = FieldColumn(label="Descripcion", field=AsientoContable_descripcion)
table_asientocontable_10_col_3_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "asientoMovimientos")
table_asientocontable_10_col_3 = LookupColumn(label="AsientoMovimientos", path=table_asientocontable_10_col_3_path, field=MovimientoContable_idMovimiento)
table_asientocontable_10 = Table(
    name="table_asientocontable_10",
    title="AsientoContable List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_asientocontable_10_col_0, table_asientocontable_10_col_1, table_asientocontable_10_col_2, table_asientocontable_10_col_3],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-asientocontable-10",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "AsientoContable List", "data-source": "class_y5dhj5f89_muhb7pxb_t0b", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idAsiento', 'label': 'IdAsiento', 'columnType': 'field', '_expanded': False}, {'field': 'fecha', 'label': 'Fecha', 'columnType': 'field', '_expanded': False}, {'field': 'descripcion', 'label': 'Descripcion', 'columnType': 'field', '_expanded': False}, {'field': 'asientoMovimientos', 'label': 'AsientoMovimientos', 'columnType': 'lookup', 'lookupEntity': 'class_wbhr7e3qa_muhb7pxb_nnr', 'lookupField': 'idMovimiento', '_expanded': False}, {'field': 'MovimientoContable', 'label': 'MovimientoContable', 'columnType': 'lookup', 'lookupEntity': 'class_wbhr7e3qa_muhb7pxb_nnr', 'lookupField': 'idMovimiento', '_expanded': False}], "id": "table-asientocontable-10", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_asientocontable_10_binding_domain = None
if domain_model_ref is not None:
    table_asientocontable_10_binding_domain = domain_model_ref.get_class_by_name("AsientoContable")
if table_asientocontable_10_binding_domain:
    table_asientocontable_10_binding = DataBinding(domain_concept=table_asientocontable_10_binding_domain, name="AsientoContableDataBinding")
else:
    # Domain class 'AsientoContable' not resolved; data binding skipped.
    table_asientocontable_10_binding = None
if table_asientocontable_10_binding:
    table_asientocontable_10.data_binding = table_asientocontable_10_binding
i44fi8 = ViewContainer(
    name="i44fi8",
    description="main container",
    view_elements={ibd5r3, ivpvtd, table_asientocontable_10},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i44fi8",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i44fi8"}
)
i44fi8_layout = Layout(flex="1")
i44fi8.layout = i44fi8_layout
icpcky = ViewContainer(
    name="icpcky",
    description=" component",
    view_elements={icsvl9, i44fi8},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="icpcky",
    display_order=0,
    custom_attributes={"id": "icpcky"}
)
icpcky_layout = Layout(layout_type=LayoutType.FLEX)
icpcky.layout = icpcky_layout
wrapper_11.view_elements = {icpcky}


# Screen: wrapper_12
wrapper_12 = Screen(name="wrapper_12", description="MovimientoContable", view_elements=set(), route_path="/movimientocontable", screen_size="Medium")
wrapper_12.component_id = "page-movimientocontable-11"
iu060x = Text(
    name="iu060x",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="iu060x",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "iu060x"}
)
ific82 = Link(
    name="ific82",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ific82",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "ific82"}
)
iasnm7 = Link(
    name="iasnm7",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iasnm7",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "iasnm7"}
)
iw6k6x = Link(
    name="iw6k6x",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iw6k6x",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "iw6k6x"}
)
it79h7 = Link(
    name="it79h7",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="it79h7",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "it79h7"}
)
i72ap8 = Link(
    name="i72ap8",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i72ap8",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "i72ap8"}
)
iz0y24 = Link(
    name="iz0y24",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iz0y24",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "iz0y24"}
)
irynhx = Link(
    name="irynhx",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="irynhx",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "irynhx"}
)
if5ehl = Link(
    name="if5ehl",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="if5ehl",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "if5ehl"}
)
invsud = Link(
    name="invsud",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="invsud",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "invsud"}
)
ihtxok = Link(
    name="ihtxok",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihtxok",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "ihtxok"}
)
ibdifa = Link(
    name="ibdifa",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ibdifa",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ibdifa"}
)
ia62j3 = Link(
    name="ia62j3",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ia62j3",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "ia62j3"}
)
imlno6 = Link(
    name="imlno6",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imlno6",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "imlno6"}
)
ivxawf = ViewContainer(
    name="ivxawf",
    description=" component",
    view_elements={ific82, iasnm7, iw6k6x, it79h7, i72ap8, iz0y24, irynhx, if5ehl, invsud, ihtxok, ibdifa, ia62j3, imlno6},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ivxawf",
    display_order=1,
    custom_attributes={"id": "ivxawf"}
)
ivxawf_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ivxawf.layout = ivxawf_layout
ioi29f = Text(
    name="ioi29f",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ioi29f",
    display_order=2,
    custom_attributes={"id": "ioi29f"}
)
i2x8ds = ViewContainer(
    name="i2x8ds",
    description="nav container",
    view_elements={iu060x, ivxawf, ioi29f},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="i2x8ds",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "i2x8ds"}
)
i2x8ds_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
i2x8ds.layout = i2x8ds_layout
iw7z5y = Text(
    name="iw7z5y",
    content="MovimientoContable",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="iw7z5y",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "iw7z5y"}
)
iovd2k = Text(
    name="iovd2k",
    content="Manage MovimientoContable data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iovd2k",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iovd2k"}
)
table_movimientocontable_11_col_0 = FieldColumn(label="IdMovimiento", field=MovimientoContable_idMovimiento)
table_movimientocontable_11_col_1 = FieldColumn(label="Debe", field=MovimientoContable_debe)
table_movimientocontable_11_col_2 = FieldColumn(label="Haber", field=MovimientoContable_haber)
table_movimientocontable_11_col_3_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "movimientoCuenta")
table_movimientocontable_11_col_3 = LookupColumn(label="MovimientoCuenta", path=table_movimientocontable_11_col_3_path, field=CuentaContable_idCuenta)
table_movimientocontable_11_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "movimientoAsiento")
table_movimientocontable_11_col_4 = LookupColumn(label="MovimientoAsiento", path=table_movimientocontable_11_col_4_path, field=AsientoContable_idAsiento)
table_movimientocontable_11 = Table(
    name="table_movimientocontable_11",
    title="MovimientoContable List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_movimientocontable_11_col_0, table_movimientocontable_11_col_1, table_movimientocontable_11_col_2, table_movimientocontable_11_col_3, table_movimientocontable_11_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-movimientocontable-11",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "MovimientoContable List", "data-source": "class_wbhr7e3qa_muhb7pxb_nnr", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idMovimiento', 'label': 'IdMovimiento', 'columnType': 'field', '_expanded': False}, {'field': 'debe', 'label': 'Debe', 'columnType': 'field', '_expanded': False}, {'field': 'haber', 'label': 'Haber', 'columnType': 'field', '_expanded': False}, {'field': 'CuentaContable', 'label': 'CuentaContable', 'columnType': 'lookup', 'lookupEntity': 'class_j1wo61blj_muhb7pxb_p14', 'lookupField': 'idCuenta', '_expanded': False}, {'field': 'AsientoContable', 'label': 'AsientoContable', 'columnType': 'lookup', 'lookupEntity': 'class_y5dhj5f89_muhb7pxb_t0b', 'lookupField': 'idAsiento', '_expanded': False}, {'field': 'movimientoCuenta', 'label': 'MovimientoCuenta', 'columnType': 'lookup', 'lookupEntity': 'class_j1wo61blj_muhb7pxb_p14', 'lookupField': 'idCuenta', '_expanded': False}, {'field': 'movimientoAsiento', 'label': 'MovimientoAsiento', 'columnType': 'lookup', 'lookupEntity': 'class_y5dhj5f89_muhb7pxb_t0b', 'lookupField': 'idAsiento', '_expanded': False}], "id": "table-movimientocontable-11", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_movimientocontable_11_binding_domain = None
if domain_model_ref is not None:
    table_movimientocontable_11_binding_domain = domain_model_ref.get_class_by_name("MovimientoContable")
if table_movimientocontable_11_binding_domain:
    table_movimientocontable_11_binding = DataBinding(domain_concept=table_movimientocontable_11_binding_domain, name="MovimientoContableDataBinding")
else:
    # Domain class 'MovimientoContable' not resolved; data binding skipped.
    table_movimientocontable_11_binding = None
if table_movimientocontable_11_binding:
    table_movimientocontable_11.data_binding = table_movimientocontable_11_binding
it5had = ViewContainer(
    name="it5had",
    description="main container",
    view_elements={iw7z5y, iovd2k, table_movimientocontable_11},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="it5had",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "it5had"}
)
it5had_layout = Layout(flex="1")
it5had.layout = it5had_layout
ipjvuc = ViewContainer(
    name="ipjvuc",
    description=" component",
    view_elements={i2x8ds, it5had},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="ipjvuc",
    display_order=0,
    custom_attributes={"id": "ipjvuc"}
)
ipjvuc_layout = Layout(layout_type=LayoutType.FLEX)
ipjvuc.layout = ipjvuc_layout
wrapper_12.view_elements = {ipjvuc}


# Screen: wrapper_13
wrapper_13 = Screen(name="wrapper_13", description="Trabajador", view_elements=set(), route_path="/trabajador", screen_size="Medium")
wrapper_13.component_id = "page-trabajador-12"
i33rug = Text(
    name="i33rug",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i33rug",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i33rug"}
)
irhmqa = Link(
    name="irhmqa",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="irhmqa",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "irhmqa"}
)
iofjj7 = Link(
    name="iofjj7",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iofjj7",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "iofjj7"}
)
iz6fs5 = Link(
    name="iz6fs5",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iz6fs5",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "iz6fs5"}
)
im7tdm = Link(
    name="im7tdm",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="im7tdm",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "im7tdm"}
)
i1s1cj = Link(
    name="i1s1cj",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i1s1cj",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "i1s1cj"}
)
i7o0i3 = Link(
    name="i7o0i3",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7o0i3",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "i7o0i3"}
)
i5dm0l = Link(
    name="i5dm0l",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i5dm0l",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "i5dm0l"}
)
i4k9zb = Link(
    name="i4k9zb",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i4k9zb",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "i4k9zb"}
)
iqtdtt = Link(
    name="iqtdtt",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iqtdtt",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "iqtdtt"}
)
imj3xk = Link(
    name="imj3xk",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imj3xk",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "imj3xk"}
)
ixmt9s = Link(
    name="ixmt9s",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ixmt9s",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ixmt9s"}
)
i8bm2k = Link(
    name="i8bm2k",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8bm2k",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "i8bm2k"}
)
i8608n = Link(
    name="i8608n",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8608n",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i8608n"}
)
i4nzlf = ViewContainer(
    name="i4nzlf",
    description=" component",
    view_elements={irhmqa, iofjj7, iz6fs5, im7tdm, i1s1cj, i7o0i3, i5dm0l, i4k9zb, iqtdtt, imj3xk, ixmt9s, i8bm2k, i8608n},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="i4nzlf",
    display_order=1,
    custom_attributes={"id": "i4nzlf"}
)
i4nzlf_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
i4nzlf.layout = i4nzlf_layout
ijahhx = Text(
    name="ijahhx",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ijahhx",
    display_order=2,
    custom_attributes={"id": "ijahhx"}
)
ivdbn7 = ViewContainer(
    name="ivdbn7",
    description="nav container",
    view_elements={i33rug, i4nzlf, ijahhx},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ivdbn7",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ivdbn7"}
)
ivdbn7_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ivdbn7.layout = ivdbn7_layout
i8xrwg = Text(
    name="i8xrwg",
    content="Trabajador",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="i8xrwg",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "i8xrwg"}
)
iiy2yx = Text(
    name="iiy2yx",
    content="Manage Trabajador data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iiy2yx",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iiy2yx"}
)
table_trabajador_12_col_0 = FieldColumn(label="IdTrabajador", field=Trabajador_idTrabajador)
table_trabajador_12_col_1 = FieldColumn(label="Nombre", field=Trabajador_nombre)
table_trabajador_12_col_2 = FieldColumn(label="Puesto", field=Trabajador_puesto)
table_trabajador_12_col_3 = FieldColumn(label="Sueldo", field=Trabajador_sueldo)
table_trabajador_12_col_4 = FieldColumn(label="FechaIngreso", field=Trabajador_fechaIngreso)
table_trabajador_12 = Table(
    name="table_trabajador_12",
    title="Trabajador List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_trabajador_12_col_0, table_trabajador_12_col_1, table_trabajador_12_col_2, table_trabajador_12_col_3, table_trabajador_12_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-trabajador-12",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Trabajador List", "data-source": "class_qpyq41o1o_muhb7pxb_n0q", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idTrabajador', 'label': 'IdTrabajador', 'columnType': 'field', '_expanded': False}, {'field': 'nombre', 'label': 'Nombre', 'columnType': 'field', '_expanded': False}, {'field': 'puesto', 'label': 'Puesto', 'columnType': 'field', '_expanded': False}, {'field': 'sueldo', 'label': 'Sueldo', 'columnType': 'field', '_expanded': False}, {'field': 'fechaIngreso', 'label': 'FechaIngreso', 'columnType': 'field', '_expanded': False}], "id": "table-trabajador-12", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_trabajador_12_binding_domain = None
if domain_model_ref is not None:
    table_trabajador_12_binding_domain = domain_model_ref.get_class_by_name("Trabajador")
if table_trabajador_12_binding_domain:
    table_trabajador_12_binding = DataBinding(domain_concept=table_trabajador_12_binding_domain, name="TrabajadorDataBinding")
else:
    # Domain class 'Trabajador' not resolved; data binding skipped.
    table_trabajador_12_binding = None
if table_trabajador_12_binding:
    table_trabajador_12.data_binding = table_trabajador_12_binding
ikju8h = ViewContainer(
    name="ikju8h",
    description="main container",
    view_elements={i8xrwg, iiy2yx, table_trabajador_12},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ikju8h",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ikju8h"}
)
ikju8h_layout = Layout(flex="1")
ikju8h.layout = ikju8h_layout
ii4hm2 = ViewContainer(
    name="ii4hm2",
    description=" component",
    view_elements={ivdbn7, ikju8h},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="ii4hm2",
    display_order=0,
    custom_attributes={"id": "ii4hm2"}
)
ii4hm2_layout = Layout(layout_type=LayoutType.FLEX)
ii4hm2.layout = ii4hm2_layout
wrapper_13.view_elements = {ii4hm2}


# Screen: wrapper_2
wrapper_2 = Screen(name="wrapper_2", description="Proveedor", view_elements=set(), route_path="/proveedor", screen_size="Medium")
wrapper_2.component_id = "page-proveedor-1"
i3r4o = Text(
    name="i3r4o",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i3r4o",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i3r4o"}
)
iifu6 = Link(
    name="iifu6",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iifu6",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "iifu6"}
)
i7nj7 = Link(
    name="i7nj7",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7nj7",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "i7nj7"}
)
idmmv = Link(
    name="idmmv",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="idmmv",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "idmmv"}
)
i0d12 = Link(
    name="i0d12",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i0d12",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "i0d12"}
)
i84lq4 = Link(
    name="i84lq4",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i84lq4",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "i84lq4"}
)
i6trn8 = Link(
    name="i6trn8",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i6trn8",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "i6trn8"}
)
il8ui7 = Link(
    name="il8ui7",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="il8ui7",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "il8ui7"}
)
i4eees = Link(
    name="i4eees",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i4eees",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "i4eees"}
)
i1gxdj = Link(
    name="i1gxdj",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i1gxdj",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "i1gxdj"}
)
is506g = Link(
    name="is506g",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="is506g",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "is506g"}
)
ia751h = Link(
    name="ia751h",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ia751h",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ia751h"}
)
ixgaa4 = Link(
    name="ixgaa4",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ixgaa4",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "ixgaa4"}
)
i3wnos = Link(
    name="i3wnos",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i3wnos",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i3wnos"}
)
ig2rq = ViewContainer(
    name="ig2rq",
    description=" component",
    view_elements={iifu6, i7nj7, idmmv, i0d12, i84lq4, i6trn8, il8ui7, i4eees, i1gxdj, is506g, ia751h, ixgaa4, i3wnos},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ig2rq",
    display_order=1,
    custom_attributes={"id": "ig2rq"}
)
ig2rq_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ig2rq.layout = ig2rq_layout
ix0941 = Text(
    name="ix0941",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ix0941",
    display_order=2,
    custom_attributes={"id": "ix0941"}
)
i94ga = ViewContainer(
    name="i94ga",
    description="nav container",
    view_elements={i3r4o, ig2rq, ix0941},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="i94ga",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "i94ga"}
)
i94ga_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
i94ga.layout = i94ga_layout
icsfqh = Text(
    name="icsfqh",
    content="Proveedor",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="icsfqh",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "icsfqh"}
)
iupe4x = Text(
    name="iupe4x",
    content="Manage Proveedor data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iupe4x",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iupe4x"}
)
table_proveedor_1_col_0 = FieldColumn(label="IdProveedor", field=Proveedor_idProveedor)
table_proveedor_1_col_1 = FieldColumn(label="Nombre", field=Proveedor_nombre)
table_proveedor_1_col_2 = FieldColumn(label="Direccion", field=Proveedor_direccion)
table_proveedor_1_col_3 = FieldColumn(label="Telefono", field=Proveedor_telefono)
table_proveedor_1_col_4 = FieldColumn(label="Email", field=Proveedor_email)
table_proveedor_1_col_5 = FieldColumn(label="TipoProveedor", field=Proveedor_tipoProveedor)
table_proveedor_1_col_6_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "proveedorOrdenesCompra")
table_proveedor_1_col_6 = LookupColumn(label="ProveedorOrdenesCompra", path=table_proveedor_1_col_6_path, field=OrdenDeCompra_idOrdenCompra)
table_proveedor_1 = Table(
    name="table_proveedor_1",
    title="Proveedor List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_proveedor_1_col_0, table_proveedor_1_col_1, table_proveedor_1_col_2, table_proveedor_1_col_3, table_proveedor_1_col_4, table_proveedor_1_col_5, table_proveedor_1_col_6],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-proveedor-1",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Proveedor List", "data-source": "class_5m6ltr0u5_muhb7pxa_f1k", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idProveedor', 'label': 'IdProveedor', 'columnType': 'field', '_expanded': False}, {'field': 'nombre', 'label': 'Nombre', 'columnType': 'field', '_expanded': False}, {'field': 'direccion', 'label': 'Direccion', 'columnType': 'field', '_expanded': False}, {'field': 'telefono', 'label': 'Telefono', 'columnType': 'field', '_expanded': False}, {'field': 'email', 'label': 'Email', 'columnType': 'field', '_expanded': False}, {'field': 'tipoProveedor', 'label': 'TipoProveedor', 'columnType': 'field', '_expanded': False}, {'field': 'proveedorOrdenesCompra', 'label': 'ProveedorOrdenesCompra', 'columnType': 'lookup', 'lookupEntity': 'class_wun8bscaa_muhb7pxa_ufx', 'lookupField': 'idOrdenCompra', '_expanded': False}], "id": "table-proveedor-1", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_proveedor_1_binding_domain = None
if domain_model_ref is not None:
    table_proveedor_1_binding_domain = domain_model_ref.get_class_by_name("Proveedor")
if table_proveedor_1_binding_domain:
    table_proveedor_1_binding = DataBinding(domain_concept=table_proveedor_1_binding_domain, name="ProveedorDataBinding")
else:
    # Domain class 'Proveedor' not resolved; data binding skipped.
    table_proveedor_1_binding = None
if table_proveedor_1_binding:
    table_proveedor_1.data_binding = table_proveedor_1_binding
ix8iis = ViewContainer(
    name="ix8iis",
    description="main container",
    view_elements={icsfqh, iupe4x, table_proveedor_1},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ix8iis",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ix8iis"}
)
ix8iis_layout = Layout(flex="1")
ix8iis.layout = ix8iis_layout
in34s = ViewContainer(
    name="in34s",
    description=" component",
    view_elements={i94ga, ix8iis},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="in34s",
    display_order=0,
    custom_attributes={"id": "in34s"}
)
in34s_layout = Layout(layout_type=LayoutType.FLEX)
in34s.layout = in34s_layout
wrapper_2.view_elements = {in34s}


# Screen: wrapper_3
wrapper_3 = Screen(name="wrapper_3", description="Producto", view_elements=set(), route_path="/producto", screen_size="Medium")
wrapper_3.component_id = "page-producto-2"
ih0nuf = Text(
    name="ih0nuf",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ih0nuf",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ih0nuf"}
)
i2exqi = Link(
    name="i2exqi",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2exqi",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i2exqi"}
)
i0elxj = Link(
    name="i0elxj",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i0elxj",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "i0elxj"}
)
ip59po = Link(
    name="ip59po",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ip59po",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "ip59po"}
)
i10xqw = Link(
    name="i10xqw",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i10xqw",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "i10xqw"}
)
ipvoqb = Link(
    name="ipvoqb",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ipvoqb",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "ipvoqb"}
)
itxpmv = Link(
    name="itxpmv",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="itxpmv",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "itxpmv"}
)
ihlqw8 = Link(
    name="ihlqw8",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihlqw8",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "ihlqw8"}
)
i8pcjo = Link(
    name="i8pcjo",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8pcjo",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "i8pcjo"}
)
itfqkm = Link(
    name="itfqkm",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="itfqkm",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "itfqkm"}
)
inwv3f = Link(
    name="inwv3f",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="inwv3f",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "inwv3f"}
)
isdmbm = Link(
    name="isdmbm",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="isdmbm",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "isdmbm"}
)
iy1bbb = Link(
    name="iy1bbb",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iy1bbb",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "iy1bbb"}
)
it59jg = Link(
    name="it59jg",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="it59jg",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "it59jg"}
)
ir0y4i = ViewContainer(
    name="ir0y4i",
    description=" component",
    view_elements={i2exqi, i0elxj, ip59po, i10xqw, ipvoqb, itxpmv, ihlqw8, i8pcjo, itfqkm, inwv3f, isdmbm, iy1bbb, it59jg},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ir0y4i",
    display_order=1,
    custom_attributes={"id": "ir0y4i"}
)
ir0y4i_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ir0y4i.layout = ir0y4i_layout
i28meg = Text(
    name="i28meg",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="i28meg",
    display_order=2,
    custom_attributes={"id": "i28meg"}
)
ijuhek = ViewContainer(
    name="ijuhek",
    description="nav container",
    view_elements={ih0nuf, ir0y4i, i28meg},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ijuhek",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ijuhek"}
)
ijuhek_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ijuhek.layout = ijuhek_layout
ir0qex = Text(
    name="ir0qex",
    content="Producto",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ir0qex",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ir0qex"}
)
ieioxs = Text(
    name="ieioxs",
    content="Manage Producto data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ieioxs",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ieioxs"}
)
table_producto_2_col_0 = FieldColumn(label="IdProducto", field=Producto_idProducto)
table_producto_2_col_1 = FieldColumn(label="Nombre", field=Producto_nombre)
table_producto_2_col_2 = FieldColumn(label="Descripcion", field=Producto_descripcion)
table_producto_2_col_3 = FieldColumn(label="PrecioUnitario", field=Producto_precioUnitario)
table_producto_2_col_4 = FieldColumn(label="UnidadMedida", field=Producto_unidadMedida)
table_producto_2_col_5 = FieldColumn(label="StockDisponible", field=Producto_stockDisponible)
table_producto_2_col_6_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "productoItemsOrdenProd")
table_producto_2_col_6 = LookupColumn(label="ProductoItemsOrdenProd", path=table_producto_2_col_6_path, field=ItemOrdenDeProduccion_idItem)
table_producto_2_col_7_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "productoItemsOrdenCompra")
table_producto_2_col_7 = LookupColumn(label="ProductoItemsOrdenCompra", path=table_producto_2_col_7_path, field=ItemOrdenDeCompra_idItem)
table_producto_2_col_8_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "productoItemsFactura")
table_producto_2_col_8 = LookupColumn(label="ProductoItemsFactura", path=table_producto_2_col_8_path, field=ItemFactura_idItem)
table_producto_2 = Table(
    name="table_producto_2",
    title="Producto List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_producto_2_col_0, table_producto_2_col_1, table_producto_2_col_2, table_producto_2_col_3, table_producto_2_col_4, table_producto_2_col_5, table_producto_2_col_6, table_producto_2_col_7, table_producto_2_col_8],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-producto-2",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Producto List", "data-source": "class_an8903wg7_muhb7pxa_bhk", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idProducto', 'label': 'IdProducto', 'columnType': 'field', '_expanded': False}, {'field': 'nombre', 'label': 'Nombre', 'columnType': 'field', '_expanded': False}, {'field': 'descripcion', 'label': 'Descripcion', 'columnType': 'field', '_expanded': False}, {'field': 'precioUnitario', 'label': 'PrecioUnitario', 'columnType': 'field', '_expanded': False}, {'field': 'unidadMedida', 'label': 'UnidadMedida', 'columnType': 'field', '_expanded': False}, {'field': 'stockDisponible', 'label': 'StockDisponible', 'columnType': 'field', '_expanded': False}, {'field': 'productoItemsOrdenProd', 'label': 'ProductoItemsOrdenProd', 'columnType': 'lookup', 'lookupEntity': 'class_a6nj9a8y5_muhb7pxa_35s', 'lookupField': 'idItem', '_expanded': False}, {'field': 'productoItemsOrdenCompra', 'label': 'ProductoItemsOrdenCompra', 'columnType': 'lookup', 'lookupEntity': 'class_6d3d7x1fz_muhb7pxa_98u', 'lookupField': 'idItem', '_expanded': False}, {'field': 'productoItemsFactura', 'label': 'ProductoItemsFactura', 'columnType': 'lookup', 'lookupEntity': 'class_2lxc64wey_muhb7pxa_a6i', 'lookupField': 'idItem', '_expanded': False}], "id": "table-producto-2", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_producto_2_binding_domain = None
if domain_model_ref is not None:
    table_producto_2_binding_domain = domain_model_ref.get_class_by_name("Producto")
if table_producto_2_binding_domain:
    table_producto_2_binding = DataBinding(domain_concept=table_producto_2_binding_domain, name="ProductoDataBinding")
else:
    # Domain class 'Producto' not resolved; data binding skipped.
    table_producto_2_binding = None
if table_producto_2_binding:
    table_producto_2.data_binding = table_producto_2_binding
i0zuzo = ViewContainer(
    name="i0zuzo",
    description="main container",
    view_elements={ir0qex, ieioxs, table_producto_2},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i0zuzo",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i0zuzo"}
)
i0zuzo_layout = Layout(flex="1")
i0zuzo.layout = i0zuzo_layout
imndur = ViewContainer(
    name="imndur",
    description=" component",
    view_elements={ijuhek, i0zuzo},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="imndur",
    display_order=0,
    custom_attributes={"id": "imndur"}
)
imndur_layout = Layout(layout_type=LayoutType.FLEX)
imndur.layout = imndur_layout
wrapper_3.view_elements = {imndur}


# Screen: wrapper_4
wrapper_4 = Screen(name="wrapper_4", description="OrdenDeProduccion", view_elements=set(), route_path="/ordendeproduccion", screen_size="Medium")
wrapper_4.component_id = "page-ordendeproduccion-3"
ikjz59 = Text(
    name="ikjz59",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ikjz59",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ikjz59"}
)
i861um = Link(
    name="i861um",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i861um",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i861um"}
)
iqibsk = Link(
    name="iqibsk",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iqibsk",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "iqibsk"}
)
ig3kci = Link(
    name="ig3kci",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ig3kci",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "ig3kci"}
)
ie3z6g = Link(
    name="ie3z6g",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ie3z6g",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "ie3z6g"}
)
inj2lw = Link(
    name="inj2lw",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="inj2lw",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "inj2lw"}
)
imq9mk = Link(
    name="imq9mk",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imq9mk",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "imq9mk"}
)
ij0qks = Link(
    name="ij0qks",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ij0qks",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "ij0qks"}
)
i9cr3f = Link(
    name="i9cr3f",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i9cr3f",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "i9cr3f"}
)
iel0a2 = Link(
    name="iel0a2",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iel0a2",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "iel0a2"}
)
i4vdbu = Link(
    name="i4vdbu",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i4vdbu",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "i4vdbu"}
)
ihjyyh = Link(
    name="ihjyyh",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihjyyh",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ihjyyh"}
)
ipewrx = Link(
    name="ipewrx",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ipewrx",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "ipewrx"}
)
iyvj16 = Link(
    name="iyvj16",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iyvj16",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "iyvj16"}
)
ivadb5 = ViewContainer(
    name="ivadb5",
    description=" component",
    view_elements={i861um, iqibsk, ig3kci, ie3z6g, inj2lw, imq9mk, ij0qks, i9cr3f, iel0a2, i4vdbu, ihjyyh, ipewrx, iyvj16},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ivadb5",
    display_order=1,
    custom_attributes={"id": "ivadb5"}
)
ivadb5_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ivadb5.layout = ivadb5_layout
iho5vp = Text(
    name="iho5vp",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iho5vp",
    display_order=2,
    custom_attributes={"id": "iho5vp"}
)
i5cbh7 = ViewContainer(
    name="i5cbh7",
    description="nav container",
    view_elements={ikjz59, ivadb5, iho5vp},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="i5cbh7",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "i5cbh7"}
)
i5cbh7_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
i5cbh7.layout = i5cbh7_layout
i6nbkx = Text(
    name="i6nbkx",
    content="OrdenDeProduccion",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="i6nbkx",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "i6nbkx"}
)
iw07dw = Text(
    name="iw07dw",
    content="Manage OrdenDeProduccion data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iw07dw",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iw07dw"}
)
table_ordendeproduccion_3_col_0 = FieldColumn(label="IdOrdenProd", field=OrdenDeProduccion_idOrdenProd)
table_ordendeproduccion_3_col_1 = FieldColumn(label="FechaCreacion", field=OrdenDeProduccion_fechaCreacion)
table_ordendeproduccion_3_col_2 = FieldColumn(label="FechaEntrega", field=OrdenDeProduccion_fechaEntrega)
table_ordendeproduccion_3_col_3 = FieldColumn(label="Estado", field=OrdenDeProduccion_estado)
table_ordendeproduccion_3_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "ordenItems")
table_ordendeproduccion_3_col_4 = LookupColumn(label="OrdenItems", path=table_ordendeproduccion_3_col_4_path, field=ItemOrdenDeProduccion_idItem)
table_ordendeproduccion_3 = Table(
    name="table_ordendeproduccion_3",
    title="OrdenDeProduccion List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_ordendeproduccion_3_col_0, table_ordendeproduccion_3_col_1, table_ordendeproduccion_3_col_2, table_ordendeproduccion_3_col_3, table_ordendeproduccion_3_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-ordendeproduccion-3",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "OrdenDeProduccion List", "data-source": "class_w54mwuy3g_muhb7pxa_xzj", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idOrdenProd', 'label': 'IdOrdenProd', 'columnType': 'field', '_expanded': False}, {'field': 'fechaCreacion', 'label': 'FechaCreacion', 'columnType': 'field', '_expanded': False}, {'field': 'fechaEntrega', 'label': 'FechaEntrega', 'columnType': 'field', '_expanded': False}, {'field': 'estado', 'label': 'Estado', 'columnType': 'field', '_expanded': False}, {'field': 'Cliente', 'label': 'Cliente', 'columnType': 'lookup', 'lookupEntity': 'class_a972xjff0_muhb7pxa_ci0', 'lookupField': 'idCliente', '_expanded': False}, {'field': 'ordenItems', 'label': 'OrdenItems', 'columnType': 'lookup', 'lookupEntity': 'class_a6nj9a8y5_muhb7pxa_35s', 'lookupField': 'idItem', '_expanded': False}], "id": "table-ordendeproduccion-3", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_ordendeproduccion_3_binding_domain = None
if domain_model_ref is not None:
    table_ordendeproduccion_3_binding_domain = domain_model_ref.get_class_by_name("OrdenDeProduccion")
if table_ordendeproduccion_3_binding_domain:
    table_ordendeproduccion_3_binding = DataBinding(domain_concept=table_ordendeproduccion_3_binding_domain, name="OrdenDeProduccionDataBinding")
else:
    # Domain class 'OrdenDeProduccion' not resolved; data binding skipped.
    table_ordendeproduccion_3_binding = None
if table_ordendeproduccion_3_binding:
    table_ordendeproduccion_3.data_binding = table_ordendeproduccion_3_binding
imv8fh = ViewContainer(
    name="imv8fh",
    description="main container",
    view_elements={i6nbkx, iw07dw, table_ordendeproduccion_3},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="imv8fh",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "imv8fh"}
)
imv8fh_layout = Layout(flex="1")
imv8fh.layout = imv8fh_layout
i6vjyg = ViewContainer(
    name="i6vjyg",
    description=" component",
    view_elements={i5cbh7, imv8fh},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i6vjyg",
    display_order=0,
    custom_attributes={"id": "i6vjyg"}
)
i6vjyg_layout = Layout(layout_type=LayoutType.FLEX)
i6vjyg.layout = i6vjyg_layout
wrapper_4.view_elements = {i6vjyg}


# Screen: wrapper_5
wrapper_5 = Screen(name="wrapper_5", description="ItemOrdenDeProduccion", view_elements=set(), route_path="/itemordendeproduccion", screen_size="Medium")
wrapper_5.component_id = "page-itemordendeproduccion-4"
in13pj = Text(
    name="in13pj",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="in13pj",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "in13pj"}
)
i7vmze = Link(
    name="i7vmze",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7vmze",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i7vmze"}
)
ibzoa3 = Link(
    name="ibzoa3",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ibzoa3",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "ibzoa3"}
)
ihxeuu = Link(
    name="ihxeuu",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihxeuu",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "ihxeuu"}
)
injyr1 = Link(
    name="injyr1",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="injyr1",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "injyr1"}
)
i2deg3 = Link(
    name="i2deg3",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2deg3",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "i2deg3"}
)
is25ad = Link(
    name="is25ad",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="is25ad",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "is25ad"}
)
ifc26l = Link(
    name="ifc26l",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ifc26l",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "ifc26l"}
)
iyyzer = Link(
    name="iyyzer",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iyyzer",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "iyyzer"}
)
i2rkq5 = Link(
    name="i2rkq5",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2rkq5",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "i2rkq5"}
)
iac8hl = Link(
    name="iac8hl",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iac8hl",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "iac8hl"}
)
itfsef = Link(
    name="itfsef",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="itfsef",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "itfsef"}
)
i2iuek = Link(
    name="i2iuek",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i2iuek",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "i2iuek"}
)
iroh0x = Link(
    name="iroh0x",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iroh0x",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "iroh0x"}
)
ikhg1k = ViewContainer(
    name="ikhg1k",
    description=" component",
    view_elements={i7vmze, ibzoa3, ihxeuu, injyr1, i2deg3, is25ad, ifc26l, iyyzer, i2rkq5, iac8hl, itfsef, i2iuek, iroh0x},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ikhg1k",
    display_order=1,
    custom_attributes={"id": "ikhg1k"}
)
ikhg1k_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ikhg1k.layout = ikhg1k_layout
iw5yh2 = Text(
    name="iw5yh2",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iw5yh2",
    display_order=2,
    custom_attributes={"id": "iw5yh2"}
)
ij0dhh = ViewContainer(
    name="ij0dhh",
    description="nav container",
    view_elements={in13pj, ikhg1k, iw5yh2},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ij0dhh",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ij0dhh"}
)
ij0dhh_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ij0dhh.layout = ij0dhh_layout
il00ts = Text(
    name="il00ts",
    content="ItemOrdenDeProduccion",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="il00ts",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "il00ts"}
)
ixoc6l = Text(
    name="ixoc6l",
    content="Manage ItemOrdenDeProduccion data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ixoc6l",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ixoc6l"}
)
table_itemordendeproduccion_4_col_0 = FieldColumn(label="IdItem", field=ItemOrdenDeProduccion_idItem)
table_itemordendeproduccion_4_col_1 = FieldColumn(label="Cantidad", field=ItemOrdenDeProduccion_cantidad)
table_itemordendeproduccion_4_col_2 = FieldColumn(label="Observaciones", field=ItemOrdenDeProduccion_observaciones)
table_itemordendeproduccion_4 = Table(
    name="table_itemordendeproduccion_4",
    title="ItemOrdenDeProduccion List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_itemordendeproduccion_4_col_0, table_itemordendeproduccion_4_col_1, table_itemordendeproduccion_4_col_2],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-itemordendeproduccion-4",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "ItemOrdenDeProduccion List", "data-source": "class_a6nj9a8y5_muhb7pxa_35s", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idItem', 'label': 'IdItem', 'columnType': 'field', '_expanded': False}, {'field': 'cantidad', 'label': 'Cantidad', 'columnType': 'field', '_expanded': False}, {'field': 'observaciones', 'label': 'Observaciones', 'columnType': 'field', '_expanded': False}, {'field': 'OrdenDeProduccion', 'label': 'OrdenDeProduccion', 'columnType': 'lookup', 'lookupEntity': 'class_w54mwuy3g_muhb7pxa_xzj', 'lookupField': 'idOrdenProd', '_expanded': False}, {'field': 'Producto', 'label': 'Producto', 'columnType': 'lookup', 'lookupEntity': 'class_an8903wg7_muhb7pxa_bhk', 'lookupField': 'idProducto', '_expanded': False}], "id": "table-itemordendeproduccion-4", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_itemordendeproduccion_4_binding_domain = None
if domain_model_ref is not None:
    table_itemordendeproduccion_4_binding_domain = domain_model_ref.get_class_by_name("ItemOrdenDeProduccion")
if table_itemordendeproduccion_4_binding_domain:
    table_itemordendeproduccion_4_binding = DataBinding(domain_concept=table_itemordendeproduccion_4_binding_domain, name="ItemOrdenDeProduccionDataBinding")
else:
    # Domain class 'ItemOrdenDeProduccion' not resolved; data binding skipped.
    table_itemordendeproduccion_4_binding = None
if table_itemordendeproduccion_4_binding:
    table_itemordendeproduccion_4.data_binding = table_itemordendeproduccion_4_binding
igsn5s = ViewContainer(
    name="igsn5s",
    description="main container",
    view_elements={il00ts, ixoc6l, table_itemordendeproduccion_4},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="igsn5s",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "igsn5s"}
)
igsn5s_layout = Layout(flex="1")
igsn5s.layout = igsn5s_layout
iq2ivj = ViewContainer(
    name="iq2ivj",
    description=" component",
    view_elements={ij0dhh, igsn5s},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="iq2ivj",
    display_order=0,
    custom_attributes={"id": "iq2ivj"}
)
iq2ivj_layout = Layout(layout_type=LayoutType.FLEX)
iq2ivj.layout = iq2ivj_layout
wrapper_5.view_elements = {iq2ivj}


# Screen: wrapper_6
wrapper_6 = Screen(name="wrapper_6", description="OrdenDeCompra", view_elements=set(), route_path="/ordendecompra", screen_size="Medium")
wrapper_6.component_id = "page-ordendecompra-5"
igo6ry = Text(
    name="igo6ry",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="igo6ry",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "igo6ry"}
)
i22az9 = Link(
    name="i22az9",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i22az9",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i22az9"}
)
i15ugy = Link(
    name="i15ugy",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i15ugy",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "i15ugy"}
)
i4q54s = Link(
    name="i4q54s",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i4q54s",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "i4q54s"}
)
ic8j2m = Link(
    name="ic8j2m",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ic8j2m",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "ic8j2m"}
)
igr1vi = Link(
    name="igr1vi",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="igr1vi",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "igr1vi"}
)
i6yv0k = Link(
    name="i6yv0k",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i6yv0k",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "i6yv0k"}
)
iwww2a = Link(
    name="iwww2a",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iwww2a",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "iwww2a"}
)
ie1xy6 = Link(
    name="ie1xy6",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ie1xy6",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "ie1xy6"}
)
ihq7wu = Link(
    name="ihq7wu",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihq7wu",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "ihq7wu"}
)
ihoqwl = Link(
    name="ihoqwl",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ihoqwl",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "ihoqwl"}
)
itzo2z = Link(
    name="itzo2z",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="itzo2z",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "itzo2z"}
)
iayyp3 = Link(
    name="iayyp3",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iayyp3",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "iayyp3"}
)
i98lbk = Link(
    name="i98lbk",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i98lbk",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "i98lbk"}
)
idfph5 = ViewContainer(
    name="idfph5",
    description=" component",
    view_elements={i22az9, i15ugy, i4q54s, ic8j2m, igr1vi, i6yv0k, iwww2a, ie1xy6, ihq7wu, ihoqwl, itzo2z, iayyp3, i98lbk},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="idfph5",
    display_order=1,
    custom_attributes={"id": "idfph5"}
)
idfph5_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
idfph5.layout = idfph5_layout
iazw4t = Text(
    name="iazw4t",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iazw4t",
    display_order=2,
    custom_attributes={"id": "iazw4t"}
)
ib209l = ViewContainer(
    name="ib209l",
    description="nav container",
    view_elements={igo6ry, idfph5, iazw4t},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ib209l",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ib209l"}
)
ib209l_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ib209l.layout = ib209l_layout
ie0c5i = Text(
    name="ie0c5i",
    content="OrdenDeCompra",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ie0c5i",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ie0c5i"}
)
iqturv = Text(
    name="iqturv",
    content="Manage OrdenDeCompra data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iqturv",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iqturv"}
)
table_ordendecompra_5_col_0 = FieldColumn(label="IdOrdenCompra", field=OrdenDeCompra_idOrdenCompra)
table_ordendecompra_5_col_1 = FieldColumn(label="FechaCreacion", field=OrdenDeCompra_fechaCreacion)
table_ordendecompra_5_col_2 = FieldColumn(label="FechaRecepcionEsperada", field=OrdenDeCompra_fechaRecepcionEsperada)
table_ordendecompra_5_col_3 = FieldColumn(label="Estado", field=OrdenDeCompra_estado)
table_ordendecompra_5_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "ordenCompraItems")
table_ordendecompra_5_col_4 = LookupColumn(label="OrdenCompraItems", path=table_ordendecompra_5_col_4_path, field=ItemOrdenDeCompra_idItem)
table_ordendecompra_5 = Table(
    name="table_ordendecompra_5",
    title="OrdenDeCompra List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_ordendecompra_5_col_0, table_ordendecompra_5_col_1, table_ordendecompra_5_col_2, table_ordendecompra_5_col_3, table_ordendecompra_5_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-ordendecompra-5",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "OrdenDeCompra List", "data-source": "class_wun8bscaa_muhb7pxa_ufx", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idOrdenCompra', 'label': 'IdOrdenCompra', 'columnType': 'field', '_expanded': False}, {'field': 'fechaCreacion', 'label': 'FechaCreacion', 'columnType': 'field', '_expanded': False}, {'field': 'fechaRecepcionEsperada', 'label': 'FechaRecepcionEsperada', 'columnType': 'field', '_expanded': False}, {'field': 'estado', 'label': 'Estado', 'columnType': 'field', '_expanded': False}, {'field': 'Proveedor', 'label': 'Proveedor', 'columnType': 'lookup', 'lookupEntity': 'class_5m6ltr0u5_muhb7pxa_f1k', 'lookupField': 'idProveedor', '_expanded': False}, {'field': 'ordenCompraItems', 'label': 'OrdenCompraItems', 'columnType': 'lookup', 'lookupEntity': 'class_6d3d7x1fz_muhb7pxa_98u', 'lookupField': 'idItem', '_expanded': False}], "id": "table-ordendecompra-5", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_ordendecompra_5_binding_domain = None
if domain_model_ref is not None:
    table_ordendecompra_5_binding_domain = domain_model_ref.get_class_by_name("OrdenDeCompra")
if table_ordendecompra_5_binding_domain:
    table_ordendecompra_5_binding = DataBinding(domain_concept=table_ordendecompra_5_binding_domain, name="OrdenDeCompraDataBinding")
else:
    # Domain class 'OrdenDeCompra' not resolved; data binding skipped.
    table_ordendecompra_5_binding = None
if table_ordendecompra_5_binding:
    table_ordendecompra_5.data_binding = table_ordendecompra_5_binding
ifsruk = ViewContainer(
    name="ifsruk",
    description="main container",
    view_elements={ie0c5i, iqturv, table_ordendecompra_5},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ifsruk",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ifsruk"}
)
ifsruk_layout = Layout(flex="1")
ifsruk.layout = ifsruk_layout
ily05h = ViewContainer(
    name="ily05h",
    description=" component",
    view_elements={ib209l, ifsruk},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="ily05h",
    display_order=0,
    custom_attributes={"id": "ily05h"}
)
ily05h_layout = Layout(layout_type=LayoutType.FLEX)
ily05h.layout = ily05h_layout
wrapper_6.view_elements = {ily05h}


# Screen: wrapper_7
wrapper_7 = Screen(name="wrapper_7", description="ItemOrdenDeCompra", view_elements=set(), route_path="/itemordendecompra", screen_size="Medium")
wrapper_7.component_id = "page-itemordendecompra-6"
ieuk4j = Text(
    name="ieuk4j",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ieuk4j",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ieuk4j"}
)
it52uh = Link(
    name="it52uh",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="it52uh",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "it52uh"}
)
iju4dd = Link(
    name="iju4dd",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iju4dd",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "iju4dd"}
)
i06esf = Link(
    name="i06esf",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i06esf",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "i06esf"}
)
icaht1 = Link(
    name="icaht1",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="icaht1",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "icaht1"}
)
ifd5zt = Link(
    name="ifd5zt",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ifd5zt",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "ifd5zt"}
)
izwqpw = Link(
    name="izwqpw",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="izwqpw",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "izwqpw"}
)
idiyos = Link(
    name="idiyos",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="idiyos",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "idiyos"}
)
iyuc3h = Link(
    name="iyuc3h",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iyuc3h",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "iyuc3h"}
)
ilcdur = Link(
    name="ilcdur",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ilcdur",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "ilcdur"}
)
irkqvr = Link(
    name="irkqvr",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="irkqvr",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "irkqvr"}
)
ildjae = Link(
    name="ildjae",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ildjae",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ildjae"}
)
i1qnk2 = Link(
    name="i1qnk2",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i1qnk2",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "i1qnk2"}
)
iowdvt = Link(
    name="iowdvt",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iowdvt",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "iowdvt"}
)
iwd60l = ViewContainer(
    name="iwd60l",
    description=" component",
    view_elements={it52uh, iju4dd, i06esf, icaht1, ifd5zt, izwqpw, idiyos, iyuc3h, ilcdur, irkqvr, ildjae, i1qnk2, iowdvt},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="iwd60l",
    display_order=1,
    custom_attributes={"id": "iwd60l"}
)
iwd60l_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
iwd60l.layout = iwd60l_layout
iip8bd = Text(
    name="iip8bd",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iip8bd",
    display_order=2,
    custom_attributes={"id": "iip8bd"}
)
ijbaxd = ViewContainer(
    name="ijbaxd",
    description="nav container",
    view_elements={ieuk4j, iwd60l, iip8bd},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ijbaxd",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ijbaxd"}
)
ijbaxd_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ijbaxd.layout = ijbaxd_layout
ie3x5m = Text(
    name="ie3x5m",
    content="ItemOrdenDeCompra",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ie3x5m",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ie3x5m"}
)
ix0v6s = Text(
    name="ix0v6s",
    content="Manage ItemOrdenDeCompra data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ix0v6s",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ix0v6s"}
)
table_itemordendecompra_6_col_0 = FieldColumn(label="IdItem", field=ItemOrdenDeCompra_idItem)
table_itemordendecompra_6_col_1 = FieldColumn(label="Cantidad", field=ItemOrdenDeCompra_cantidad)
table_itemordendecompra_6_col_2 = FieldColumn(label="PrecioUnitario", field=ItemOrdenDeCompra_precioUnitario)
table_itemordendecompra_6 = Table(
    name="table_itemordendecompra_6",
    title="ItemOrdenDeCompra List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_itemordendecompra_6_col_0, table_itemordendecompra_6_col_1, table_itemordendecompra_6_col_2],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-itemordendecompra-6",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "ItemOrdenDeCompra List", "data-source": "class_6d3d7x1fz_muhb7pxa_98u", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idItem', 'label': 'IdItem', 'columnType': 'field', '_expanded': False}, {'field': 'cantidad', 'label': 'Cantidad', 'columnType': 'field', '_expanded': False}, {'field': 'precioUnitario', 'label': 'PrecioUnitario', 'columnType': 'field', '_expanded': False}, {'field': 'OrdenDeCompra', 'label': 'OrdenDeCompra', 'columnType': 'lookup', 'lookupEntity': 'class_wun8bscaa_muhb7pxa_ufx', 'lookupField': 'idOrdenCompra', '_expanded': False}, {'field': 'Producto', 'label': 'Producto', 'columnType': 'lookup', 'lookupEntity': 'class_an8903wg7_muhb7pxa_bhk', 'lookupField': 'idProducto', '_expanded': False}], "id": "table-itemordendecompra-6", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_itemordendecompra_6_binding_domain = None
if domain_model_ref is not None:
    table_itemordendecompra_6_binding_domain = domain_model_ref.get_class_by_name("ItemOrdenDeCompra")
if table_itemordendecompra_6_binding_domain:
    table_itemordendecompra_6_binding = DataBinding(domain_concept=table_itemordendecompra_6_binding_domain, name="ItemOrdenDeCompraDataBinding")
else:
    # Domain class 'ItemOrdenDeCompra' not resolved; data binding skipped.
    table_itemordendecompra_6_binding = None
if table_itemordendecompra_6_binding:
    table_itemordendecompra_6.data_binding = table_itemordendecompra_6_binding
ixldgz = ViewContainer(
    name="ixldgz",
    description="main container",
    view_elements={ie3x5m, ix0v6s, table_itemordendecompra_6},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="ixldgz",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "ixldgz"}
)
ixldgz_layout = Layout(flex="1")
ixldgz.layout = ixldgz_layout
i3q5hp = ViewContainer(
    name="i3q5hp",
    description=" component",
    view_elements={ijbaxd, ixldgz},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i3q5hp",
    display_order=0,
    custom_attributes={"id": "i3q5hp"}
)
i3q5hp_layout = Layout(layout_type=LayoutType.FLEX)
i3q5hp.layout = i3q5hp_layout
wrapper_7.view_elements = {i3q5hp}


# Screen: wrapper_8
wrapper_8 = Screen(name="wrapper_8", description="Factura", view_elements=set(), route_path="/factura", screen_size="Medium")
wrapper_8.component_id = "page-factura-7"
irg78d = Text(
    name="irg78d",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="irg78d",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "irg78d"}
)
i3y95e = Link(
    name="i3y95e",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i3y95e",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "i3y95e"}
)
i8ici4 = Link(
    name="i8ici4",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i8ici4",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "i8ici4"}
)
i5nlhi = Link(
    name="i5nlhi",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i5nlhi",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "i5nlhi"}
)
isjksq = Link(
    name="isjksq",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="isjksq",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "isjksq"}
)
iuelu4 = Link(
    name="iuelu4",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iuelu4",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "iuelu4"}
)
i9s2x5 = Link(
    name="i9s2x5",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i9s2x5",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "i9s2x5"}
)
i7d5lg = Link(
    name="i7d5lg",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i7d5lg",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "i7d5lg"}
)
ip29jl = Link(
    name="ip29jl",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ip29jl",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "ip29jl"}
)
iixi55 = Link(
    name="iixi55",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iixi55",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "iixi55"}
)
ivljck = Link(
    name="ivljck",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ivljck",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "ivljck"}
)
ir2dvd = Link(
    name="ir2dvd",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ir2dvd",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "ir2dvd"}
)
iiogo5 = Link(
    name="iiogo5",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iiogo5",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "iiogo5"}
)
iki52j = Link(
    name="iki52j",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iki52j",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "iki52j"}
)
i88b0w = ViewContainer(
    name="i88b0w",
    description=" component",
    view_elements={i3y95e, i8ici4, i5nlhi, isjksq, iuelu4, i9s2x5, i7d5lg, ip29jl, iixi55, ivljck, ir2dvd, iiogo5, iki52j},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="i88b0w",
    display_order=1,
    custom_attributes={"id": "i88b0w"}
)
i88b0w_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
i88b0w.layout = i88b0w_layout
izuq25 = Text(
    name="izuq25",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="izuq25",
    display_order=2,
    custom_attributes={"id": "izuq25"}
)
ic00sk = ViewContainer(
    name="ic00sk",
    description="nav container",
    view_elements={irg78d, i88b0w, izuq25},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ic00sk",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ic00sk"}
)
ic00sk_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ic00sk.layout = ic00sk_layout
ip6vy8 = Text(
    name="ip6vy8",
    content="Factura",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ip6vy8",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ip6vy8"}
)
itkazb = Text(
    name="itkazb",
    content="Manage Factura data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="itkazb",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "itkazb"}
)
table_factura_7_col_0 = FieldColumn(label="IdFactura", field=Factura_idFactura)
table_factura_7_col_1 = FieldColumn(label="FechaEmision", field=Factura_fechaEmision)
table_factura_7_col_2 = FieldColumn(label="Total", field=Factura_total)
table_factura_7_col_3 = FieldColumn(label="EstadoPago", field=Factura_estadoPago)
table_factura_7_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "facturaItems")
table_factura_7_col_4 = LookupColumn(label="FacturaItems", path=table_factura_7_col_4_path, field=ItemFactura_idItem)
table_factura_7 = Table(
    name="table_factura_7",
    title="Factura List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_factura_7_col_0, table_factura_7_col_1, table_factura_7_col_2, table_factura_7_col_3, table_factura_7_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-factura-7",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Factura List", "data-source": "class_78m7ywlbr_muhb7pxa_0b1", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idFactura', 'label': 'IdFactura', 'columnType': 'field', '_expanded': False}, {'field': 'fechaEmision', 'label': 'FechaEmision', 'columnType': 'field', '_expanded': False}, {'field': 'total', 'label': 'Total', 'columnType': 'field', '_expanded': False}, {'field': 'estadoPago', 'label': 'EstadoPago', 'columnType': 'field', '_expanded': False}, {'field': 'Cliente', 'label': 'Cliente', 'columnType': 'lookup', 'lookupEntity': 'class_a972xjff0_muhb7pxa_ci0', 'lookupField': 'idCliente', '_expanded': False}, {'field': 'facturaItems', 'label': 'FacturaItems', 'columnType': 'lookup', 'lookupEntity': 'class_2lxc64wey_muhb7pxa_a6i', 'lookupField': 'idItem', '_expanded': False}], "id": "table-factura-7", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_factura_7_binding_domain = None
if domain_model_ref is not None:
    table_factura_7_binding_domain = domain_model_ref.get_class_by_name("Factura")
if table_factura_7_binding_domain:
    table_factura_7_binding = DataBinding(domain_concept=table_factura_7_binding_domain, name="FacturaDataBinding")
else:
    # Domain class 'Factura' not resolved; data binding skipped.
    table_factura_7_binding = None
if table_factura_7_binding:
    table_factura_7.data_binding = table_factura_7_binding
i0pr1l = ViewContainer(
    name="i0pr1l",
    description="main container",
    view_elements={ip6vy8, itkazb, table_factura_7},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i0pr1l",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i0pr1l"}
)
i0pr1l_layout = Layout(flex="1")
i0pr1l.layout = i0pr1l_layout
iy7hdi = ViewContainer(
    name="iy7hdi",
    description=" component",
    view_elements={ic00sk, i0pr1l},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="iy7hdi",
    display_order=0,
    custom_attributes={"id": "iy7hdi"}
)
iy7hdi_layout = Layout(layout_type=LayoutType.FLEX)
iy7hdi.layout = iy7hdi_layout
wrapper_8.view_elements = {iy7hdi}


# Screen: wrapper_9
wrapper_9 = Screen(name="wrapper_9", description="ItemFactura", view_elements=set(), route_path="/itemfactura", screen_size="Medium")
wrapper_9.component_id = "page-itemfactura-8"
inf2lk = Text(
    name="inf2lk",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="inf2lk",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "inf2lk"}
)
iicpsx = Link(
    name="iicpsx",
    description="Link element",
    label="Cliente",
    url="/cliente",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iicpsx",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/cliente", "id": "iicpsx"}
)
imufdw = Link(
    name="imufdw",
    description="Link element",
    label="Proveedor",
    url="/proveedor",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="imufdw",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/proveedor", "id": "imufdw"}
)
ikmy0j = Link(
    name="ikmy0j",
    description="Link element",
    label="Producto",
    url="/producto",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ikmy0j",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/producto", "id": "ikmy0j"}
)
iw270s = Link(
    name="iw270s",
    description="Link element",
    label="OrdenDeProduccion",
    url="/ordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iw270s",
    tag_name="a",
    display_order=3,
    custom_attributes={"href": "/ordendeproduccion", "id": "iw270s"}
)
in8e7u = Link(
    name="in8e7u",
    description="Link element",
    label="ItemOrdenDeProduccion",
    url="/itemordendeproduccion",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="in8e7u",
    tag_name="a",
    display_order=4,
    custom_attributes={"href": "/itemordendeproduccion", "id": "in8e7u"}
)
i3m2e2 = Link(
    name="i3m2e2",
    description="Link element",
    label="OrdenDeCompra",
    url="/ordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i3m2e2",
    tag_name="a",
    display_order=5,
    custom_attributes={"href": "/ordendecompra", "id": "i3m2e2"}
)
iocfju = Link(
    name="iocfju",
    description="Link element",
    label="ItemOrdenDeCompra",
    url="/itemordendecompra",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iocfju",
    tag_name="a",
    display_order=6,
    custom_attributes={"href": "/itemordendecompra", "id": "iocfju"}
)
ijbp9p = Link(
    name="ijbp9p",
    description="Link element",
    label="Factura",
    url="/factura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ijbp9p",
    tag_name="a",
    display_order=7,
    custom_attributes={"href": "/factura", "id": "ijbp9p"}
)
io43at = Link(
    name="io43at",
    description="Link element",
    label="ItemFactura",
    url="/itemfactura",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="io43at",
    tag_name="a",
    display_order=8,
    custom_attributes={"href": "/itemfactura", "id": "io43at"}
)
iad06n = Link(
    name="iad06n",
    description="Link element",
    label="CuentaContable",
    url="/cuentacontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iad06n",
    tag_name="a",
    display_order=9,
    custom_attributes={"href": "/cuentacontable", "id": "iad06n"}
)
in585h = Link(
    name="in585h",
    description="Link element",
    label="AsientoContable",
    url="/asientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="in585h",
    tag_name="a",
    display_order=10,
    custom_attributes={"href": "/asientocontable", "id": "in585h"}
)
iavg68 = Link(
    name="iavg68",
    description="Link element",
    label="MovimientoContable",
    url="/movimientocontable",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iavg68",
    tag_name="a",
    display_order=11,
    custom_attributes={"href": "/movimientocontable", "id": "iavg68"}
)
inwpux = Link(
    name="inwpux",
    description="Link element",
    label="Trabajador",
    url="/trabajador",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="inwpux",
    tag_name="a",
    display_order=12,
    custom_attributes={"href": "/trabajador", "id": "inwpux"}
)
ippiw6 = ViewContainer(
    name="ippiw6",
    description=" component",
    view_elements={iicpsx, imufdw, ikmy0j, iw270s, in8e7u, i3m2e2, iocfju, ijbp9p, io43at, iad06n, in585h, iavg68, inwpux},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ippiw6",
    display_order=1,
    custom_attributes={"id": "ippiw6"}
)
ippiw6_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ippiw6.layout = ippiw6_layout
iq6twd = Text(
    name="iq6twd",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iq6twd",
    display_order=2,
    custom_attributes={"id": "iq6twd"}
)
imqlcj = ViewContainer(
    name="imqlcj",
    description="nav container",
    view_elements={inf2lk, ippiw6, iq6twd},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="imqlcj",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "imqlcj"}
)
imqlcj_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
imqlcj.layout = imqlcj_layout
ickb8k = Text(
    name="ickb8k",
    content="ItemFactura",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ickb8k",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ickb8k"}
)
imk3ij = Text(
    name="imk3ij",
    content="Manage ItemFactura data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="imk3ij",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "imk3ij"}
)
table_itemfactura_8_col_0 = FieldColumn(label="IdItem", field=ItemFactura_idItem)
table_itemfactura_8_col_1 = FieldColumn(label="Cantidad", field=ItemFactura_cantidad)
table_itemfactura_8_col_2 = FieldColumn(label="PrecioUnitario", field=ItemFactura_precioUnitario)
table_itemfactura_8_col_3 = FieldColumn(label="Subtotal", field=ItemFactura_subtotal)
table_itemfactura_8 = Table(
    name="table_itemfactura_8",
    title="ItemFactura List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_itemfactura_8_col_0, table_itemfactura_8_col_1, table_itemfactura_8_col_2, table_itemfactura_8_col_3],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-itemfactura-8",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "ItemFactura List", "data-source": "class_2lxc64wey_muhb7pxa_a6i", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'idItem', 'label': 'IdItem', 'columnType': 'field', '_expanded': False}, {'field': 'cantidad', 'label': 'Cantidad', 'columnType': 'field', '_expanded': False}, {'field': 'precioUnitario', 'label': 'PrecioUnitario', 'columnType': 'field', '_expanded': False}, {'field': 'subtotal', 'label': 'Subtotal', 'columnType': 'field', '_expanded': False}, {'field': 'Factura', 'label': 'Factura', 'columnType': 'lookup', 'lookupEntity': 'class_78m7ywlbr_muhb7pxa_0b1', 'lookupField': 'idFactura', '_expanded': False}, {'field': 'Producto', 'label': 'Producto', 'columnType': 'lookup', 'lookupEntity': 'class_an8903wg7_muhb7pxa_bhk', 'lookupField': 'idProducto', '_expanded': False}], "id": "table-itemfactura-8", "filter": ""}
)
domain_model_ref = globals().get('domain_model')
table_itemfactura_8_binding_domain = None
if domain_model_ref is not None:
    table_itemfactura_8_binding_domain = domain_model_ref.get_class_by_name("ItemFactura")
if table_itemfactura_8_binding_domain:
    table_itemfactura_8_binding = DataBinding(domain_concept=table_itemfactura_8_binding_domain, name="ItemFacturaDataBinding")
else:
    # Domain class 'ItemFactura' not resolved; data binding skipped.
    table_itemfactura_8_binding = None
if table_itemfactura_8_binding:
    table_itemfactura_8.data_binding = table_itemfactura_8_binding
i249oc = ViewContainer(
    name="i249oc",
    description="main container",
    view_elements={ickb8k, imk3ij, table_itemfactura_8},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i249oc",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i249oc"}
)
i249oc_layout = Layout(flex="1")
i249oc.layout = i249oc_layout
inf51f = ViewContainer(
    name="inf51f",
    description=" component",
    view_elements={imqlcj, i249oc},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="inf51f",
    display_order=0,
    custom_attributes={"id": "inf51f"}
)
inf51f_layout = Layout(layout_type=LayoutType.FLEX)
inf51f.layout = inf51f_layout
wrapper_9.view_elements = {inf51f}

gui_module = Module(
    name="GUI_Module",
    screens={wrapper, wrapper_10, wrapper_11, wrapper_12, wrapper_13, wrapper_2, wrapper_3, wrapper_4, wrapper_5, wrapper_6, wrapper_7, wrapper_8, wrapper_9}
)

# GUI Model
gui_model = GUIModel(
    name="GUI",
    package="",
    versionCode="1.0",
    versionName="1.0",
    modules={gui_module},
    description="GUI"
)

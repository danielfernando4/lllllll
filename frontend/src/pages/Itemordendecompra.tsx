import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Itemordendecompra: React.FC = () => {
  return (
    <div id="page-itemordendecompra-6">
    <div id="i3q5hp" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="ijbaxd" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="ieuk4j" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iwd60l" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="it52uh" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cliente">{"Cliente"}</a>
          <a id="iju4dd" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/proveedor">{"Proveedor"}</a>
          <a id="i06esf" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/producto">{"Producto"}</a>
          <a id="icaht1" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendeproduccion">{"OrdenDeProduccion"}</a>
          <a id="ifd5zt" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendeproduccion">{"ItemOrdenDeProduccion"}</a>
          <a id="izwqpw" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendecompra">{"OrdenDeCompra"}</a>
          <a id="idiyos" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendecompra">{"ItemOrdenDeCompra"}</a>
          <a id="iyuc3h" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/factura">{"Factura"}</a>
          <a id="ilcdur" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemfactura">{"ItemFactura"}</a>
          <a id="irkqvr" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cuentacontable">{"CuentaContable"}</a>
          <a id="ildjae" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/asientocontable">{"AsientoContable"}</a>
          <a id="i1qnk2" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/movimientocontable">{"MovimientoContable"}</a>
          <a id="iowdvt" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/trabajador">{"Trabajador"}</a>
        </div>
        <p id="iip8bd" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ixldgz" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ie3x5m" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ItemOrdenDeCompra"}</h1>
        <p id="ix0v6s" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ItemOrdenDeCompra data"}</p>
        <TableBlock id="table-itemordendecompra-6" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ItemOrdenDeCompra List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "IdItem", "column_type": "field", "field": "idItem", "type": "str", "required": true}, {"label": "Cantidad", "column_type": "field", "field": "cantidad", "type": "int", "required": true}, {"label": "PrecioUnitario", "column_type": "field", "field": "precioUnitario", "type": "float", "required": true}], "formColumns": [{"column_type": "field", "field": "idItem", "label": "idItem", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "cantidad", "label": "cantidad", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "precioUnitario", "label": "precioUnitario", "type": "float", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "ordendecompra", "field": "ordendecompra", "lookup_field": "idOrdenCompra", "target_field": "id", "entity": "OrdenDeCompra", "type": "str", "required": true}, {"column_type": "lookup", "path": "producto_1", "field": "producto_1", "lookup_field": "idProducto", "target_field": "id", "entity": "Producto", "type": "str", "required": true}]}} dataBinding={{"entity": "ItemOrdenDeCompra", "endpoint": "/itemordendecompra/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Itemordendecompra;

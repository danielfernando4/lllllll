import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Factura: React.FC = () => {
  return (
    <div id="page-factura-7">
    <div id="iy7hdi" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="ic00sk" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="irg78d" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i88b0w" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i3y95e" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cliente">{"Cliente"}</a>
          <a id="i8ici4" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/proveedor">{"Proveedor"}</a>
          <a id="i5nlhi" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/producto">{"Producto"}</a>
          <a id="isjksq" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendeproduccion">{"OrdenDeProduccion"}</a>
          <a id="iuelu4" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendeproduccion">{"ItemOrdenDeProduccion"}</a>
          <a id="i9s2x5" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendecompra">{"OrdenDeCompra"}</a>
          <a id="i7d5lg" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendecompra">{"ItemOrdenDeCompra"}</a>
          <a id="ip29jl" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/factura">{"Factura"}</a>
          <a id="iixi55" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemfactura">{"ItemFactura"}</a>
          <a id="ivljck" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cuentacontable">{"CuentaContable"}</a>
          <a id="ir2dvd" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/asientocontable">{"AsientoContable"}</a>
          <a id="iiogo5" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/movimientocontable">{"MovimientoContable"}</a>
          <a id="iki52j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/trabajador">{"Trabajador"}</a>
        </div>
        <p id="izuq25" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i0pr1l" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ip6vy8" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"Factura"}</h1>
        <p id="itkazb" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage Factura data"}</p>
        <TableBlock id="table-factura-7" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Factura List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "IdFactura", "column_type": "field", "field": "idFactura", "type": "str", "required": true}, {"label": "FechaEmision", "column_type": "field", "field": "fechaEmision", "type": "date", "required": true}, {"label": "Total", "column_type": "field", "field": "total", "type": "float", "required": true}, {"label": "EstadoPago", "column_type": "field", "field": "estadoPago", "type": "enum", "options": ["Pagado", "Pendiente", "Vencido"], "required": true}, {"label": "FacturaItems", "column_type": "lookup", "path": "facturaItems", "entity": "ItemFactura", "field": "idItem", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "idFactura", "label": "idFactura", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "fechaEmision", "label": "fechaEmision", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "total", "label": "total", "type": "float", "required": true, "defaultValue": "0.0"}, {"column_type": "field", "field": "estadoPago", "label": "estadoPago", "type": "enum", "required": true, "defaultValue": null, "options": ["Pagado", "Pendiente", "Vencido"]}, {"column_type": "lookup", "path": "cliente_1", "field": "cliente_1", "lookup_field": "email", "target_field": "id", "entity": "Cliente", "type": "str", "required": true}, {"column_type": "lookup", "path": "facturaItems", "field": "facturaItems", "lookup_field": "idItem", "target_field": "id", "entity": "ItemFactura", "type": "list", "required": false}]}} dataBinding={{"entity": "Factura", "endpoint": "/factura/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Factura;

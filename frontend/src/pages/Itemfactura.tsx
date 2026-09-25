import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Itemfactura: React.FC = () => {
  return (
    <div id="page-itemfactura-8">
    <div id="inf51f" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="imqlcj" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="inf2lk" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ippiw6" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="iicpsx" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cliente">{"Cliente"}</a>
          <a id="imufdw" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/proveedor">{"Proveedor"}</a>
          <a id="ikmy0j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/producto">{"Producto"}</a>
          <a id="iw270s" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendeproduccion">{"OrdenDeProduccion"}</a>
          <a id="in8e7u" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendeproduccion">{"ItemOrdenDeProduccion"}</a>
          <a id="i3m2e2" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendecompra">{"OrdenDeCompra"}</a>
          <a id="iocfju" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendecompra">{"ItemOrdenDeCompra"}</a>
          <a id="ijbp9p" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/factura">{"Factura"}</a>
          <a id="io43at" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemfactura">{"ItemFactura"}</a>
          <a id="iad06n" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cuentacontable">{"CuentaContable"}</a>
          <a id="in585h" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/asientocontable">{"AsientoContable"}</a>
          <a id="iavg68" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/movimientocontable">{"MovimientoContable"}</a>
          <a id="inwpux" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/trabajador">{"Trabajador"}</a>
        </div>
        <p id="iq6twd" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i249oc" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ickb8k" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ItemFactura"}</h1>
        <p id="imk3ij" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ItemFactura data"}</p>
        <TableBlock id="table-itemfactura-8" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ItemFactura List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "IdItem", "column_type": "field", "field": "idItem", "type": "str", "required": true}, {"label": "Cantidad", "column_type": "field", "field": "cantidad", "type": "int", "required": true}, {"label": "PrecioUnitario", "column_type": "field", "field": "precioUnitario", "type": "float", "required": true}, {"label": "Subtotal", "column_type": "field", "field": "subtotal", "type": "float", "required": true}], "formColumns": [{"column_type": "field", "field": "idItem", "label": "idItem", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "cantidad", "label": "cantidad", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "precioUnitario", "label": "precioUnitario", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "subtotal", "label": "subtotal", "type": "float", "required": true, "defaultValue": "0.0"}, {"column_type": "lookup", "path": "factura", "field": "factura", "lookup_field": "idFactura", "target_field": "id", "entity": "Factura", "type": "str", "required": true}, {"column_type": "lookup", "path": "producto_2", "field": "producto_2", "lookup_field": "idProducto", "target_field": "id", "entity": "Producto", "type": "str", "required": true}]}} dataBinding={{"entity": "ItemFactura", "endpoint": "/itemfactura/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Itemfactura;

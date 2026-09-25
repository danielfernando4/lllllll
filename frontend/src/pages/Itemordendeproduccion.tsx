import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Itemordendeproduccion: React.FC = () => {
  return (
    <div id="page-itemordendeproduccion-4">
    <div id="iq2ivj" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="ij0dhh" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="in13pj" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ikhg1k" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i7vmze" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cliente">{"Cliente"}</a>
          <a id="ibzoa3" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/proveedor">{"Proveedor"}</a>
          <a id="ihxeuu" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/producto">{"Producto"}</a>
          <a id="injyr1" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendeproduccion">{"OrdenDeProduccion"}</a>
          <a id="i2deg3" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendeproduccion">{"ItemOrdenDeProduccion"}</a>
          <a id="is25ad" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendecompra">{"OrdenDeCompra"}</a>
          <a id="ifc26l" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendecompra">{"ItemOrdenDeCompra"}</a>
          <a id="iyyzer" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/factura">{"Factura"}</a>
          <a id="i2rkq5" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemfactura">{"ItemFactura"}</a>
          <a id="iac8hl" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cuentacontable">{"CuentaContable"}</a>
          <a id="itfsef" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/asientocontable">{"AsientoContable"}</a>
          <a id="i2iuek" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/movimientocontable">{"MovimientoContable"}</a>
          <a id="iroh0x" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/trabajador">{"Trabajador"}</a>
        </div>
        <p id="iw5yh2" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="igsn5s" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="il00ts" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"ItemOrdenDeProduccion"}</h1>
        <p id="ixoc6l" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage ItemOrdenDeProduccion data"}</p>
        <TableBlock id="table-itemordendeproduccion-4" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="ItemOrdenDeProduccion List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "IdItem", "column_type": "field", "field": "idItem", "type": "str", "required": true}, {"label": "Cantidad", "column_type": "field", "field": "cantidad", "type": "int", "required": true}, {"label": "Observaciones", "column_type": "field", "field": "observaciones", "type": "str", "required": true}], "formColumns": [{"column_type": "field", "field": "idItem", "label": "idItem", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "cantidad", "label": "cantidad", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "observaciones", "label": "observaciones", "type": "str", "required": false, "defaultValue": null}, {"column_type": "lookup", "path": "ordendeproduccion", "field": "ordendeproduccion", "lookup_field": "idOrdenProd", "target_field": "id", "entity": "OrdenDeProduccion", "type": "str", "required": true}, {"column_type": "lookup", "path": "producto", "field": "producto", "lookup_field": "idProducto", "target_field": "id", "entity": "Producto", "type": "str", "required": true}]}} dataBinding={{"entity": "ItemOrdenDeProduccion", "endpoint": "/itemordendeproduccion/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Itemordendeproduccion;

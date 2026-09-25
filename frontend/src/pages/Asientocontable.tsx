import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Asientocontable: React.FC = () => {
  return (
    <div id="page-asientocontable-10">
    <div id="icpcky" style={{"height": "100vh", "fontFamily": "Arial, sans-serif", "display": "flex", "--chart-color-palette": "default"}}>
      <nav id="icsvl9" style={{"width": "250px", "padding": "20px", "display": "flex", "overflowY": "auto", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "--chart-color-palette": "default", "flexDirection": "column"}}>
        <h2 id="i67vai" style={{"fontSize": "24px", "fontWeight": "bold", "marginTop": "0", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ipsubl" style={{"display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "flex": "1"}}>
          <a id="i2uq3l" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cliente">{"Cliente"}</a>
          <a id="ixzyx4" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/proveedor">{"Proveedor"}</a>
          <a id="iikuvg" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/producto">{"Producto"}</a>
          <a id="ihw23j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendeproduccion">{"OrdenDeProduccion"}</a>
          <a id="iqwmw4" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendeproduccion">{"ItemOrdenDeProduccion"}</a>
          <a id="ibj105" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/ordendecompra">{"OrdenDeCompra"}</a>
          <a id="imwbvg" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemordendecompra">{"ItemOrdenDeCompra"}</a>
          <a id="ilh72j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/factura">{"Factura"}</a>
          <a id="ich1vq" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/itemfactura">{"ItemFactura"}</a>
          <a id="ix3trg" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/cuentacontable">{"CuentaContable"}</a>
          <a id="i12u7j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "rgba(255,255,255,0.2)", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/asientocontable">{"AsientoContable"}</a>
          <a id="ii0hkh" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/movimientocontable">{"MovimientoContable"}</a>
          <a id="i5pc4j" style={{"padding": "10px 15px", "textDecoration": "none", "marginBottom": "5px", "display": "block", "background": "transparent", "color": "white", "borderRadius": "4px", "--chart-color-palette": "default"}} href="/trabajador">{"Trabajador"}</a>
        </div>
        <p id="ildaru" style={{"fontSize": "11px", "paddingTop": "20px", "marginTop": "auto", "textAlign": "center", "opacity": "0.8", "borderTop": "1px solid rgba(255,255,255,0.2)", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i44fi8" style={{"padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default", "flex": "1"}}>
        <h1 id="ibd5r3" style={{"fontSize": "32px", "marginTop": "0", "marginBottom": "10px", "color": "#333", "--chart-color-palette": "default"}}>{"AsientoContable"}</h1>
        <p id="ivpvtd" style={{"marginBottom": "30px", "color": "#666", "--chart-color-palette": "default"}}>{"Manage AsientoContable data"}</p>
        <TableBlock id="table-asientocontable-10" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="AsientoContable List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "IdAsiento", "column_type": "field", "field": "idAsiento", "type": "str", "required": true}, {"label": "Fecha", "column_type": "field", "field": "fecha", "type": "date", "required": true}, {"label": "Descripcion", "column_type": "field", "field": "descripcion", "type": "str", "required": true}, {"label": "AsientoMovimientos", "column_type": "lookup", "path": "asientoMovimientos", "entity": "MovimientoContable", "field": "idMovimiento", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "idAsiento", "label": "idAsiento", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "fecha", "label": "fecha", "type": "date", "required": true, "defaultValue": null}, {"column_type": "field", "field": "descripcion", "label": "descripcion", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "asientoMovimientos", "field": "asientoMovimientos", "lookup_field": "idMovimiento", "target_field": "id", "entity": "MovimientoContable", "type": "list", "required": false}, {"column_type": "lookup", "path": "movimientocontable_1", "field": "movimientocontable_1", "lookup_field": "idMovimiento", "target_field": "id", "entity": "MovimientoContable", "type": "list", "required": false}]}} dataBinding={{"entity": "AsientoContable", "endpoint": "/asientocontable/", "row_key_fields": ["id"]}} />
      </main>
    </div>    </div>
  );
};

export default Asientocontable;

import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Cliente from "./pages/Cliente";
import Cuentacontable from "./pages/Cuentacontable";
import Asientocontable from "./pages/Asientocontable";
import Movimientocontable from "./pages/Movimientocontable";
import Trabajador from "./pages/Trabajador";
import Proveedor from "./pages/Proveedor";
import Producto from "./pages/Producto";
import Ordendeproduccion from "./pages/Ordendeproduccion";
import Itemordendeproduccion from "./pages/Itemordendeproduccion";
import Ordendecompra from "./pages/Ordendecompra";
import Itemordendecompra from "./pages/Itemordendecompra";
import Factura from "./pages/Factura";
import Itemfactura from "./pages/Itemfactura";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/cliente" element={<Cliente />} />
            <Route path="/cuentacontable" element={<Cuentacontable />} />
            <Route path="/asientocontable" element={<Asientocontable />} />
            <Route path="/movimientocontable" element={<Movimientocontable />} />
            <Route path="/trabajador" element={<Trabajador />} />
            <Route path="/proveedor" element={<Proveedor />} />
            <Route path="/producto" element={<Producto />} />
            <Route path="/ordendeproduccion" element={<Ordendeproduccion />} />
            <Route path="/itemordendeproduccion" element={<Itemordendeproduccion />} />
            <Route path="/ordendecompra" element={<Ordendecompra />} />
            <Route path="/itemordendecompra" element={<Itemordendecompra />} />
            <Route path="/factura" element={<Factura />} />
            <Route path="/itemfactura" element={<Itemfactura />} />
            <Route path="/" element={<Navigate to="/cliente" replace />} />
            <Route path="*" element={<Navigate to="/cliente" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;

import uuid
import frappe
import pandas as pd
from pathlib import Path

EXCEL_PATH = Path("/home/diegovarela/Export CI Sharp2026_12_6_19_29_39.xlsx")

COLUMNAS = {
    "Status":                   "status",
    "Marca":                    "marca",
    "Model1":                   "modelo",
    "Series1":                  "numero_serie",
    "Model Type":               "model_type",
    "Inventario":               "inventario",
    "Folio Sharp":              "folio_sharp",
    "Cliente":                  "cliente",
    "Contrato":                 "contrato",
    "Unidad Organizativa (UO)": "unidad_organizativa",
    "UO Dirección":             "direccion",
    "UO Ciudad":                "ciudad",
    "UO Estado":                "estado",
    "IP Address":               "ip_address",
    "Fecha Instalación":        "fecha_instalacion",
    "Responsable Nombre":       "responsable_nombre",
    "Responsable Correo":       "responsable_correo",
    "Responsable Teléfono":     "responsable_telefono",
    "Area":                     "area",
    "Piso":                     "piso",
}

def generar_device_id(marca, modelo, ns):
    cadena = f"{marca.strip().lower()}-{modelo.strip().lower()}-{ns.strip().lower()}"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, cadena))

def limpiar(valor):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    return str(valor).strip() or None

def ejecutar():
    df = pd.read_excel(EXCEL_PATH, dtype=str)
    df = df.rename(columns=COLUMNAS)

    insertados = actualizados = omitidos = 0

    for _, fila in df.iterrows():
        marca  = limpiar(fila.get("marca"))
        modelo = limpiar(fila.get("modelo"))
        ns     = limpiar(fila.get("numero_serie"))

        if not all([marca, modelo, ns]):
            omitidos += 1
            continue

        device_id = generar_device_id(marca, modelo, ns)

        datos = {"device_id": device_id, "marca": marca, "modelo": modelo, "numero_serie": ns}
        for campo in ["status", "model_type", "inventario", "folio_sharp", "cliente",
                      "contrato", "unidad_organizativa", "direccion", "ciudad", "estado",
                      "ip_address", "fecha_instalacion", "responsable_nombre",
                      "responsable_correo", "responsable_telefono", "area", "piso"]:
            datos[campo] = limpiar(fila.get(campo))

        if frappe.db.exists("Equipo", {"device_id": device_id}):
            doc = frappe.get_doc("Equipo", {"device_id": device_id})
            for k, v in datos.items():
                setattr(doc, k, v)
            doc.save()
            actualizados += 1
        else:
            doc = frappe.get_doc({"doctype": "Equipo", **datos})
            doc.insert()
            insertados += 1

    frappe.db.commit()
    print(f"Insertados: {insertados} | Actualizados: {actualizados} | Omitidos: {omitidos}")

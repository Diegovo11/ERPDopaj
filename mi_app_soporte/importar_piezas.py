import re
import frappe
import pandas as pd
from pathlib import Path

EXCEL_PATH = Path("/home/diegovarela/triguide_data.xlsx")

def limpiar(valor):
    if valor is None or (isinstance(valor, float) and pd.isna(valor)):
        return None
    return str(valor).strip() or None

def extraer_vida_util(descripcion):
    if not descripcion:
        return None
    match = re.search(r'(\d+(?:\.\d+)?)\s*([Kk])?\s*[Pp]gs?', descripcion)
    if not match:
        return None
    numero = float(match.group(1))
    if match.group(2):
        numero *= 1000
    return int(numero)

def calcular_minmax(vida_util, tolerancia):
    if not vida_util:
        return None, None
    minima = int(vida_util * (1 - tolerancia / 100))
    maxima = int(vida_util * (1 + tolerancia / 100))
    return minima, maxima

def ejecutar():
    df = pd.read_excel(EXCEL_PATH, dtype=str)

    insertados = actualizados = omitidos = 0

    for _, fila in df.iterrows():
        marca        = limpiar(fila.get("Fabricante Buscado"))
        modelo       = limpiar(fila.get("Modelo Buscado"))
        numero_pieza = limpiar(fila.get("Número de Pieza"))

        if not all([marca, modelo, numero_pieza]):
            omitidos += 1
            continue

        descripcion      = limpiar(fila.get("Descripción"))
        vida_util        = extraer_vida_util(descripcion)
        tolerancia       = 5.00
        minima, maxima   = calcular_minmax(vida_util, tolerancia)

        datos = {
            "numero_pieza":         numero_pieza.upper(),
            "marca":                marca.upper(),
            "modelo":               modelo.upper(),
            "fabricante":           limpiar(fila.get("Fabricante")),
            "descripcion":          descripcion,
            "nombre_comun":         limpiar(fila.get("Nombre Común")),
            "regiones":             limpiar(fila.get("Regiones")),
            "vida_util_paginas":    vida_util,
            "tolerancia_porcentaje": tolerancia,
            "vida_util_minima":     minima,
            "vida_util_maxima":     maxima,
        }

        if frappe.db.exists("Pieza", numero_pieza.upper()):
            doc = frappe.get_doc("Pieza", numero_pieza.upper())
            for k, v in datos.items():
                if k != "tolerancia_porcentaje":
                    setattr(doc, k, v)
            doc.save()
            actualizados += 1
        else:
            doc = frappe.get_doc({"doctype": "Pieza", **datos})
            doc.insert()
            insertados += 1

    frappe.db.commit()
    print(f"Insertados: {insertados} | Actualizados: {actualizados} | Omitidos: {omitidos}")

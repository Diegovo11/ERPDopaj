# Copyright (c) 2026, Diego Varela and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SolicituddePiezas(Document):
    pass


@frappe.whitelist()
def get_conteo_por_estado():
    usuario = frappe.session.user
    roles = frappe.get_roles(usuario)

    es_tecnico = "Tecnico" in roles
    es_revisor = "Revisor" in roles or "System Manager" in roles

    filtros_base = {"docstatus": ["!=", 2]}

    if es_tecnico and not es_revisor:
        filtros_base["owner"] = usuario

    conteos = {}
    for estado in ["Pendiente", "Aprobada", "Rechazada"]:
        filtros = dict(filtros_base)
        filtros["estado"] = estado
        conteos[estado] = frappe.db.count("Solicitud de Piezas", filtros)

    return conteos

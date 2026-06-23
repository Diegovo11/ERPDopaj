import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class SolicitudDePiezas(Document):
    def before_insert(self):
        self.fecha_hora_solicitud = now_datetime()
        self.estado = "Pendiente"

    def before_save(self):
        if self.is_new():
            return

        usuario = frappe.session.user
        roles = frappe.get_roles(usuario)

        # System Manager puede todo
        if "System Manager" in roles:
            return

        doc_anterior = frappe.get_doc("Solicitud de Piezas", self.name)

        # Campos que NADIE excepto Admin puede modificar
        campos_bloqueados = [
            "numero_serie", "equipo", "marca", "modelo", "cliente",
            "ubicacion", "tecnico", "fecha_hora_solicitud",
            "contador_actual", "evidencia_contador", "observaciones",
            "piezas_solicitadas",
        ]
        for campo in campos_bloqueados:
            self.set(campo, doc_anterior.get(campo))

        # Tecnico no puede modificar nada en absoluto
        if "Tecnico" in roles:
            self.set("estado", doc_anterior.get("estado"))
            self.set("comentario_revisor", doc_anterior.get("comentario_revisor"))
            self.set("fecha_hora_revision", doc_anterior.get("fecha_hora_revision"))
            frappe.throw("No tienes permiso para modificar una solicitud ya creada.")

        # Revisor solo puede cambiar estado y comentario_revisor
        if "Revisor" in roles:
            if self.estado != doc_anterior.estado and self.estado in ["Aprobada", "Rechazada"]:
                self.fecha_hora_revision = now_datetime()

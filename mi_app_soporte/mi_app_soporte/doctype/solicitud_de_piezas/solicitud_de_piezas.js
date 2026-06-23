frappe.ui.form.on('Solicitud de Piezas', {
    refresh: function(frm) {
        let roles = frappe.user_roles;
        let esTecnico = roles.includes('Tecnico') && !roles.includes('System Manager');
        let esRevisor = roles.includes('Revisor') && !roles.includes('System Manager');
        let esDocumentoExistente = frm.docname && !frm.docname.startsWith('new-');

        if (esDocumentoExistente && esTecnico) {
            // Tecnico: todo bloqueado
            frm.fields.forEach(function(field) {
                frm.set_df_property(field.df.fieldname, 'read_only', 1);
            });
            frm.disable_save();
            frm.page.clear_primary_action();
            frm.page.clear_secondary_action();
        }

        if (esDocumentoExistente && esRevisor) {
            // Revisor: todo bloqueado excepto estado y comentario_revisor
            frm.fields.forEach(function(field) {
                let fieldname = field.df.fieldname;
                if (fieldname === 'estado' || fieldname === 'comentario_revisor') {
                    frm.set_df_property(fieldname, 'read_only', 0);
                } else {
                    frm.set_df_property(fieldname, 'read_only', 1);
                }
            });
        }
    },

    numero_serie: function(frm) {
        if (!frm.doc.numero_serie) return;

        frappe.db.get_list('Equipo', {
            filters: { numero_serie: frm.doc.numero_serie },
            fields: ['name', 'marca', 'modelo', 'cliente', 'unidad_organizativa'],
            limit: 1
        }).then(function(results) {
            if (results.length === 0) {
                frappe.msgprint('No se encontro ningun equipo con ese numero de serie.');
                frm.set_value('equipo', '');
                frm.set_value('marca', '');
                frm.set_value('modelo', '');
                frm.set_value('cliente', '');
                frm.set_value('ubicacion', '');
                return;
            }
            let equipo = results[0];
            frm.set_value('equipo', equipo.name);
            frm.set_value('marca', equipo.marca);
            frm.set_value('modelo', equipo.modelo);
            frm.set_value('cliente', equipo.cliente);
            frm.set_value('ubicacion', equipo.unidad_organizativa);
            frappe.show_alert({
                message: 'Equipo encontrado: ' + equipo.marca + ' ' + equipo.modelo,
                indicator: 'green'
            });
        });
    }
});

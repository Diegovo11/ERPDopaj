frappe.ui.form.on('Solicitud de Piezas', {
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

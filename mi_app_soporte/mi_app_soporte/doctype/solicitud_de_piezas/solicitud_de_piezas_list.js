frappe.listview_settings["Solicitud de Piezas"] = {
    onload: function(listview) {
        setTimeout(function() {
            frappe.call({
                method: "mi_app_soporte.mi_app_soporte.doctype.solicitud_de_piezas.solicitud_de_piezas.get_conteo_por_estado",
                callback: function(r) {
                    if (!r.message) return;

                    var conteos = r.message;

                    var colores = {
                        "Pendiente": "#f39c12",
                        "Aprobada":  "#27ae60",
                        "Rechazada": "#e74c3c"
                    };

                    var html = '<div id="dopaj-contadores" style="display:flex; gap:12px; padding:8px 16px;">';
                    ["Pendiente", "Aprobada", "Rechazada"].forEach(function(estado) {
                        html += '<div class="dopaj-contador" data-estado="' + estado + '" style="'
                            + 'cursor:pointer; padding:8px 18px; border-radius:6px;'
                            + 'background:' + colores[estado] + '; color:#fff;'
                            + 'font-weight:bold; font-size:14px;">'
                            + estado + ': ' + (conteos[estado] || 0)
                            + '</div>';
                    });
                    html += '</div>';

                    var $barra = $(html);

                    $barra.find(".dopaj-contador").on("click", function() {
                        var estado = $(this).data("estado");
                        listview.filter_area.clear();
                        listview.filter_area.add("Solicitud de Piezas", "estado", "=", estado);
                        listview.refresh();
                    });

                    $(".frappe-list").before($barra);
                }
            });
        }, 500);
    }
};

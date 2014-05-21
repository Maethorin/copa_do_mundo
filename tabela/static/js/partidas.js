var tabs = null;
function montaTabs(index) {
    tabs = $('#tabs').tabs();
    tabs.tabs('select', index);
    $('ul.indice li a').each(function() {
        var rodada_id = this.href.split('#');
        this.href = '/rodada/' + rodada_id[1];
    });
}
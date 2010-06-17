$(function() {
    $('li.partida input.palpite').setMask('9');

    $('li.partida form').each(function() {
        $(this).append('<input type="hidden" name="json" value="json" />');
        $(this).submit(function() {
             $(this).ajaxSubmit({
                 dataType: 'json',
                 success: function(resultado) {
                     atual = partida(resultado.partida_id);
                     atual.$gols_time_1.html(resultado.gols_time_1);
                     atual.$gols_time_2.html(resultado.gols_time_2);
                     atual.$votos.html('Total: ' + resultado.votos);
                     atual.$computado.show();
                     atual.$parcial.show();
                     atual.$enviar.hide();
                 },
              });
             return false
         });
    });
});

var tabs = null;
function montaTabs(index) {
    tabs = $('#tabs').tabs();
    tabs.tabs('select', index);
    $('ul.indice li a').each(function() {
        rodada_id = this.href.split('#');
        this.href = '/rodada/' + rodada_id[1];
    });
}

function partida(partida_id) { 
    $li = $('li#' + partida_id);
    gols_time_1 = null;
    gols_time_2 = null;
    computado = null;
    $parcial = $li.find('div.resultado-parcial');
    if ($parcial && !$parcial.hasClass('realizada')) {
        gols_time_1 = $parcial.find('span.gols')[0];
        gols_time_2 = $parcial.find('span.gols')[1];
        $computado = $li.find('div.computado');
        $votos = $parcial.find('span.votos');
        $enviar = $li.find('form input.enviar');
    }

    return {
        id: partida_id,
        $gols_time_1: $(gols_time_1),
        $gols_time_2: $(gols_time_2),
        $computado: $computado,
        $votos: $votos,
        $enviar: $enviar,
        $parcial: $parcial
    };
}
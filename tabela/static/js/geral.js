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
             }
          });
         return false
     });
});

function partida(partida_id) { 
    var $li = $('li#' + partida_id);
    var gols_time_1 = null;
    var gols_time_2 = null;
    var computado = null;
    var $parcial = $li.find('div.resultado-parcial');
    if ($parcial && !$parcial.hasClass('realizada')) {
        gols_time_1 = $parcial.find('span.gols')[0];
        gols_time_2 = $parcial.find('span.gols')[1];
        var $computado = $li.find('div.computado');
        var $votos = $parcial.find('span.votos');
        var $enviar = $li.find('form input.enviar');
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

$('.partidas-index').on('click', '.slide-up', function() {
    var $body = $(this).parent().find('.corpo-painel').slideToggle();
});
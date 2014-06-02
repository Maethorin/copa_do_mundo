$('.partida').on('submit', 'form', function(event) {
    event.preventDefault();
    var $this = $(this);
    var $partida = $this.parents(".partida");
    var data = $this.serializeArray();
    $(data).each(function() {
        if (this.name == "time_1" || this.name == "time_2") {
            if (this.value == "") {
                this.value = "0";
            }
        }
    });
    $.post($this[0].action, data)
        .done(function(data) {
            $partida.find(".placar-palpite").slideUp();
            $partida.find(".placar-simulado").slideDown();
            localStorage["partida-" + $partida.data("partida")] = 1;
            $partida.find(".time_1").text(data['gols_time_1']);
            $partida.find(".time_2").text(data['gols_time_2']);
            $partida.find(".votos").text(data['votos']);
        })
        .fail(function() {
            alert(0);
        }
    );
});

$('.partidas-index').on('click', '.slide-up', function() {
    var $body = $(this).parent().find('.corpo-painel').slideToggle();
});

$('.partida').each(function() {
    if (localStorage["partida-" + $(this).data("partida")]) {
        $(this).find(".placar-palpite").css("display", "none");
        $(this).find(".placar-simulado").css("display", "");
    }
});
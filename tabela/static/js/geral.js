$.cookie.json = true;

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
            var partidas = $.cookie('partidas');
            if (!partidas) {
                partidas = [];
            }
            partidas.push($partida.data("partida"));
            $.cookie('partidas', partidas, { expires: 180 });
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

function redimencionaCentral() {
    var viewportWidth = $(window).width();
    var viewportHeight = $(window).height();
    var $central = $(".central");
    var diferenca = 0;
    if (viewportWidth <= 768) {
        diferenca = 166;
        $(".navbar").addClass('navbar-fixed-top');
        $(".conteudo").removeClass("flex");
        $("body").css("padding-top", "45px");
    }
    else {
        diferenca = 276;
        $(".navbar").removeClass('navbar-fixed-top');
        $(".conteudo").addClass("flex");
        $("body").css("padding-top", "");
    }
    $central.css("height", (viewportHeight - diferenca) + "px");
}

$(window).load(function() {
    redimencionaCentral();
});

$(window).resize(function() {
    redimencionaCentral();
});
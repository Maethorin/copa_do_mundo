$.cookie.json = true;

$('.votar').on('submit', 'form', function(event) {
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
            $partida.find(".votar").toggle( "slide", "left", function() {
                $partida.find(".simulada").toggle( "slide", "right");
            });
            var partidas = $.cookie('partidas');
            if (!partidas) {
                partidas = [];
            }
            partidas.push($partida.data("partida"));
            $.cookie('partidas', partidas, { expires: 180, path:'/' });
            $partida.find(".time_1").text(data['gols_time_1']);
            $partida.find(".time_2").text(data['gols_time_2']);
            $partida.find(".votos").text(data['votos']);
        })
        .fail(function() {
            alert(0);
        }
    );
});

$('.conteudo').on('click', '.andamento', function() {
    animaPartidas($('.partidas-andamento'), 'left');
});

$('.conteudo').on('click', '.proximas', function() {
    animaPartidas($('.partidas-proximas'), 'right');
});

function animaPartidas($partidas, direcao) {
    var aminacao = {};
    if ($partidas.data("posicao") == 'aberto') {
        $partidas.find('.corpo-painel').slideToggle(function() {
            aminacao = (direcao == 'left' ? {left: -545} : {right: -545});
            $partidas.animate(aminacao);
            $partidas.data("posicao", ($partidas.data("posicao") == 'fechado' ? 'aberto' : 'fechado'))
        });
    }
    else {
        aminacao = (direcao == 'left' ? {left: 15} : {right: 15});
        $partidas.animate(aminacao, function() {
            $partidas.find('.corpo-painel').slideToggle();
            $partidas.data("posicao", ($partidas.data("posicao") == 'fechado' ? 'aberto' : 'fechado'))
        });
    }
}


function redimencionaCentral() {
    var viewportWidth = $(window).width();
    var viewportHeight = $(window).height();
    var $central = $(".central");
    var diferenca = 0;
    if (viewportWidth <= 768) {
        diferenca = 139;
        $(".navbar").addClass('navbar-fixed-top');
        $(".conteudo").removeClass("flex");
        $("body").css("padding-top", "45px");
    }
    else {
        diferenca = 249;
        $(".navbar").removeClass('navbar-fixed-top');
        $(".conteudo").addClass("flex");
        $("body").css("padding-top", "");
    }
    $central.css("height", (viewportHeight - diferenca) + "px");
    $('.ad-sense').css("height", (viewportHeight - diferenca) + "px");
    $("#accordion .panel-body").css('max-height', (viewportHeight - diferenca - 211) + "px");
}

$(window).load(function() {
    redimencionaCentral();
});


$(window).resize(function() {
    redimencionaCentral();
});

$(".time").tooltip();
$(".time-container").tooltip();

$(".label").tooltip();

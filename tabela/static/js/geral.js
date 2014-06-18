$.cookie.json = true;
var $partida_container = $('.partida');
$partida_container.on('click', '.novo-palpite', function() {
    var $this = $(this);
    var $partida = $this.parents(".partida");
    $.get("/form_de_partida/" + $partida.data('partida'))
        .done(function(li) {
            $partida.find(".placar-partida").append(li);
            $partida.find(".simulada").toggle( "slide", function() {
                $partida.find(".votar").toggle( "slide");
            });
        });
});

function popOver($partida, data) {
    $partida.find(".simulada").attr("title", data['mensagem']);
    $partida.find(".simulada").tooltip({"trigger": "manual"});
    $partida.find(".simulada").tooltip('show');
}

$partida_container.on('submit', '.votar form', function(event) {
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
            $partida.find(".votar").toggle( "slide", function() {
                $partida.find(".simulada").toggle( "slide");
                $partida.find(".votar").remove();
            });
            var partidas = $.cookie('partidas');
            if (!partidas) {
                partidas = [];
            }
            partidas.push($partida.data("partida"));
            $.cookie('partidas', partidas, { expires: 180, path:'/' });
            $partida.find(".time_1").text(data['gols_time_1']);
            $partida.find(".time_2").text(data['gols_time_2']);
            var $labelVotos = $partida.find(".label-votos");
            $labelVotos.attr("title", "Placar simulado - " + data['votos'] + " votos");
            $labelVotos.tooltip("destroy");
            $labelVotos.tooltip();
            popOver($partida, data);
        });
});

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
$(".fa").tooltip();


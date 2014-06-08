$(window).load(function() {
    var primeira = false;
    $('.barras').animate({top: -20}, 600);
    $('.tabela-classificacao').animate({top: 0}, 600, function() {
        if (!primeira) {
            $('.corpo').slideToggle(600);
        }
        primeira = true;
    });
});

$(".linha-titulo span").tooltip();
$(window).load(function() {
    var primeira = false;
    $('.barras').animate({top: -20}, 600);
    $('.rodada').animate({top: 0}, 600, function() {
        if (!primeira) {
            $('.partida').slideToggle(600);
        }
        primeira = true;
    });
});

$('.partida').css("display", "none");
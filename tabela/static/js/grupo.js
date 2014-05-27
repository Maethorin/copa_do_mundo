$(window).load(function() {
    $('.rodada').animate({top: 0}, 600, function() {
        $('.partida-1').slideToggle(600);
        $('.partida-2').slideToggle(600);
        $('.partida-3').slideToggle(600);
    });
});
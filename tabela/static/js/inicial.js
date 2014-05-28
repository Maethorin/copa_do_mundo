$(window).load(function() {
    $('.barras').animate({top: -20}, 600);
    $('.introducao').animate({top: 0}, 600, function() {
        $('.introducao .texto').slideToggle(600, function() {
            $('.partidas-index .painel').show().animate({bottom: 20})
            $('.barras-baixo').show().animate({top: 40})
        });
    });
});
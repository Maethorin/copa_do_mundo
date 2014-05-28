$(window).load(function() {
    $('.barras').animate({top: -20}, 600);
    $('.introducao').animate({top: 0}, 600, function() {
        $('.introducao .texto').slideToggle(600, function() {
            $('.partidas-index .painel').show().animate({bottom: 20});
            $('.barras-baixo').show().animate({top: 40});
        });
    });
});

$(window).unload(function() {
    $('.barras-baixo').show().animate({top: 66});
    $('.partidas-index .painel').show().animate({bottom: -52}, function() {
        $('.introducao .texto').slideToggle(600, function() {
            $('.barras').animate({top: 105}, 600);
            $('.introducao').animate({top: -75}, 600);
        });
    });
});


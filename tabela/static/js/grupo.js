$(window).load(function() {
    $('.rodada').animate({top: 0}, 600, function() {
        $('.partida').slideToggle(600, function() {
            console.log(1);
        });
    });
});
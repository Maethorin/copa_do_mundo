$(window).load(function() {
    $('.barras').animate({top: -20}, 600);
    $('.introducao').animate({top: 0}, 600, function() {
        $('.introducao .texto').slideToggle(600);
    });
});
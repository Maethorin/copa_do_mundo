$("#accordion").on("click", "h3", function() {
    var $collapse = $(this).parent().find(".panel-collapse");
    $("#accordion").find(".in").collapse('toggle');
    $collapse.collapse('toggle');
});

$("#accordion").on("show.bs.collapse", function(event) {
    $(event.target).parent().find("h3 .fa").toggleClass("fa-chevron-up fa-chevron-down");
});

$("#accordion").on("hide.bs.collapse", function(event) {
    $(event.target).parent().find("h3 .fa").toggleClass("fa-chevron-up fa-chevron-down");
});
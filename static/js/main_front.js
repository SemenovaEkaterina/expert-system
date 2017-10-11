$(function () {
    $(".main-menu li a").on("click", function () {
        $(".main-menu li.active").removeClass("active"), $(this).closest("li").addClass("active")
    }), $(".mobile-menu-trigger").on("click", function () {
        $(".mobile-menu-holder").slideToggle(400)
    })
});
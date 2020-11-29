$(document).keyup(function (event) {
    if ($("#price_ori").is(":focus") && (event.key == "Enter")) {
        $("#submit").click();
    }
});
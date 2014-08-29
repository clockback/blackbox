
$( document ).ready(function() {

    $("td.outer_default").click(function(){
        var cell = $(this);
        var number = cell.text();
        console.log("number: " + number);
        $.ajax({
            type: "POST",
            url: "/get_feedback",
            data: {number: number}
        }).done(function(response) {
            console.log(JSON.parse(response));
            cell.css("font-weight", "bold");
        });
    });
});







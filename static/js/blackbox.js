
$( document ).ready(function() {

    $("td.numbered").click(function(){
        var cell = $(this);
        var number = cell.text();
        $.ajax({
            type: "POST",
            url: "/get_feedback",
            data: {number: number, fname: "Elliot"}
        }).done(function(response) {
            console.log(JSON.parse(response));
            cell.css("font-weight", "bold");
        });
    });
});







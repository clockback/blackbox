
$( document ).ready(function() {

    $("td.numbered").click(function(){
        var cell = $(this);
        var entry = cell.text();
        var coords_str = $("p#coords").text();
        $.ajax({
            type: "POST",
            url: "/get_feedback",
            data: {
                coords_str: coords_str,
                entry: entry
            }
        }).done(function(response) {
            if(response == '"Did Not Emerge"'){
                var feedback = entry + " did not emerge";
            } else if (response == entry) {
                var feedback = entry + " came back to itself";
            } else {
                var feedback = entry + " emerged at " + response;
            }
            $("p#feedback").text(feedback);
            cell.css("font-weight", "bold");
        });
    });
        
    $("td.middle").click(function(){
        var cell = $(this);
        if(cell.hasClass("flagged")){
            cell.removeClass("flagged");
        } else if(cell.hasClass("question")){
            cell.removeClass("question");
            cell.addClass("flagged");
        } else {
            cell.addClass("question");
        };
    });
});







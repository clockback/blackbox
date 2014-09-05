
var colours = [
    'Black', 'Blue', 'BlueViolet', 'Brown',
    'CadetBlue', 'Chocolate', 'Coral',
    'CornflowerBlue', 'Crimson', 'DarkBlue', 'DarkCyan',
    'DarkGoldenRod', 'DarkGreen', 'DarkKhaki', 'DarkMagenta',
    'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon',
    'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkTurquoise',
    'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DodgerBlue',
    'FireBrick', 'ForestGreen', 'Fuchsia',
    'GoldenRod', 'Green',
    'HotPink', 'IndianRed', 'Indigo',
    'LawnGreen', 'LightBlue', 'LightCoral',
    'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray',
    'Lime', 'LimeGreen', 'Magenta',
    'Maroon', 'MediumAquaMarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple',
    'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise',
    'MediumVioletRed', 'MidnightBlue',
    'Navy', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleVioletRed',
    'Peru', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown',
    'SeaGreen', 'Sienna', 'SlateBlue',
    'SpringGreen', 'SteelBlue', 'Tan', 'Teal',
    'Tomato', 'Turquoise', 'Violet',
    'YellowGreen']

$( document ).ready(function() {
    
    var score = Number($("p#starting_score").text());
    
    $("td.numbered").click(function(){
        var cell = $(this);
        var entry = cell.attr('id');
        var coords_str = $("p#coords").text();
        $.ajax({
            type: "POST",
            url: "/get_feedback",
            data: {
                coords_str: coords_str,
                entry: entry
            }
        }).done(function(response) {
            /*
            When the blackbox returns "DNE" or hits the cell where it
            came from, the score increases by one point. If the blackbox
            returns an entry and a different exit, then the score increases 
            by two points.
            */
            var web_colour = colours.pop();
            if(response == '"Did Not Emerge"'){
                var feedback = entry + " did not emerge";
                cell.text("?");
                score++;
            } else if (response == entry) {
                var feedback = entry + " came back to itself";
                cell.text("b");
                score++;
            } else {
                var feedback = entry + " emerged at " + response;
                cell.css("background-color", web_colour);
                $("td#" + response).css("background-color", web_colour);
                score = score + 2;
            }
            if(score == 1){
                $("p#score").text("Score: " + score + " point");
            } else {
                $("p#score").text("Score: " + score + " points");
            };
            $("p#feedback").text(feedback);
            //$("p#debug").text(web_colour);
            cell.css("font-weight", "bold");
        });
    });

    var coords_n = JSON.parse($("p#coords").text()).length;
    var flags_n = 0;
    $("#reveal").attr('disabled', 'disabled');
    $("td.middle").click(function(){
        var cell = $(this);
        if(cell.hasClass("flagged")){
            cell.removeClass("flagged");
            flags_n--;
        } else if(cell.hasClass("question")){
            cell.removeClass("question");
            cell.addClass("flagged");
            flags_n++;
        } else {
            cell.addClass("question");
        };
        if(flags_n == coords_n){
            $("#reveal").removeAttr('disabled');
        } else {
            $("#reveal").attr('disabled', 'disabled');
        };
    });
});


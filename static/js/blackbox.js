
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
    
    var score = $("p#starting_score").text();
    
    $("td.numbered").click(function(){
        var cell = $(this);
        if(score < 1){
            score = 0;
            $("p#score").text("No points in it now - only the glory ;-)");
        } else {
            --score;
            $("p#score").text("Score: " + score + " points");
        };
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
            var web_colour = colours.pop();
            if(response == '"Did Not Emerge"'){
                var feedback = entry + " did not emerge";
                cell.text("?");
            } else if (response == entry) {
                var feedback = entry + " came back to itself";
                cell.text("b");
            } else {
                var feedback = entry + " emerged at " + response;
                cell.css("background-color", web_colour);
                $("td#" + response).css("background-color", web_colour);
            }
            $("p#feedback").text(feedback);
            //$("p#debug").text(web_colour);
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







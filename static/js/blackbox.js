
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
var flagged_class = "flagged";

$( document ).ready(function() {
    
    var score = Number($("p#starting_score").text());
    var atom_coords_str = $("p#atom_coords").text();
    $("td.numbered").click(function(){
        var cell = $(this);
        var entry = cell.attr('id');        
        $.ajax({
            type: "POST",
            url: "/get_feedback",
            data: {
                atom_coords_str: atom_coords_str,
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
    var atoms_n = JSON.parse($("p#atom_coords").text()).length;
    var flags_n = 0;
    $("#reveal").attr('disabled', 'disabled');
    $("td.middle").click(function(){
        var cell = $(this);
        if(cell.hasClass(flagged_class)){
            cell.removeClass(flagged_class);
            flags_n--;
        } else if(cell.hasClass("question")){
            cell.removeClass("question");
            cell.addClass(flagged_class);
            flags_n++;
        } else {
            cell.addClass("question");
        };
        if(flags_n == atoms_n){
            $("#reveal").removeAttr('disabled');
        } else {
            $("#reveal").attr('disabled', 'disabled');
        };
    });

    function feedback(details) {
        $("#dialog").html("<p>" + details + "</p>");
        $("#dialog").dialog({
            title: "Score results",
            autoOpen: false,
            width: 400,
            position: {my: "left bottom", at: "left+370 bottom", of: $("#reveal") },
            dialogClass: "no-close",
            buttons: [
	            {
		            text: "OK",
		            click: function() {
			            $( this ).dialog("close");
		            }
	            }
            ]
        });
        $("#dialog").dialog("open");
    };
    
    $("#reveal").click(function(){
        var flagged_cells = $("." + flagged_class);
        var flag_coords = [];
        for (var i = 0; i < flagged_cells.length; i++) {
            flag_coords.push("[" + flagged_cells[i].id + "]");
        }
        flag_coords_str = "[" + flag_coords.join() + "]"
        $.ajax({
            type: "POST",
            url: "/get_results",
            data: {
                atom_coords_str: atom_coords_str,
                flag_coords_str: flag_coords_str
            }
        }).done(function(response) {
            var response = JSON.parse(response);
            for (var i = 0; i < response.correct_coords.length; i++) {
                var correct_coord = response.correct_coords[i];
                correct_coord_str = correct_coord[0] + "\\," + correct_coord[1]; // must escape ,
                $("#" + correct_coord_str).removeClass(flagged_class);
                $("#" + correct_coord_str).addClass("correct");
            }
            for (var i = 0; i < response.incorrect_coords.length; i++) {
                var incorrect_coord = response.incorrect_coords[i];
                incorrect_coord_str = incorrect_coord[0] + "\\," + incorrect_coord[1];
                $("#" + incorrect_coord_str).removeClass(flagged_class);
                $("#" + incorrect_coord_str).addClass("incorrect");
            }
            for (var i = 0; i < response.unfound_coords.length; i++) {
                var unfound_coord = response.unfound_coords[i];
                unfound_coord_str = unfound_coord[0] + "\\," + unfound_coord[1];
                $("#" + unfound_coord_str).addClass("unfound");
            }
            $("#reveal").attr('disabled', 'disabled');
            feedback(response.message)
        });
    });
   
});


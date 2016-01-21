(function() {
    var shows = {};
    var showNames = [];

    function loadShows() {
        B.api("/shows", {        
            success: function(data, status, xhr) {
                console.log("Loaded shows ", data);
                shows = data;

                showNames = [];
                for(var name in shows) {
                    showNames.push(name);
                }
                showNames.sort();

                makeShows();
            }

            , error: function(xhr, status, err) {
                B.showError("Unable to load shows: "+ err);
            }
        });
    }

    function makeShows() {

        for(var i=0; i<showNames.length; i++) {
            var name = showNames[i];
            var show = shows[name];
            var s = "<div class='ui segment show ";
            if (show.random) {
                s += "random ";
            }
            s += show.type;
            s += "'><div class='ui header'>"+name+"";


            if (show.type == "master") {
                s += "<button class='ui right floated primary start button' data-name='"+name+"'>Start</button>";
            }
            for (var control_name in show.controls) {
                if (show.controls[control_name] == "color") {
                    s += " <input name='foo' class='jscolor picker floated ui right button' value='5050ff' readonly='true' >";
                }

            }

            "</div></div>";

            $("#showList").append(s);

            $('.jscolor').each(function(i, obj) {
                if (!obj.hasOwnProperty("hasPicker")) {
                    var picker = new jscolor(obj, {});
                    obj.hasPicker = true;
                }
                obj.value = '';
            });

        }

        $(".start.button").bind("click", startShow);
        $(".jscolor").bind("change", changeColor);
    }

    function changeColor(evt) {
        var color = $(this).context.value;
        console.log("Changing color to " + color);
        // $(this).context.value = ''; 
        B.api("/config", {
            data: {
                ix: 0,
                color: color,
                command: "set_color"
            }
            , error: function(xhr, status, err) {
                B.showError("Unable to set color: "+err);
            }
        });
    }

    function startShow(evt) {
        console.log("start show this=",this," evt=",evt);
        var el = $(this);
        var name = el.data("name")

        el.addClass("loading");
        B.api("/start_show", {
            data: {
                name: name
            }
            , error: function(xhr, status, err) {
                B.showError("Unable to run show: "+err);
            }
            , complete: function() {
                el.removeClass("loading");
                updateStatus();
            }
        })
    }

    var statusTimeout = null;

    function formatDuration(d) {
        if (!d) return "0s";

        d = parseInt(d);

        var tSecs = parseInt(d / 1000);
        var tMins = parseInt(tSecs / 60);

        var hours = parseInt(tMins / 60);
        var mins = tMins % 60;
        var secs = tSecs % 60;

        var out = [];
        if (hours > 0) {
            out.push(""+hours);
            out.push("h ");
        }
        if (mins > 0) {
            out.push(""+mins);
            out.push("m ");
        }
        out.push(secs);
        out.push("s");

        return out.join("");
    }

    function updateStatus() {
        if (statusTimeout) {
            clearTimeout(statusTimeout);
            statusTimeout = null;
        }

        B.api("/status", {
            success: function(data) {
                console.log("Got status data ", data);
                if (data.show) {
                    $("#currentShowName").text(data.show.name);

                    $("#currentShowRunTime").text(formatDuration(data.show.run_time))
                }
                $('#statusIcon').css("background-color", "lightgreen");
                $("#maxShowRuntime").text(formatDuration(data.max_time));

            }
            , error: function(xhr, status, err) {
                console.log("Status err ", err);
                $('#statusIcon').css("background-color", "red");
            }
            , complete: function() {
                if (!statusTimeout) {
                    statusTimeout = setTimeout(updateStatus, 5000);
                }
            }
            , timeout: 3000 // sets timeout to 3 seconds
        });
    }


    $(document).ready(function() {
        console.log("document ready");

        // Load the show names
        loadShows();
        updateStatus();

    });



})();

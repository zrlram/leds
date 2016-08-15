(function() {
    var shows = {};
    var showNames = [];
    var overlayNames = [];
    var controls_initialized = 0;

    function loadShows() {
        B.api("/shows", {        
            success: function(data, status, xhr) {
                console.log("Loaded shows ", data);
                shows = data;

                showNames = [];
                overlayNames = [];
                for(var name in shows) {
                    if (shows[name].type=="master") {
                        showNames.push(name);
                    }
                    else if (shows[name].type=="overlay") {
                        overlayNames.push(name)
                    }
                }
                showNames.sort();
                overlayNames.sort();

                makeShows();
            }

            , error: function(xhr, status, err) {
                B.showError("Unable to load shows: "+ err);
            }
        });
    }

    function makeShows() {

        s = "";
        for(var i=0; i<showNames.length; i++) {
            var name = showNames[i];
            var show = shows[name];
            s += "<a class='item show start' data-name='"+name+"'>"+name+"</a>";
        }
        $("#showList").append(s);
        $(".show.start").bind("click", startShow);

        s = "";
        for(var i=0; i<overlayNames.length; i++) {
            var name = overlayNames[i];
            var show = shows[name];
            s += "<a class='item overlay start' data-name='"+name+"'>"+name+"</a>";
        }
        s += "<button class='ui effect button overlay stop'>Stop</button>";
        $("#showOverlays").append(s);
        $(".overlay.start").bind("click", startOverlay);
        $(".overlay.stop").bind("click", stopOverlay);
    }

    function changeColor(evt) {
        var color = $(this).context.value;
        var id = parseInt($(this).context.id);
        // console.log("Changing color "+id+" to " + color);
        B.api("/config", {
            data: {
                ix: id,
                color: color,
                command: "set_color"
            }
            , error: function(xhr, status, err) {
                B.showError("Unable to set color: "+err);
            }
        });
    }
    
    function changeCheckbox(evt) {
        var value = 0;
        if ($(this).context.checked) { 
            value = 1;
        }
        console.log("checkbox value", value);
        var id = parseInt($(this).context.id);
        B.api("/config", {
            data: {
                checkbox: id, 
                value: value,     
                command: "set_checkbox"
            }
            , error: function(xhr, status, err) {
                B.showError("Unable to set checkbox value: "+err);
            }
        });
    }


    function showControls() {
        var name = $("#currentShowName").text();
        console.log("shows", shows, shows.length);
        if (shows === undefined || Object.keys(shows).length == 0) {
            console.log("no shows yet, waiting");
            setTimeout(showControls, 1000);  
        }
        var show = shows[name];
        // console.log("shows",shows);
        // console.log("name", name, "show", show.controls);

        
        $("#showControls").html("");         // rest first

        var color = 0;
        var range = 0;
        var checkbox = 0;
        for (control_name in show.controls) {
            
            // building color sliders
            if (show.controls[control_name] == "color") {
                $("#showControls").append( "<div class='item'>"+control_name+"&nbsp;<input class='ui jscolor picker button' id='"+color+"' value='5050ff' readonly='true' ></div>");
                color++;
            }
            
            // take care of ranges, which are represented as arrays
            if( Object.prototype.toString.call( show.controls[control_name] ) === '[object Array]' ) {

                entry = show.controls[control_name];
                min_value = entry[0];
                max_value = entry[1];
                // if it's there
                start = entry[2] || (max_value - min_value) / 2;
                step = entry[3] || (max_value - min_value) / 10;

                $("#showControls").append( "<div class='item' >" + control_name + " <span id='range_"+control_name+"'></span><div class='ui item range' id='control_range"+ range +"'></div></div>");

                $('#control_range'+ range).range({ min: min_value, max: max_value, start: start, step: step, range_id: range,
                       onChange: function(value) {
                           B.api("/config", {
                                data: {
                                    // such a hack. SORRY
                                    range: $(this)[0].range_id,
                                    value: value,     
                                    command: "set_range"
                                }
                                , success: function(data) {
                                    $('#range-value').text(data.value)
                                }
                                , error: function(xhr, status, err) {
                                    B.showError("Unable to set range value: "+err);
                                }
                            })
                       }

                });
                range++;
            }
            
            // take care of checkboxes
            if (show.controls[control_name] == "checkbox") {

                entry = show.controls[control_name];

                $("#showControls").append( "<div class='item' >" + control_name + " <input type='checkbox' class='ui item checkbox' id='"+ checkbox +"' value=1></input></div>");

                checkbox++;
            }

        }

        $('#speed-range').range({ min: 0, max: 4, start: speed, step: 0.1,
           onChange: function(value) {
                B.api("/config", {
                    data: {
                        speed: value,     
                        command: "set_speed"
                    }
                    , success: function(data) {
                        console.log("data",data);
                        $('#speed-value').text(data.speed)
                    }
                    , error: function(xhr, status, err) {
                        B.showError("Unable to set speed: "+err);
                    }
                });
           }
        });
        $('#brightness-range').range({ min: 0, max: 1, start: brightness, step: 0.1,
           onChange: function(value) {
                B.api("/config", {
                    data: {
                        brightness: value, 
                        command: "set_brightness"
                    }
                    , success: function(data) {
                        console.log("data",data);
                        // $('#brigthness-value').text(data.brigthness)
                    }
                    , error: function(xhr, status, err) {
                        B.showError("Unable to set brightness: "+err);
                    }
                });
           }
        });
        // times are in seconds
        $('#max-show-time-range').range({ min: 10, max: 20*60, start: max_runtime,
           onChange: function(value) {
                B.api("/config", {
                    data: {
                        runtime: value,     
                        command: "set_max_runtime"
                    }
                    , success: function(data) {
                        console.log("data",data);
                        $('#max-show-time-value').text(data.max_runtime)
                    }
                    , error: function(xhr, status, err) {
                        B.showError("Unable to set max show runtime: "+err);
                    }
                });
           }
        });

        $('.jscolor').each(function(i, obj) {
            if (!obj.hasOwnProperty("hasPicker")) {
                var picker = new jscolor(obj, {});
                obj.hasPicker = true;
            }
            obj.value = '';
        });
        $(".jscolor").bind("change", changeColor);

        $(".checkbox").bind("change", changeCheckbox);
    }

    function startShow(evt) {
        console.log("start show this=",this," evt=",evt);
        var el = $(this);
        var name = el.data("name")

        // make sure the controls are being shown 
        controls_initialized = 0

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
        });


    }

    function startOverlay(evt) {
        console.log("start overlay this=",this," evt=",evt);
        var el = $(this);
        var name = el.data("name")

        B.api("/run_overlay", {
            data: {
                name: name
            }
            , error: function(xhr, status, err) {
                B.showError("Unable to run overlay: "+err);
            }
        });
    }

    function stopOverlay(evt) {
        console.log("stop overlays");
        B.api("/stop_overlay", {
            data: {},
            error: function(xhr, status, err) {
                B.showError("Unable to stop overlays");
            }
        });
    }

    // some global parameters
    var statusTimeout = null;
    var speed = 0;
    var max_runtime = 0;
    var brightness = 0;

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
                max_runtime = data.max_time / 1000;    // store to initialize the control correctly
                brightness = data.brightness;
                speed = data.speed;             // again, for the controls
                if (!controls_initialized) {
                    showControls();
                    controls_initialized = 1;
                }       
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

        // build shutdown button
        $("#shutdown").click(function(value) {
           B.api("/shutdown", { data:{ please: 1 } });
        });

        /*
        $('#speed-plus').click(function(value) {
                B.api("/config", {
                    data: {
                        speed: 0.1,     // relative change
                        command: "set_speed"
                    }
                    , success: function(data) {
                        console.log("data",data);
                        $('#speed-value').text(data.speed)
                    }
                    , error: function(xhr, status, err) {
                        B.showError("Unable to set speed: "+err);
                    }
                });
        }); 
        */


        /*
        $('#dither').click(function(value) {
                B.api("/config", {
                    data: {
                        speed: 0.1,     // relative change
                        command: "set_speed"
                    }
                    , success: function(data) {
                        console.log("data",data);
                        $('#speed-value').text(data.speed)
                    }
                    , error: function(xhr, status, err) {
                        B.showError("Unable to set speed: "+err);
                    }
                });
        }); 
    */

        // in case there are controls for the current show already
        $('.jscolor').each(function(i, obj) {
            if (!obj.hasOwnProperty("hasPicker")) {
                var picker = new jscolor(obj, {});
                obj.hasPicker = true;
            }
            obj.value = '';
        });
        $(".jscolor").bind("change", changeColor);

    });
})();

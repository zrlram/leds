(function() {
    var shows = {};
    var showNames = [];
    var controls_initialized = 0;

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

        s = "";
        for(var i=0; i<showNames.length; i++) {
            var name = showNames[i];
            var show = shows[name];
            s += "<a class='item show start' data-name='"+name+"'>"+name+"</a>";
        }


        $("#showList").append(s);

        $(".show.start").bind("click", startShow);
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
        var value = $(this).context.value; 
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
        var show = shows[name];
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

                $("#showControls").append( "<div class='item' >" + control_name + " <div class='ui item range' id='control_range"+ range +"'></div></div>");

                $('#control_range'+ range).range({ min: min_value, max: max_value, start: start, step: (max_value - min_value) / 10, range_id: range,
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
                // console.log("Got status data ", data);
                if (data.show) {
                    $("#currentShowName").text(data.show.name);
                    $("#currentShowRunTime").text(formatDuration(data.show.run_time))
                }
                $('#statusIcon').css("background-color", "lightgreen");
                $("#maxShowRuntime").text(formatDuration(data.max_time));
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

        $('#speed-range').range({ min: 0, max: 4, start: 0.1, step: 0.1,
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
        $('#brightness-range').range({ min: 0, max: 1, start: 1.0, step: 0.1,
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
        $('#max-show-time-range').range({ min: 10, max: 20*60, start: 4 * 60,
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

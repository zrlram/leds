import time

class ControlsModel(object):

    def __init__(self):

        ## Speed setting. This is multiplied against the "rate", so that
        # means if you're calculating delays, 2.0 here should result in 
        # calculating a delay half as long. This will be done automatically
        # by the show runner if you are yielding something more than about 0.001,
        # but if you are doing proper time based "as fast as we can" calculations
        # yourself, you will need to respect this value.
        self.speed_multi = 1.0

        # who has to be informed of changes?
        self.listeners = set()

        self._tap_times = []

        self.show_names = []
        # current show's name
        self.show_name = ""

        # shortest and longest possible show time 
        self.time_limits = [10, 20 * 60]
        self.max_time = 42.0

        self.brightness = 1.0

        # The RGB values of the chosen colors. There are two
        # To keep things generic, there are two colors that can be set 
        self.chosen_colors = [ (255, 255, 0), (0,255,255) ]         

        # custom range to be used by shows - they have to set the extremes
        self.ranges = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]

        # custom booleans / checkboxes
        self.checkbox = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def add_listener(self, listener):
        self.listeners.add(listener)

    def del_listener(self, listener):
        self.listeners.discard(listener)

    # not really used 
    '''
    def _notify_refresh(self):
        for listener in self.listeners:
            try:
                listener.control_refresh_all()
            except AttributeError:
                pass # whatever...
    '''


    def speed_reset(self):
        self.speed_multi = 1.0
        self._notify_speed_changed()

    def speed_change_rel(self, amt):
        # Scale this value some so it's a log scale or similar?
        self.speed_multi = 1.0 + amt
        if self.speed_multi <= 0.0:
            self.speed_multi = 0.01

        self._notify_speed_changed()

    def speed_tap(self):
        now = time.time()
        if len(self._tap_times) == 0:
            # It is the first tap so record it and move on
            self._tap_times.append(now)
            print "First tap"
            return

        # There is at least one previous time.

        # How long has it been? There is a maximum amount of time between taps
        # that corresponds to some low bpm after which we start over
        elapsed = now - self._tap_times[len(self._tap_times) - 1] 

        if elapsed > 2.0:
            # OMG! So long ago! It's totally time to reset
            self._tap_times = [now]
            print "Elapsed was %f, resettting" % elapsed
            return

        # Hmm, okay, not all that old, so let's add it and then process
        # all of them if we can
        self._tap_times.append(now)

        while len(self._tap_times) > 16:
            self._tap_times.pop(0)

        # There are now 1 to 8 elements in the list
        if len(self._tap_times) < 4:
            # Not enough
            print "Only have %d taps, not enough" % len(self._tap_times)
            return

        # I'm not sure if this is the "right" way to find intervals, but it makes sense to me.
        # Rather than just average from the begining time to the end time, we convert the times
        # into intervals and then average the intervals
        int_total = 0.0
        num_ints = 0
        last = 0.0
        for ix, v in enumerate(self._tap_times):            
            if ix == 0:
                last = v
                continue
            int_total += v - last
            last = v
            num_ints += 1

        avg_interval = int_total / num_ints

        # Reference time is 120bpm, which is 0.5s between quarter notes (i.e. taps)
        print "avgInterval=%f  intTotal=%f numInts=%d" % (avg_interval, int_total, num_ints)
        self.speed_multi = 0.5 / avg_interval

        self._notify_speed_changed()


    def _notify_speed_changed(self):
        print "_notify_speed_changed"
        for listener in self.listeners:
            try:
                listener.control_speed_changed()
            except AttributeError:
                pass # ignore

    def set_color_rgb(self, c_ix, data):
        """
        Sets the color at index c_ix to the value given by rgb data in
        three-tuple. 
        """
        if c_ix < 0 or c_ix > 1: 
            print "Don't understand color ix %d" % c_ix 
            return

        if len(data) < 3: 
            print "Not enough data values to set rgb color: %s" % (str(data))
            return

        self.chosen_colors[c_ix] = (data[0],data[1],data[2])

        self._notify_color_changed(c_ix)

    def _notify_color_changed(self, c_ix):
        print "_notify_color_changed"
        for listener in self.listeners:
            try: 
                listener.control_color_changed(c_ix)
            except AttributeError:
                pass # ignore


    def set_colorized(self, val):
        self.colorized = val

        self._notify_colorized_changed()


    def _notify_colorized_changed(self):
        print "_notify_colorized_changed"
        for listener in self.listeners:
            try:
                listener.control_colorized_changed()
            except AttributeError:
                pass # ignore

    def set_brightness(self, val):
        self.brightness = val

        self._notify_brightness_changed()


    def _notify_brightness_changed(self):
        print "_notify_brightness_changed"
        for listener in self.listeners:
            try:
                listener.control_brightness_changed(self.brightness)
            except AttributeError:
                pass # ignore


    def set_show_names(self, names):
        self.master_names = names
        self._notify_show_names_changed()

    def _notify_show_names_changed(self):
        print "_notify_show_names_changed"
        for listener in self.listeners:
            try:
                listener.control_master_names_changed()
            except AttributeError:
                pass # ignore      

    def set_show_name(self, name):
        self.master_name = name
        self._notify_show_name_changed()

    def _notify_show_name_changed(self):
        print "_notify_show_name_changed"
        for listener in self.listeners:
            try:
                listener.control_master_name_changed()
            except AttributeError:
                pass # ignore      


    def set_max_time(self, secs):
        self.max_time = float(secs)
        self._notify_max_time_changed()

    def set_max_time_scaled(self, scaled):
        _range = self.time_limits[1] - self.time_limits[0]
        self.max_time = self.time_limits[0] + (scaled * _range)
        self._notify_max_time_changed()

    def _notify_max_time_changed(self):
        print "_notify_max_time_changed"
        for listener in self.listeners:
            try:
                listener.control_max_time_changed()
            except AttributeError:
                pass # ignore      

    def set_custom_checkbox_value(self, checkbox, value):
        self.checkbox[checkbox] = value
        self._notify_custom_checkbox_value_changed(checkbox)

    def _notify_custom_checkbox_value_changed(self, checkbox):
        print "_notify_custom_checkbox_change"
        for listener in self.listeners:
            try:
                listener.custom_checkbox_value_changed(checkbox)
            except AttributeError:
                pass # ignore      


    def set_custom_range_value(self, range, value):
        self.ranges[range] = value
        self._notify_custom_range_value_changed(range)

    def _notify_custom_range_value_changed(self, range):
        print "_notify_custom_range_change"
        for listener in self.listeners:
            try:
                listener.custom_range_value_changed(range)
            except AttributeError, e:
                pass # ignore      

    def set_config(self, key, value):
        # if ..
        # fc_config.xx    
        pass




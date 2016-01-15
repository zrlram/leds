import time


class ControlsModel(object):
    """
    Holds the state of the user interface for the overall show server. This
    is useful both for re-establishing state in clients that come and go, like
    the TouchOSC client, but also as THE place that shows come to in order
    to understand how they should modify their behavior.

    From the show side, there are a lot of un-encapsulated properties/attributes
    of a ControlsModel instance that can be read. Some key ones are:

        speed_multi
        intensified
        colorized
        modifiers[]

    Shows should try to change what they are doing based on these values. See
    the individual documentation below for more detail about each of them.

    This class understands OSC messages and will update it's internal
    state based on received messages. What happens based on which message
    can be see in incomingOSC()

    The normal MVC interaction is that an OSC message comes in, modifying the
    state stored here. This class then notifies all of it's listeners about
    the state change (via some form of control_XXX method call). One of those
    listeners is probably an instance of the TouchOSC class, which then
    broadcasts a whole bunch of messages to TouchOSC clients so that their
    UIs all stay in sync based on whatever the state modification was.

    Presumably state modifications could come from other UIs like a web
    interface, although nothing like that is currently implemented.

    In general, a show implementation should read from here, but almost
    certainly shouldn't be writing to this object. If anything DOES want
    to write to this guy, then it should be using the setters to ensure that
    appropriate notifications are sent to interested listeners.

    """

    

    def __init__(self):

        ## Speed setting. This is multiplied against the "rate", so that
        # means if you're calculating delays, 2.0 here should result in 
        # calculating a delay half as long. This will be done automatically
        # by the show runner if you are yielding something more than about 0.001,
        # but if you are doing proper time based "as fast as we can" calculations
        # yourself, you will need to respect this value.
        self.speed_multi = 1.0

        # A value that ranges from -1.0 (maximum calm) to 1.0 (maximum intensity).
        # It should be interpretted by each show in a show appropriate manner
        self.intensified = 0.0

        # A value that ranges from -1.0 (totally monochrome) to 1.0 (max color).
        # If the currently running show does not set handles_colorized to True this
        # will be handled by the system, otherwise it is left to the show to modify
        # it's colors appropriately
        self.colorized = 0.0

        self.listeners = set()

        self._tap_times = []

        # A message that is shown in the UI
        self.message = ""

        self.show_names = []

        self.show_name = ""

        self.time_limits = [30, 20 * 60]
        self.max_time = 42.0

        self.brightness = 1.0


    def add_listener(self, listener):
        self.listeners.add(listener)

    def del_listener(self, listener):
        self.listeners.discard(listener)

    def _notify_refresh(self):
        for listener in self.listeners:
            try:
                listener.control_refresh_all()
            except AttributeError:
                pass # whatever...


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



    def set_intensified(self, val):
        self.intensified = val

        self._notify_intensified_changed()


    def _notify_intensified_changed(self):
        print "_notify_intensified_changed"
        for listener in self.listeners:
            try:
                listener.control_intensified_changed()
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


    def set_message(self, msg):
        self.message = msg
        self._notify_message_changed()

    def _notify_message_changed(self):
        print "_notify_message_changed"
        for listener in self.listeners:
            try:
                listener.control_message_changed()
            except AttributeError:
                pass # ignore      



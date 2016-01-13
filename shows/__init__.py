import os
import importlib

# partly stolen from: https://github.com/baaahs/lights

def load_shows(path=None):
    _shows = []

    if not path:
        path = __path__[0]

    for m in [m for m in os.listdir(path) if not m.startswith('_') and m.endswith('.py')]:
        try:
            assert m.endswith('.py')
            m = m[:-3] # drop the .py from the filename
            module_name = "shows." + m

            # load module
            mod = importlib.import_module(module_name)

            # module must explicitly export shows
            if hasattr(mod, '__shows__'):
                _shows.extend(mod.__shows__)

        except Exception, e:
            print "Exception loading module from %s, skipping" % m
            import traceback
            traceback.print_exc()

    return _shows

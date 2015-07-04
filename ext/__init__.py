import os, sys

"""Two functions below included becouse packp3d not include importlib
in standard python library even if -r morepy used
"""

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)
    
def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]



extensions = []
ext_names = []
module, module_name = None, None
for f in os.listdir(__path__[0]):
    if not f.startswith('__') and (f.endswith('.py') \
                                   or f.endswith('.pyo') \
                                   or f.endswith('.pyc')):
        module_name = os.path.splitext(f)[0]
        if module_name not in ext_names:
            module = import_module('.'+module_name, __package__)
            if 'target' in dir(module) and 'order' in dir(module) and 'invoke' in dir(module):
                extensions.append(module)
                ext_names.append(module_name)
extensions.sort(key = lambda e: e.order)
del f, module, module_name

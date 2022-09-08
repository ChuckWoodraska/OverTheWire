import types
import importlib.util
import sys
import logging
from urllib.request import urlopen

log_FORMAT = "%(message)s"
logging.basicConfig(format=log_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class MemoryImporter:
    def __init__(self, modules, base_url):
        self.module_names = modules
        self.base_url = f'{base_url}/'

    def find_module(self, fullname, path=None):
        if fullname.split('.')[0] not in self.module_names:
            return None
        try:
            if loader := importlib.util.spec_from_file_location(fullname, path):
                return None
        except ImportError:
            pass
        return None if fullname.split('.').count(fullname.split('.')[-1]) > 1 else self

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        if name.split('.')[-1] in sys.modules:
            return sys.modules[name.split('.')[-1]]

        module_url = f"{self.base_url}{name.replace('.', '/')}.py"
        package_url = f"{self.base_url}{name.replace('.', '/')}/__init__.py"
        final_url = None
        final_src = None

        try:
            package_src = None
            if package_src is None:
                package_src = urlopen(package_url).read()
            final_src = package_src
            final_url = package_url
        except IOError:
            package_src = None

        if final_src is None:
            try:
                module_src = None
                if module_src is None:  # .pyc file not found, falling back to .py
                    module_src = urlopen(module_url).read()
                final_src = module_src
                final_url = module_url
            except IOError:
                return None

        mod = types.ModuleType(name)
        mod.__loader__ = self
        mod.__file__ = final_url
        mod.__package__ = name.split('.')[0] if package_src else name
        mod.__path__ = ['/'.join(mod.__file__.split('/')[:-1]) + '/']
        sys.modules[name] = mod
        exec(final_src, mod.__dict__)
        return mod


def load(module_name, url='http://localhost:8000/'):
    importer = MemoryImporter([module_name], url)
    if loader := importer.find_module(module_name):
        if module := loader.load_module(module_name):
            return module

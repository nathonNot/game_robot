import importlib


lib = importlib.import_module("test_import.test_a")
print(lib)
instance = lib.A()
instance.funcname()
import os
import importlib

filters = []

for module in os.listdir(os.path.dirname(__file__)):
	if module == '__init__.py' or module[-3:] != '.py':
		continue
	filters.append(importlib.import_module("filters.%s" % module[:-3]))

isort $(find pyexcel_htmlr -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 pyexcel_htmlr
black -l 79 tests

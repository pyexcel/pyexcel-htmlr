#/bin/bash
pip freeze
coverage run -m --source=pyexcel_htmlr pytest --doctest-modules && coverage report --show-missing

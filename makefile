test-project:
	pipenv run coverage run -m unittest discover -s test -v
coverage:
	pipenv run coverage report -m 
generate:
	pipenv run coverage html
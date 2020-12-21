test:
	pipenv run coverage run -m unittest discover -s $(dir) -v
coverage:
	pipenv run coverage report -m 
generate:
	pipenv run coverage $(file)
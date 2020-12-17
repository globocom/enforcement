build:
	docker build -t enforcement .
test:
	coverage run -m unittest discover -s $(dir) -v
coverage:
	coverage report -m 
generate:
	coverage $(file)
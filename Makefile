init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run python -m unittest tests/mock_tests.py

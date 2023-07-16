test:
	@pytest

cov:
	@coverage run -m pytest -q
	@coverage report

setup-win:
	python -m venv .venv
	.venv\Scripts\activate.bat && pip install -r requirements.txt

setup-unix:
	python3 -m venv .venv
	. .venv/bin/activate && pip3 install -r requirements.txt

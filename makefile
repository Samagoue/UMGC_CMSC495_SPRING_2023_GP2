install:
	pip install -r requirements.txt

run:
	FLASK_APP=run.py flask run

all: install run
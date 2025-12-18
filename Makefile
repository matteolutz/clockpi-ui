PIP = pip3

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    PYTHON := python
else
    PYTHON := python3
endif

init:
	$(PIP) install -r requirements.txt

clean:
	rm -rf venv/

run:
	$(PYTHON) -m clockpi_ui

freeze:
	$(PIP) freeze > requirements.txt

.PHONY: init clean freeze

SHELL := /bin/bash

.PHONY: install
install:
	@which python3 && python3 -m venv venv || python -m venv venv
	@source venv/bin/activate && pip install -r requirements.txt

.PHONY: build
build:
	@source venv/bin/activate && python generate_rcc.py icons/tango/index.theme

.PHONY: clean
clean:
	rm -rf ./venv
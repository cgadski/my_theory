.PHONY: all

all:
	rm -rf generated
	mkdir generated
	python3 stacker.py

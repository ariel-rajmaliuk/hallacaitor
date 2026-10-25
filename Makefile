.PHONY: export check motion docs
export:
	python scripts/export.py
check:
	python -m unittest discover -s tests -v
	python scripts/validate.py
motion:
	python scripts/check_motion.py
docs:
	python scripts/illustrate.py
	python scripts/manual.py

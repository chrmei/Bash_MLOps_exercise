<<<<<<< HEAD
.PHONY: tests

bash:




tests:
	pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

=======
.PHONY: tests

bash:




tests:
	pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

>>>>>>> main
all: 
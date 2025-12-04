.PHONY: tests bash all

# path handling
PROJECT_ROOT := $(shell pwd)
SCRIPTS_DIR := $(PROJECT_ROOT)/scripts

bash:
	@echo "========================="
	@echo "=== Starting Pipeline ==="
	@echo "========================="
	@echo "Step 1: Data Collection"
	@bash $(SCRIPTS_DIR)/collect.sh
	@echo ""
	@echo "Step 2: Data Pre-Processing"
	@bash $(SCRIPTS_DIR)/preprocessed.sh
	@echo ""
	@echo "Step 3: Model Training"
	@bash $(SCRIPTS_DIR)/train.sh
	@echo ""
	@echo "======================================="
	@echo "=== Pipeline completed successfully ==="
	@echo "======================================="


tests:
	pytest tests/test_collect.py && \
	pytest tests/test_preprocessed.py && \
	pytest tests/test_model.py

all: 

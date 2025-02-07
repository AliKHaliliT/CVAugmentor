# Makefile for building Sphinx documentation

# Set the paths
SOURCE_DIR := .
BUILD_DIR := docs

# Check if Python is installed
check_python:
	@command -v python >/dev/null 2>&1 || { echo "Python is not installed. Please install it first."; exit 1; }

# Check if Sphinx is installed
check_sphinx: check_python
	@command -v sphinx-build >/dev/null 2>&1 || { echo "Sphinx is not installed. Please install it using 'pip install sphinx'."; exit 1; }

# Run the augmentations_rst_generator.py script
run_augmentations_rst_generator:
	@echo "Running augmentations_rst_generator.py..."
	python augmentations_rst_generator.py

# Run the Sphinx build command
build: check_sphinx run_augmentations_rst_generator
	@echo "Building Sphinx documentation..."
	sphinx-build -b html $(SOURCE_DIR) $(BUILD_DIR)

# Check if the build was successful
	@if [ $$? -eq 0 ]; then \
		echo "Sphinx build completed successfully"; \
	else \
		echo "Sphinx build failed."; \
		exit 1; \
	fi

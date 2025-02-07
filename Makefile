# Makefile for building Sphinx documentation

# Set the paths
SOURCE_DIR := .
BUILD_DIR := docs

# Check if Sphinx is installed
check_sphinx:
	@command -v sphinx-build >/dev/null 2>&1 || { echo "Sphinx is not installed. Please install it using 'pip install sphinx'."; exit 1; }

# Run the Sphinx build command
build: check_sphinx
	@echo "Building Sphinx documentation..."
	sphinx-build -b html $(SOURCE_DIR) $(BUILD_DIR)

# Check if the build was successful
	@if [ $$? -eq 0 ]; then \
		echo "Sphinx build completed successfully"; \
	else \
		echo "Sphinx build failed."; \
		exit 1; \
	fi

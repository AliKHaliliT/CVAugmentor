# Define the build directory
BUILD_DIR := $(CURDIR)/_build

# Default target
all: build

# Create the build directory if it doesn't exist
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Run Sphinx build command
build: $(BUILD_DIR)
	sphinx-build -b html . $(BUILD_DIR)/html
	cp -r $(BUILD_DIR)/html/* $(CURDIR)/
	rm -rf $(BUILD_DIR)

# Clean up the build directory
clean:
	rm -rf $(BUILD_DIR)

# Phony targets
.PHONY: all build clean
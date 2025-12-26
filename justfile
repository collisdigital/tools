# List available recipes
default:
    @just --list

# Generate the site
build:
    python scripts/generate_index.py

# Serve the site locally
serve: build
    python -m http.server --directory dist

# Serve the tools directory directly for development
dev:
    python -m http.server --directory tools

# Clean the dist directory
clean:
    rm -rf dist

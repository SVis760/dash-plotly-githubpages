# Makefile for deploying Dash app to GitHub Pages using wget

# Variables
APP_PORT := 8050
APP_URL := http://127.0.0.1:$(APP_PORT)
DOWNLOAD_DIR := 127.0.0.1:8050

.PHONY: html update submodules clean gh-pages all teardown-python

html:
	@echo "Starting Dash app..."
	# Launch the Dash app in the background (with DEBUG off)
	export DEBUG=False && python3 app.py &

	# Wait 60 seconds for the app to start (adjust if needed)
	sleep 60

	@echo "Downloading site with wget..."
	# Download the root page and Dash endpoints
	wget -r http://127.0.0.1:8050/ 
	wget -r http://127.0.0.1:8050/_dash-layout 
	wget -r http://127.0.0.1:8050/_dash-dependencies

	@echo "Post-processing downloaded files..."
	# Replace strings in the downloaded dash_renderer JS files


	# Rename downloaded Dash endpoints
	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json	
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json

	# Copy assets to the downloaded site (your clientside.js and any other assets)
	cp -r assets/* $(DOWNLOAD_DIR)/assets/

	@echo "Killing the Dash app..."
	# Kill the Python process running the Dash app
	pkill -f python || echo "No Python process found"
	@echo "Build complete: the static site is in $(DOWNLOAD_DIR)"

gh-pages:
	cd 127.0.0.1:8050 && touch .nojekyll && git init && git add * && git add .nojekyll && git commit -m "update" && git branch -M main && git remote add origin https://github.com/SVis760/dash-plotly-githubpages.git && git push -f origin main

all: gh-pages

teardown-python:
	pkill -f python || echo "No Python process found"

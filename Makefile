# Makefile for deploying Dash app to GitHub Pages using wget
# This Makefile is adapted to be as close as possible to your provided example.

# Variables
APP_PORT := 8050
APP_URL := http://127.0.0.1:$(APP_PORT)
DOWNLOAD_DIR := 127.0.0.1:$(APP_PORT)

.PHONY: html update submodules clean gh-pages all teardown-python

html:
	@echo "Starting Dash app..."
	# Launch the Dash app in the background (with DEBUG off)
	export DEBUG=False && python3 app.py &
	# Wait 60 seconds for the app to start (adjust if needed)
	sleep 60
	@echo "Downloading site with wget..."
	# Download the root page and Dash endpoints
	wget -r $(APP_URL)/ 
	wget -r $(APP_URL)/_dash-layout 
	wget -r $(APP_URL)/_dash-dependencies
	@echo "Post-processing downloaded files..."
	# Replace strings in the downloaded dash_renderer JS files
	sed -i 's/_dash-layout/_dash-layout.json/g' $(DOWNLOAD_DIR)/_dash-component-suites/dash_renderer/*.js
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' $(DOWNLOAD_DIR)/_dash-component-suites/dash_renderer/*.js
	# Optionally, if head.html exists, insert its contents into index.html
	if [ -f head.html ]; then sed -i '/<head>/ r head.html' $(DOWNLOAD_DIR)/index.html; fi
	# Rename downloaded Dash endpoints
	mv $(DOWNLOAD_DIR)/_dash-layout $(DOWNLOAD_DIR)/_dash-layout.json
	mv $(DOWNLOAD_DIR)/_dash-dependencies $(DOWNLOAD_DIR)/_dash-dependencies.json
	# Copy assets to the downloaded site (your clientside.js and any other assets)
	cp -r assets/* $(DOWNLOAD_DIR)/assets/
	@echo "Killing the Dash app..."
	# Kill the Python process running the Dash app
	ps | grep python | awk '{print $$1}' | xargs kill -9
	@echo "Build complete: the static site is in $(DOWNLOAD_DIR)"



submodules:
	git submodule init
	git submodule update

clean:
	rm -rf $(DOWNLOAD_DIR)/
	# Remove any other generated files if needed

gh-pages:
	@echo "Deploying to GitHub Pages..."
	# In this example, we change into the downloaded directory, add a .nojekyll file,
	# initialize a git repo, and push to the remote GitHub Pages repo.
	cd $(DOWNLOAD_DIR) && touch .nojekyll && \
	git init && \
	git add * && \
	git add .nojekyll && \
	git commit -m "update" && \
	git remote add origin https://github.com/SVis760/dash-plotly-githubpages.git && \
	git push -f origin main

all: gh-pages

teardown-python:
	ps | grep python | awk '{print $$1}' | xargs kill -9

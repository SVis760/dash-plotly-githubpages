APP_PORT := 8050
DOWNLOAD_DIR := 127.0.0.1:$(APP_PORT)

.PHONY: html gh-pages teardown-python

html:
	@echo "Starting Dash app..."
	export DEBUG=False && python3 app.py &

	# Wait 30 seconds for the app to start
	sleep 30

	@echo "Downloading site with wget..."
	wget -r -np -nH --cut-dirs=1 -P $(DOWNLOAD_DIR) http://127.0.0.1:8050/

	@echo "Post-processing files..."
	sed -i 's/_dash-layout/_dash-layout.json/g' $(DOWNLOAD_DIR)/_dash-component-suites/dash_renderer/*.js
	sed -i 's/_dash-dependencies/_dash-dependencies.json/g' $(DOWNLOAD_DIR)/_dash-component-suites/dash_renderer/*.js

	mv $(DOWNLOAD_DIR)/_dash-layout $(DOWNLOAD_DIR)/_dash-layout.json
	mv $(DOWNLOAD_DIR)/_dash-dependencies $(DOWNLOAD_DIR)/_dash-dependencies.json

	cp -r assets/* $(DOWNLOAD_DIR)/assets/

	@echo "Killing Dash app..."
	pkill -f python || echo "No Python process found"
	@echo "Build complete. Static site in $(DOWNLOAD_DIR)"

gh-pages:
	cd $(DOWNLOAD_DIR) && touch .nojekyll && git init && git add . && git commit -m "update" && git branch -M main && git remote add origin https://github.com/SVis760/dash-plotly-githubpages.git && git push -f origin main

teardown-python:
	pkill -f python || echo "No Python process found"

run_app:
	# Ensure necessary directories exist
	mkdir -p pages_files
	mkdir -p pages_files/assets
	mkdir -p pages_files/pages  # Ensure Dash Pages are copied
	\
	# Start the Dash app in the background and capture its PID
	python3 app.py & APP_PID=$$! ; \
	\
	# Poll for the _dash-layout endpoint until it’s available (max 60 seconds)
	for i in {1..30}; do \
	    CONTENT=$$(wget -qO- http://127.0.0.1:8050/dash-plotly-githubpages/_dash-layout); \
	    if echo "$$CONTENT" | grep -q "{" ; then \
	        echo "Dash app is ready."; \
	        break; \
	    fi; \
	    echo "Waiting for Dash app to be ready..."; \
	    sleep 2; \
	done ; \
	\
	# Download necessary Dash-generated static files directly into pages_files/
	wget -O pages_files/_dash-layout.json http://127.0.0.1:8050/dash-plotly-githubpages/_dash-layout || (echo "Failed to download _dash-layout"; exit 1) ; \
	if [ ! -s pages_files/_dash-layout.json ]; then \
	    echo "Downloaded _dash-layout.json is empty!"; \
	    exit 1; \
	fi ; \
	\
	wget -O pages_files/_dash-dependencies.json http://127.0.0.1:8050/dash-plotly-githubpages/_dash-dependencies || (echo "Failed to download _dash-dependencies"; exit 1) ; \
	if [ ! -s pages_files/_dash-dependencies.json ]; then \
	    echo "Downloaded _dash-dependencies.json is empty!"; \
	    exit 1; \
	fi ; \
	\
	# Copy Dash Pages so they are included in the build
	cp -r pages pages_files/pages || echo "No pages directory found, skipping." ; \
	\
	# (Any additional processing, such as sed path fixes, goes here)
	\
	# Kill the running Dash app process cleanly using the captured PID
	kill $$APP_PID || echo "No running Dash app found."

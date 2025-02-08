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
	    if wget -q --spider http://127.0.0.1:8050/dash-plotly-githubpages/_dash-layout; then \
	        echo "Dash app is ready."; \
	        break; \
	    fi; \
	    echo "Waiting for Dash app to be ready..."; \
	    sleep 2; \
	done ; \
	\
	# Download necessary Dash-generated static files directly into pages_files/
	wget -q -O pages_files/_dash-layout.json http://127.0.0.1:8050/dash-plotly-githubpages/_dash-layout || (echo "Failed to download _dash-layout"; exit 1) ; \
	wget -q -O pages_files/_dash-dependencies.json http://127.0.0.1:8050/dash-plotly-githubpages/_dash-dependencies || (echo "Failed to download _dash-dependencies"; exit 1) ; \
	\
	# Copy Dash Pages so they are included in the build
	cp -r pages pages_files/pages || echo "No pages directory found, skipping." ; \
	\
	# Only process files if pages_files is not empty
	if [ -d "pages_files" ] && [ "$$(ls -A pages_files 2>/dev/null)" ]; then \
	    find pages_files -type f -exec sed -i.bak 's|_dash-component-suites|dash-plotly-githubpages/_dash-component-suites|g' {} \; && \
	    find pages_files -type f -exec sed -i.bak 's|_dash-layout|dash-plotly-githubpages/_dash-layout.json|g' {} \; && \
	    find pages_files -type f -exec sed -i.bak 's|_dash-dependencies|dash-plotly-githubpages/_dash-dependencies.json|g' {} \; && \
	    find pages_files -type f -exec sed -i.bak 's|_reload-hash|dash-plotly-githubpages/_reload-hash|g' {} \; && \
	    find pages_files -type f -exec sed -i.bak 's|_dash-update-component|dash-plotly-githubpages/_dash-update-component|g' {} \; && \
	    find pages_files -type f -exec sed -i.bak 's|assets|dash-plotly-githubpages/assets|g' {} \; ; \
	else \
	    echo "Warning: pages_files is empty or missing, skipping path fixes."; \
	fi ; \
	\
	# Kill the running Dash app process cleanly using the captured PID
	kill $$APP_PID || echo "No running Dash app found."

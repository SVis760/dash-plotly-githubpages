run_app:
	# Ensure necessary directories exist
	mkdir -p pages_files
	mkdir -p pages_files/assets

	# Start the Dash app and wait for it to fully start
	python3 app.py & sleep 60

	# Download necessary Dash-generated static files directly into `pages_files/`
	wget -q -O pages_files/_dash-layout.json http://127.0.0.1:8050/_dash-layout
	wget -q -O pages_files/_dash-dependencies.json http://127.0.0.1:8050/_dash-dependencies

	# Download component files while removing "127.0.0.1:8050/" from the directory structure
	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-graph.js
	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-highlight.js
	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-markdown.js
	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dcc/async-datepicker.js

	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-table.js
	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/dash/dash_table/async-highlight.js

	wget -r -np -nH --cut-dirs=1 -P pages_files http://127.0.0.1:8050/_dash-component-suites/plotly/package_data/plotly.min.js

	# Ensure correct directory structure
	ls -a pages_files
	ls -a pages_files/assets

	# Fix file paths inside the downloaded files to match GitHub Pages structure
	find pages_files -type f -exec sed -i.bak 's|_dash-component-suites|dash-plotly-githubpages/_dash-component-suites|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-layout|dash-plotly-githubpages/_dash-layout.json|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-dependencies|dash-plotly-githubpages/_dash-dependencies.json|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_reload-hash|dash-plotly-githubpages/_reload-hash|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|_dash-update-component|dash-plotly-githubpages/_dash-update-component|g' {} \;
	find pages_files -type f -exec sed -i.bak 's|assets|dash-plotly-githubpages/assets|g' {} \;

	# Move assets to the correct directory
	mv assets/* pages_files/assets/ || true  # Ignore errors if assets are already in place

	# Kill the running Dash app process cleanly
	kill $(ps -C python -o pid=) || true

clean_dirs:
	# Remove temporary directories
	rm -rf 127.0.0.1:8050/
	rm -rf pages_files/
	rm -rf joblib

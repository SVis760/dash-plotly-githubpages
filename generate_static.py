import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import request
from app import app  # Import your Dash app

# Function to stop the Flask server after rendering
def shutdown_server():
    """Send a shutdown request to the Flask server."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func:
        func()

def run_dash():
    """Run the Dash app in a separate thread."""
    app.run_server(debug=False, port=8050, use_reloader=False)

def save_static_html():
    """Launch Dash app, visit it with Selenium, and save the page as HTML."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Automatically install Chrome and ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Start the Dash app in a separate thread
        server_thread = threading.Thread(target=run_dash)
        server_thread.daemon = True  # Allows the script to exit when done
        server_thread.start()

        # Wait for the server to start
        time.sleep(5)

        # Ensure 'static' directory exists
        os.makedirs("static", exist_ok=True)

        # Visit the page and save it
        driver.get("http://127.0.0.1:8050")
        with open("static/index.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Send shutdown request
        shutdown_server()

    finally:
        driver.quit()

if __name__ == "__main__":
    save_static_html()

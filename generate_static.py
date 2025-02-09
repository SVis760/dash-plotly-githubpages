import os
import time
import threading
import signal
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from app import app  # Import your Dash app

# Global variable to store the Flask thread
server_thread = None

def run_dash():
    """Run the Dash app in a separate thread."""
    app.run_server(debug=False, port=8050, use_reloader=False)

def stop_dash():
    """Stop the Dash app by sending a SIGINT (CTRL+C)."""
    global server_thread
    if server_thread:
        print("Stopping Dash app...")
        os.kill(os.getpid(), signal.SIGINT)  # Simulate CTRL+C to stop Flask

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
        global server_thread
        server_thread = threading.Thread(target=run_dash)
        server_thread.daemon = True  # Allows script to exit
        server_thread.start()

        # Wait for the server to start
        time.sleep(5)

        # Ensure 'static' directory exists
        os.makedirs("static", exist_ok=True)

        # Visit the page and save it
        driver.get("http://127.0.0.1:8050")
        with open("static/index.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

    finally:
        driver.quit()
        stop_dash()  # Stop the Dash app after saving

if __name__ == "__main__":
    save_static_html()

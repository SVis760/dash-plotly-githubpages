from playwright.sync_api import sync_playwright
import time

# Define the URL of your locally running Dash app
URL = "http://127.0.0.1:8050/dash-plotly-githubpages/"

def capture_snapshot():
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to the Dash app and wait until network is idle
        page.goto(URL, wait_until="networkidle")
        
        # Optional: wait for a specific selector to ensure data is rendered (e.g., your data table)
        page.wait_for_selector("#data-table", timeout=60000)
        
        # Give extra time if needed
        time.sleep(2)

        # Get the page's HTML content
        html = page.content()
        
        # Save the HTML snapshot to a file
        with open("static_index.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        browser.close()
        print("Snapshot saved as static_index.html")

if __name__ == "__main__":
    capture_snapshot()

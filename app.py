from dash import Dash, html, dcc
import dash
import plotly.express as px

px.defaults.template = "ggplot2"

# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
# app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

app = Dash(__name__, pages_folder='pages', use_pages=True,  suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Br(),
    # html.P('testing multiple pages', classname='text-dark'),
    html.Div(children=[
        dcc.Link(page['name'], href=page['relative_path'])\
            for page in dash.page_registry.values()]
    ),
    dash.page_container
])

if __name__== '__main__':
    app.run(debug=True)


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def save_static_html():
    """Launch Dash app and take a static snapshot."""
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        app.run_server(debug=False, port=8050, use_reloader=False)
        driver.get("http://127.0.0.1:8050")
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    save_static_html()

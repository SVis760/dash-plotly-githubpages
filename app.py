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

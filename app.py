from dash import Dash, html, dcc
import dash
import plotly.express as px

px.defaults.template = "ggplot2"

app = Dash(
    __name__,
    pages_folder="pages",
    use_pages=True,
    suppress_callback_exceptions=True,
    requests_pathname_prefix="/dash-plotly-githubpages/"  # Set this to match your repo
)

app.layout = html.Div([
    html.Br(),
    html.Div(children=[
        dcc.Link(page["name"], href=page["relative_path"])\
            for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=False)

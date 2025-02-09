from dash import Dash, dcc, html, dash_table, Input, Output
import dash
import plotly.express as px
import json

px.defaults.template = "ggplot2"

app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           requests_pathname_prefix="/dash-plotly-githubpages/")

# Import your page module (it should register itself)
import pages.kwaliteitsanalyse
# Import the merged dataframe from your page module.
from pages.kwaliteitsanalyse import merged_df

# Modify the main layout to include a dcc.Store.
app.layout = html.Div([
    # This store makes the full dataset available to the clientside callback.
    dcc.Store(id="store-data", data=merged_df.to_dict("records")),
    html.Br(),
    html.Div(children=[
        dcc.Link(page["name"], href=page["relative_path"])
        for page in dash.page_registry.values()
    ]),
    dash.page_container
])

# Register the clientside callback (it now finds the "store-data" component).
app.clientside_callback(
    """
    function(storeData, dropdown1) {
        var filtered = storeData;
        if (dropdown1) {
            filtered = filtered.filter(function(row) {
                return row["prefLabelLaag1"] === dropdown1;
            });
        }
        return filtered;
    }
    """,
    Output("data-table", "data"),
    [Input("store-data", "data"),
     Input("dropdown-1", "value")]
)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)

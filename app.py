from dash import Dash, dcc, html, dash_table, Input, Output
import dash
import plotly.express as px

px.defaults.template = "ggplot2"

app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           requests_pathname_prefix="/dash-plotly-githubpages/")

# Import your page modules (which should register themselves via dash.register_page)
import pages.kwaliteitsanalyse

# Register a clientside callback that filters data from a dcc.Store
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

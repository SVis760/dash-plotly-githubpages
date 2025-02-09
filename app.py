from dash import Dash, dcc, html, dash_table
import dash
import plotly.express as px

px.defaults.template = "ggplot2"


app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           requests_pathname_prefix="/dash-plotly-githubpages/")

import pages.kwaliteitsanalyse

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
    app.run(debug=False)

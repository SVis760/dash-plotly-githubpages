from dash import Dash, dcc, html, dash_table, Input, Output
import dash
import plotly.express as px
import pandas as pd

px.defaults.template = "ggplot2"

# Create the app instance
app = Dash(__name__,
           use_pages=True,
           suppress_callback_exceptions=True,
           requests_pathname_prefix="/dash-plotly-githubpages/")

# Import your page module(s) so that they register themselves.
# It is assumed that your page module performs data processing and makes available a DataFrame.
import pages.kwaliteitsanalyse

# For this example, we assume that pages.kwaliteitsanalyse defines a variable named merged_df.
# (If not, adjust accordingly. You might alternatively load your data here.)
# For instance:
# from pages.kwaliteitsanalyse import merged_df

# Define the main layout. Here we add a dcc.Store to hold the data so that it is available to clientside callbacks.
app.layout = html.Div([
    # dcc.Store holds the full dataset. Adjust the data source as needed.
    dcc.Store(id="store-data", data=pages.kwaliteitsanalyse.merged_df.to_dict("records")),
    
    # Navigation links (optional) and page container.
    html.Div([
        # Create a navigation menu from the registered pages.
        html.Div([dcc.Link(page["name"], href=page["relative_path"]) 
                  for page in dash.page_registry.values()])
    ]),
    # The page container will render the layout for the current page.
    dash.page_container
])

# Register a clientside callback that filters the stored data based on the first dropdown's selection.
# Make sure that your page layout (from pages.kwaliteitsanalyse) includes:
#   - a DataTable with id "data-table"
#   - a Dropdown with id "dropdown-1"
app.clientside_callback(
    """
    function(storeData, dropdown1) {
        // storeData is the array of data records stored in dcc.Store.
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

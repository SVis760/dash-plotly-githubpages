app = dash.get_app()  # Get the current Dash app instance

app.clientside_callback(
    """
    function(storeData, dropdown1) {
        // storeData is an array of objects representing your data
        var filtered = storeData;
        // If a value is selected in dropdown-1, filter by the corresponding column.
        if (dropdown1) {
            filtered = filtered.filter(function(row) {
                return row["prefLabelLaag1"] === dropdown1;
            });
        }
        return filtered;
    }
    """,
    dash.Output("data-table", "data"),
    [dash.Input("store-data", "data"),
    dash.Input("dropdown-1", "value")]
)

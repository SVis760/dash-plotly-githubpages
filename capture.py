from dash import Dash, html, dcc, dash_table
import dash
import json

app = Dash(__name__, 
           pages_folder="pages",
           use_pages=True,
           suppress_callback_exceptions=True,
           requests_pathname_prefix="/your-repo-name/")

app.layout = html.Div([
    dcc.Input(id='my-input', value='initial value'),
    html.Div(id='my-output')
])

# Clientside callback
app.clientside_callback(
    """
    function(input_value) {
        // Do something in JavaScript.
        return "You entered: " + input_value;
    }
    """,
    dash.Output('my-output', 'children'),
    [dash.Input('my-input', 'value')]
)

if __name__ == '__main__':
    app.run(debug=False)

# app.py
from dash import Dash, html, dcc, Input, Output, State, ClientsideFunction
import dash

APP_PORT = 8050  # Port on which the app will run

# Initialize the Dash app with multi-page support.
app = Dash(__name__, pages_folder='pages', use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Br(),
    # Navigation links automatically generated from dash.page_registry
    html.Div(children=[
        dcc.Link(page['name'], href=page['relative_path'])
        for page in dash.page_registry.values()
    ]),
    dash.page_container
])

# Clientside callback for updating dropdown options and display styles.
app.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='updateDropdowns'),
    output=[
        Output('dropdown-2', 'options'),
        Output('div-dropdown-2', 'style'),
        Output('dropdown-3', 'options'),
        Output('div-dropdown-3', 'style'),
        # (Add additional outputs if you have more dropdowns)
    ],
    inputs=[Input(f'dropdown-{i}', 'value') for i in range(1, 12)],
    state=[State('store', 'data')]
)

# Clientside callback for updating the data table based on dropdown selections.
app.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='updateDataTable'),
    output=Output('data-table', 'data'),
    inputs=[Input(f'dropdown-{i}', 'value') for i in range(1, 12)],
    state=[State('store', 'data')]
)

if __name__ == '__main__':
    app.run(debug=True, port=APP_PORT)

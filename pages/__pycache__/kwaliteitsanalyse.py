# pages/kwaliteitsanalyse.py
import dash
from dash import dcc, html, dash_table
from data_processing import process_data

# Register the page.
dash.register_page(__name__, path='/', name='Missing ScopeNotes CHT')

# Process data (this happens at build time so the rendered HTML includes your data).
filtered_df = process_data()

# Convert the processed DataFrame to JSON for clientside use.
filtered_df_json = filtered_df.to_json(orient='records')

max_level = 11

# Create the initial dropdown (for prefLabelLaag1).
dropdown_divs = [
    html.Div([
        html.Label("Selecteer Top Concept:"),
        dcc.Dropdown(
            id="dropdown-1",
            options=[{'label': x, 'value': x}
                     for x in sorted(filtered_df["prefLabelLaag1"].dropna().unique())],
            placeholder="Selecteer top concept"
        )
    ], style={'width': '100%', 'padding': '10px'})
]

# Create additional dropdowns (initially hidden).
for i in range(2, max_level + 1):
    dropdown_divs.append(
        html.Div([
            html.Label(f"Select prefLabelLaag{i}:"),
            dcc.Dropdown(id=f"dropdown-{i}", placeholder=f"Selecteer concept {i}")
        ], id=f"div-dropdown-{i}", style={'width': '100%', 'padding': '10px', 'display': 'none'})
    )

layout = html.Div([
    html.H1("Dashboard Datakwaliteit Cultuurhistorische Thesaurus Concepten"),
    html.Div([
        html.Div(dropdown_divs + [
            html.H2("Samenvatting geselecteerde concept"),
            html.Div(id="summary-div")
        ], style={'width': '33%', 'padding': '10px'}),
        html.Div([
            html.H2("Tabel weergave"),
            dash_table.DataTable(
                id="data-table",
                columns=[{'name': col, 'id': col} for col in filtered_df.columns],
                data=filtered_df.to_dict("records"),
                page_size=10,
                filter_action="native",
                sort_action="native",
            )
        ], style={'width': '67%', 'padding': '10px'})
    ], style={'display': 'flex'}),
    # Store the processed data for use in clientside callbacks.
    dcc.Store(id='store', data=filtered_df_json)
], style={'padding': '20px'})

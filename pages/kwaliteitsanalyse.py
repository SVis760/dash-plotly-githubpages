import json
import dash
from dash import dcc, html, dash_table

dash.register_page(__name__, path='/', name='Missing ScopeNotes CHT')

# Load preprocessed JSON
with open("assets/processed_data.json", "r", encoding="utf-8") as f:
    filtered_df_json = json.load(f)

layout = html.Div([
    html.H1("Dashboard Datakwaliteit Cultuurhistorische Thesaurus Concepten"),
    dcc.Store(id='store', data=filtered_df_json),
    dash_table.DataTable(
        id="data-table",
        columns=[{'name': col, 'id': col} for col in filtered_df_json[0].keys()],
        data=filtered_df_json,
        page_size=10,
        filter_action="native",
        sort_action="native"
    )
], style={'padding': '20px'})

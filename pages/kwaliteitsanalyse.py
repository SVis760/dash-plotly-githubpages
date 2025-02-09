import requests
import json
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

# Register this module as a page.
dash.register_page(__name__, path='/', name='Missing ScopeNotes CHT')

# ----------------------
# Data fetching and processing
# ----------------------
def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Define your URLs
urls = [
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/topTerm/2/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote01/18/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote02/34/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote03/35/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote04/20/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote05/17/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote06/13/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote07/15/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote08/17/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote09/14/run?pageSize=10000",
    "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote10/8/run?pageSize=10000"
]

# Fetch data for each URL and store in a list
data_list = [fetch_data(url) for url in urls]

# Convert each fetched data into a DataFrame and store in a list
dfs = [pd.DataFrame(data) for data in data_list]

# Rename column in the first DataFrame (if needed)
dfs[0].rename(columns={'topTermLabel': 'prefLabelLaag1'}, inplace=True)

# Merge the DataFrames using the specified keys
merge_keys = [
    'prefLabelLaag1','prefLabelLaag2','prefLabelLaag3','prefLabelLaag4',
    'prefLabelLaag5','prefLabelLaag6','prefLabelLaag7','prefLabelLaag8',
    'prefLabelLaag9','prefLabelLaag10'
]

merged_df = dfs[0]
for i in range(len(merge_keys)):
    suffix_left = f"_df{i+1}"
    suffix_right = f"_df{i+2}"
    merged_df = pd.merge(
        merged_df,
        dfs[i+1],
        on=merge_keys[i],
        how='outer',
        suffixes=(suffix_left, suffix_right)
    )

# Convert specified columns to numeric
colsAantalNarrower = [
    'aantalNarrowerZonderScopeNote_df2','aantalNarrowerZonderScopeNote_df3',
    'aantalNarrowerZonderScopeNote_df4','aantalNarrowerZonderScopeNote_df5',
    'aantalNarrowerZonderScopeNote_df6','aantalNarrowerZonderScopeNote_df7',
    'aantalNarrowerZonderScopeNote_df8','aantalNarrowerZonderScopeNote_df9',
    'aantalNarrowerZonderScopeNote_df10'
]
merged_df[colsAantalNarrower] = merged_df[colsAantalNarrower].apply(pd.to_numeric, errors='coerce')

# Filter the merged data using paired columns
paired_columns = [
    ('mistEigenScopeNote_df2','aantalNarrowerZonderScopeNote_df2'),
    ('mistEigenScopeNote_df3','aantalNarrowerZonderScopeNote_df3'),
    ('mistEigenScopeNote_df4','aantalNarrowerZonderScopeNote_df4'),
    ('mistEigenScopeNote_df5','aantalNarrowerZonderScopeNote_df5'),
    ('mistEigenScopeNote_df6','aantalNarrowerZonderScopeNote_df6'),
    ('mistEigenScopeNote_df7','aantalNarrowerZonderScopeNote_df7'),
    ('mistEigenScopeNote_df8','aantalNarrowerZonderScopeNote_df8'),
    ('mistEigenScopeNote_df9','aantalNarrowerZonderScopeNote_df9'),
    ('mistEigenScopeNote_df10','aantalNarrowerZonderScopeNote_df10'),
    ('mistEigenScopeNote_df11','aantalNarrowerZonderScopeNote_df11')
]
filtered_df = merged_df[~merged_df.apply(
    lambda row: any(
        (row[pair[0]]==0 and row[pair[1]]=='nee') or (row[pair[1]]==0 and row[pair[0]]=='nee')
        for pair in paired_columns
    ), axis=1
)]

max_level = 11

# ----------------------
# Build the Page Layout
# ----------------------
layout = html.Div([
    # Store the complete merged data (this is what our clientside callbacks can use)
    dcc.Store(id="store-data", data=merged_df.to_dict("records")),
    
    html.H1("Dashboard Datakwaliteit Cultuurhistorische Thesaurus Concepten"),
    html.Div([
        # Left column: dropdowns and summary
        html.Div([
            html.Div([
                html.Label("Selecteer Top Concept:"),
                dcc.Dropdown(
                    id="dropdown-1",
                    options=[{'label': x, 'value': x} 
                             for x in sorted(filtered_df["prefLabelLaag1"].dropna().unique())],
                    placeholder="Selecteer top concept"
                )
            ], style={'width': '100%', 'padding': '10px'}),
            html.H2("Samenvatting geselecteerde concept"),
            html.Div(id="summary-div")
        ], style={'width': '33%', 'padding': '10px'}),
        
        # Right column: data table
        html.Div([
            html.H2("Tabel weergave"),
            dash_table.DataTable(
                id="data-table",
                columns=[{'name': col, 'id': col} for col in merged_df.columns],
                # Initially, the data is empty; it will be updated via callbacks.
                page_size=10,
                filter_action="native",
                sort_action="native"
            )
        ], style={'width': '67%', 'padding': '10px'})
    ], style={'display': 'flex'})
], style={'padding': '20px'})

# ----------------------
# Callbacks (server-side)
# ----------------------
# Dropdown update callback (server-side example)
input_ids = [Input(f"dropdown-{i}", "value") for i in range(1, max_level+1)]
output_list = []
for i in range(2, max_level+1):
    output_list.append(Output(f"dropdown-{i}", "options"))
    output_list.append(Output(f"div-dropdown-{i}", "style"))

@dash.callback(output_list, input_ids)
def update_dropdowns(*vals):
    outputs = []
    for i in range(2, max_level+1):
        # Ensure all previous dropdowns have a selection.
        valid = all(vals[j] is not None for j in range(i-1))
        if not valid:
            outputs.append([])
            outputs.append({'width': '100%', 'padding': '10px', 'display': 'none'})
        else:
            df_local = merged_df.copy()
            for j in range(1, i):
                df_local = df_local[df_local[f"prefLabelLaag{j}"] == vals[j-1]]
            options = [{'label': x, 'value': x} 
                       for x in sorted(df_local[f"prefLabelLaag{i}"].dropna().unique())]
            outputs.append(options)
            outputs.append({'width': '100%', 'padding': '10px', 'display': 'block'})
    return outputs

@dash.callback(Output("summary-div", "children"),
               [Input(f"dropdown-{i}", "value") for i in range(1, max_level+1)])
def update_summary(*vals):
    deepest = 0
    for i, v in enumerate(vals, start=1):
        if v is not None:
            deepest = i
        else:
            break
    if deepest == 0:
        return "Geen selectie gemaakt."
    df_local = filtered_df.copy()
    for i in range(1, deepest+1):
        df_local = df_local[df_local[f"prefLabelLaag{i}"] == vals[i-1]]
    summary_cols = (["prefLabelLaag1", "countWithoutScopeNote"] if deepest == 1 
                    else [f"prefLabelLaag{deepest}", f"mistEigenScopeNote_df{deepest}", 
                          f"aantalNarrowerZonderScopeNote_df{deepest}", f"uitklappen_df{deepest}"])
    summary_df = df_local[summary_cols].head(1)
    if summary_df.empty:
        return "No details available for this selection."
    return dash_table.DataTable(
        columns=[{'name': col, 'id': col} for col in summary_df.columns],
        data=summary_df.to_dict("records"),
        style_table={"overflowX": "auto"},
        page_size=1
    )

@dash.callback(Output("data-table", "data"),
               [Input(f"dropdown-{i}", "value") for i in range(1, max_level+1)])
def update_data_table(*vals):
    df_local = merged_df.copy()
    for i, v in enumerate(vals, start=1):
        if v is not None:
            df_local = df_local[df_local[f"prefLabelLaag{i}"] == v]
    return df_local.to_dict("records")


# Optional: Try loading data from a local file for caching purposes.
try:
    with open("data.json", "r") as f:
        _ = json.load(f)
except Exception as e:
    url = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/topTerm/2/run?pageSize=10000"
    data = requests.get(url).json()
    with open("data.json", "w") as f:
        json.dump(data, f)

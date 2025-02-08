import requests, json, pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

dash.register_page(__name__, path='/', name='Missing ScopeNotes CHT')


#----------------------------------------


def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

url1 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/topTerm/2/run?pageSize=10000"
url2 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote01/18/run?pageSize=10000"
url3 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote02/34/run?pageSize=10000"
url4 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote03/35/run?pageSize=10000"
url5 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote04/20/run?pageSize=10000"
url6 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote05/17/run?pageSize=10000"
url7 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote06/13/run?pageSize=10000"
url8 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote07/15/run?pageSize=10000"
url9 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote08/17/run?pageSize=10000"
url10 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote09/14/run?pageSize=10000"
url11 = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/missingscopenote10/8/run?pageSize=10000"
urls = [url1, url2, url3, url4, url5, url6, url7, url8, url9, url10, url11]

for i, url in enumerate(urls, start=1):
    data = fetch_data(url)
    globals()[f"dataLaag{i}"] = data

dfs = ['dataLaag1','dataLaag2','dataLaag3','dataLaag4','dataLaag5','dataLaag6','dataLaag7','dataLaag8','dataLaag9','dataLaag10','dataLaag11']
for i, df in enumerate(dfs, start=1):
    df = pd.DataFrame(globals()[df])
    globals()[f"df{i}"] = df

df1.rename(columns={'topTermLabel': 'prefLabelLaag1'}, inplace=True)
dfs2 = [df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11]
merge_keys = ['prefLabelLaag1','prefLabelLaag2','prefLabelLaag3','prefLabelLaag4','prefLabelLaag5','prefLabelLaag6','prefLabelLaag7','prefLabelLaag8','prefLabelLaag9','prefLabelLaag10']
merged_df = dfs2[0]
for i in range(len(merge_keys)):
    suffix_left = f"_df{i+1}"
    suffix_right = f"_df{i+2}"
    merged_df = pd.merge(merged_df, dfs2[i+1], on=merge_keys[i], how='outer', suffixes=(suffix_left, suffix_right))

colsAantalNarrower = ['aantalNarrowerZonderScopeNote_df2','aantalNarrowerZonderScopeNote_df3','aantalNarrowerZonderScopeNote_df4','aantalNarrowerZonderScopeNote_df5',
                       'aantalNarrowerZonderScopeNote_df6','aantalNarrowerZonderScopeNote_df7','aantalNarrowerZonderScopeNote_df8','aantalNarrowerZonderScopeNote_df9',
                       'aantalNarrowerZonderScopeNote_df10']
merged_df[colsAantalNarrower] = merged_df[colsAantalNarrower].apply(pd.to_numeric, errors='coerce')

paired_columns = [('mistEigenScopeNote_df2','aantalNarrowerZonderScopeNote_df2'),
                    ('mistEigenScopeNote_df3','aantalNarrowerZonderScopeNote_df3'),
                    ('mistEigenScopeNote_df4','aantalNarrowerZonderScopeNote_df4'),
                    ('mistEigenScopeNote_df5','aantalNarrowerZonderScopeNote_df5'),
                    ('mistEigenScopeNote_df6','aantalNarrowerZonderScopeNote_df6'),
                    ('mistEigenScopeNote_df7','aantalNarrowerZonderScopeNote_df7'),
                    ('mistEigenScopeNote_df8','aantalNarrowerZonderScopeNote_df8'),
                    ('mistEigenScopeNote_df9','aantalNarrowerZonderScopeNote_df9'),
                    ('mistEigenScopeNote_df10','aantalNarrowerZonderScopeNote_df10'),
                    ('mistEigenScopeNote_df11','aantalNarrowerZonderScopeNote_df11')]
filtered_df = merged_df[~merged_df.apply(lambda row: any((row[pair[0]]==0 and row[pair[1]]=='nee') or (row[pair[1]]==0 and row[pair[0]]=='nee') for pair in paired_columns), axis=1)]



max_level = 11

# Build the dropdown containers. The first dropdown is visible, the rest are initially hidden. 
# This is for 'object' as the topconcept and the narrower concepts appear as they are chosen from the menu.
dropdown_divs = []
dropdown_divs.append(
    html.Div([
        html.Label("Selecteer Top Concept:"),
        dcc.Dropdown(
            id="dropdown-1",
            options=[{'label': x, 'value': x} 
                     for x in sorted(filtered_df["prefLabelLaag1"].dropna().unique())],
            placeholder="Selecteer top concept"
        )
    ], style={'width': '100%', 'padding': '10px'})
)
for i in range(2, max_level+1):
    dropdown_divs.append(
        html.Div([
            html.Label(f"Select prefLabelLaag{i}:"),
            dcc.Dropdown(
                id=f"dropdown-{i}",
                placeholder=f"Selecteer concept {i}"
            )
        ], id=f"div-dropdown-{i}", style={'width': '100%', 'padding': '10px', 'display': 'none'})
    )

# Layout: left column (33%) for dropdowns and summary; right column (67%) for the data table.
layout = html.Div([
    html.H1("Dashboard Datakwaliteit Cultuurhistorische Thesaurus Concepten"),
    html.Div([
        html.Div(dropdown_divs + [html.H2("Samenvatting geselecteerde concept"), html.Div(id="summary-div")],
                 style={'width': '33%', 'padding': '10px'}),
        html.Div([
            html.H2("Tabel weergave"),
            dash_table.DataTable(
                id="data-table",
                columns=[{'name': col, 'id': col} for col in merged_df.columns],
                data=merged_df.to_dict("records"),
                page_size=10,
                filter_action="native",
                sort_action="native",
                # style_table={'overflowX': 'auto'},
                # style_cell={'whiteSpace': 'normal', 'textAlign': 'left'}
            )
        ], style={'width': '67%', 'padding': '10px'})
    ], style={'display': 'flex'})
], style={'padding': '20px'})

# dropdown update callback.
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

dash_table.DataTable(
    id="data-table",
    columns=[{'name': col, 'id': col} for col in merged_df.columns],
    data=merged_df.to_dict("records"),
    page_size=10,
    filter_action="native",
    sort_action="native",
)

# Try loading data from a local file first
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    # If file doesn't exist, fetch data from API
    url = "https://api.linkeddata.cultureelerfgoed.nl/queries/sablina-vis/topTerm/2/run?pageSize=10000"
    data = requests.get(url).json()

    # Save data for future use
    with open("data.json", "w") as f:
        json.dump(data, f)

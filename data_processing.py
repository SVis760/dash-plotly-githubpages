import os
import pandas as pd
import json
import requests

DATA_PATH = "assets/processed_data.json"

def fetch_data(url):
    """Fetch JSON data from the given URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_data():
    """Fetch, merge, clean, and process the dataset."""
    
    # **Step 1: Load cached data if available (to prevent redundant API calls)**
    if os.path.exists(DATA_PATH):
        print("Using cached data from assets/processed_data.json")
        return pd.read_json(DATA_PATH)

    print("Fetching fresh data...")

    # **Step 2: Define API endpoints for data fetching**
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

    # **Step 3: Fetch all datasets & convert to DataFrames**
    dfs = [pd.DataFrame(fetch_data(url)) for url in urls]

    # **Step 4: Rename first dataset column**
    if not dfs[0].empty and 'topTermLabel' in dfs[0].columns:
        dfs[0].rename(columns={'topTermLabel': 'prefLabelLaag1'}, inplace=True)

    # **Step 5: Define merge keys**
    merge_keys = [
        'prefLabelLaag1', 'prefLabelLaag2', 'prefLabelLaag3', 'prefLabelLaag4',
        'prefLabelLaag5', 'prefLabelLaag6', 'prefLabelLaag7', 'prefLabelLaag8',
        'prefLabelLaag9', 'prefLabelLaag10'
    ]

    # **Step 6: Merge all datasets sequentially**
    merged_df = dfs[0]
    for i in range(1, len(dfs)):
        key = merge_keys[i - 1] if i - 1 < len(merge_keys) else None
        suffix_left = f"_df{i}"
        suffix_right = f"_df{i+1}"
        
        if key and key in merged_df.columns and key in dfs[i].columns:
            merged_df = pd.merge(merged_df, dfs[i], on=key, how='outer', suffixes=(suffix_left, suffix_right))
        else:
            merged_df = pd.merge(merged_df, dfs[i], how='outer')

    # **Step 7: Convert relevant columns to numeric where needed**
    colsAantalNarrower = [
        'aantalNarrowerZonderScopeNote_df2', 'aantalNarrowerZonderScopeNote_df3',
        'aantalNarrowerZonderScopeNote_df4', 'aantalNarrowerZonderScopeNote_df5',
        'aantalNarrowerZonderScopeNote_df6', 'aantalNarrowerZonderScopeNote_df7',
        'aantalNarrowerZonderScopeNote_df8', 'aantalNarrowerZonderScopeNote_df9',
        'aantalNarrowerZonderScopeNote_df10'
    ]
    
    for col in colsAantalNarrower:
        if col in merged_df.columns:
            merged_df[col] = pd.to_numeric(merged_df[col], errors='coerce')

    # **Step 8: Apply row filtering logic**
    paired_columns = [
        ('mistEigenScopeNote_df2', 'aantalNarrowerZonderScopeNote_df2'),
        ('mistEigenScopeNote_df3', 'aantalNarrowerZonderScopeNote_df3'),
        ('mistEigenScopeNote_df4', 'aantalNarrowerZonderScopeNote_df4'),
        ('mistEigenScopeNote_df5', 'aantalNarrowerZonderScopeNote_df5'),
        ('mistEigenScopeNote_df6', 'aantalNarrowerZonderScopeNote_df6'),
        ('mistEigenScopeNote_df7', 'aantalNarrowerZonderScopeNote_df7'),
        ('mistEigenScopeNote_df8', 'aantalNarrowerZonderScopeNote_df8'),
        ('mistEigenScopeNote_df9', 'aantalNarrowerZonderScopeNote_df9'),
        ('mistEigenScopeNote_df10', 'aantalNarrowerZonderScopeNote_df10'),
        ('mistEigenScopeNote_df11', 'aantalNarrowerZonderScopeNote_df11')
    ]

    def row_valid(row):
        for col1, col2 in paired_columns:
            if col1 in row and col2 in row:
                if (row[col1] == 0 and row[col2] == 'nee') or (row[col2] == 0 and row[col1] == 'nee'):
                    return False
        return True

    filtered_df = merged_df[merged_df.apply(row_valid, axis=1)]

    # **Step 9: Save processed data**
    filtered_df.to_json(DATA_PATH, orient="records", force_ascii=False)
    print(f"Processed data saved to {DATA_PATH}")

    return filtered_df


if __name__ == '__main__':
    processed = process_data()

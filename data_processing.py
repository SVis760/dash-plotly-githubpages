# data_processing.py
import requests
import pandas as pd

def fetch_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def process_data():
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
    
    # Fetch data from each URL and convert to DataFrames.
    dfs = [pd.DataFrame(fetch_data(url)) for url in urls]
    
    # Rename a column in the first DataFrame.
    if not dfs[0].empty and 'topTermLabel' in dfs[0].columns:
        dfs[0].rename(columns={'topTermLabel': 'prefLabelLaag1'}, inplace=True)
    
    # Define merge keys for sequential merging.
    merge_keys = [
        'prefLabelLaag1', 'prefLabelLaag2', 'prefLabelLaag3', 'prefLabelLaag4',
        'prefLabelLaag5', 'prefLabelLaag6', 'prefLabelLaag7', 'prefLabelLaag8',
        'prefLabelLaag9', 'prefLabelLaag10'
    ]
    
    merged_df = dfs[0]
    for i in range(1, len(dfs)):
        if i - 1 < len(merge_keys):
            key = merge_keys[i - 1]
            suffix_left = f"_df{i}"
            suffix_right = f"_df{i+1}"
            merged_df = pd.merge(merged_df, dfs[i], on=key, how='outer',
                                 suffixes=(suffix_left, suffix_right))
        else:
            merged_df = pd.merge(merged_df, dfs[i], how='outer')
    
    # Convert numeric columns if present.
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
    
    # Filter rows based on paired column conditions.
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
    return filtered_df

if __name__ == '__main__':
    processed = process_data()
    processed.to_json("assets/processed_data.json", orient="records", force_ascii=False)
    print("Processed data saved to assets/processed_data.json")

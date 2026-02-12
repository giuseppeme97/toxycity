import pandas as pd
import re

def get_n_rows(df):    
    return len(df)
    
def get_columns(df):
    return df.columns.tolist()

def extract_drug(input_string: str):
    return " - ".join(re.findall(r'\[([A-Z ,]+)\]', input_string))

def extract_hystology(input_string: str):
    istologia_match = re.search(r'\(S - (.*?) - ', input_string)
    return istologia_match.group(1) if istologia_match else None

def merge_reactions(df):
    my_column = 'Reaction List PT (Duration – Outcome - Seriousness Criteria)'
    df = df.copy()

    group_id = df['ID'].notna().cumsum()
    df_valid_notes = df[df[my_column].notna()].copy()

    merged_notes = (
        df_valid_notes
        .groupby(group_id)[my_column]
        .agg(lambda x: ' '.join(x.astype(str)))
    )

    result = df[df['ID'].notna()].copy()
    result[my_column] = merged_notes.values
    return result



if __name__ == "__main__":
    df = pd.read_excel("dataset.xlsx")
    # favorite_columns = ['ID', 'AGE', 'GENDER', 'HYSTOPATHOLOGY', 'COMBO', 'DRUG', 'Reaction List PT (Duration – Outcome - Seriousness Criteria)']
    # print(df[['ID', 'Reaction List PT (Duration – Outcome - Seriousness Criteria)']].head(30))

    # print("Numero righe iniziali: ", get_n_rows(df))

    # different_rows1 = (~df["HYSTOPATHOLOGY"].eq(df["DRUG"])).sum()
    # different_rows2 = df["ID"].isna().sum()
    # print("Righe vuote: ", different_rows1, different_rows2)
    
    merged_df = merge_reactions(df)
    # print("Numero righe dopo merge: ", get_n_rows(merged_df))

    merged_df["HYSTOPATHOLOGY"] = merged_df["HYSTOPATHOLOGY"].apply(extract_hystology)
    merged_df["DRUG"] = merged_df["DRUG"].apply(extract_drug)

    # print("Numero righe dopo extraction: ", get_n_rows(merged_df))
    
    merged_df.to_excel("output.xlsx")





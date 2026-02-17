import pandas as pd
import re
import json

def get_n_rows(df):    
    return len(df)
    
def get_columns(df):
    return df.columns.tolist()

def extract_drugs(input_string: str):
    drugs_list = " - ".join(re.findall(r'\[([A-Z ,]+)\]', input_string))
    return drugs_list

def extract_hystology(input_string: str):
    hystology = re.search(r'\(S - (.*?) - ', input_string)
    return hystology.group(1) if hystology else None

def extract_PT(input_string: str):
    pattern = r'\s*([^,(]+?)\s*\('
    PT_list = re.findall(pattern, input_string)    
    PT_list = [p.strip() for p in PT_list]
    return PT_list

def merge_PT(df):
    pt_column = 'Reaction List PT (Duration – Outcome - Seriousness Criteria)'
    df = df.copy()

    group_id = df['ID'].notna().cumsum()
    df_valid_notes = df[df[pt_column].notna()].copy()

    merged_toxicities = (
        df_valid_notes
        .groupby(group_id)[pt_column]
        .agg(lambda x: ' '.join(x.astype(str)))
    )

    result_df = df[df['ID'].notna()].copy()
    result_df[pt_column] = merged_toxicities.values
    return result_df

def map_PT_to_SOC(PT: str):
    pt_soc_df = pd.read_excel("mapping_PT2SOC.xlsx")
    mask = pt_soc_df["Preferred Term"].astype(str).str.contains(PT, na=False)
    
    if mask.any():
        return pt_soc_df.loc[mask, "System Organ Class"].iloc[0]
    else:
        return None    
    
def map_SOC_to_colum(SOC: str):
    with open('categorie_soc.json') as json_file:
        data = json.load(json_file)
        return data[SOC]


def delete_PT_column(df):
    pass


if __name__ == "__main__":
    main_df = pd.read_excel("dataset 2024 corretto.xlsx")
    pt_soc_df = pd.read_excel("mapping_PT2SOC.xlsx")    

    print(pt_soc_df.head(10))


    # print("Numero righe iniziali: ", get_n_rows(df))
    # different_rows1 = (~df["HYSTOPATHOLOGY"].eq(df["DRUG"])).sum()
    # different_rows2 = df["ID"].isna().sum()
    # print("Righe vuote: ", different_rows1, different_rows2)
    
    # ---------- FASE DI MERGING DELLE TOXICITIES ED ESTRAZIONE DELLE ISTOPATOLOGIE E DELLE DRUGS ----------- #
    # merged_main_df = merge_toxicities(main_df)
    # # print("Numero righe dopo merge: ", get_n_rows(merged_df))
    # merged_main_df["HYSTOPATHOLOGY"] = merged_main_df["HYSTOPATHOLOGY"].apply(extract_hystology)
    # merged_main_df["DRUG"] = merged_main_df["DRUG"].apply(extract_drugs)
    # # print("Numero righe dopo extraction: ", get_n_rows(merged_df))
    # merged_main_df.to_excel("output.xlsx")
    # ------------------------------------------------------------------------------------------------------- #





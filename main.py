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

def extract_PTs(input_string: str):
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

def set_all_zero_SOC(df):
    soc_columns = [
        "1 Blood and lymphatic system disorders",
        "2 Cardiac disorders",
        "3 Congenital, familial and genetic disorders",
        "4 Ear and labyrinth disorders",
        "5 endocrine disorders",
        "6 eye disorders",
        "7 gastro intestinal disorders",
        "8 General disorders and administration site conditions",
        "9 Hepatobiliary disorders",
        "10 immune system disorders",
        "11 Infections and infestations",
        "12 Injury, poisoning and procedural complications",
        "13 investigations",
        "14 Metabolism and nutrition disorders",
        "15 Musculoskeletal and connective tissue disorders",
        "16 Neoplasms benign, malignant and unspecified (incl cysts and polyps)",
        "17 Nervous system disorders",
        "18 Psychiatric disorders",
        "19 Renal and urinary disorders",
        "24 Reproductive system and breast disorders ",
        "20 Respiratory, thoracic and mediastinal disorders",
        "21 Skin and subcutaneous tissue disorders",
        "25 Social circumstances",
        "22 Surgical and medical procedures",
        "23 vascular disorders",
        "26 Pregnancy, puerperium and perinatal conditions"
    ]
    df[soc_columns] = 0

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
        if SOC in data:
            return data[SOC]
        else:
            return None


def delete_PT_column(df):
    pass


if __name__ == "__main__":
    main_df = pd.read_excel("output 20260218-1.xlsx")

    # ---------- FASE DI CATEGORIZZAZIONE DELLE PT ----------- #
    pt_column = "Reaction List PT (Duration - Outcome - Seriousness Criteria)"
    
    for index, row in main_df.iterrows():
        pt_list = extract_PTs(row[pt_column])
        print(f"Row {index} - PTs: {pt_list}")
        for PT in pt_list:
            soc = map_PT_to_SOC(PT)
            soc_column = map_SOC_to_colum(soc) if soc else None
            if soc_column:
                # row[soc_column] = 1
                main_df.loc[index, soc_column] = 1

    main_df.to_excel("output.xlsx")
    # -------------------------------------------------------- #

    # ---------- CONTROLLO NUMERO RIGHE ----------- #
    # print("Numero righe iniziali: ", get_n_rows(df))
    # different_rows1 = (~df["HYSTOPATHOLOGY"].eq(df["DRUG"])).sum()
    # different_rows2 = df["ID"].isna().sum()
    # print("Righe vuote: ", different_rows1, different_rows2)
    # --------------------------------------------- #
    
    # ---------- FASE DI MERGING DELLE TOXICITIES ED ESTRAZIONE DELLE ISTOPATOLOGIE E DELLE DRUGS ----------- #
    # merged_main_df = merge_toxicities(main_df)
    # merged_main_df["HYSTOPATHOLOGY"] = merged_main_df["HYSTOPATHOLOGY"].apply(extract_hystology)
    # merged_main_df["DRUG"] = merged_main_df["DRUG"].apply(extract_drugs)
    # merged_main_df.to_excel("output.xlsx")
    # ------------------------------------------------------------------------------------------------------- #





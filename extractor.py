import re
import pandas as pd
import json

def extract_toxicities(testo):
    pattern = r'\s*([^,(]+?)\s*\('
    patologie = re.findall(pattern, testo)    
    patologie = [p.strip() for p in patologie]
    return patologie

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


if __name__ == "__main__":
    stringa = "Acute kidney injury (n/a - Not Recovered/Not Resolved - Other Medically Important Condition), Decreased appetite (n/a - Not Recovered/Not Resolved - Caused/Prolonged Hospitalisation), Immune-mediated dermatitis (n/a - Not Recovered/Not Resolved - Other Medically Important Condition), Malignant neoplasm progression (n/a - Fatal - Results in Death, Other Medically Important Condition), Vomiting (n/a - Not Recovered/Not Resolved - Caused/Prolonged Hospitalisation)"
    toxicities = extract_toxicities(stringa)

    for t in toxicities:
        soc = map_PT_to_SOC(t)
        column = map_SOC_to_colum(soc) if soc else None
        print(f"PT: {t}, SOC: {soc}, Column: {column}")



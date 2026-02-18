import pandas as pd
import re
import json

class Engine:
    def __init__(self, input_dataset, output_dataset):
        self.input_dataset = input_dataset
        self.output_dataset = output_dataset
        self.main_df = pd.read_excel(self.input_dataset)
        self.pt_soc_df = pd.read_excel("mapping_PT2SOC.xlsx")
        self.pts_column = 'Reaction List PT (Duration - Outcome - Seriousness Criteria)'
        
        with open('categorie_soc.json') as json_file:
            self.soc_categories = json.load(json_file)
        
        with open('categorie_istopatologie.json') as json_file:
            self.hystopatologies_categories = json.load(json_file)
        
        self.soc_columns = [
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

    def get_n_rows(self):    
        return len(self.main_df)
    
    def get_columns(self):
        return self.main_df.columns.tolist()
    
    def get_distinct_values(self, column_name):
        if column_name in self.main_df.columns:
            return self.main_df[column_name].dropna().unique().tolist()
        else:
            raise ValueError(f"Colonna non presente nel dataset.")

    def extract_drugs(self, input_string: str):
        drugs = " - ".join(re.findall(r'\[([A-Z ,]+)\]', input_string))
        return drugs

    def extract_hystology(self, input_string: str):
        hystology = re.search(r'\(S - (.*?) - ', input_string)
        return hystology.group(1) if hystology else None

    def extract_pts(self, input_string: str):
        pattern = r'\s*([^,(]+?)\s*\('
        pts = re.findall(pattern, input_string)    
        pts = [p.strip() for p in pts]
        return pts
    
    def map_PT_to_SOC(self, pt: str):
        mask = self.pt_soc_df["Preferred Term"].astype(str).str.contains(pt)
        
        if mask.any():
            return self.pt_soc_df.loc[mask, "System Organ Class"].iloc[0]
        else:
            return None
        
    def map_SOC_to_colum(self, SOC: str):
        if SOC in self.soc_categories:
            return self.soc_categories[SOC]
        else:
            return None
        
    def save_dataset(self):
        self.main_df.to_excel(self.output_dataset, index=False)

    def run_set_all_zero_SOC(self):
        self.main_df[self.soc_columns] = 0

    def run_extract_drug(self):
        self.main_df["DRUG"] = self.main_df["DRUG"].apply(self.extract_drugs)

    def run_map_drug(self):
        pass

    def run_extract_hystopatology(self):
        self.main_df["HYSTOPATHOLOGY"] = self.main_df["HYSTOPATHOLOGY"].apply(self.extract_hystology)

    def run_map_hystopatology(self):
        pass
    
    def run_merge_pts(self):
        tmp_df = self.main_df.copy()
        group_id = tmp_df['ID'].notna().cumsum()
        valid_pts = tmp_df[tmp_df[self.pts_column].notna()].copy()

        merged_pts = (
            valid_pts
            .groupby(group_id)[self.pts_column]
            .agg(lambda x: ' '.join(x.astype(str)))
        )

        result_df = tmp_df[tmp_df['ID'].notna()].copy()
        result_df[self.pts_column] = merged_pts.values
        self.main_df = result_df.copy()

    def run_map_pt(self):
        for index, row in self.main_df.iterrows():
            pts = self.extract_pts(row[self.pts_column])
            # print(f"Row {index}")
            for pt in pts:
                soc = self.map_PT_to_SOC(pt)
                if soc:
                    soc_column = self.map_SOC_to_colum(soc)
                    self.main_df.loc[index, soc_column] = 1
                else:
                    print(f"PT {pt} non mappato.")

    def run_delete_PT_column(self):
        pass


if __name__ == "__main__":
    e = Engine("./dataset/3 - Dataset 2024 (corretto + SOC zero).xlsx", "output.xlsx")
    # print("DRUG: ", len(e.get_distinct_values("DRUG")))
    # print("HYSTOPATHOLOGY: ", len(e.get_distinct_values("HYSTOPATHOLOGY")))

    # ---------- RESET DELLE SOC ----------- #
    # e.run_set_all_zero_SOC()
    # -------------------------------------- #


    # ---------- CATEGORIZZAZIONE DELLE PT ----------- #
    e.run_map_pt()
    # ------------------------------------------------ #


    # ---------- MERGE DELLE PT ----------- #
    # e.run_merge_pt()
    # ------------------------------------- #

    # ---------- ESTRAZIONE DRUGS e HYSTOPATOLOGY ----------- #
    # e.run_extract_drugs()
    # e.run_extract_hystology()
    # ------------------------------------------------------- #

    # e.save_dataset()

    
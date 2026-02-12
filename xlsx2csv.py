import pandas as pd
import sys
import os

def xlsx_to_csv(input_file, output_file=None):
    if not os.path.exists(input_file):
        print("File non trovato.")
        return

    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".csv"

    # Legge il primo foglio
    df = pd.read_excel(input_file)

    # Salva in CSV
    df.to_csv(output_file, index=False, encoding="utf-8")

    print(f"Conversione completata: {output_file}")

if __name__ == "__main__":
    input_path = "dataset.xlsx"
    output_path = "dataset.csv"
    xlsx_to_csv(input_path, output_path)
        

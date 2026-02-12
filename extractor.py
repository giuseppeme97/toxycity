import re

def extractor(input_string: str):
    farmaci = re.findall(r'\[([A-Z ,]+)\]', input_string)
    istologia_match = re.search(r'\(S - (.*?) - ', input_string)
    istologia = istologia_match.group(1) if istologia_match else None

    return " - ".join(farmaci), istologia


if __name__ == "__main__":
    stringa = "PEMBROLIZUMAB [PEMBROLIZUMAB] (S - Non-small cell lung cancer metastatic - Drug withdrawn - [22d - n/a - Intravenous use - More in ICSR]),<BR><BR>PEMETREXED [PEMETREXED, PEMETREXED DISODIUM HEMIPENTAHYDRATE] (S - Non-small cell lung cancer metastatic - Drug withdrawn - [22d - 1000mg - Intravenous use - More in ICSR]),<BR><BR>[CARBOPLATIN] (S - Non-small cell lung cancer metastatic - Drug withdrawn - [22d - 650mg - Intravenous use - More in ICSR]),<BR><BR>[TOBEMSTOMIG] (S - Non-small cell lung cancer metastatic - Drug withdrawn - [22d - n/a - Intravenous use - More in ICSR])"
    (farmaci, istologia) = extractor(stringa)

    print(farmaci)
    print("-----")
    print(istologia)

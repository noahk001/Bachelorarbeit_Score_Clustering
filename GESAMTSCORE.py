import pandas as pd
import glob
import os
from functools import reduce

INPUT_FOLDER = 'Ergebnisse_nach_Feedback'
OUTPUT_FILE = "Gesamtscore_Alle_Files_Neu.csv"

def run_folder_aggregation():
    search_path = os.path.join(INPUT_FOLDER, "*.csv")
    all_files = glob.glob(search_path)
    if not all_files:
        print(f"Keine CSV-Dateien im Ordner '{INPUT_FOLDER}' gefunden!")
        return
    print(f"Gefundene Dateien im Ordner: {len(all_files)}")
    dfs_to_merge = []

    for file_path in all_files:
        file_name = os.path.basename(file_path)
        if file_name == OUTPUT_FILE:
            continue
        try:
            df = pd.read_csv(file_path, sep=';', decimal=',')
            if 'ID' in df.columns:
                score_cols = [c for c in df.columns if 'Score' in c]
                if score_cols:
                    s_col = score_cols[0]
                    col_label = f"Score_{file_name.replace('.csv', '')}"
                    df_temp = df[['ID', s_col]].rename(columns={s_col: col_label})
                    dfs_to_merge.append(df_temp)
                    print(f"  [EINGELESEN] {file_name}")
                else:
                    print(f"  [!] {file_name}: Keine 'Score'-Spalte gefunden. Datei wird ignoriert.")
            else:
                print(f"  [!] {file_name}: Keine 'ID'-Spalte gefunden. Datei wird ignoriert.")

        except Exception as e:
            print(f"  [FEHLER] Konnte {file_name} nicht lesen: {e}")
    if not dfs_to_merge:
        print("Keine gültigen Daten zum Zusammenführen gefunden.")
        return

    df_master = reduce(lambda left, right: pd.merge(left, right, on='ID', how='outer'), dfs_to_merge)
    score_fields = [c for c in df_master.columns if c != 'ID']
    df_master['Gesamtscore'] = df_master[score_fields].mean(axis=1)
    df_master = df_master.sort_values('ID')
    df_master.round(4).to_csv(OUTPUT_FILE, index=False, sep=';', decimal=',')
    print("-" * 40)
    print(f"ERFOLGREICH!")
    print(f"Master-Tabelle erstellt mit {len(df_master)} Probanden.")
    print(f"Speicherort: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    run_folder_aggregation()

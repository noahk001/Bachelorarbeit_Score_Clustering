from calculations import load_and_clean_data, attainment_analysis, run_timing_analysis, attainment_analysis_slope

FILE_IST = '/Users/noahkleinoder/Library/Mobile Documents/com~apple~CloudDocs/Persönliche Unterlagen /Studium/Bachelor DGM/Bachelorarbeit/Bachelorarbeit Noah Kleinöder/data_time.csv'
FILE_SOLL = '/Users/noahkleinoder/Library/Mobile Documents/com~apple~CloudDocs/Persönliche Unterlagen /Studium/Bachelor DGM/Bachelorarbeit/Bachelorarbeit Noah Kleinöder/data_soll.csv'
TIME_COL = 'zeit_min_sec'

ATTAINMENT_TASKS = [
    {'param': 'vo2_l_min', 'soll': 'vo2_max'},
    {'param': 'hr_1_min', 'soll': 'soll_hr'},
    {'param': 'o2puls_ml_beat', 'soll': 'soll_o2_puls'},
    {'param': 'last_w', 'soll': 'soll_watt'},
    {'param': 'vco2_l_min', 'soll': 'soll_vco2_l_min'},
    {'param': 've_l_min', 'soll': 'soll_ve_l_min'},
    {'param': 've_vo2', 'soll': 'soll_ve_vo2'}
]

ATTAINMENT_TASK_SLOPE = [
    {'param': 've_vco2', 'soll': 've_vco2_slope'}
]
TIMING_TASKS = [
    {'param': 'peto2_mm_hg', 'm': 'min', 't': 'VT1', 'f': 'peto2_min_timing.csv'},
    {'param': 'petco2_mm_hg', 'm': 'max', 't': 'VT1', 'f': 'petco2_max_timing.csv'}
]

def main():
    print("Starte Analyse...")
    df_ist, df_soll = load_and_clean_data(FILE_IST, FILE_SOLL)

    for task in ATTAINMENT_TASKS:
        attainment_analysis(df_ist, df_soll, task['param'], task['soll'], f"{task['param']}_attainment.csv")
    for task in ATTAINMENT_TASK_SLOPE:
        attainment_analysis_slope(df_ist, df_soll, task['soll'], task['soll'], f"{task['param']}_attainment_slope.csv")
    for task in TIMING_TASKS:
        run_timing_analysis(df_ist, df_soll, task['param'], task['m'], task['t'], TIME_COL, task['f'])
    print("\nAlle Berechnungen erfolgreich abgeschlossen.")

if __name__ == "__main__":
    main()
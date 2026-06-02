import pandas as pd

def load_and_clean_data(file_ist, file_soll):
    df_ist = pd.read_csv(file_ist, sep=';', decimal=',')
    df_soll = pd.read_csv(file_soll, sep=';', decimal=',')
    df_ist.columns = df_ist.columns.str.strip()
    df_soll.columns = df_soll.columns.str.strip()
    if 'phase' in df_ist.columns:
        df_ist = df_ist[df_ist['phase'] == 'Last'].copy()
    return df_ist, df_soll

def attainment_analysis(df_ist, df_soll, param_name, col_soll, output_name):
    results = []
    for _, row_soll in df_soll.iterrows():
        u_id, soll_wert = row_soll['id'], row_soll[col_soll]
        user_data = df_ist[df_ist['id'] == u_id]
        if not user_data.empty and pd.notna(soll_wert) and soll_wert != 0:
            max_ist = user_data[param_name].max()
            score = min(max_ist / soll_wert, 1.0)
            results.append({'ID': u_id, 'Parameter': param_name, 'Max_Ist': round(max_ist, 2),
                            'Soll': soll_wert, 'Score': round(score, 4)})
    pd.DataFrame(results).to_csv(output_name, index=False, sep=';', decimal=',')

def attainment_analysis_slope(df_ist, df_soll, param_name, col_soll, output_name):
    results = []
    for _, row_soll in df_soll.iterrows():
        u_id = row_soll['id']
        reached_val = row_soll[col_soll]
        if pd.notna(reached_val) and reached_val != 0:
            if 25 <= reached_val <= 30:
                score = 1.0
            else:
                deviation = abs(reached_val - 27.5) / 27.5
                score = max(0.0, 1.0 - deviation)

            results.append({
                'ID': u_id,
                'Parameter': param_name,
                'Reached_Val': round(reached_val, 2),
                'Score': round(score, 4)
            })
    pd.DataFrame(results).to_csv(output_name, index=False, sep=';', decimal=',')

def run_timing_analysis(df_ist, df_soll, param_name, mode, col_target, col_time, output_name):
    results = []
    for _, row_soll in df_soll.iterrows():
        u_id = row_soll['id']
        t_target = row_soll[col_target]
        user_data = df_ist[df_ist['id'] == u_id].sort_values(col_time)
        if not user_data.empty and pd.notna(t_target):
            if mode == 'min':
                t_ist = user_data.loc[user_data[param_name].idxmin(), col_time]
            else:
                t_ist = user_data.loc[user_data[param_name].idxmax(), col_time]
            t_total = user_data[col_time].max() - user_data[col_time].min()
            diff = abs(t_ist - t_target)
            score = max(0, 1 - (diff / t_total)) if t_total > 0 else 0
            results.append({
                'ID': u_id,
                'Parameter': param_name,
                'Modus': mode,
                'Ist_Zeit': round(t_ist, 1),
                'Soll_Zeit': round(t_target, 1),
                'Diff_Sek': round(diff, 1),
                'Score': round(score, 4)
            })
    if results:
        pd.DataFrame(results).to_csv(output_name, index=False, sep=';', decimal=',')


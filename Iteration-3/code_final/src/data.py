import pandas as pd
import os


def read_files(path):
    print('reading data...')
    flow = pd.read_csv(os.path.join(path, "flow.tsv"), na_values=['-'], delimiter="\t", error_bad_lines=False)
    occupancy = pd.read_csv(os.path.join(path, "occupancy.tsv"), na_values=['-'], delimiter="\t", error_bad_lines=False)
    speed = pd.read_csv(os.path.join(path, "speed.tsv"), na_values=['-'], delimiter="\t", error_bad_lines=False)
    prob = pd.read_csv(os.path.join(path, "prob.tsv"), na_values=['-'], delimiter="\t", error_bad_lines=False)
    timestamp = pd.read_csv(os.path.join(path, "timestamp.tsv"), na_values=['-'], delimiter="\t", error_bad_lines=False)

    print('\nsetting up data...')
    columns, flow_cols, occupancy_cols, speed_cols, prob_cols = setup_columns(flow)
    df = pd.concat([flow, occupancy, speed, prob, timestamp], axis=1)
    df.columns = columns

    df_arr = merge_columns(df, flow, flow_cols, occupancy_cols, prob_cols, speed_cols)

    frames = df_arr
    result = pd.concat(frames)
    result.fillna(0, inplace=True)
    result = result.sort_values("timestamp")

    print('\ncleaning data...')
    result = cleanse_data(result)

    print('\ndata preprocessing done...')
    return df, result, flow_cols, prob_cols


def merge_columns(df, flow, flow_cols, occupancy_cols, prob_cols, speed_cols):
    df_arr = []
    for i in range(0, len(flow.columns), 1):
        df_arr.append(pd.DataFrame(
            {
                "flow": df[flow_cols[i]],
                "occupancy": df[occupancy_cols[i]],
                "speed": df[speed_cols[i]],
                "probability": df[prob_cols[i]],
                "timestamp": df.timestamp,
                "detector": "x" + str(i)
            }
        ))
    return df_arr


def cleanse_data(result):
    remove_result1 = result[(result['speed'] < 0)]
    # removeResult2 = result[(result['flow'] == 0) & (result['speed'] > 0)]
    jam_occupancy_threshold = 120
    remove_result3 = result[((result['speed'] == 0) &
                            (result['flow'] == 0) &
                            (result['occupancy'] != 0) &
                            (result['occupancy'] < jam_occupancy_threshold))]
    remove_result5 = result[(result['speed'] == 0) & (result['flow'] != 0) & (result["occupancy"] == 0)]
    remove_result6 = result[
        (pd.isnull(result['speed'])) | (pd.isnull(result['occupancy'])) | (pd.isnull(result['flow']))]
    # removeResult4 = result[(result['speed'] == 0) & (result['flow'] == 0) & (result["occupancy"] == 0)]

    # result = pd.concat([result, remove_result1, remove_result1]).drop_duplicates(keep=False)
    # result = pd.concat([result,removeResult2,removeResult2]).drop_duplicates(keep=False)
    # result = pd.concat([result, remove_result3, remove_result3]).drop_duplicates(keep=False)
    # result = pd.concat([result,removeResult4,removeResult4]).drop_duplicates(keep=False)
    # result = pd.concat([result, remove_result5, remove_result5]).drop_duplicates(keep=False)
    # result = pd.concat([result, remove_result6, remove_result6]).drop_duplicates(keep=False)
    result = result.reset_index(drop=True)
    result['index_col'] = result.index
    return result


def setup_columns(flow):
    columns = []
    columns_flow = []
    columns_occupancy = []
    columns_speed = []
    columns_prob = []
    for i in range(1, len(flow.columns) + 1, 1):
        columns_flow.append("flow" + str(i))
        columns_occupancy.append("occupancy" + str(i))
        columns_speed.append("speed" + str(i))
        columns_prob.append("prob" + str(i))
    columns.extend(columns_flow)
    columns.extend(columns_occupancy)
    columns.extend(columns_speed)
    columns.extend(columns_prob)
    columns.append("timestamp")

    return columns, columns_flow, columns_occupancy, columns_speed, columns_prob

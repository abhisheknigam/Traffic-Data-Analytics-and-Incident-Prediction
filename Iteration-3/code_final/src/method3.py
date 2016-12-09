import pandas as pd


def predict_flow(result):
    print('\nstarting method 3...')
    columns = ['detector', 'flow', 'probability', 'timestamp', 'index_col']
    result = result[columns]
    new_columns = ['detector', 'flow_predicted', 'probability', 'timestamp', 'index_col']
    result.columns = new_columns
    result['confidence'] = result['probability']
    return result

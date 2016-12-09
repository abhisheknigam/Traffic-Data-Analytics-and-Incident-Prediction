from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import pandas as pd
import numpy as np


def linear_reg(df, columns, predict_column, y_col):
    print('\ntraining regression for cols : ' + str(columns))
    x_train, x_test, y_train, y_test = train_test_split(
        df[columns], df[y_col], test_size=0.2, random_state=42)

    regression_model = linear_model.LinearRegression()
    regression_model.fit(x_train, y_train)
    print('Coefficients: \n', regression_model.coef_)
    print("Mean squared error: %.2f" % np.mean((regression_model.predict(x_test) - y_test) ** 2))
    df[predict_column] = regression_model.predict(df[columns])
    return df


def merge_columns_regression(df, flow_cols, prob_cols):
    print('\nfixing columns after regression')
    df_arr = []
    for i in range(0, len(flow_cols), 1):
        df_arr.append(pd.DataFrame(
            {
                "flow": df[flow_cols[i]],
                "flow_predict": df[flow_cols[i]+'_predicted'],
                "probability": df[prob_cols[i]],
                "timestamp": df.timestamp,
                "detector": "x" + str(i),
                "confidence": df[prob_cols[i]],
                "index_col": df['idx'+str(i+1)]
            }
        ))

    result = pd.concat(df_arr)
    result = result.sort_values("timestamp")
    return result

import pandas as pd
import numpy as np
import math
from datetime import datetime

count = 0
flow_cols = []


def predict_flow_by_detector(result, columns_flow):
    global flow_cols
    flow_cols = columns_flow
    print('\nstarting method 2 predict')
    all_flows = []
    for i in range(0, len(columns_flow), 1):
        all_flows.append(result[result.detector == str("x" + str(i))].reset_index(drop=True))

    results = []
    confidences = []
    for i in range(0, len(columns_flow), 1):
        result_x = all_flows[i].sort_values("timestamp")
        result_x = result_x.reset_index(drop=True)
        result_x['timestamp'] = pd.to_datetime(result_x['timestamp'])
        timestamp = result_x["timestamp"]
        timestamp = np.asarray(timestamp)
        flow_x1 = result_x["flow"]
        flow_x1 = np.asarray(flow_x1)
        density = result_x["probability"]
        density = np.asarray(density)
        resultant, confidence = predict_flow(timestamp, flow_x1, density, i)
        results.append(resultant)
        confidences.append(confidence)

    for i in range(0, len(columns_flow), 1):
        all_flows[i]["Expected_" + str(i+1)] = pd.DataFrame(results[i])
        all_flows[i]["Confidence_" + str(i+1)] = pd.DataFrame(confidences[i])
        del all_flows[i]["occupancy"]
        del all_flows[i]["speed"]

    test = all_flows[0]
    for i in range(1, len(columns_flow), 1):
        test = test.append(all_flows[i])

    print('\nmerging flows...method 2...')
    test['flow_predicted'] = test.apply(lambda row: expected_flow(row), axis=1)
    global count
    count = 0
    test['confidence'] = test.apply(lambda row: expected_confidence(row), axis=1)

    for i in range(0, len(columns_flow), 1):
        del test["Expected_" + str(i+1)]
        del test["Confidence_" + str(i+1)]

    return test


def expected_flow(row):
    global count
    count += 1
    if count % 500000 == 0:
        print(count)

    expected = 0
    # try:
    for i in range(0, len(flow_cols), 1):
        if pd.isnull(row["Expected_" + str(i+1)]) == False:
            expected = row["Expected_" + str(i+1)]
    # except:
    #     print(row)

    return expected


def expected_confidence(row):
    global count
    count += 1
    if count % 500000 == 0:
        print(count)

    confidence = 0
    # try:
    for i in range(0, len(flow_cols), 1):
        if row["detector"] == "x" + str(i):
            confidence = row["Confidence_" + str(i+1)]
    # except:
    #     print(row)

    return confidence


def predict_flow(timestamp, flow_x1, density, index):
    arr = []
    confidence = []
    arr.extend([flow_x1[0],flow_x1[1]])
    confidence.extend([density[0],density[1]])
    for i in range(2, len(timestamp)-2, 1):
        prePreceding = timestamp[i-2]
        preceding = timestamp[i-1]
        present = timestamp[i]
        following = timestamp[i+1]
        followFollowing = timestamp[i+2]
        
        time_difference = 150;
        
        keptFlowPreceding = []
        keptDensityPreceding = []
        
        totalFlowPreceding = 0
        totalDensityPreceding = 0
        
        keptFlowFollowing = []
        keptDensityFollowing = []
        
        totalFlowFollowing = 0
        totalDensityFollowing = 0

        bestConfidenceValue = 0
        
        W1 = 0
        W2 = 0
        
        if int((present - prePreceding)/np.timedelta64(1,'s')) <= time_difference :
            keptFlowPreceding.append(flow_x1[i-2])
            keptDensityPreceding.append(density[i-2])
            
        if int((present - preceding)/np.timedelta64(1,'s')) <= time_difference :
            keptFlowPreceding.append(flow_x1[i-1])
            keptDensityPreceding.append(density[i-1])
            
        if int((following - present)/np.timedelta64(1,'s')) <= time_difference :
            keptFlowFollowing.append(flow_x1[i+1])
            keptDensityFollowing.append(density[i+1])
            
        if int((followFollowing - present)/np.timedelta64(1,'s')) <= time_difference :
            keptFlowFollowing.append(flow_x1[i+2])
            keptDensityFollowing.append(density[i+2])
        
        for k in range(0,len(keptFlowPreceding),1):
            totalFlowPreceding = totalFlowPreceding + keptFlowPreceding[k]
            totalDensityPreceding = totalDensityPreceding + keptDensityPreceding[k]
            
        for k in range(0,len(keptFlowFollowing),1):
            totalFlowFollowing = totalFlowFollowing + keptFlowFollowing[k]
            totalDensityFollowing = totalDensityFollowing + keptDensityFollowing[k]
              
        if (totalDensityPreceding != 0):
            W1 = totalDensityPreceding/(totalDensityPreceding + totalDensityFollowing)
        W2 = 1-W1
            
        if totalFlowPreceding != 0 or totalFlowFollowing != 0:
            averageFlow = W1*(totalFlowPreceding/2) + W2*(totalFlowFollowing/2)
        else:
            averageFlow = flow_x1[i]

        arr.append(averageFlow)
        if len(keptDensityPreceding) > 0:
            average_preceding = totalDensityPreceding / len(keptDensityPreceding)
        else:
            average_preceding = 0
        if len(keptDensityFollowing) > 0:
            average_following = totalDensityFollowing / len(keptDensityFollowing)
        else:
            average_following = 0

        bestConfidenceValue = min(average_preceding, average_following)
        # print(str(average_preceding) + "\t" + str(average_following) + "\t" + str(bestConfidenceValue))
        if not math.isnan(bestConfidenceValue) and bestConfidenceValue > 0:
            confidence.append(bestConfidenceValue)
        else:
            confidence.append(density[i])

        if i % 200000 == 0:
            print(i)
    
    arr.extend([flow_x1[len(flow_x1)-2],flow_x1[len(flow_x1)-1]])
    confidence.extend([density[len(density)-2],density[len(density)-1]])
    return arr,confidence

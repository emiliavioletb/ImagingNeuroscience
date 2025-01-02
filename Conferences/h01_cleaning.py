
from common.functions import *

def active_period(participant, task, period):
    mat_filepath = (study_folder + f'DATA_FOR_PROCESSING/{participant}/hddot/{participant}_{task}.mat')
    hbo = load_mat(mat_filepath, 'dotimg/hbo/gm')
    hbr = load_mat(mat_filepath, 'dotimg/hbr/gm')
    period_conv = convert_period(period)
    active_hbo = hbo[:, period[0]:period[1]]
    active_hbr = hbr[:, period[0]:period[1]]
    return active_hbo, active_hbr

def mean_change(x, m):
    avg_change_time = np.mean(x, 1)
    avg_change_chan = np.mean(x,0)
    assert len(avg_change_time) == x.shape[0]
    assert (len(avg_change_chan)) == x.shape[1]
    print(f'The mean change across time series and channels for {m} is {round(np.mean(avg_change_chan),3)} \u03BCm '
          f'±{round(np.std(avg_change_chan), 3)}')
    std_change_time = np.std(x, 1) # Std of time across channels (e.g., std of reconstruction)
    std_change_chan = np.std(x, 0) # Std of channels across time (e.g., std of hrf)
    assert len(std_change_time) == len(avg_change_time)
    assert len(std_change_chan) == len(avg_change_chan)
    return avg_change_time, avg_change_chan, std_change_time, std_change_chan, round(np.mean(avg_change_chan),3), \
        round(np.std(avg_change_chan), 3)


def maxmin_change(x):
    print(f'The max change is {round(max(x),3)} \u03BCm and the min change is {round(min(x),3)} \u03BCm')
    return round(max(x), 3), round(min(x), 3)

def percent_active(x, threshold=0.1):
    active = x>threshold
    percent = round(sum(active)/len(active)*100, 3)
    print(f'Percentage of all channels which reach {threshold} activation is {round(percent,3)}%')
    return percent

participants = ['HC_s03', 'AD_s15']
tasks = ['a_visual', 'b_visual']

for i in participants:
    for j in tasks:
        active_hbo, active_hbr = active_period(i, j, [25, 75]) #TODO: make function to find indices
        a, b, c, d, e, f = mean_change(active_hbo, (str(i) + '_' + str(j)))
        max_a, min_a = maxmin_change(a)
        percent = percent_active(np.squeeze(np.max(active_hbo, 1)))
        metrics = {
            'mean_all': e,
            'std_all': f,
            'max_all': max_a,
            'min_all': min_a,
            'percent_active': percent
        }
        fname = f'./data/{i}_{j}_metrics.json'
        save_json(metrics, fname)

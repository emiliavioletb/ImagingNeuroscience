
import seaborn as sns
import matplotlib.pyplot as plt
from common.functions import *

def bar_chart(f, dat, ax=None, params=None, save=False):
    if ax is None:
        ax = str(f)
    sns.boxplot(x='diagnosis', y=ax, data=dat, palette='Blues', width=0.3)
    plt.xlabel('Group')
    if params is not None:
        h_add = 0
        for m in params:
            dif = get_ind(m)
            dif1 = dif[0]
            dif2 = dif[1]
            res = params[m]
            x1, x2, x3, x4  = 0,1,2,3
            y, h, col = (max(dat[f]) + 1), 1, 'k'
            h = (h*2) + h_add
            plt.plot([dif1, dif1, dif2, dif2], [y+1, y+h, y+h, y+1], lw=1.5, c=col)
            plt.text((dif1+dif2)*.5, y+h, res, ha='center', va='bottom', color=col)
            h_add += 0.9
    if save:
        plt.savefig(f'./figures/c02_neuropsych/bar_{f}.svg', format='svg')
        print('saving')
        plt.close()
    else:
        plt.show()

def signifiance_bars(feature):
    a = load_pickle(f'./figures/significance_levels/{feature}_significance.pkl')
    return a

def fc_matrix(data, parcelLabels = None, fsave=None):
    plt.figure()
    ax = sns.heatmap(data, vmin=-1, vmax=1, cbar_kws={'label': 'r'}, cmap="RdBu_r")
    plt.xticks([])
    plt.yticks([])
    if not fsave:
        plt.show()
    else:
        plt.savefig(fsave, format='png')
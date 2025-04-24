
import matplotlib.pyplot as plt
from common.functions import *
plt.rcParams["font.family"] = "Arial"  # Set global font to Arial

hatch_size = 0.8  # Change me
class UpTriangleHatch(mpl.hatch.Shapes):
    """
    Custom hatches defined by a path drawn inside [-0.5, 0.5] square.
    Identifier 'c'.
    """
    filled = True
    size = hatch_size*1.1
    path = Polygon(
    [[-0.4, -0.35], [0.4, -0.35], [0, 0.35]],
    closed=True, fill=False).get_path()

    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('n')) * density
        self.shape_vertices = self.path.vertices
        self.shape_codes = self.path.codes
        mpl.hatch.Shapes.__init__(self, hatch, density)

class SquareHatch(mpl.hatch.Shapes):
    filled = True
    size = hatch_size
    path = Polygon(
    [[-0.4, -0.4], [0.4, -0.4], [0.4, 0.4], [-0.4, 0.4]],
    closed=True, fill=False).get_path()

    def __init__(self, hatch, density):
        self.num_rows = (hatch.count('s')) * density
        self.shape_vertices = self.path.vertices
        self.shape_codes = self.path.codes
        mpl.hatch.Shapes.__init__(self, hatch, density)

mpl.hatch._hatch_types.append(UpTriangleHatch)
mpl.hatch._hatch_types.append(SquareHatch)

motifs = pd.read_csv('~/Documents/PUBLICATIONS/Human Brain Mapping/data/motifs.csv')
motifs = motifs.drop(motifs[motifs.Motif == ' triangle_extra'].index)

remap_labels = {'triangle': 'Triangle',
                'open_triad': 'Open Triad',
                'chain': 'Chain',
                ' star': 'Star',
                'square': 'Square',
                'clique': 'Clique'}

fig, ax = plt.subplots(figsize=(9, 6))
sns.set_theme(style='whitegrid')

pal = sns.color_palette()
hatches = ['nn', 'XXX', '...', '**', 'ss', 'OO']

boxplot = sns.boxplot(data=motifs, x='Group', y='Values', order=['HC', 'MCI', 'AD'], hue='Motif')

patches = [patch for patch in ax.patches if type(patch) == mpl.patches.PathPatch]
h = hatches * (len(patches) // len(hatches))
for i, (patch, hatch) in enumerate(zip(patches, h)):
    patch.set_hatch(hatch)
    if i < 6:
        patch.set_edgecolor(pal[0])
        patch.set_facecolor('none')
    elif 6 <= i < 12:
        patch.set_edgecolor(pal[1])
        patch.set_facecolor('none')
    else:
        patch.set_edgecolor(pal[2])
        patch.set_facecolor('none')

handles, labels = ax.get_legend_handles_labels()
remapped_labels = [remap_labels.get(label, label) for label in labels]
l = ax.legend(handles=handles, labels=remapped_labels, title='Motif',
           loc='upper left', bbox_to_anchor=(1, 1.03), fontsize=20,
           markerscale=2, handlelength=2, title_fontproperties={'weight': 'bold', 'size': 20})
for lp, hatch in zip(l.get_patches(), hatches):
    lp.set_hatch(hatch)
    # fc = lp.get_facecolor()
    lp.set_edgecolor('black')
    lp.set_facecolor('none')

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.2f}'))

plt.ylim(0, 0.23)
x1, x2, x3 = 0, 1, 2
y_max = max(motifs['Values']) - 0.01
bar_height = 0.005  # Distance from top value
bracket_y = y_max + bar_height - 0.005
plt.plot([x1, x1, x2, x2], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.text((x1 + x2) / 2, bracket_y + bar_height - 0.005, "***", ha='center', va='bottom', fontsize=25)
bracket_y = y_max-0.01 + bar_height
plt.plot([(-0.35), (-0.35), (0.3), (0.3)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.plot([(0.65), (0.65), (1.35), (1.35)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)

y_max = max(motifs['Values']) + 0.015
bracket_y = y_max + bar_height - 0.005
plt.plot([x1, x1, x3, x3], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.text((x1 + x3) / 2, bracket_y + bar_height - 0.005, "***", ha='center', va='bottom', fontsize=25)
bracket_y = y_max-0.01 + bar_height
plt.plot([(-0.35), (-0.35), (0.3), (0.3)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.plot([(1.65), (1.65), (2.35), (2.35)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)


plt.ylabel('Average Count', fontsize=25)
plt.xlabel('Group', fontsize=25)
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=14)
plt.tight_layout()

sns.set_theme(style='whitegrid')

# plt.show()
plt.savefig((f'./output/graph_theory/figures/motifs.png'), format='png', dpi=500)

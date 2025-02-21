import matplotlib as mpl
from common.visualisation import *
plt.rcParams["font.family"] = "Arial"  # Set global font to Arial
participant_coefficient = pd.read_csv('~/Documents/PUBLICATIONS/Human Brain Mapping/data/participation_coefficient.csv')
remap_labels = {'control_network': 'Control',
                'default_mode': 'Default Mode',
                'limbic': 'Limbic',
                'salience': 'Salience'}

fig, ax = plt.subplots(figsize=(9, 6))
sns.set_theme(style='whitegrid')

pal = sns.color_palette()
hatches = ['//', '..', 'xx', '*']

boxplot = sns.boxplot(data=participant_coefficient, x='Group', y='Values', order=['HC', 'MCI', 'AD'],
            hue='Network')
patches = [patch for patch in ax.patches if type(patch) == mpl.patches.PathPatch]

h = hatches * (len(patches) // len(hatches))

for i, (patch, hatch) in enumerate(zip(patches, h)):
    patch.set_hatch(hatch)
    fc = patch.get_facecolor()

    if i < 4:
        patch.set_edgecolor(pal[0])
        patch.set_facecolor('none')
    elif 4 <= i < 8:
        patch.set_edgecolor(pal[1])
        patch.set_facecolor('none')
    else:
        assert 8 <= i < 12
        patch.set_edgecolor(pal[2])
        patch.set_facecolor('none')

handles, labels = ax.get_legend_handles_labels()
remapped_labels = [remap_labels.get(label, label) for label in labels]
l = ax.legend(
    handles=handles,
    labels=remapped_labels,
    title="Network",
    loc="upper left",
    bbox_to_anchor=(1, 1),
    fontsize=20,  # Font size for the legend labels
    markerscale=2,
    handlelength=2,
    title_fontproperties={'weight': 'bold', 'size': 20}  # Font weight and size for title
)
for lp, hatch in zip(l.get_patches(), hatches):
    lp.set_hatch(hatch)
    fc = lp.get_facecolor()
    lp.set_edgecolor('black')
    lp.set_facecolor('none')

plt.ylabel('Average Participation Coefficient', fontsize=25, family='Arial')
plt.xlabel('Group', fontsize=25, family='Arial')
plt.ylim(0.2, 0.9)
x_s = list(range(0,12))
y, h, col = max(participant_coefficient['Values']) + (max(participant_coefficient['Values']) * 0.03), 0.2, 'k'
ax.tick_params(axis='x', labelsize=18)
ax.tick_params(axis='y', labelsize=14)

x1, x2 = 0, 2
y_max = max(participant_coefficient['Values']) + 0.05
bar_height = 0.03  # Distance from top value
bracket_y = y_max + bar_height + 0.01
plt.plot([x1, x1, x2, x2], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.text((x1 + x2) / 2, bracket_y + bar_height - 0.01, "**", ha='center', va='bottom', fontsize=25)
bracket_y = y_max-0.01 + bar_height
bar_height = 0.02
plt.plot([(-0.35), (-0.35), (0.35), (0.35)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)
plt.plot([(1.65), (1.65), (2.35), (2.35)], [bracket_y, bracket_y + bar_height, bracket_y + bar_height, bracket_y], color='black', lw=1.5)

plt.tight_layout()
# plt.show()
plt.savefig((f'./output/graph_theory/figures/part_coef_networks.png'), format='png', dpi=500)

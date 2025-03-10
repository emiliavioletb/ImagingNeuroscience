import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from matplotlib.patches import Arc, Patch
from common.functions import *
from common.stats_test import *
import matplotlib as mpl

# Define data folders
datFolder = '/Users/emilia/Documents/Publications/Human Brain Mapping/data/'
datasets = {
    'HC': mat73.loadmat(datFolder + 'HC_avgMatrix.mat')['thresholded_matrix'],
    'MCI': mat73.loadmat(datFolder + 'MCI_avgMatrix.mat')['thresholded_matrix'],
    'AD': mat73.loadmat(datFolder + 'AD_avgMatrix.mat')['thresholded_matrix']
}

left_indices = np.arange(200)
right_indices = np.arange(200, 400)
right_reordered = right_indices[::-1]
new_order = np.concatenate([left_indices, right_reordered])

# Get all weights for normalisation
adj_mats = np.concatenate((
    mat73.loadmat(datFolder + 'HC_weights.mat')['avg_mat'],
    mat73.loadmat(datFolder + 'MCI_weights.mat')['avg_mat'],
    mat73.loadmat(datFolder + 'AD_weights.mat')['avg_mat']))
cleaned_array = adj_mats[~np.isnan(adj_mats)]
global_max = np.max(cleaned_array)
global_min = np.min(cleaned_array)
normalized_array = (cleaned_array - global_min) / (global_max - global_min)

# Get network labels
network_name_labels = {'LH_DefaultA': 'LH_DMN', 'LH_DefaultB': 'LH_DMN', 'LH_DefaultC': 'LH_DMN',
                       'LH_VisCent': 'LH_Visual', 'LH_VisPeri': 'LH_Visual', 'LH_SomMotA': 'LH_Somato \nmotor',
                       'LH_SomMotB': 'LH_Somato \nmotor', 'LH_DorsAttnA': 'LH_Dorsal \nAttention',
                       'LH_DorsAttnB': 'LH_Dorsal \nAttention', 'LH_LimbicA': 'LH_Limbic',
                       'LH_LimbicB': 'LH_Limbic', 'LH_ContA': 'LH_Control', 'LH_ContB': 'LH_Control',
                       'LH_ContC': 'LH_Control', 'LH_TempPar': 'LH_Temporo \nparietal',
                       'LH_SalVentAttnA': 'LH_Salience', 'LH_SalVentAttnB': 'LH_Salience','RH_DefaultA': 'RH_DMN',
                       'RH_DefaultB': 'RH_DMN', 'RH_DefaultC': 'RH_DMN',
                       'RH_VisCent': 'RH_Visual', 'RH_VisPeri': 'RH_Visual', 'RH_SomMotA': 'RH_Somato \nmotor',
                       'RH_SomMotB': 'RH_Somato \nmotor', 'RH_DorsAttnA': 'RH_Dorsal \nAttention',
                       'RH_DorsAttnB': 'RH_Dorsal \nAttention', 'RH_LimbicA': 'RH_Limbic',
                       'RH_LimbicB': 'RH_Limbic', 'RH_ContA': 'RH_Control', 'RH_ContB': 'RH_Control',
                       'RH_ContC': 'RH_Control', 'RH_TempPar': 'RH_Temporo \nparietal',
                       'RH_SalVentAttnA': 'RH_Salience', 'RH_SalVentAttnB': 'RH_Salience'}

networks_to_remove = [
    'LH_Temporo \nparietal', 'RH_Temporo \nparietal',
    'LH_Visual', 'RH_Visual',
    'LH_Somato \nmotor', 'RH_Somato \nmotor'
]

file_path = '/Users/emilia/Documents/MATLAB/Lumo/final_scripts/' \
            'utils/parcellation/Schaefer2018_400Parcels_17Networks_order.txt'
node_network_mapping = {}
with open(file_path, 'r') as file:
    for line in file:
        columns = line.split()
        node_num = int(columns[0]) - 1
        network_name = columns[1]
        stripped_network_name = network_name[11:]
        stripped_network_name = '_'.join(stripped_network_name.split('_')[:2])
        node_network_mapping[node_num] = network_name_labels[stripped_network_name]

network_nodes = {}
for node, network_name in node_network_mapping.items():
    network_nodes.setdefault(network_name, []).append(node)

def flipping_right(to_flip):
    flipped = []
    for j in to_flip:
        flipped.append(399-(j-200))
    return flipped

for key, val in network_nodes.items():
    if key[0] == 'R':
        flipped_val = flipping_right(val)
        network_nodes[key] = flipped_val

nodes_to_remove = []
keys_to_remove = []
for key, val in network_nodes.items():
    if key in networks_to_remove:
        nodes_to_remove.append(val)
        keys_to_remove.append(key)
nodes_to_remove = [j for n in nodes_to_remove for j in n]

for key in keys_to_remove:
    del network_nodes[key]

cmap = plt.cm.viridis_r
norm = mpl.colors.Normalize(vmin=0, vmax=1)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(32, 9), gridspec_kw={'width_ratios': [1, 1, 1.4]})
for i, (group, data) in enumerate(datasets.items()):
    # Create graph
    data_for_graph = datasets[group]
    data_reordered = data_for_graph[np.ix_(new_order, new_order)]
    graph = np.nan_to_num(data_reordered, nan=0)
    G = nx.from_numpy_array(graph)
    G.remove_nodes_from(nodes_to_remove)

    # Get edge weights (for color mapping)
    adj_mat = mat73.loadmat((datFolder + group + '_weights.mat'))['avg_mat']
    adj_mat_reordered = adj_mat[np.ix_(new_order, new_order)]
    edges = list(G.edges)
    weights = [adj_mat_reordered[u, v] for u, v in edges]
    weights_normalized = [(w - global_min) / (global_max - global_min) for w in weights]

    edge_colors = [cmap(norm(w)) for w in weights]

    # Plot graph
    pos = nx.circular_layout(G)

    # Rotate so the left side of the graph is left hemisphere
    def rotate_layout(layout, angle=np.pi / 2):
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                     [np.sin(angle), np.cos(angle)]])
        return {node: np.dot(rotation_matrix, coord) for node, coord in layout.items()}

    pos = rotate_layout(pos, angle=np.pi / 2)
    node_opts = {"node_size": 0, "node_color": "white",  "linewidths": 2.0}
    nx.draw_networkx_nodes(G, pos, **node_opts, ax=ax[i])
    nx.draw_networkx_edges(G, pos, width=4, edge_color=edge_colors, edge_cmap=cmap, ax=ax[i])

    shift = {'Dorsal \nAttention': 0.3, 'Salience': -0.3, 'Limbic': -0.25, 'Control': -0.15}
    for network_name, nodes in network_nodes.items():
        network_pos = np.mean([pos[node] for node in nodes], axis=0)
        radius = 1.3
        network_name_short = network_name[3:]
        if network_name[0] == 'R':
            if network_name_short == 'DMN':
                network_pos[1] = network_pos[1] + 0.1
                network_pos[0] = network_pos[0] - 0.1
            elif network_name_short == 'Salience':
                network_pos[1] = network_pos[1] - 0.3
                network_pos[0] = network_pos[0]
            else:
                network_pos = network_pos + shift[network_name_short]
        network_pos = network_pos / np.linalg.norm(network_pos) * radius

        # Add network label
        ax[i].text(network_pos[0], network_pos[1], network_name_short,
                 fontsize=30, ha='center', va='center',
                 fontweight='bold', color='black', family='Arial')

        # Calculate the arc angles for the network
        theta_start = np.degrees(np.arctan2(pos[nodes[0]][1], pos[nodes[0]][0]))
        theta_end = np.degrees(np.arctan2(pos[nodes[-1]][1], pos[nodes[-1]][0]))
        theta_start = (theta_start + 360) % 360
        theta_end = (theta_end + 360) % 360

        # Flip right hemisphere over x axis
        if network_name[0] == 'R':
            theta_start = (360 - theta_start) % 360
            theta_end = (360 - theta_end) % 360

        if network_name[0] == 'L':
            if network_name_short == 'Dorsal \nAttention':
                theta_start = theta_start + 2
            if network_name_short == 'DMN':
                theta_end = theta_end - 2
        color = 'black'
        theta_start = theta_start + 1
        theta_end = theta_end - 1
        if theta_start > theta_end:
            arc1 = Arc((0, 0), 2, 2, theta1=theta_start, theta2=360,
                       edgecolor=color, lw=5)
            arc2 = Arc((0, 0), 2, 2, theta1=0, theta2=theta_end,
                       edgecolor=color, lw=5)
            ax[i].add_patch(arc1)
            ax[i].add_patch(arc2)
        else:
            arc = Arc((0, 0), 2.04, 2.04, theta1=theta_start, theta2=theta_end,
                      edgecolor=color, lw=5)
            ax[i].add_patch(arc)
    ax[i].plot([0, 0], [-1, 1], linestyle='--', color='dimgray', lw=4)
    ax[i].set_title(group, fontsize=70, fontweight='bold', family='Arial', pad=75)
    ax[i].set_axis_off()
    fig.tight_layout()
sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax[2], label="Weight", pad=0.15)
cbar.ax.tick_params(labelsize=25)
cbar.set_label("Weight", fontsize=40, fontweight='bold', family='Arial')
cbar.ax.yaxis.labelpad = 20
plt.tight_layout()
plt.subplots_adjust(wspace=0.3)
# plt.show()
plt.savefig(f'./output/graph_theory/figures/functional_connectomes.png',
            format='png', dpi=500)


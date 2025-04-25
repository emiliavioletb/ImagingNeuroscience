function motif_counts = Calc3NodeMotif(w_mtx)
%A 3-node motif analysis involves identifying and quantifying all possible
% triadic patterns (motifs) in a network. In an undirected network, there
% are 2 unique 3-node motifs: triangles (fully connected 3-node subgraphs),
% and open triads (2 nodes connected with a shared neighbor).
%
% Triangle motifs often indicate strong interconnectivity (e.g., cliques or
% densely connected groups). Open triads reflect less cohesive structures.
%
% The adjacency matrix must be undirected and have no subgraphs (NaNs).


% Initialize total motif counts
norm_triangle_count = NaN(size(w_mtx,3),1);
norm_open_triad_count = NaN(size(w_mtx,3),1);

counts4nodes = table();

for subj = 1:size(w_mtx, 3)

    A = w_mtx(:,:,subj);

    % Preprocessing similarity matrix
    A(isnan(A)) = 0;    % replace NaNs with 0
    A_binary = A > 0;   % binarize the matrix (threshold > 0)
    A_binary = max(A_binary, A_binary');    % ensure symmetry (if undirected)

    % Remove isolated nodes
    degrees = sum(A_binary, 2);     % Degree of each node
    non_isolated = degrees > 0;     % Logical index for non-isolated nodes
    A_filtered = A_binary(non_isolated, non_isolated);

    %A_filtered = A_binary;
    n = size(A_filtered, 1);    % Number of nodes in the filtered matrix
    
    % total_triads = n * (n-1) * (n-2) / 6; % Total number of 3-node subgraphs
    % edge_density = sum(A_filtered(:)) / (n * (n-1)); % Density of the network
    % expected_triangles = edge_density^3 * total_triads; % Approximation for triangles


    % Initialize motif counts for subj
    triangle_count = 0;
    open_triad_count = 0;

    % Enumerate all possible triads
    for i = 1:n-2
        for j = i+1:n-1
            for k = j+1:n
                % Subgraph of 3 nodes
                subgraph = A_filtered([i j k], [i j k]);

                % Count edges in the subgraph
                edges = sum(subgraph(:)) / 2; % Divide by 2 for undirected graphs

                % Classify the subgraph
                if edges == 3
                    triangle_count = triangle_count + 1;
                elseif edges == 2
                    open_triad_count = open_triad_count + 1;
                end
            end
        end
    end

    % Normalization by Total Motif Count: divide the count of each motif type
    % by the total number of 3-node subgraphs in the network to get a
    % proportion.
    % The total number of 3-node subgraphs is given the Newton binomial:
    % (n choose 3) = n * (n-1) * (n-2) / 6
    counts.triangle(subj,1) = triangle_count/nchoosek(n, 3);
    counts.open_triad(subj,1) = open_triad_count/nchoosek(n, 3);

    motif_4nodes = count_4node_motifs(A_filtered);
    counts4nodes{end+1, :} = motif_4nodes{:,:} ./ nchoosek(n, 4);
end

counts4nodes.Properties.VariableNames = {'chain', ' star', ' triangle_extra', 'square', 'clique'};

motif_counts = struct2table(counts);

motif_counts = horzcat(motif_counts, counts4nodes);

return
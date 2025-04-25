function modularity = CalcModularity(w_mtx_all)
% This function uses the similarity matrix defined in w_mtx to compute the
% modularity coefficient for each graph; it runs the Louvain algorithm
% multiple times for stability of the communities required to compute
% modularity, and it can only be performed in a fully connected graph
% (i.e., without subgraphs with NaNs)


for subj = 1:length(w_mtx_all)
    % Run Louvain algorithm multiple times for stability
    num_iterations = 100;
    max_modularity = 0;

    for i = 1:num_iterations
        [Ci, Q] = community_louvain(w_mtx_all{subj});

        if Q > max_modularity
            max_modularity = Q;
            best_partition = Ci;
        end
    end

    modularity(subj) = max_modularity;
end

modularity = modularity';

return
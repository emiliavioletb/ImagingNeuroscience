function [P, Pavg_table] = CalcPartCoeff(A, M)
% This function computes the participation coefficient of a weighted/binary
% matrix A considering the module distribution given by vector M. This
% implementation allows for non-existing connections within subpartitions
% (marked as NaN), unlike other implementations for the partition
% coefficient.
% The outputs are:
%       P: vector containing all partition coefficients for each node
%       Pavg: mean participation coefficient per cluster
%


% Number of nodes and unique modules
num_nodes = size(A, 1);
unique_modules = unique(M);
num_subjs = size(A, 3);

P = NaN(num_nodes, num_subjs);
Pavg = NaN(num_subjs, length(unique_modules));

% Loop through all subjects
for subj = 1:num_subjs

    Asubj = A(:,:,subj);

    % Compute the total degree for each node
    degree = nansum(Asubj, 2); % Row-wise sum

    % Iterate over each node to compute participation coefficient
    for i = 1:num_nodes
        % Total degree of node i
        k_i = degree(i);

        if k_i == 0
            % Isolated nodes have a participation coefficient of 0
            P(i, subj) = 0;
            continue;
        end

        % Initialize sum for within-module degree fractions
        sum_fraction = 0;

        % Compute k_{i,m} for each module
        for m = unique_modules'
            % Indices of nodes in module m
            module_nodes = (M == m);

            % Degree of node i within module m
            k_i_m = nansum(Asubj(i, module_nodes));

            % Update sum of squared fractions
            sum_fraction = sum_fraction + (k_i_m / k_i)^2;
        end

        % Compute participation coefficient
        P(i, subj) = 1 - sum_fraction;
    end

    % Compute average participation for each network
    for net = 1:length(unique_modules)
        Pavg(subj, net) = sum( P(M == net, subj) )./ ( length( find(P(M == net, subj) > 0) ) );
    end


    % % Scatter plot of degree vs. participation coefficient
    % figure, 
    % scatter(degree, P(:,subj), 50, M, 'filled'); % Color by cluster
    % xlabel('Degree');
    % ylabel('Participation Coefficient');
    % title('Node Roles Based on Degree and Participation Coefficient');
    % colorbar;

end

Pavg_table = array2table(Pavg, 'VariableNames', {'control_network', 'default_mode',...
    'dorsal_attention', 'limbic', 'salience', 'somatomotor', 'temporoparietal',...
    'visual'});

return
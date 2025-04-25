function graph_size = CalcGraphProperties(folderPath, filtGroupFOlders, outputFile, N_PARCELS)
% This function loads all .mat files containing data to be analysed under
% the parent folder available on 'folderPath,' and saves the results into a
% .mat file named as 'outputFile.'
% The results are organized into two main matlab structs:
%   - macroProperties: containing the average results per subject
%   (macroscopic scale)
%   - localProperties: containing the local results (microscopic scale) per
%   node (defined as parcels).




% ****************************
% Constant Definitions
% ****************************

w_threshold = 0.2;    % normalized z threshold to ignore for network construction



% ****************************
% Get a list of all folder paths for analysis
% ****************************
% 
% % Initialize the output cell array
% filenames = {};
% 
% % Check whether folderPath is a full path, and extract full path if
% % necessary
% if ~isFullPath(folderPath)
%     folderPath = getAbsolutePath(folderPath);
% end
% 
% % Generate a list of all folders and subfolders
% allFolders = genpath(folderPath);
% % Split this list into individual folder paths
% folderList = split(allFolders, pathsep);


% ****************************
% Load data for each .mat file
% ****************************

% Initialize variable that will keep global graph properties;
macroProperties.totalStrength = [];
macroProperties.avgDegree = [];
macroProperties.avgDegDensity = [];
macroProperties.avgClustering = [];
macroProperties.globEfficiency = [];
macroProperties.avgBtwCentrality = [];
macroProperties.avgEigCentrality = [];
macroProperties.num_parcels = [];
macroProperties.fname = [];

graph_size = [];

% Initialize variable that will keep local graph properties;
localProperties.strength = [];
localProperties.degree = [];
localProperties.degDensity = [];
localProperties.clustering = [];
localProperties.efficiency = [];
localProperties.btwCentrality = [];
localProperties.eigCentrality = [];

% Initialise variable that will keep all adjacency matrices
group_matrices.matrix = [];

cnt = 1;

% Iterate over each folder in the list
for file = 1:length(filtGroupFOlders)

    currFolder = [folderPath, '/', filtGroupFOlders(file).name, '/hddot/', filtGroupFOlders(file).name, ...
            '_resting_parc.mat'];

    if ~isempty(currFolder)
        
        % % Ensure the folder path ends with a slash for compatibility
        % if currFolder(end) ~= '/' && currFolder(end) ~= '\'
        %     currFolder = [currFolder, '/'];
        % end
        % 
        % % List all .mat files in the folder
        % matFiles = dir(fullfile(currFolder, '*.mat'));

        % Iterate through all mat files
      

        % log of matFile analsed
        % filenames{end + 1} = fullfile(currFolder, matFiles(j).name);

        % load mat file
        % df = load(fullfile(currFolder, matFiles(j).name), '-mat');
        df = load(currFolder, '-mat');

        % Transform data into standard fNIRS datatype
        % Create a 'data' 2D-array containing T (# timpe points) x N (# spatial
        % information/parcels)
        data = zeros(size(df.parc.HbO_parc{1,2},1), N_PARCELS)*NaN;
        for ml = 1:length(df.parc.HbO_parc)
            data(:,df.parc.HbO_parc{ml,1}) = df.parc.HbO_parc{ml,2};
        end

        % COMPUTE SIMILARITY MATRIX FROM DATA
        % Similarity is computed based on Pearson correlation coefficient, then
        % transformed to z-transform using Fisher's r-to-z transform. Matrix is
        % reduced to eliminate the parcels not measured from the atlas of this
        % specific measurement.
        % Parcels with no data is stored in 'bad_meas' to convert back to 
        % main graph in the end.
        [conn_mtx, pvals]  = corr(data,  'Rows', 'pairwise', 'Type', 'Pearson');
        z_mtx = 0.5*( log(1+conn_mtx) - log(1-conn_mtx) );
        
        pvals(isnan(pvals)) = 1;  
        pvals_vector = pvals(:);
        pvals_corrected = mafdr(pvals_vector, 'BHFDR', true); 
        pvals_corrected = reshape(pvals_corrected, size(pvals));   
        pvals_thresholded = pvals_corrected <= 0.05;
        conn_mtx_sig = z_mtx.*pvals_thresholded;

        % get rid of parcels not used
        bad_meas = [];
        reduced_conn_mtx = conn_mtx;
        reduced_z_mtx = z_mtx;
        for line = size(conn_mtx,1):-1:1
            if isnan(reduced_conn_mtx(line,line))
                reduced_conn_mtx(line,:) = [];
                reduced_conn_mtx(:,line) = [];
                reduced_z_mtx(line,:) = [];
                reduced_z_mtx(:,line) = [];
                bad_meas = [line; bad_meas];
            end
        end
        bad_meas_all{cnt} = bad_meas;   % save all discarded parcels

        % Weighted Matrix construction
        for line = 1:size(reduced_conn_mtx,1)
            for column = 1:size(reduced_conn_mtx,2)
                if reduced_conn_mtx(line,column) >= w_threshold
                    if reduced_conn_mtx(line, column) == 1  % get rid of cycles in the nodes

                        w_mtx(line,column) = 0;
                    else
                        w_mtx(line,column) = reduced_z_mtx(line,column);
                    end
                else
                    w_mtx(line,column) = 0;
                end
            end
        end
        
        before_thresh = nnz(reduced_conn_mtx(triu(true(size(reduced_conn_mtx)), 1)));
        after_thresh = nnz(w_mtx(triu(true(size(w_mtx)), 1)));
        graph_size = [graph_size; (after_thresh/(before_thresh + after_thresh)*100)];

        % Normalize matrix so that weights are all within [0,1]
        w_mtx = w_mtx/2.65; % 2.65 is (almost) max z-value, so w_mtx is normalized between 0 and 1

        w_mtx_all{cnt} = w_mtx; % save reduced matrix
        cnt = cnt + 1;


        % COMPUTE MAIN GRAPH PROPERTIES FROM WEIGHTED MATRIX

        % Using the BCT (Brain Connectivity Toolbox for properties' computation)
        strength_tmp = strengths_und(w_mtx);    % node strength, based on the weights
        degree_tmp = degrees_und(w_mtx);        % degree, # of connected links
        degdensity_tmp = degree_tmp/(length(degree_tmp) - 1); % degree density (fraction of present connections to possible connections)
        cluster_tmp = clustering_coef_wu(w_mtx);    % fraction of node's neighbors that are neighbors of each other
        locEfficiency_tmp = efficiency_wei(w_mtx, 2);   % average inverse shortest path in the network (0) or on the neighborhood of the node (2)
        btwCentral_tmp = betweenness_wei(w_mtx)/( (length(betweenness_wei(w_mtx)) -1)*(length(betweenness_wei(w_mtx))-2) );       % nodes that participate in a large number of shortest paths
        eigCentral_tmp = eigenvector_centrality_und(w_mtx); % nodes that connect to other nodes that have high eigenvector centrality (similar nodes)

        % Computing global metrics
        macroProperties.totalStrength = [macroProperties.totalStrength; nansum(strength_tmp)];
        macroProperties.avgDegree = [macroProperties.avgDegree; nanmean(degree_tmp)];
        macroProperties.avgDegDensity = [macroProperties.avgDegDensity; nanmean(degree_tmp)/(length(degree_tmp) - 1)];
        macroProperties.avgClustering = [macroProperties.avgClustering; nanmean(cluster_tmp)];
        macroProperties.globEfficiency = [macroProperties.globEfficiency; efficiency_wei(w_mtx, 0)];
        macroProperties.avgBtwCentrality = [macroProperties.avgBtwCentrality; nanmean(btwCentral_tmp)];
        macroProperties.avgEigCentrality = [macroProperties.avgEigCentrality; nanmean(eigCentral_tmp)];

        group_matrices.matrix(:,:,file) = conn_mtx_sig;
        macroProperties.num_parcels = [macroProperties.num_parcels; length(df.parc.HbO_parc)];
        macroProperties.fname = cellstr([macroProperties.fname; string(filtGroupFOlders(file).name)]);


        % Rearrange the strengths at the correct node
        % position
        i = 1;
        for chn = 1:N_PARCELS
            lst = find(chn == bad_meas);
            if isempty(lst)
                strength(chn) = strength_tmp(i);
                degree(chn) = degree_tmp(i);
                degDensity(chn) = degdensity_tmp(i);
                clustering(chn) = cluster_tmp(i);
                locEfficiency(chn) = locEfficiency_tmp(i);
                btwCentrality(chn) = btwCentral_tmp(i);
                eigCentrality(chn) = eigCentral_tmp(i);
                i = i + 1;
            else
                strength(chn) = NaN;
                degree(chn) = NaN;
                degDensity(chn) = NaN;
                clustering(chn) = NaN;
                locEfficiency(chn) = NaN;
                btwCentrality(chn) = NaN;
                eigCentrality(chn) = NaN;
            end
        end

        % Transfer data to main local variable
        localProperties.strength = [localProperties.strength; strength];
        localProperties.degree = [localProperties.degree; degree];
        localProperties.degDensity = [localProperties.degDensity; degDensity];
        localProperties.clustering = [localProperties.clustering; clustering];
        localProperties.efficiency = [localProperties.efficiency; locEfficiency];
        localProperties.btwCentrality = [localProperties.btwCentrality; btwCentrality];
        localProperties.eigCentrality = [localProperties.eigCentrality; eigCentrality];


        clear *Centrality *Efficiency clustering deg* strength
        clear *_tmp df data *conn_mtx *z_mtx w_mtx bad_meas
        clear ml line column chn lst

        close all
    end
end
clear *Folder* ansclear folder* i j 

% Save .mat file with graph properties
save(outputFile, '-v7.3');



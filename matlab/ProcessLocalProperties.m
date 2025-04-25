function [clusterProp, degProp] = ProcessLocalProperties(filePath, N_PARCELS, Ci, atlasInfo)

% load file
load(filePath)
clear all* c* f* g* i* j m name out* 

% Recreate correlation matrix containing all parcels
w_mtx = RecreateCorrelationMatrix(w_mtx_all, bad_meas_all, N_PARCELS);
clear bad_meas_all w_threshold pvals


% ****************************
% Step 2: Analyze local properties at the micro- & mesoscopic scales
% ****************************

% Modularity
clusterProp.modularity = CalcModularity(w_mtx_all);

% Partition Pattern
clusterProp.motifs = Calc3NodeMotif(w_mtx);

% Partition coefficients for each degree and cluster
[degProp.P, clusterProp.Pavg] = CalcPartCoeff(w_mtx, Ci);

% Hub Analysis
degProp.hubs = AnalyzeHubs(localProperties, atlasInfo, degProp.P);

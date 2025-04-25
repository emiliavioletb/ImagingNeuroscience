% ************************************************************************
%
% MAIN SCRIPT FOR rsFC DATA FROM CAMBRIDGE
%
% This script performs graph-based analysis on rsFC data acqquired with 
% fNIRS at the ROI level (i.e., sparse fNIRS). The script assumes the fNIRS
% data were previously processed, and all data files are save as .mat files
% containing a variable (datatype 'struc') named 'parc' consisted of 2
% fields (one for each haemoglobin, HbO & HbR). Each field is a cell with
% varying length, depending on the number of parcels measured. For each
% cell, there is a list identifying the parcel and its time series. 
%
% Script created by R. Mesquita (2024-03-28)
%
% Last modified by: R. Mesquita (2024-08-29)
%
% ************************************************************************

clear
close all


% ****************************
% Setup environment
% ****************************

addpath(genpath('../utils/'));   % Prepend auxiliary files from this project (saved in /utils/) to the path


% ****************************
% Step 1: load data & compute graph properties
% ****************************

N_PARCELS = 400;    % assuming data is parcellated using the 400-parcel atlas


% data to be analysed is under a parent folder called '/data/'
folderPath = '/Users/emilia/Documents/STUDIES/ONAC/hpc/';

groupList = {'MCI', 'HC', 'AD'};

filename = '~/Documents/Publications/Human Brain Mapping/included.csv';  
included = readcell(filename, 'Delimiter', ',', 'TextType', 'string');

allFolders = dir(folderPath);
allFolders = allFolders([allFolders.isdir]);
allFolders = allFolders(~ismember({allFolders.name}, {'.', '..'}));
folderNames = {allFolders.name};

% Initialize logical array for inclusion
isIncluded = false(length(allFolders), 1);

for i = 1:length(allFolders)
    name = allFolders(i).name;
    for j = 1:length(included)
        if name == string(included(j))
            isIncluded(i) = true;
        end
    end
end

groupFolders = allFolders(isIncluded);

%%
for m=1:length(groupList)
    group = char(groupList(m));
    
    outputFile = ['~/Documents/Publications/Human Brain Mapping/data/', group, '_gtMetrics.mat'];  
    groupFolderNames = {groupFolders.name};
    containsGroup = contains(groupFolderNames, group);
    filtGroupFOlders = groupFolders(containsGroup);
    
    size = CalcGraphProperties(folderPath, filtGroupFOlders, outputFile, N_PARCELS);
    outputFile = ['~/Documents/Publications/Human Brain Mapping/data/', group, '_graph_size.mat'];
    save(outputFile, 'size', '-v7.3');
end 


%% ****************************
% Step 2: analyse local Properties
% ****************************

filePath = '~/Documents/PUBLICATIONS/Human Brain Mapping/data/AD_gtMetrics.mat';

load(filePath)
clear all* c* f* g* i* j m name out* 


% Functional roles of nodes
% ---------------------------

% Compute highly connected nodes considering all subgraphs from all
% subjects
normOccurHubs = FindHighNodes(localProperties, N_PARCELS);

% Plot output matrix to visually observe the highly connected parcels

figure
imagesc(normOccurHubs)
title('CONSISTENCY OF NODES WITH HIGHEST GRAPH PROPERTIES (HC)')
xlabel('Property')
xticks([1 2 3 4 5])
xticklabels({'Degree', 'Betweeness Centrality','Eigenvector Centrality','Clustering','Efficiency'})
ylabel('Parcel')
set(gca, 'FontSize', 18)
colormap("hot")





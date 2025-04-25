function atlasInfo = AnalyzeHubs(localProperties, atlasInfo, partCoeff)
% This function uses the local properties struct, the anatomical atlas
% information, and the partition coefficient for every node to analyze the
% functional role within the network. 


% Find highly connected nodes considering all subgraphs from all subjects
% and returns the parcels which are consistently observed as hubs for every
% metric
normOccurHubs = FindHighNodes(localProperties, height(atlasInfo));

overall_centr = nanmedian(normOccurHubs(:,[1 2 3])')'; 

for subj = 1:size(partCoeff,2)
    lst = find(partCoeff(:,subj)== 0);
    partCoeff(lst,subj) = NaN;
end
avgPC = nanmean(partCoeff,2);  

% Show main hubs
subj_threshold = 0.2;   % will look at parcels consistently marked as hub in at least 20% of all subjects

for node = 1:height(atlasInfo)  % add info to the main nodes
    if (~isnan(normOccurHubs(node,1))) && (normOccurHubs(node,1) > subj_threshold)
        atlasInfo.DegCentrality(node) = normOccurHubs(node, 1);
    else
        atlasInfo.DegCentrality(node) = NaN;
    end

    if (~isnan(normOccurHubs(node,2))) && (normOccurHubs(node,2) > subj_threshold)
        atlasInfo.BtwCentrality(node) = normOccurHubs(node, 2);
    else
        atlasInfo.BtwCentrality(node) = NaN;
    end

    if (~isnan(normOccurHubs(node,3))) && (normOccurHubs(node,3) > subj_threshold)
        atlasInfo.EigCentrality(node) = normOccurHubs(node, 3);
    else
        atlasInfo.EigCentrality(node) = NaN;
    end
    
    if (~isnan(overall_centr(node))) && (overall_centr(node) > subj_threshold)
        atlasInfo.OverallCentrality(node) = overall_centr(node);
    else
        atlasInfo.OverallCentrality(node) = NaN;
    end

    if (~isnan(avgPC(node))) && (avgPC(node) > 0)
        atlasInfo.PartCoeff(node) = avgPC(node);
    else
        atlasInfo.PartCoeff(node) = NaN;
    end
end


return



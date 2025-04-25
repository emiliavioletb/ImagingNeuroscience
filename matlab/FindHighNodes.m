function normOccurHubs = FindHighNodes(localProperties, N_PARCELS);
% This function receives a matlab struct containing the local properties
% for all subjects in a group and uses this information to compute the
% ocurrence matrix of the top nodes showing the highest local properties in
% connectivity (degree, centrality), segregation (clustering), and flow
% (efficiency). 
% Because each participant has a different subgraph, this computation is
% first performed considering the whole graph structure (whose nodes are 
% given by 'N_PARCELS'), and then it discards the parcels with very low
% counts (currently, < 15% across the group). 
% 
% Function output is a matrix containing the frequency in which each parcel
% was found as a top node for each of five local properties: degree,
% betweeness centrality, eigenvector centrality, clustering, efficiency;
% parcels that were measured less than 15% of the times, or that were
% signposted as a top parcel in less than 10% of the participants, are
% discarded (NaN). 
%
% The results from this matrix can be combined to find consistent parcels
% that play stable and influential roles in the network. In particular,
% hubs with high centrality + high clustering and efficiency reveal whether
% they are core hubs (well-connected locally) or just peripheral hubs
% (i.e., they act as bridges wihtout a dense local structure). 



% Initialize 3 main variables
numParcels = zeros(N_PARCELS, 1);    % register total number of times a parcel was measured (and, therefore, could have been a hub)
occurrenceMtx = zeros(N_PARCELS, 5);       % register total number of times a parcel was observed as a hub in the network across all subjects
normOccurHubs = zeros(N_PARCELS,3);    % Occurrence Hubs normalized by the maximum number of times possible that a given parcel could have been a hub

for subj = 1:size(localProperties.degDensity,1)
    % find valid parcels for current subject
    validParcels = find(~isnan(localProperties.degDensity(subj,:)));
    % update number of times that parcel is valid
    numParcels(validParcels) = numParcels(validParcels) + 1;
    % total number of nodes
    numNodes = length(validParcels);

    % identify hubs (defined here as top 10% values)
    hubDegrees = find(localProperties.degDensity(subj,:) >= ...
                        prctile(localProperties.degDensity(subj,:),90));
    hubBtwCentr = find(localProperties.btwCentrality(subj,:) >= ...
                        prctile(localProperties.btwCentrality(subj,:),90));
    hubEigCentr = find(localProperties.eigCentrality(subj,:) >= ...
                        prctile(localProperties.eigCentrality(subj,:),90));
    % update hubs occurrence
    occurrenceMtx(hubDegrees, 1) = occurrenceMtx(hubDegrees, 1) + 1;
    occurrenceMtx(hubBtwCentr, 2) = occurrenceMtx(hubBtwCentr, 2) + 1;
    occurrenceMtx(hubEigCentr, 3) = occurrenceMtx(hubEigCentr, 3) + 1;

    % find parcels with high clustering
    highCC = find( localProperties.clustering(subj,:) >= ...
                        prctile(localProperties.clustering(subj,:),80));
    occurrenceMtx(highCC, 4) = occurrenceMtx(highCC, 4) + 1;

    % find parcels with high efficiency
    highEff = find( localProperties.efficiency(subj,:) >= ...
                        prctile(localProperties.efficiency(subj,:),80));
    occurrenceMtx(highEff, 5) = occurrenceMtx(highEff, 5) + 1;

end

% Ignore parcels with very low counts (< 15% across all subjects)
for i=1:length(numParcels)
    if numParcels(i) < round(0.20*max(numParcels))
        numParcels(i) = 0;
        occurrenceMtx(i,:) = 0;
    end
end


% compute frequency of hubs appearance, ignore hubs with very low counts 
% (< 10% across all subjects)
normOccurHubs = occurrenceMtx./repmat(numParcels, 1, size(occurrenceMtx, 2));
for prop = 1:size(normOccurHubs, 2)
    for parcel = 1:size(normOccurHubs, 1)
        if (isnan(normOccurHubs(parcel, prop))) || (isinf(normOccurHubs(parcel, prop))) || (normOccurHubs(parcel, prop) < 0.1)
            normOccurHubs(parcel, prop) = NaN;
        end
    end
end

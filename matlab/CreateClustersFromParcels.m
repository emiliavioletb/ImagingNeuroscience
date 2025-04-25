function Ci = CreateClustersFromParcels(atlasInfo)
% This function reads the table containing the atlas information from
% Schaeffer parcellation and returns the cluster assignment for each parcel
% based on the rsFC defined by Yeo et al. (2011)

Ci = zeros(height(atlasInfo), 1);   % create cluster assignment vector

for i = 1:8 % loop through all rsFC networks
    if i == 1
        net = atlasInfo(contains(atlasInfo.Network, 'ContA') | contains(atlasInfo.Network, 'ContB') | contains(atlasInfo.Network, 'ContC'),:);
    elseif i == 2
        net = atlasInfo(contains(atlasInfo.Network, 'DefaultA') | contains(atlasInfo.Network, 'DefaultB') | contains(atlasInfo.Network, 'DefaultC'),:);
    elseif i == 3
        net = atlasInfo(contains(atlasInfo.Network, 'DorsAttnA') | contains(atlasInfo.Network, 'DorsAttnB'),:);
    elseif i == 4
        net = atlasInfo(contains(atlasInfo.Network, 'LimbicA') | contains(atlasInfo.Network, 'LimbicB'),:);
    elseif i == 5
        net = atlasInfo(contains(atlasInfo.Network, 'SalVentAttnA') | contains(atlasInfo.Network, 'SalVentAttnB'),:);
    elseif i == 6
        net = atlasInfo(contains(atlasInfo.Network, 'SomMotA') | contains(atlasInfo.Network, 'SomMotB'),:);
    elseif i == 7
        net = atlasInfo(contains(atlasInfo.Network, 'TempPar'),:);
    elseif i == 8
        net = atlasInfo(contains(atlasInfo.Network, 'VisCent') | contains(atlasInfo.Network, 'VisPeri'),:);
    end
    C1 = table2array(net(:,1));
    Ci(C1) = i;
end

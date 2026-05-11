function report = svpwm_diagnostics(cfg, stopTime)
%SVPWM_DIAGNOSTICS Run repeatable diagnostics for a three-level SVPWM path.
%
% Recommended usage:
%   cfg = struct();
%   cfg.model = "YourModel";
%   cfg.stateBlock = "YourModel/SVPWM/Subsystem1";
%   cfg.gateBlock = "YourModel/SVPWM/Subsystem3";
%   cfg.voltageBlocks = ["YourModel/Va", "YourModel/Vb", "YourModel/Vc"];
%   cfg.gateTags = {'SA1','SA2','SA3','SA4','SB1','SB2','SB3','SB4','SC1','SC2','SC3','SC4'};
%   cfg.stopTime = "0.10";
%   cfg.analysisCycle = 0.02;
%   report = svpwm_diagnostics(cfg);
%
% Compatibility shortcut:
%   report = svpwm_diagnostics("YourModel", "0.10");
%
% The shortcut assumes conventional paths under YourModel/SVPWM and should be
% treated as a convenience only. For reusable workflows, pass cfg explicitly.

if nargin == 0
    error('svpwm_diagnostics:MissingConfig', ...
        'Pass a cfg struct with at least cfg.model, or pass a model name.');
end

if nargin >= 2
    stopTimeArg = stopTime;
else
    stopTimeArg = [];
end
cfg = localNormalizeCfg(cfg, nargin, stopTimeArg);
modelName = char(cfg.model);

open_system(modelName);
set_param(modelName, 'SimulationCommand', 'update');

report = struct();
report.model = modelName;
report.stopTime = char(cfg.stopTime);
report.config = cfg;

if strlength(string(cfg.referenceSubsystem)) > 0
    report.referenceSubsystemCommented = localGetParam(cfg.referenceSubsystem, 'Commented');
    report.referenceGotosAllOff = localCheckGotos(cfg.referenceSubsystem);
else
    report.referenceSubsystemCommented = "";
    report.referenceGotosAllOff = [];
end

localClearLogging(modelName);

if strlength(string(cfg.stateBlock)) > 0
    localLogOutport(cfg.stateBlock, cfg.statePort, 'State');
end
if strlength(string(cfg.gateBlock)) > 0
    localLogOutport(cfg.gateBlock, cfg.gatePort, 'SV_Gates');
end
if ~isempty(cfg.voltageBlocks)
    for k = 1:numel(cfg.voltageBlocks)
        localLogOutport(cfg.voltageBlocks(k), cfg.voltagePorts(k), cfg.voltageNames{k});
    end
end
localLogNamedBlocks(cfg.extraLogBlocks);
localLogRootFroms(modelName, cfg.rootFromSearchDepth);

in = Simulink.SimulationInput(modelName);
in = in.setModelParameter( ...
    'StopTime', char(cfg.stopTime), ...
    'SignalLogging', 'on', ...
    'SignalLoggingName', 'logsout');
out = sim(in);
logs = out.logsout;

if strlength(string(cfg.gateBlock)) > 0 && ~isempty(cfg.gateTags)
    [report.gateMismatchSamples, report.missingRootGateTags] = localCompareRootGates(logs, cfg.gateTags);
else
    report.gateMismatchSamples = [];
    report.missingRootGateTags = {};
end

if strlength(string(cfg.stateBlock)) > 0
    report.stateCounts = localStateCounts(logs.get('State').Values.Data);
else
    report.stateCounts = [];
end

if strlength(string(cfg.gateBlock)) > 0
    report.gateRows = localGateRows(logs.get('SV_Gates').Values.Data);
else
    report.gateRows = {};
end

if numel(cfg.voltageBlocks) == 3
    report.finalCycle = localVoltageStats(logs, str2double(string(cfg.stopTime)), cfg.analysisCycle, cfg.voltageNames);
else
    report.finalCycle = struct();
end

localPrintReport(report);
end

function cfg = localNormalizeCfg(inputCfg, narginValue, stopTimeArg)
if isstruct(inputCfg)
    cfg = inputCfg;
else
    cfg = struct();
    cfg.model = string(inputCfg);
    if narginValue >= 2
        cfg.stopTime = string(stopTimeArg);
    end
    cfg.svpwmSubsystem = cfg.model + "/SVPWM";
    cfg.stateBlock = cfg.svpwmSubsystem + "/Subsystem1";
    cfg.gateBlock = cfg.svpwmSubsystem + "/Subsystem3";
    cfg.voltageBlocks = strings(0, 1);
end

cfg = localDefault(cfg, 'stopTime', "0.10");
cfg = localDefault(cfg, 'analysisCycle', 0.02);
cfg = localDefault(cfg, 'svpwmSubsystem', "");
cfg = localDefault(cfg, 'stateBlock', "");
cfg = localDefault(cfg, 'statePort', 1);
cfg = localDefault(cfg, 'gateBlock', "");
cfg = localDefault(cfg, 'gatePort', 1);
cfg = localDefault(cfg, 'voltageBlocks', strings(0, 1));
cfg = localDefault(cfg, 'voltagePorts', []);
cfg = localDefault(cfg, 'voltageNames', {});
cfg = localDefault(cfg, 'gateTags', {'SA1','SA2','SA3','SA4','SB1','SB2','SB3','SB4','SC1','SC2','SC3','SC4'});
cfg = localDefault(cfg, 'referenceSubsystem', "");
cfg = localDefault(cfg, 'extraLogBlocks', struct('block', {}, 'port', {}, 'name', {}));
cfg = localDefault(cfg, 'rootFromSearchDepth', 1);

if ~isfield(cfg, 'model') || strlength(string(cfg.model)) == 0
    error('svpwm_diagnostics:MissingModel', 'cfg.model is required.');
end

cfg.model = string(cfg.model);
cfg.stopTime = string(cfg.stopTime);
cfg.stateBlock = string(cfg.stateBlock);
cfg.gateBlock = string(cfg.gateBlock);
cfg.referenceSubsystem = string(cfg.referenceSubsystem);
cfg.voltageBlocks = string(cfg.voltageBlocks);

if isempty(cfg.voltagePorts) && ~isempty(cfg.voltageBlocks)
    cfg.voltagePorts = ones(1, numel(cfg.voltageBlocks));
end
if isempty(cfg.voltageNames) && ~isempty(cfg.voltageBlocks)
    defaultNames = {'Va_out', 'Vb_out', 'Vc_out'};
    if numel(cfg.voltageBlocks) <= numel(defaultNames)
        cfg.voltageNames = defaultNames(1:numel(cfg.voltageBlocks));
    else
        cfg.voltageNames = arrayfun(@(k) sprintf('V%d_out', k), ...
            1:numel(cfg.voltageBlocks), 'UniformOutput', false);
    end
end

cfg.voltagePorts = double(cfg.voltagePorts);
cfg.voltageNames = cellstr(string(cfg.voltageNames));
cfg.gateTags = cellstr(string(cfg.gateTags));

if numel(cfg.voltagePorts) ~= numel(cfg.voltageBlocks)
    error('svpwm_diagnostics:VoltagePortCountMismatch', ...
        'cfg.voltagePorts must have one entry per cfg.voltageBlocks entry.');
end
if numel(cfg.voltageNames) ~= numel(cfg.voltageBlocks)
    error('svpwm_diagnostics:VoltageNameCountMismatch', ...
        'cfg.voltageNames must have one entry per cfg.voltageBlocks entry.');
end
if cfg.analysisCycle <= 0
    error('svpwm_diagnostics:InvalidAnalysisCycle', ...
        'cfg.analysisCycle must be positive.');
end
end

function cfg = localDefault(cfg, fieldName, value)
if ~isfield(cfg, fieldName) || isempty(cfg.(fieldName))
    cfg.(fieldName) = value;
end
end

function value = localGetParam(blockPath, paramName)
try
    value = get_param(char(blockPath), paramName);
catch
    value = "";
end
end

function ok = localCheckGotos(subsystemPath)
gotos = find_system(char(subsystemPath), ...
    'LookUnderMasks', 'all', ...
    'FollowLinks', 'on', ...
    'IncludeCommented', 'on', ...
    'BlockType', 'Goto');
ok = true;
for k = 1:numel(gotos)
    ok = ok && strcmp(get_param(gotos{k}, 'Commented'), 'off');
end
end

function localClearLogging(modelName)
lines = find_system(modelName, 'FindAll', 'on', 'Type', 'line');
for k = 1:numel(lines)
    try
        set_param(lines(k), 'DataLogging', 'off');
    catch
    end
end
end

function localLogOutport(blockPath, portIndex, logName)
handles = get_param(char(blockPath), 'PortHandles');
port = handles.Outport(portIndex);
set_param(port, 'DataLogging', 'on');
set_param(port, 'DataLoggingNameMode', 'Custom');
set_param(port, 'DataLoggingName', logName);
end

function localLogNamedBlocks(extraLogBlocks)
for k = 1:numel(extraLogBlocks)
    localLogOutport(extraLogBlocks(k).block, extraLogBlocks(k).port, extraLogBlocks(k).name);
end
end

function localLogRootFroms(modelName, searchDepth)
froms = find_system(modelName, 'SearchDepth', searchDepth, 'BlockType', 'From');
for k = 1:numel(froms)
    tag = get_param(froms{k}, 'GotoTag');
    name = get_param(froms{k}, 'Name');
    localLogOutport(froms{k}, 1, ['Root_' tag '_' name]);
end
end

function [mismatchSamples, missingTags] = localCompareRootGates(logs, gateTags)
svElement = logs.get('SV_Gates');
if isempty(svElement)
    error('svpwm_diagnostics:MissingLoggedSignal', ...
        'Logged signal SV_Gates was not found.');
end

svGates = localSignalMatrix(svElement.Values.Data, numel(gateTags));
if size(svGates, 1) ~= numel(gateTags)
    error('svpwm_diagnostics:GateDimensionMismatch', ...
        'SV_Gates has %d channels, but cfg.gateTags has %d entries.', ...
        size(svGates, 1), numel(gateTags));
end

rootGates = nan(numel(gateTags), size(svGates, 2));
missingTags = {};
names = logs.getElementNames;
for i = 1:numel(gateTags)
    prefix = ['Root_' char(gateTags{i}) '_'];
    found = false;
    for j = 1:numel(names)
        if startsWith(names{j}, prefix)
            rootData = localSignalMatrix(logs.get(names{j}).Values.Data, 1);
            if size(rootData, 2) ~= size(rootGates, 2)
                error('svpwm_diagnostics:GateSampleCountMismatch', ...
                    'Root gate %s has %d samples, but SV_Gates has %d samples.', ...
                    names{j}, size(rootData, 2), size(rootGates, 2));
            end
            rootGates(i,:) = rootData;
            found = true;
            break;
        end
    end
    if ~found
        missingTags{end + 1} = char(gateTags{i}); %#ok<AGROW>
    end
end

if ~isempty(missingTags)
    mismatchSamples = NaN;
else
    mismatchSamples = sum(any(abs(svGates - rootGates) > 1e-9, 1));
end
end

function counts = localStateCounts(stateData)
state = localSignalMatrix(stateData, 3).';
if size(state, 2) ~= 3
    error('svpwm_diagnostics:StateDimensionMismatch', ...
        'State must have 3 channels for [Sa Sb Sc].');
end
counts = zeros(3, 3);
for phase = 1:3
    for value = 0:2
        counts(phase, value + 1) = nnz(state(:, phase) == value);
    end
end
end

function rows = localGateRows(gateData)
gates = localSignalMatrix(gateData, 12);
if mod(size(gates, 1), 4) ~= 0
    error('svpwm_diagnostics:GateRowsNotGroupedByFour', ...
        'Gate output channel count must be divisible by 4.');
end
phaseCount = size(gates, 1) / 4;
rows = cell(phaseCount, 1);
for phase = 1:phaseCount
    phaseRows = gates((phase-1)*4 + (1:4), :).';
    [uniqueRows, ~, group] = unique(phaseRows, 'rows');
    rows{phase} = [uniqueRows accumarray(group, 1)];
end
end

function stats = localVoltageStats(logs, stopTime, cycle, voltageNames)
vaTs = logs.get(voltageNames{1}).Values;
vbTs = logs.get(voltageNames{2}).Values;
vcTs = logs.get(voltageNames{3}).Values;
t = vaTs.Time;
va = squeeze(vaTs.Data);
vb = squeeze(vbTs.Data);
vc = squeeze(vcTs.Data);

windowStart = max(0, stopTime - cycle);
idx = t >= windowStart & t < stopTime;
if ~any(idx)
    error('svpwm_diagnostics:NoSamplesInAnalysisWindow', ...
        'No voltage samples were found in the final analysis window.');
end

stats = struct();
stats.window = [windowStart stopTime];
stats.phaseRms = [localRms(va(idx)) localRms(vb(idx)) localRms(vc(idx))];
stats.lineRms = [localRms(va(idx)-vb(idx)) localRms(vb(idx)-vc(idx)) localRms(vc(idx)-va(idx))];
stats.sumRms = localRms(va(idx)+vb(idx)+vc(idx));
stats.phaseMean = [mean(va(idx)) mean(vb(idx)) mean(vc(idx))];
end

function value = localRms(x)
value = sqrt(mean(x(:).^2));
end

function data = localSignalMatrix(rawData, expectedChannels)
data = squeeze(rawData);
if isempty(data)
    data = zeros(expectedChannels, 0);
elseif isvector(data)
    data = data(:).';
elseif nargin >= 2 && expectedChannels > 0
    if size(data, 1) == expectedChannels
        % Already channels x samples.
    elseif size(data, 2) == expectedChannels
        data = data.';
    end
end
end

function localPrintReport(report)
fprintf('\nSVPWM diagnostics for %s\n', report.model);
fprintf('  StopTime: %s s\n', report.stopTime);
if strlength(string(report.referenceSubsystemCommented)) > 0
    fprintf('  Reference subsystem Commented: %s\n', report.referenceSubsystemCommented);
    fprintf('  Reference internal Gotos all off: %d\n', report.referenceGotosAllOff);
end
if ~isempty(report.gateMismatchSamples)
    if isnan(report.gateMismatchSamples)
        fprintf('  Root gate mismatch samples: not computed\n');
    else
        fprintf('  Root gate mismatch samples: %d\n', report.gateMismatchSamples);
    end
end
if isfield(report, 'missingRootGateTags') && ~isempty(report.missingRootGateTags)
    fprintf('  Missing root gate tags: %s\n', strjoin(report.missingRootGateTags, ', '));
end
if isfield(report, 'finalCycle') && isfield(report.finalCycle, 'window')
    fprintf('  Final window: %.6f to %.6f s\n', report.finalCycle.window(1), report.finalCycle.window(2));
    fprintf('  Phase RMS: %.6g %.6g %.6g\n', report.finalCycle.phaseRms);
    fprintf('  Line RMS: %.6g %.6g %.6g\n', report.finalCycle.lineRms);
    fprintf('  Va+Vb+Vc RMS: %.6g\n', report.finalCycle.sumRms);
end
if ~isempty(report.stateCounts)
    fprintf('\nState counts [N O P] by phase:\n');
    disp(report.stateCounts);
end
end

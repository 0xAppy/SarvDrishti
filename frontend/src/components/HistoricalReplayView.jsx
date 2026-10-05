import React, { useState } from 'react';
import { Upload, Play, CheckCircle2, RotateCcw, FileText, Database } from 'lucide-react';

export default function HistoricalReplayView() {
  const [file, setFile] = useState(null);
  const [sourceId, setSourceId] = useState('src-historical');
  const [replayState, setReplayState] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleStartReplay = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('source_id', sourceId);

    try {
      const res = await fetch('/api/replay/upload', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setReplayState(data);
      pollStatus(data.replay_id);
    } catch (err) {
      console.error(err);
      setLoading(false);
    }
  };

  const pollStatus = (replayId) => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch(`/api/replay/status/${replayId}`);
        const data = await res.json();
        setReplayState(data);
        if (data.status === 'completed') {
          clearInterval(interval);
          setLoading(false);
        }
      } catch (err) {
        clearInterval(interval);
        setLoading(false);
      }
    }, 500);
  };

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Database className="w-4 h-4 text-accentCyan" /> HISTORICAL BATCH INGESTION
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Offline Log Archive Replay & Analysis</p>
        </div>
      </div>

      <div className="flex-1 bg-darkBg border border-darkBorder rounded p-4 flex flex-col justify-start max-w-3xl space-y-6">
        
        {/* Setup Configuration */}
        <div className="space-y-4">
          <h3 className="text-xs font-semibold text-textMuted uppercase tracking-wider border-b border-darkBorder pb-2">Batch Replay Configuration</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* File Selection */}
            <div className="bg-darkPanel border border-darkBorder rounded p-3 flex flex-col justify-between">
              <div>
                <label className="text-[10px] font-mono text-textMuted uppercase block font-bold mb-1">
                  1. Source Log Archive
                </label>
                <div className="text-[10px] text-textMuted font-mono mb-2">Upload raw unparsed logs.</div>
              </div>
              <input
                type="file"
                onChange={handleFileChange}
                className="w-full text-[10px] font-mono text-textMuted file:mr-2 file:py-1 file:px-2 file:rounded file:border file:border-darkBorder file:text-[10px] file:font-bold file:uppercase file:bg-darkHover file:text-textMain hover:file:bg-darkBorder cursor-pointer transition-colors"
              />
              {file && (
                <div className="mt-2 text-[10px] font-mono text-statusGood flex items-center gap-1">
                  <FileText className="w-3 h-3" /> {file.name} ({Math.round(file.size / 1024)} KB)
                </div>
              )}
            </div>

            {/* Ingestion Stream */}
            <div className="bg-darkPanel border border-darkBorder rounded p-3 flex flex-col justify-between">
              <div>
                <label className="text-[10px] font-mono text-textMuted uppercase block font-bold mb-1">
                  2. Target Broker Topic / Source ID
                </label>
                <div className="text-[10px] text-textMuted font-mono mb-2">Assign to existing pipeline.</div>
              </div>
              <select
                value={sourceId}
                onChange={(e) => setSourceId(e.target.value)}
                className="w-full p-1.5 bg-darkBg border border-darkBorder rounded text-[10px] font-mono text-textMain focus:outline-none focus:border-accentCyan transition-colors"
              >
                <option value="src-firewall-01">src-firewall-01 (Firewall)</option>
                <option value="src-syslog-live">src-syslog-live (Syslog)</option>
                <option value="src-webapp-01">src-webapp-01 (App Server)</option>
                <option value="src-historical">src-historical (Default Offline)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div className="pt-2">
          <button
            onClick={handleStartReplay}
            disabled={!file || loading}
            className="flex items-center gap-2 px-4 py-2 bg-accentCyan hover:bg-accentBlue text-white rounded text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Play className="w-3.5 h-3.5" /> {loading ? 'Streaming Batch...' : 'Initiate Batch Replay'}
          </button>
        </div>

        {/* Telemetry Display */}
        {replayState && (
          <div className="mt-4 bg-darkPanel border border-darkBorder rounded p-4 space-y-3">
            <div className="flex items-center justify-between text-[10px] font-mono uppercase font-bold">
              <span className={replayState.status === 'completed' ? 'text-statusGood' : 'text-accentCyan animate-pulse'}>
                STATUS: {replayState.status}
              </span>
              <span className="text-textMuted">
                {replayState.processed_lines} / {replayState.total_lines} RECORDS
              </span>
            </div>

            <div className="w-full h-1.5 bg-darkBg rounded-full overflow-hidden border border-darkBorder relative">
              <div 
                className={`h-full transition-all duration-300 ${replayState.status === 'completed' ? 'bg-statusGood' : 'bg-accentCyan'}`}
                style={{ width: `${replayState.progress_percent}%` }}
              />
            </div>

            <div className="flex justify-between items-center text-[10px] font-mono">
              <span className="text-textMuted">{replayState.progress_percent}% PROGRESS</span>
              {replayState.status === 'completed' && (
                <span className="text-statusGood flex items-center gap-1">
                  <CheckCircle2 className="w-3 h-3" /> Replay Pipeline Offline
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { 
  Play, CheckCircle2, XCircle, Terminal, Radio, FileText, 
  Send, Zap, RefreshCw, Sliders, ShieldAlert, Cpu, Check, AlertTriangle
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

export default function TestingSandboxView() {
  // --- Pytest Runner State ---
  const [runningTests, setRunningTests] = useState(false);
  const [testResult, setTestResult] = useState(null);

  // --- Synthetic Log Generator State ---
  const [genMode, setGenMode] = useState('api');
  const [genCount, setGenCount] = useState(50);
  const [genFilename, setGenFilename] = useState('sample_historical.log');
  const [generatingLogs, setGeneratingLogs] = useState(false);
  const [genOutput, setGenOutput] = useState(null);

  // --- Synthetic Live Stream Generator State ---
  const [liveStatus, setLiveStatus] = useState({ is_running: false, delay: 1.5 });
  const [liveDelay, setLiveDelay] = useState(1.5);
  const [togglingStream, setTogglingStream] = useState(false);

  // --- Real Machine Journalctl Stream State ---
  const [journalctlStatus, setJournalctlStatus] = useState({ is_running: false });
  const [togglingJournalctl, setTogglingJournalctl] = useState(false);

  // --- Real System Log State ---
  const [sendingRealLogs, setSendingRealLogs] = useState(false);
  const [realLogsOutput, setRealLogsOutput] = useState(null);

  // Fetch initial live stream status
  useEffect(() => {
    fetchLiveStreamStatus();
    fetchJournalctlStreamStatus();
    const interval = setInterval(() => {
      fetchLiveStreamStatus();
      fetchJournalctlStreamStatus();
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchJournalctlStreamStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/testing/journalctl-stream/status`);
      if (res.ok) {
        const data = await res.json();
        setJournalctlStatus(data);
      }
    } catch (e) {
      console.error('Failed to fetch journalctl stream status:', e);
    }
  };

  const fetchLiveStreamStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/testing/live-stream/status`);
      if (res.ok) {
        const data = await res.json();
        setLiveStatus(data);
      }
    } catch (e) {
      console.error('Failed to fetch live stream status:', e);
    }
  };

  // Run Pytest Suite
  const handleRunTests = async () => {
    setRunningTests(true);
    setTestResult(null);
    try {
      const res = await fetch(`${API_BASE}/api/testing/run-tests`, { method: 'POST' });
      const data = await res.json();
      setTestResult(data);
    } catch (e) {
      setTestResult({
        status: 'error',
        metrics: { passed: 0, failed: 1, skipped: 0, total: 1 },
        output: `Error connecting to backend testing endpoint: ${e.message}`
      });
    } finally {
      setRunningTests(false);
    }
  };

  // Generate Synthetic Logs
  const handleGenerateLogs = async () => {
    setGeneratingLogs(true);
    setGenOutput(null);
    try {
      const res = await fetch(`${API_BASE}/api/testing/generate-logs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode: genMode, count: Number(genCount), filename: genFilename })
      });
      const data = await res.json();
      setGenOutput(data);
    } catch (e) {
      setGenOutput({ status: 'error', output: `Log generation failed: ${e.message}` });
    } finally {
      setGeneratingLogs(false);
    }
  };

  // Toggle Live Stream
  const handleToggleLiveStream = async (action) => {
    setTogglingStream(true);
    try {
      const res = await fetch(`${API_BASE}/api/testing/live-stream/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action, delay: Number(liveDelay) })
      });
      if (res.ok) {
        await fetchLiveStreamStatus();
      }
    } catch (e) {
      console.error('Failed to toggle live stream:', e);
    } finally {
      setTogglingStream(false);
    }
  };

  // Toggle Journalctl Stream
  const handleToggleJournalctlStream = async (action) => {
    setTogglingJournalctl(true);
    try {
      const res = await fetch(`${API_BASE}/api/testing/journalctl-stream/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action })
      });
      if (res.ok) {
        await fetchJournalctlStreamStatus();
      }
    } catch (e) {
      console.error('Failed to toggle journalctl stream:', e);
    } finally {
      setTogglingJournalctl(false);
    }
  };

  // Send Real Laptop / System Security Logs
  const handleSendRealLogs = async () => {
    setSendingRealLogs(true);
    setRealLogsOutput(null);
    try {
      const res = await fetch(`${API_BASE}/api/testing/send-real-logs`, { method: 'POST' });
      const data = await res.json();
      setRealLogsOutput(data);
    } catch (e) {
      setRealLogsOutput({ status: 'error', output: `Sending real system logs failed: ${e.message}` });
    } finally {
      setSendingRealLogs(false);
    }
  };

  return (
    <div className="flex flex-col h-full space-y-4">
      {/* Header Banner */}
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Cpu className="w-4 h-4 text-accentCyan" /> TESTING SANDBOX & SIMULATION
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">
            Execute unit tests, generate synthetic logs, and trigger live data streams.
          </p>
        </div>
        <div className="text-[10px] font-mono text-textMuted uppercase font-bold border border-darkBorder px-2 py-1 rounded">
          TEST ENVIRONMENT
        </div>
      </div>

      {/* Grid Layout: Top 2 Panels */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        
        {/* Panel 1: Pytest Test Suite Runner */}
        <div className="bg-darkBg border border-darkBorder rounded p-4 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-darkBorder pb-2">
            <h3 className="text-xs font-semibold text-textMain uppercase flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5 text-accentCyan" /> Backend Pytest Suite
            </h3>
            {testResult && (
              <span className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                testResult.status === 'success' ? 'bg-statusGood/10 text-statusGood' : 'bg-statusError/10 text-statusError'
              }`}>
                {testResult.status === 'success' ? 'PASSING' : 'FAILED'}
              </span>
            )}
          </div>

          <div className="flex-1 flex flex-col justify-end space-y-4 min-h-0">
            {/* Test Metrics Display */}
            {testResult?.metrics && (
              <div className="grid grid-cols-4 gap-2">
                <div className="bg-darkPanel border border-darkBorder p-2 rounded text-center">
                  <div className="text-[10px] text-textMuted font-mono uppercase">Total</div>
                  <div className="text-sm font-bold text-textMain font-mono">{testResult.metrics.total}</div>
                </div>
                <div className="bg-darkPanel border border-statusGood/30 p-2 rounded text-center">
                  <div className="text-[10px] text-statusGood font-mono uppercase">Passed</div>
                  <div className="text-sm font-bold text-statusGood font-mono">{testResult.metrics.passed}</div>
                </div>
                <div className="bg-darkPanel border border-statusError/30 p-2 rounded text-center">
                  <div className="text-[10px] text-statusError font-mono uppercase">Failed</div>
                  <div className="text-sm font-bold text-statusError font-mono">{testResult.metrics.failed}</div>
                </div>
                <div className="bg-darkPanel border border-darkBorder p-2 rounded text-center">
                  <div className="text-[10px] text-textMuted font-mono uppercase">Skipped</div>
                  <div className="text-sm font-bold text-textMuted font-mono">{testResult.metrics.skipped}</div>
                </div>
              </div>
            )}

            {/* Terminal Console Output */}
            {testResult?.output && (
              <div className="bg-darkPanel p-2 rounded border border-darkBorder font-mono text-[10px] text-textMuted max-h-32 overflow-y-auto whitespace-pre-wrap">
                {testResult.output}
              </div>
            )}

            <button
              onClick={handleRunTests}
              disabled={runningTests}
              className="w-full flex items-center justify-center gap-1.5 py-2 rounded bg-darkHover hover:bg-darkBorder border border-darkBorder text-textMain text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
            >
              {runningTests ? (
                <><RefreshCw className="w-3 h-3 animate-spin text-accentCyan" /> Executing Pytest Suite...</>
              ) : (
                <><Play className="w-3 h-3 text-accentCyan" /> Run Pytest Suite</>
              )}
            </button>
          </div>
        </div>

        {/* Panel 2: Synthetic Log Generator */}
        <div className="bg-darkBg border border-darkBorder rounded p-4 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-darkBorder pb-2">
            <h3 className="text-xs font-semibold text-textMain uppercase flex items-center gap-2">
              <Sliders className="w-3.5 h-3.5 text-accentCyan" /> Synthetic Log Generator
            </h3>
          </div>

          <div className="space-y-4 flex-1 flex flex-col justify-end min-h-0">
            {/* Mode selection buttons */}
            <div>
              <label className="text-[10px] font-mono text-textMuted uppercase font-bold block mb-1">Ingestion Mode</label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: 'api', label: 'REST API', icon: Send },
                  { id: 'syslog', label: 'Syslog UDP', icon: Radio },
                  { id: 'file', label: 'File', icon: FileText },
                ].map((item) => {
                  const Icon = item.icon;
                  const isSelected = genMode === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setGenMode(item.id)}
                      className={`flex items-center justify-center gap-1.5 py-1.5 px-2 rounded text-[10px] font-mono font-bold transition-all border ${
                        isSelected
                          ? 'bg-darkHover border-accentCyan text-accentCyan'
                          : 'bg-darkPanel border-darkBorder text-textMuted hover:text-textMain hover:bg-darkHover'
                      }`}
                    >
                      <Icon className="w-3 h-3" /> {item.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Event Count Slider */}
            <div>
              <div className="flex justify-between items-center text-[10px] font-mono text-textMuted uppercase mb-1">
                <span>Record Count</span>
                <span className="text-textMain font-bold">{genCount}</span>
              </div>
              <input
                type="range"
                min="5"
                max="200"
                step="5"
                value={genCount}
                onChange={(e) => setGenCount(e.target.value)}
                className="w-full accent-accentCyan bg-darkPanel h-1 rounded cursor-pointer"
              />
            </div>

            {/* File name input if file mode */}
            {genMode === 'file' && (
              <div>
                <label className="text-[10px] font-mono text-textMuted uppercase font-bold block mb-1">Target Filename</label>
                <input
                  type="text"
                  value={genFilename}
                  onChange={(e) => setGenFilename(e.target.value)}
                  className="w-full bg-darkPanel border border-darkBorder rounded px-2 py-1.5 text-[10px] font-mono text-textMain focus:outline-none focus:border-accentCyan"
                />
              </div>
            )}

            {/* Generator output banner */}
            {genOutput && (
              <div className={`p-2 rounded border text-[10px] font-mono ${
                genOutput.status === 'success'
                  ? 'bg-statusGood/10 text-statusGood border-statusGood/30'
                  : 'bg-statusError/10 text-statusError border-statusError/30'
              }`}>
                {genOutput.output || 'Log generation completed successfully.'}
              </div>
            )}

            <button
              onClick={handleGenerateLogs}
              disabled={generatingLogs}
              className="w-full flex items-center justify-center gap-1.5 py-2 rounded bg-darkHover hover:bg-darkBorder border border-darkBorder text-textMain text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
            >
              {generatingLogs ? (
                <><RefreshCw className="w-3 h-3 animate-spin text-accentCyan" /> Generating...</>
              ) : (
                <><Zap className="w-3 h-3 text-accentCyan" /> Generate {genCount} Synthetic Logs</>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Grid Layout: Bottom 2 Panels */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">

        {/* Panel 3: Synthetic Continuous Streamer */}
        <div className="bg-darkBg border border-darkBorder rounded p-4 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-darkBorder pb-2">
            <h3 className="text-xs font-semibold text-textMain uppercase flex items-center gap-2">
              <Radio className="w-3.5 h-3.5 text-accentCyan" /> Synthetic Live Stream
            </h3>
            <div className="flex items-center gap-1.5">
              <span className={`w-2 h-2 rounded-full ${
                liveStatus.is_running ? 'bg-statusGood animate-pulse' : 'bg-darkBorder'
              }`} />
              <span className="text-[10px] font-mono text-textMuted uppercase font-bold">
                {liveStatus.is_running ? 'STREAMING' : 'IDLE'}
              </span>
            </div>
          </div>

          <div className="flex-1 flex flex-col justify-end space-y-4 min-h-0">
            <div className="bg-darkPanel p-3 rounded border border-darkBorder space-y-3">
              <div className="flex items-center justify-between text-[10px] font-mono text-textMuted uppercase">
                <span>Interval Delay</span>
                <span className="text-textMain font-bold">{liveDelay} sec</span>
              </div>
              <input
                type="range"
                min="0.5"
                max="5.0"
                step="0.5"
                value={liveDelay}
                disabled={liveStatus.is_running}
                onChange={(e) => setLiveDelay(e.target.value)}
                className="w-full accent-accentCyan bg-darkBg h-1 rounded cursor-pointer disabled:opacity-50"
              />
              
              <div className="text-[10px] font-mono text-textMuted grid grid-cols-2 gap-2 pt-2 border-t border-darkBorder">
                <div>UDP Syslog: <span className="text-textMain">127.0.0.1:5140</span></div>
                <div>REST API: <span className="text-textMain">/api/events/ingest</span></div>
              </div>
            </div>

            {liveStatus.is_running ? (
              <button
                onClick={() => handleToggleLiveStream('stop')}
                disabled={togglingStream}
                className="w-full flex items-center justify-center gap-1.5 py-2 rounded bg-statusError/20 hover:bg-statusError/30 border border-statusError/40 text-statusError text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
              >
                {togglingStream ? <RefreshCw className="w-3 h-3 animate-spin" /> : <XCircle className="w-3 h-3" />}
                Stop Live Stream
              </button>
            ) : (
              <button
                onClick={() => handleToggleLiveStream('start')}
                disabled={togglingStream}
                className="w-full flex items-center justify-center gap-1.5 py-2 rounded bg-accentCyan hover:bg-accentBlue text-white text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
              >
                {togglingStream ? <RefreshCw className="w-3 h-3 animate-spin" /> : <Radio className="w-3 h-3" />}
                Start Continuous Stream ({liveDelay}s)
              </button>
            )}
          </div>
        </div>

        {/* Panel 4: Real Host System Log Injector */}
        <div className="bg-darkBg border border-darkBorder rounded p-4 flex flex-col space-y-4">
          <div className="flex items-center justify-between border-b border-darkBorder pb-2">
            <h3 className="text-xs font-semibold text-textMain uppercase flex items-center gap-2">
              <ShieldAlert className="w-3.5 h-3.5 text-statusWarn" /> Real Host Journalctl Injection
            </h3>
          </div>

          <div className="flex-1 flex flex-col justify-end space-y-4 min-h-0">
            <div className="bg-darkPanel p-3 rounded border border-darkBorder text-[10px] font-mono space-y-2 text-textMuted uppercase">
              <div className="flex items-center gap-2 text-statusWarn font-bold">
                <Check className="w-3 h-3" /> ACTUAL OS Logs (`journalctl`)
              </div>
              <ul className="list-disc list-inside space-y-1">
                <li>Netfilter Firewall Allow/Deny</li>
                <li>SSH Auth Events</li>
                <li>Systemd / Kernel Logs</li>
                <li>Web Access Events</li>
              </ul>
            </div>

            <div className="flex flex-col gap-3">
               <div className="flex items-center justify-between bg-darkPanel border border-darkBorder rounded p-2">
                 <div className="flex flex-col">
                   <span className="text-[10px] font-bold text-textMain uppercase font-mono">Live Stream</span>
                   <span className="text-[10px] text-textMuted font-mono uppercase">`journalctl -f`</span>
                 </div>
                 
                 {journalctlStatus.is_running ? (
                    <button
                      onClick={() => handleToggleJournalctlStream('stop')}
                      disabled={togglingJournalctl}
                      className="flex items-center gap-1.5 py-1.5 px-3 rounded bg-statusError/20 text-statusError hover:bg-statusError/30 border border-statusError/40 font-bold text-[10px] font-mono uppercase transition-colors disabled:opacity-50"
                    >
                      {togglingJournalctl ? <RefreshCw className="w-3 h-3 animate-spin" /> : <XCircle className="w-3 h-3" />}
                      Stop
                    </button>
                  ) : (
                    <button
                      onClick={() => handleToggleJournalctlStream('start')}
                      disabled={togglingJournalctl}
                      className="flex items-center gap-1.5 py-1.5 px-3 rounded bg-statusGood/20 text-statusGood hover:bg-statusGood/30 border border-statusGood/40 font-bold text-[10px] font-mono uppercase transition-colors disabled:opacity-50"
                    >
                      {togglingJournalctl ? <RefreshCw className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}
                      Start
                    </button>
                  )}
               </div>

              <button
                onClick={handleSendRealLogs}
                disabled={sendingRealLogs}
                className="w-full flex items-center justify-center gap-1.5 py-2 rounded bg-darkHover hover:bg-darkBorder border border-darkBorder text-textMain text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
              >
                {sendingRealLogs ? (
                  <><RefreshCw className="w-3 h-3 animate-spin" /> Injecting Batch...</>
                ) : (
                  <><Send className="w-3 h-3" /> Inject One-Off Batch</>
                )}
              </button>
            </div>
            
            {realLogsOutput && (
              <div className="bg-darkPanel p-2 rounded border border-darkBorder font-mono text-[10px] text-textMuted max-h-24 overflow-y-auto whitespace-pre-wrap">
                {realLogsOutput.output || 'Host logs injected successfully.'}
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

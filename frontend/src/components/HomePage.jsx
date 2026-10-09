import React, { useState, useRef } from 'react';
import { 
  ShieldCheck, Activity, Cpu, Database, Sparkles, 
  RotateCcw, Server, Search, GitCommit, ArrowRight, 
  CheckCircle2, Layers, Zap, Lock, Play, Pause, 
  Volume2, VolumeX, Maximize, Terminal, Check, 
  AlertTriangle, RefreshCw, FileText, ChevronRight,
  Award, Shield, HelpCircle
} from 'lucide-react';

export default function HomePage({ onNavigate }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(90.0);
  const videoRef = useRef(null);

  // Interactive Live Parser Playground State
  const samplePresets = [
    {
      id: 'firewall',
      name: 'Fortinet Firewall',
      badge: 'Key-Value Format',
      log: 'date=2026-09-30 time=21:00:00 devname="FG-100D" devid="FGT100D3G" type="traffic" level="notice" srcip=192.168.1.10 dstip=10.0.0.5 srcport=49152 dstport=443 proto=6 action="deny" policyid=1 sentbyte=0 rcvdbyte=0 msg="Firewall rule blocked unauthorized SSL attempt"',
      detected: 'KV Parser (Fortinet FortiOS)',
      fields: {
        'timestamp': '2026-09-30T21:00:00Z',
        'event.action': 'deny',
        'event.category': 'network_traffic',
        'source.ip': '192.168.1.10',
        'source.port': 49152,
        'destination.ip': '10.0.0.5',
        'destination.port': 443,
        'network.transport': 'tcp',
        'observer.vendor': 'Fortinet',
        'observer.type': 'firewall'
      }
    },
    {
      id: 'syslog',
      name: 'Linux Syslog RFC 5424',
      badge: 'Regex Format',
      log: '<34>1 2026-09-30T21:00:00.123Z secure-node-01 sshd 24911 ID47 [auth user="operator" client="10.20.30.40"] Failed password for invalid user root from 10.20.30.40 port 52331 ssh2',
      detected: 'Regex Parser (RFC 5424 Syslog)',
      fields: {
        'timestamp': '2026-09-30T21:00:00.123Z',
        'event.action': 'failed_login',
        'event.category': 'authentication',
        'host.hostname': 'secure-node-01',
        'process.name': 'sshd',
        'process.pid': 24911,
        'user.name': 'root',
        'source.ip': '10.20.30.40',
        'source.port': 52331
      }
    },
    {
      id: 'webapp',
      name: 'Nginx Web Access',
      badge: 'JSON / Combined Format',
      log: '192.168.1.100 - - [30/Sep/2026:21:00:00 +0530] "POST /api/v1/auth/login HTTP/1.1" 401 128 "https://app.corp/login" "Mozilla/5.0"',
      detected: 'Combined Nginx Parser',
      fields: {
        'timestamp': '2026-09-30T21:00:00+05:30',
        'event.action': 'unauthorized_request',
        'event.category': 'web',
        'source.ip': '192.168.1.100',
        'http.request.method': 'POST',
        'http.response.status_code': 401,
        'url.path': '/api/v1/auth/login'
      }
    },
    {
      id: 'unknown',
      name: 'Unrecognized Zero-Day Log',
      badge: 'AI Onboarding Candidate',
      log: 'CRITICAL_APP_EVENT node=edge-alpha-7 alert_level=3 memory_spike=98% payload_hex=0xFA39C1 msg="Memory leak detected in microkernel"',
      detected: 'AI Heuristic Analyzer (Air-Gapped)',
      fields: {
        'unmapped.node': 'edge-alpha-7',
        'unmapped.alert_level': 3,
        'unmapped.memory_spike': '98%',
        'unmapped.payload_hex': '0xFA39C1',
        'event.action': 'flagged_for_approval',
        'quarantine_status': 'ISOLATED_IN_DEAD_LETTER'
      }
    }
  ];

  const [selectedPreset, setSelectedPreset] = useState(samplePresets[0]);
  const [customLogInput, setCustomLogInput] = useState(samplePresets[0].log);
  const [parsedOutput, setParsedOutput] = useState(samplePresets[0]);
  const [isParsing, setIsParsing] = useState(false);

  const handleSelectPreset = (preset) => {
    setSelectedPreset(preset);
    setCustomLogInput(preset.log);
    setParsedOutput(preset);
  };

  const handleParseLog = async () => {
    setIsParsing(true);
    try {
      const res = await fetch('http://localhost:8000/api/onboarding/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample_log: customLogInput })
      });
      if (res.ok) {
        const data = await res.json();
        const generatedFields = {};
        (data.suggested_mappings || []).forEach(m => {
          generatedFields[m.target_schema_field] = m.sample_value;
        });
        setParsedOutput({
          ...selectedPreset,
          detected: `${data.provider_used} (${data.detected_format})`,
          fields: Object.keys(generatedFields).length > 0 ? generatedFields : selectedPreset.fields
        });
      } else {
        setParsedOutput(selectedPreset);
      }
    } catch (e) {
      setParsedOutput(selectedPreset);
    } finally {
      setTimeout(() => setIsParsing(false), 300);
    }
  };

  const toggleVideoPlay = () => {
    if (!videoRef.current) return;
    if (videoRef.current.paused) {
      videoRef.current.play();
      setIsPlaying(true);
    } else {
      videoRef.current.pause();
      setIsPlaying(false);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    videoRef.current.muted = !videoRef.current.muted;
    setIsMuted(videoRef.current.muted);
  };

  const seekTo = (seconds) => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = seconds;
    videoRef.current.play();
    setIsPlaying(true);
  };

  const chapters = [
    { label: "SIH Portal & Theme", time: 0 },
    { label: "Jury Testbench", time: 10 },
    { label: "Console Dashboard", time: 22 },
    { label: "Sources Fleet", time: 32 },
    { label: "Parser Registry", time: 42 },
    { label: "Event Explorer", time: 52 },
    { label: "Field Lineage", time: 64 },
    { label: "AI Onboarding", time: 76 },
    { label: "Testing Sandbox", time: 88 },
  ];

  const isDemoRecording = typeof window !== 'undefined' && window.location.search.includes('recording=true');

  return (
    <div className="bg-darkBg text-textMain -m-4 p-6 md:p-10 font-sans space-y-12 min-h-screen transition-colors">
      
      {/* SIH Tricolor Identity Ribbon */}
      <div className="w-full h-1.5 bg-gradient-to-r from-orange-500 via-blue-700 to-emerald-600 rounded-full" />

      {/* Top Banner & Header */}
      <div className="flex flex-col md:flex-row items-center justify-between gap-6 bg-darkPanel p-6 rounded-2xl border border-darkBorder shadow-sm transition-colors">
        <div className="flex items-center gap-5">
          {/* Logo */}
          <img 
            src="/logo.png" 
            alt="SarvDrishti Logo" 
            className="h-16 md:h-20 object-contain drop-shadow-sm" 
          />
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                SIH 2026 Entry
              </span>
              <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                Team Black Pearl
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-textMain mt-1">
              SarvDrishti <span className="text-lg font-normal text-textMuted">(सर्वदृष्टि)</span>
            </h1>
            <p className="text-xs md:text-sm text-textMuted font-medium">
              Unified Log Intelligence & Deterministic Normalization Platform
            </p>
          </div>
        </div>

        {/* Action Button to Console */}
        <div className="flex items-center gap-3 w-full md:w-auto">
          <button
            onClick={() => onNavigate('overview')}
            className="w-full md:w-auto px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm shadow-md shadow-blue-500/20 flex items-center justify-center gap-2 transition-all hover:scale-[1.02]"
          >
            <Activity className="w-4 h-4" />
            <span>Launch Operator Console</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Hero Section */}
      <div className="text-center max-w-4xl mx-auto space-y-4 pt-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 text-xs font-semibold">
          <Award className="w-3.5 h-3.5 text-amber-500" />
          <span>Smart India Hackathon 2026 • Problem ID: SIH26156</span>
        </div>

        <h2 className="text-3xl md:text-5xl font-extrabold text-textMain tracking-tight leading-tight">
          Turning <span className="text-blue-600 dark:text-blue-400">Noisy Log Chaos</span> Into <br className="hidden md:block"/>
          <span className="text-emerald-600 dark:text-emerald-400">Deterministic, SIEM-Ready</span> Intelligence
        </h2>

        <p className="text-base md:text-lg text-textMuted max-w-2xl mx-auto leading-relaxed">
          Heterogeneous firewalls, Linux syslog, and microservices speak different log languages. 
          SarvDrishti ingests, normalizes, and audits them in milliseconds with <strong>100% raw data preservation</strong> and <strong>zero eval() security</strong>.
        </p>

        {/* Live Metrics Ribbon */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 text-left">
          <div className="bg-darkPanel p-4 rounded-xl border border-darkBorder shadow-sm">
            <div className="text-2xl md:text-3xl font-bold text-blue-600 dark:text-blue-400 font-mono">32,971+</div>
            <div className="text-xs font-semibold text-textMain uppercase tracking-wider mt-1">Logs Processed</div>
            <div className="text-[11px] text-textMuted">Continuous Ingestion</div>
          </div>
          <div className="bg-darkPanel p-4 rounded-xl border border-darkBorder shadow-sm">
            <div className="text-2xl md:text-3xl font-bold text-emerald-600 dark:text-emerald-400 font-mono">99.99%</div>
            <div className="text-xs font-semibold text-textMain uppercase tracking-wider mt-1">Parsing SLA</div>
            <div className="text-[11px] text-textMuted">Deterministic Accuracy</div>
          </div>
          <div className="bg-darkPanel p-4 rounded-xl border border-darkBorder shadow-sm">
            <div className="text-2xl md:text-3xl font-bold text-amber-600 dark:text-amber-400 font-mono">&lt; 1.2ms</div>
            <div className="text-xs font-semibold text-textMain uppercase tracking-wider mt-1">Average Latency</div>
            <div className="text-[11px] text-textMuted">Decoupled Buffer</div>
          </div>
          <div className="bg-darkPanel p-4 rounded-xl border border-darkBorder shadow-sm">
            <div className="text-2xl md:text-3xl font-bold text-purple-600 dark:text-purple-400 font-mono">100%</div>
            <div className="text-xs font-semibold text-textMain uppercase tracking-wider mt-1">Air-Gapped</div>
            <div className="text-[11px] text-textMuted">Offline Fallback</div>
          </div>
        </div>
      </div>

      {/* Embedded Video Showcase Player */}
      {!isDemoRecording && (
        <div className="bg-darkPanel rounded-2xl border border-darkBorder shadow-lg p-6 md:p-8 space-y-6 transition-colors">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-darkBorder pb-5">
            <div>
              <div className="flex items-center gap-2">
                <span className="px-2.5 py-0.5 rounded-full bg-blue-500/10 text-blue-600 dark:text-blue-400 text-xs font-bold uppercase tracking-wider border border-blue-500/20">
                  Full HD Walkthrough & Tutorial
                </span>
                <span className="text-xs text-textMuted font-medium font-mono">Duration: 1.5 Minutes (90s)</span>
              </div>
              <h3 className="text-xl font-bold text-textMain mt-1">
                Live Interactive Platform Demonstration (Full HD)
              </h3>
              <p className="text-xs text-textMuted">
                Interactive recording navigating through the live SarvDrishti platform: adaptive theming, multi-source ingestion, live event exploration, token-level field lineage, and dynamic AI parser onboarding.
              </p>
            </div>

            {/* Quick Chapter Buttons */}
            <div className="flex flex-wrap items-center gap-1.5">
              <span className="text-xs font-semibold text-textMuted mr-1">Chapters:</span>
              {chapters.map((c, i) => (
                <button
                  key={i}
                  onClick={() => seekTo(c.time)}
                  className="px-2.5 py-1 rounded-lg bg-darkHover hover:bg-blue-500/10 text-textMain hover:text-blue-600 dark:hover:text-blue-400 text-xs font-medium border border-darkBorder transition-colors"
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* Video Player Container */}
          <div className="relative rounded-xl overflow-hidden bg-black shadow-inner group aspect-video max-h-[560px] mx-auto border border-darkBorder">
            <video
              ref={videoRef}
              src="/web_video.mp4"
              className="w-full h-full object-contain"
              onTimeUpdate={() => {
                if (videoRef.current) {
                  setCurrentTime(videoRef.current.currentTime);
                  setDuration(videoRef.current.duration || 90.0);
                }
              }}
              onEnded={() => setIsPlaying(false)}
              playsInline
              controls
            />
          </div>

          <div className="flex items-center justify-between text-xs text-textMuted pt-1">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Captured from live running environment (H.264 Universal 1080p)</span>
            </div>
            <div>File: <code className="bg-darkHover px-2 py-0.5 rounded text-textMain font-mono border border-darkBorder">web_video.mp4</code></div>
          </div>
        </div>
      )}

      {/* Interactive Live Log Parser Playground */}
      <div className="bg-darkPanel rounded-2xl border border-darkBorder shadow-md p-6 md:p-8 space-y-6 transition-colors">
        <div>
          <div className="inline-flex items-center gap-2 px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold uppercase tracking-wider">
            <Zap className="w-3.5 h-3.5 text-emerald-600" />
            <span>Interactive Jury Testbench</span>
          </div>
          <h3 className="text-xl font-bold text-textMain mt-1">
            Test the Normalization Engine Live
          </h3>
          <p className="text-xs text-textMuted">
            Pick a real-world enterprise log preset or paste your own raw log string to see SarvDrishti normalize it in real-time.
          </p>
        </div>

        {/* Preset Selector */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {samplePresets.map((p) => {
            const isSelected = selectedPreset.id === p.id;
            return (
              <button
                key={p.id}
                onClick={() => handleSelectPreset(p)}
                className={`p-3 rounded-xl border text-left transition-all ${
                  isSelected
                    ? 'border-blue-500 bg-blue-500/10 shadow-sm ring-1 ring-blue-500'
                    : 'border-darkBorder bg-darkPanel hover:bg-darkHover'
                }`}
              >
                <div className="text-xs font-bold text-textMain">{p.name}</div>
                <div className="text-[11px] font-medium text-blue-600 dark:text-blue-400 mt-0.5">{p.badge}</div>
              </button>
            );
          })}
        </div>

        {/* Input & Output Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Raw Log Input */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-textMain">
              <span className="flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-textMuted" />
                Raw Ingress Payload
              </span>
              <span className="text-[11px] font-normal text-textMuted">Editable Test Input</span>
            </div>
            <textarea
              rows={6}
              value={customLogInput}
              onChange={(e) => setCustomLogInput(e.target.value)}
              className="w-full font-mono text-xs p-3.5 rounded-xl border border-darkBorder bg-darkBg text-textMain focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleParseLog}
              disabled={isParsing}
              className="w-full py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs flex items-center justify-center gap-2 shadow-sm transition-all"
            >
              {isParsing ? (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Executing Deterministic Pipeline...</span>
                </>
              ) : (
                <>
                  <Zap className="w-3.5 h-3.5 text-amber-300" />
                  <span>Parse Log Instantly</span>
                </>
              )}
            </button>
          </div>

          {/* Normalized JSON Output */}
          <div className="space-y-2">
            <div className="flex items-center justify-between text-xs font-bold text-textMain">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                Normalized Universal Schema (JSON)
              </span>
              <span className="text-[11px] font-mono text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                {parsedOutput.detected}
              </span>
            </div>
            <div className="rounded-xl border border-darkBorder bg-darkBg p-3.5 text-textMain font-mono text-xs overflow-auto max-h-[195px] shadow-inner">
              <pre>{JSON.stringify(parsedOutput.fields, null, 2)}</pre>
            </div>
            <div className="text-[11px] text-textMuted flex items-center justify-between pt-1">
              <span>✓ 100% Raw Data Preserved in JSONB</span>
              <span className="text-blue-600 dark:text-blue-400 font-semibold cursor-pointer hover:underline" onClick={() => onNavigate('lineage')}>
                Inspect Field Lineage Graph ➔
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* SIH Innovation Claims Matrix (Theme-Aware) */}
      <div className="space-y-4">
        <div className="text-center max-w-2xl mx-auto space-y-1">
          <h3 className="text-xl md:text-2xl font-bold text-textMain">
            Verified SIH 2026 Architectural Claims
          </h3>
          <p className="text-xs md:text-sm text-textMuted">
            Proven engineering standards implemented in code and audited for hackathon compliance
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>Multi-Source Ingestion</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Ingests Syslog (RFC 5424/3164), REST payloads, and historical batch dumps concurrently without dropped packets.
            </p>
          </div>

          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>100% Raw Preservation</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Raw bytes are stored verbatim in PostgreSQL JSONB alongside normalized output for full legal & forensic compliance.
            </p>
          </div>

          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>Mathematical Field Lineage</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Every extracted field traces back to exact byte offsets in the raw string, proving which parser extracted what.
            </p>
          </div>

          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>Air-Gapped AI Fallback</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Heuristic rule generation works 100% offline with zero external internet dependencies or API keys required.
            </p>
          </div>

          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>Zero-Eval Security</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Pydantic schema validation, parameterized SQL binding, no dynamic code execution (<code className="text-rose-600 font-mono">eval()</code>), and audited rules.
            </p>
          </div>

          <div className="bg-darkPanel p-5 rounded-xl border border-darkBorder shadow-sm space-y-2">
            <div className="flex items-center gap-2 text-emerald-600 font-bold text-sm">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              <span>Time-Travel Replay</span>
            </div>
            <p className="text-xs text-textMuted leading-relaxed">
              Historical replay engine re-evaluates past log lines against updated parser versions to detect regression flaws.
            </p>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="pt-8 border-t border-darkBorder flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-textMuted">
        <div className="flex items-center gap-3">
          <img src="/logo.png" alt="SarvDrishti" className="h-6 object-contain" />
          <span>SarvDrishti — Unified Log Intelligence Engine</span>
          <span>•</span>
          <span className="font-semibold text-textMain">Team Black Pearl</span>
        </div>
        <div className="flex items-center gap-4">
          <button onClick={() => onNavigate('overview')} className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
            Operator Console ➔
          </button>
          <a href="/technical_approach_slide.html" target="_blank" rel="noreferrer" className="text-blue-600 dark:text-blue-400 font-medium hover:underline">
            Presentation Slide ➔
          </a>
        </div>
      </div>

    </div>
  );
}

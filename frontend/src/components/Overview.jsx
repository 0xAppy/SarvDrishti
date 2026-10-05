import React, { useState, useEffect, Suspense } from 'react';
import { Activity, ShieldCheck, Server, AlertTriangle, Database, Cpu, Network } from 'lucide-react';

const LogPipelineNetwork = React.lazy(() => import('./LogPipelineNetwork'));

export default function Overview() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/stats');
      const data = await res.json();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between pb-2 border-b border-darkBorder">
        <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
          <Activity className="w-4 h-4 text-accentCyan" /> SYSTEM STATUS
        </h2>
        <div className="text-[10px] text-textMuted font-mono">UPDATED: LIVE</div>
      </div>

      {/* Top Header Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-darkBg p-3 rounded border border-darkBorder flex flex-col justify-between">
          <div className="text-[10px] font-mono text-textMuted uppercase tracking-wider mb-1">Events Processed</div>
          <div className="text-xl font-semibold text-textMain font-mono">
            {stats ? stats.events_processed.toLocaleString() : '0'}
          </div>
          <div className="text-[10px] text-accentCyan mt-2 flex items-center gap-1 font-mono">
            <Activity className="w-3 h-3" />
            {stats ? `${stats.events_per_sec} evt/s (ESTIMATED)` : '0 evt/s'}
          </div>
        </div>

        <div className="bg-darkBg p-3 rounded border border-darkBorder flex flex-col justify-between">
          <div className="text-[10px] font-mono text-textMuted uppercase tracking-wider mb-1">Parsing Success</div>
          <div className="text-xl font-semibold text-textMain font-mono">
            {stats ? `${stats.parsing_success_rate}%` : '100%'}
          </div>
          <div className="text-[10px] text-statusGood mt-2 flex items-center gap-1">
            <ShieldCheck className="w-3 h-3" />
            DETERMINISTIC RULES
          </div>
        </div>

        <div className="bg-darkBg p-3 rounded border border-darkBorder flex flex-col justify-between">
          <div className="text-[10px] font-mono text-textMuted uppercase tracking-wider mb-1">Active Parsers</div>
          <div className="text-xl font-semibold text-textMain font-mono">
            {stats ? `${stats.active_parsers}` : '4'}
          </div>
          <div className="text-[10px] text-textMuted mt-2 flex items-center gap-1">
            <Server className="w-3 h-3" />
            {stats ? `${stats.active_sources}` : '4'} ACTIVE SOURCES
          </div>
        </div>

        <div className="bg-darkBg p-3 rounded border border-darkBorder flex flex-col justify-between">
          <div className="text-[10px] font-mono text-textMuted uppercase tracking-wider mb-1">Validation Failures</div>
          <div className="text-xl font-semibold text-statusError font-mono">
            {stats ? stats.validation_failures : '0'}
          </div>
          <div className="text-[10px] text-statusWarn mt-2 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            REVIEW REQUIRED
          </div>
        </div>
      </div>

      {/* Infrastructure Health Status & Pipeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        
        {/* Node Health */}
        <div className="bg-darkBg border border-darkBorder rounded p-3 lg:col-span-1 space-y-3">
          <h3 className="text-xs font-semibold text-textMuted uppercase tracking-wider flex items-center gap-2 mb-3">
            <Cpu className="w-3 h-3" /> Infrastructure Health
          </h3>
          
          <div className="flex items-center justify-between p-2 bg-darkPanel rounded border border-darkBorder">
            <div>
              <div className="text-[10px] text-textMuted font-mono">QUEUE / BROKER</div>
              <div className="text-xs font-medium text-textMain mt-0.5">Stream Buffer</div>
            </div>
            <div className="text-[10px] text-statusGood font-mono font-bold">{stats?.kafka_status || 'ONLINE'}</div>
          </div>

          <div className="flex items-center justify-between p-2 bg-darkPanel rounded border border-darkBorder">
            <div>
              <div className="text-[10px] text-textMuted font-mono">PARSER ENGINE</div>
              <div className="text-xs font-medium text-textMain mt-0.5">Python Workers</div>
            </div>
            <div className="text-[10px] text-statusGood font-mono font-bold">{stats?.worker_status || 'RUNNING'}</div>
          </div>

          <div className="flex items-center justify-between p-2 bg-darkPanel rounded border border-darkBorder">
            <div>
              <div className="text-[10px] text-textMuted font-mono">DATA STORE</div>
              <div className="text-xs font-medium text-textMain mt-0.5">Lossless DB</div>
            </div>
            <div className="text-[10px] text-statusGood font-mono font-bold">{stats?.database_status || 'CONNECTED'}</div>
          </div>
        </div>

        {/* 3D Pipeline Visualizer */}
        <div className="bg-darkBg border border-darkBorder rounded p-3 lg:col-span-2 flex flex-col">
          <h3 className="text-xs font-semibold text-textMuted uppercase tracking-wider flex items-center gap-2 mb-3">
            <Network className="w-3 h-3" /> Log Pipeline Network
          </h3>
          <div className="flex-1 relative bg-darkPanel rounded border border-darkBorder">
            <Suspense fallback={
              <div className="absolute inset-0 flex items-center justify-center text-xs text-textMuted font-mono">
                INITIALIZING WEBGL SUBSYSTEM...
              </div>
            }>
              <LogPipelineNetwork />
            </Suspense>
          </div>
        </div>

      </div>
    </div>
  );
}

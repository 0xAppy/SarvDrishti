import React, { useState, useEffect } from 'react';
import { Shield, Server, Globe, HelpCircle, Activity } from 'lucide-react';

export default function SourcesView() {
  const [sources, setSources] = useState([]);

  useEffect(() => {
    fetch('/api/sources')
      .then(res => res.json())
      .then(data => setSources(data))
      .catch(err => console.error(err));
  }, []);

  const getSourceIcon = (type) => {
    switch (type) {
      case 'firewall': return <Shield className="w-3.5 h-3.5 text-accentCyan" />;
      case 'syslog': return <Server className="w-3.5 h-3.5 text-accentBlue" />;
      case 'application': return <Globe className="w-3.5 h-3.5 text-textMuted" />;
      default: return <HelpCircle className="w-3.5 h-3.5 text-statusWarn" />;
    }
  };

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Server className="w-4 h-4 text-accentCyan" /> INFRASTRUCTURE ENDPOINTS
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Heterogeneous Log Ingestion Inventory</p>
        </div>
        <div className="text-[10px] font-mono text-textMuted">
          TOTAL SOURCES: <span className="text-textMain font-bold">{sources.length}</span>
        </div>
      </div>

      <div className="flex-1 overflow-auto rounded border border-darkBorder bg-darkBg">
        <table className="w-full text-left text-xs whitespace-nowrap">
          <thead className="bg-darkPanel text-[10px] text-textMuted uppercase font-mono tracking-wider sticky top-0 border-b border-darkBorder shadow-sm">
            <tr>
              <th className="px-4 py-2 font-semibold">Endpoint Name</th>
              <th className="px-4 py-2 font-semibold">Source ID</th>
              <th className="px-4 py-2 font-semibold">Protocol / Ingestion</th>
              <th className="px-4 py-2 font-semibold">Parser Engine Binding</th>
              <th className="px-4 py-2 font-semibold">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-darkBorder">
            {sources.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-4 py-8 text-center text-textMuted text-xs font-mono">
                  No endpoint sources registered.
                </td>
              </tr>
            ) : (
              sources.map(src => (
                <tr key={src.id} className="hover:bg-darkHover transition-colors group">
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-2">
                      {getSourceIcon(src.type)}
                      <span className="font-semibold text-textMain group-hover:text-accentCyan transition-colors">{src.name}</span>
                    </div>
                  </td>
                  <td className="px-4 py-2 font-mono text-textMuted">{src.id}</td>
                  <td className="px-4 py-2 text-textMuted">{src.ingestion_method}</td>
                  <td className="px-4 py-2 font-mono text-accentCyan font-semibold">{src.parser_assigned}</td>
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-1.5 font-mono text-[10px] font-bold">
                      {src.status === 'active' ? (
                        <><span className="w-1.5 h-1.5 rounded-full bg-statusGood" /> <span className="text-statusGood">ACTIVE</span></>
                      ) : (
                        <><span className="w-1.5 h-1.5 rounded-full bg-statusWarn" /> <span className="text-statusWarn">PENDING AI</span></>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

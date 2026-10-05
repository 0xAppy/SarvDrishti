import React, { useState, useEffect } from 'react';
import { Cpu, CheckCircle2, ShieldAlert } from 'lucide-react';

export default function ParserRegistryView() {
  const [parsers, setParsers] = useState([]);

  useEffect(() => {
    fetch('/api/parsers')
      .then(res => res.json())
      .then(data => setParsers(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Cpu className="w-4 h-4 text-accentCyan" /> PARSER REGISTRY
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Deterministic Parsing Rules & Signatures</p>
        </div>
        <div className="text-[10px] font-mono text-textMuted">
          TOTAL PARSERS: <span className="text-textMain font-bold">{parsers.length}</span>
        </div>
      </div>

      <div className="flex-1 overflow-auto rounded border border-darkBorder bg-darkBg">
        <table className="w-full text-left text-xs whitespace-nowrap">
          <thead className="bg-darkPanel text-[10px] text-textMuted uppercase font-mono tracking-wider sticky top-0 border-b border-darkBorder shadow-sm">
            <tr>
              <th className="px-4 py-2 font-semibold">Parser ID</th>
              <th className="px-4 py-2 font-semibold">Format Signature</th>
              <th className="px-4 py-2 font-semibold">Version</th>
              <th className="px-4 py-2 font-semibold">Execution Engine</th>
              <th className="px-4 py-2 font-semibold">Validation Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-darkBorder">
            {parsers.length === 0 ? (
              <tr>
                <td colSpan="5" className="px-4 py-8 text-center text-textMuted text-xs font-mono">
                  No parsers registered.
                </td>
              </tr>
            ) : (
              parsers.map((p, idx) => (
                <tr key={idx} className="hover:bg-darkHover transition-colors group">
                  <td className="px-4 py-2 font-mono text-accentCyan font-semibold group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{p.parser_id}</td>
                  <td className="px-4 py-2 font-mono text-textMuted">{p.format_name}</td>
                  <td className="px-4 py-2 font-mono text-textMuted">v{p.version}</td>
                  <td className="px-4 py-2 font-mono text-[10px] text-textMuted">
                    {p.parser_id.includes('custom') ? 'AI-Generated Rule' : 'Native Regex/KV'}
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex items-center gap-1.5 font-mono text-[10px] font-bold text-statusGood">
                      <CheckCircle2 className="w-3 h-3" /> PASSED
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

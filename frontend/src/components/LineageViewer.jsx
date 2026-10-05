import React, { useState, useEffect } from 'react';
import { GitCommit, ArrowRight, ArrowDown } from 'lucide-react';

export default function LineageViewer({ eventId }) {
  const [lineageData, setLineageData] = useState(null);
  const [selectedMapping, setSelectedMapping] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!eventId) return;
    setLoading(true);
    fetch(`/api/events/lineage/${eventId}`)
      .then(res => res.json())
      .then(data => {
        setLineageData(data);
        if (data.lineage && data.lineage.length > 0) {
          setSelectedMapping(data.lineage[0]);
        }
      })
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [eventId]);

  if (!eventId) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center border border-darkBorder bg-darkBg rounded p-12">
        <GitCommit className="w-8 h-8 text-textMuted mb-3" />
        <h3 className="text-sm font-semibold text-textMain uppercase tracking-wider">No Event Selected</h3>
        <p className="text-[10px] text-textMuted mt-1 font-mono">
          Navigate to Event Explorer and click "Trace Lineage" on a normalized record.
        </p>
      </div>
    );
  }

  if (loading) {
    return <div className="text-center py-12 text-[10px] font-mono text-textMuted uppercase tracking-widest">Loading provenance graph...</div>;
  }

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <GitCommit className="w-4 h-4 text-accentCyan" /> FIELD LINEAGE VIEWER
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Audit Trail & Provenance Data</p>
        </div>
        <div className="text-[10px] font-mono text-textMuted text-right">
          EVENT ID<br/>
          <span className="text-textMain font-bold">{eventId}</span>
        </div>
      </div>

      {/* Raw Event Banner */}
      <div className="bg-darkHover rounded border border-darkBorder flex flex-col">
        <div className="px-3 py-1.5 border-b border-darkBorder text-[10px] font-mono text-textMuted uppercase font-bold">
          Untouched Raw Payload
        </div>
        <div className="p-3 text-[10px] font-mono text-textMuted whitespace-pre-wrap break-all">
          {lineageData?.raw_payload}
        </div>
      </div>

      <div className="flex-1 flex gap-4 min-h-0">
        {/* Left: Fields List */}
        <div className="w-1/3 bg-darkBg border border-darkBorder rounded flex flex-col overflow-hidden">
          <div className="px-3 py-2 bg-darkPanel border-b border-darkBorder text-[10px] font-mono text-textMuted uppercase font-bold flex justify-between">
            <span>Extracted Fields</span>
            <span>{lineageData?.lineage?.length || 0} Total</span>
          </div>
          <div className="flex-1 overflow-auto divide-y divide-darkBorder">
            {lineageData?.lineage?.map((m, idx) => {
              const isSelected = selectedMapping?.normalized_field === m.normalized_field;
              return (
                <div 
                  key={idx}
                  onClick={() => setSelectedMapping(m)}
                  className={`px-3 py-2 cursor-pointer transition-colors flex items-center justify-between ${
                    isSelected ? 'bg-darkHover border-l-2 border-accentCyan' : 'hover:bg-darkHover border-l-2 border-transparent'
                  }`}
                >
                  <div>
                    <div className={`font-mono text-[10px] font-bold ${isSelected ? 'text-accentCyan' : 'text-textMain'}`}>
                      {m.normalized_field}
                    </div>
                    <div className="text-[10px] text-textMuted font-mono truncate max-w-[150px]">
                      {m.raw_value}
                    </div>
                  </div>
                  <ArrowRight className={`w-3 h-3 ${isSelected ? 'text-accentCyan' : 'text-darkBorder'}`} />
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Lineage Graph */}
        <div className="flex-1 bg-darkBg border border-darkBorder rounded flex flex-col items-center justify-center p-6 relative overflow-hidden">
          {selectedMapping ? (
            <div className="w-full max-w-sm flex flex-col items-center space-y-2">
              {/* Box 1: Normalized Field */}
              <div className="w-full p-3 bg-darkPanel border border-accentCyan rounded text-center shadow-[0_0_15px_rgba(8,145,178,0.1)]">
                <div className="text-[10px] font-mono text-textMuted uppercase mb-1">Normalized Field</div>
                <div className="text-sm font-mono font-bold text-accentCyan">{selectedMapping.normalized_field}</div>
              </div>
              
              <ArrowDown className="w-4 h-4 text-darkBorder" />
              
              {/* Box 2: Raw Field */}
              <div className="w-full p-3 bg-darkPanel border border-darkBorder rounded text-center">
                <div className="text-[10px] font-mono text-textMuted uppercase mb-1">Raw Key Mapping</div>
                <div className="text-xs font-mono font-bold text-textMain">{selectedMapping.raw_field}</div>
              </div>
              
              <ArrowDown className="w-4 h-4 text-darkBorder" />

              {/* Box 3: Raw Value */}
              <div className="w-full p-3 bg-darkPanel border border-darkBorder rounded text-center">
                <div className="text-[10px] font-mono text-textMuted uppercase mb-1">Extracted Value</div>
                <div className="text-xs font-mono font-bold text-statusGood">{selectedMapping.raw_value}</div>
              </div>

              <ArrowDown className="w-4 h-4 text-darkBorder" />

              {/* Box 4: Parser Rules */}
              <div className="w-full p-3 bg-darkHover border border-darkBorder rounded flex justify-between items-center">
                <div className="text-left">
                  <div className="text-[10px] font-mono text-textMuted uppercase mb-1">Parser ID</div>
                  <div className="text-[10px] font-mono font-bold text-textMain">{selectedMapping.parser_id}</div>
                </div>
                <div className="text-right border-l border-darkBorder pl-4">
                  <div className="text-[10px] font-mono text-textMuted uppercase mb-1">Version</div>
                  <div className="text-[10px] font-mono font-bold text-textMain">v{selectedMapping.parser_version}</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-[10px] font-mono text-textMuted uppercase tracking-widest">
              Select a field mapping to view diagram
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

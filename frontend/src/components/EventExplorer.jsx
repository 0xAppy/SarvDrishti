import React, { useState, useEffect } from 'react';
import { Search, Filter, RefreshCcw, GitCommit } from 'lucide-react';

export default function EventExplorer({ onSelectLineage }) {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchEvents = async () => {
    try {
      const res = await fetch('/api/events');
      const data = await res.json();
      setEvents(data);
      if (data.length > 0 && !selectedEvent) {
        setSelectedEvent(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col h-full space-y-4">
      {/* Header */}
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Search className="w-4 h-4 text-accentCyan" /> EVENT EXPLORER
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Live Normalized Event Stream</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-[10px] font-mono text-textMuted">
            EVENTS: <span className="text-textMain font-bold">{events.length}</span>
          </div>
          <button 
            onClick={fetchEvents}
            className="flex items-center gap-1.5 px-2 py-1 bg-darkHover hover:bg-darkBorder text-textMain rounded border border-darkBorder transition-colors text-[10px] font-mono uppercase"
          >
            <RefreshCcw className="w-3 h-3" /> Refresh
          </button>
        </div>
      </div>

      {/* Dense Table */}
      <div className="flex-1 min-h-[300px] overflow-auto rounded border border-darkBorder bg-darkBg">
        <table className="w-full text-left text-xs whitespace-nowrap">
          <thead className="bg-darkPanel text-[10px] text-textMuted uppercase font-mono tracking-wider sticky top-0 border-b border-darkBorder shadow-sm">
            <tr>
              <th className="px-3 py-2 font-semibold">Time</th>
              <th className="px-3 py-2 font-semibold">Source</th>
              <th className="px-3 py-2 font-semibold">Category</th>
              <th className="px-3 py-2 font-semibold">Source IP</th>
              <th className="px-3 py-2 font-semibold">Action</th>
              <th className="px-3 py-2 font-semibold">Validation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-darkBorder">
            {events.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-3 py-8 text-center text-textMuted text-xs font-mono">
                  Waiting for incoming log events...
                </td>
              </tr>
            ) : (
              events.map((evt, idx) => {
                const isSelected = selectedEvent?.db_record?.id === evt.db_record?.id;
                const isValid = evt.db_record.is_valid !== false;
                
                return (
                  <tr 
                    key={idx}
                    onClick={() => setSelectedEvent(evt)}
                    className={`cursor-pointer transition-colors font-mono text-[10px] ${
                      isSelected ? 'bg-darkBorder' : 'hover:bg-darkHover'
                    }`}
                  >
                    <td className="px-3 py-1.5 text-textMuted">
                      {new Date(evt.db_record.created_at).toISOString().split('T')[1].slice(0, -1)}
                    </td>
                    <td className="px-3 py-1.5 text-accentCyan font-bold">{evt.db_record.source_id}</td>
                    <td className="px-3 py-1.5 text-textMuted">{evt.normalized.event?.category || '-'}</td>
                    <td className="px-3 py-1.5 text-textMain">{evt.normalized.source?.ip || '-'}</td>
                    <td className="px-3 py-1.5 text-textMain">{evt.normalized.event?.action || '-'}</td>
                    <td className="px-3 py-1.5">
                      {isValid ? (
                        <span className="text-statusGood">VALID</span>
                      ) : (
                        <span className="text-statusError">INVALID</span>
                      )}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Inspector Panel */}
      <div className="h-64 shrink-0 bg-darkBg border border-darkBorder rounded flex flex-col overflow-hidden">
        {selectedEvent ? (
          <>
            <div className="flex items-center justify-between px-3 py-2 bg-darkPanel border-b border-darkBorder">
              <h3 className="text-xs font-semibold text-textMain uppercase tracking-wider">Event Details Inspector</h3>
              <button 
                onClick={() => onSelectLineage(selectedEvent.db_record.id)}
                className="flex items-center gap-1.5 px-2 py-1 bg-accentCyan hover:bg-accentBlue text-white rounded text-[10px] font-mono uppercase font-bold transition-colors"
              >
                <GitCommit className="w-3 h-3" /> Trace Lineage
              </button>
            </div>
            
            <div className="flex-1 flex min-h-0 divide-x divide-darkBorder">
              {/* Raw Event */}
              <div className="flex-1 flex flex-col min-w-0">
                <div className="px-3 py-1 border-b border-darkBorder bg-darkHover text-[10px] font-mono text-textMuted uppercase">
                  Raw Event
                </div>
                <div className="flex-1 p-3 overflow-auto text-[10px] font-mono text-textMuted whitespace-pre-wrap break-words">
                  {selectedEvent.raw_payload}
                </div>
              </div>

              {/* Normalized Event */}
              <div className="flex-1 flex flex-col min-w-0">
                <div className="px-3 py-1 border-b border-darkBorder bg-darkHover text-[10px] font-mono text-textMuted uppercase">
                  Normalized Universal Schema
                </div>
                <pre className="flex-1 p-3 overflow-auto text-[10px] font-mono text-accentCyan">
                  {JSON.stringify(selectedEvent.normalized, null, 2)}
                </pre>
              </div>
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-textMuted text-xs font-mono uppercase tracking-widest">
            Select an event to inspect details
          </div>
        )}
      </div>
    </div>
  );
}

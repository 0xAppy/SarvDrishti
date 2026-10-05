import React, { useState } from 'react';
import { Sparkles, CheckCircle2, Play, Save, Code } from 'lucide-react';

export default function AIOnboardingStudio() {
  const [sampleLog, setSampleLog] = useState('[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL');
  const [analysis, setAnalysis] = useState(null);
  const [validationResult, setValidationResult] = useState(null);
  const [approvedStatus, setApprovedStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setValidationResult(null);
    setApprovedStatus(null);
    try {
      const res = await fetch('/api/onboarding/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sample_log: sampleLog })
      });
      const data = await res.json();
      setAnalysis(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    if (!analysis) return;
    setLoading(true);
    try {
      const res = await fetch('/api/onboarding/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sample_log: sampleLog,
          parser_id: analysis.proposed_parser_id,
          version: '1.0.0',
          mappings: analysis.suggested_mappings
        })
      });
      const data = await res.json();
      setValidationResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async () => {
    if (!analysis) return;
    setLoading(true);
    try {
      const res = await fetch('/api/onboarding/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          parser_id: analysis.proposed_parser_id,
          version: '1.0.0',
          format_name: 'custom_onboarded',
          mappings: analysis.suggested_mappings,
          regex_pattern: analysis.generated_regex
        })
      });
      const data = await res.json();
      setApprovedStatus(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full space-y-4">
      <div className="flex justify-between items-end border-b border-darkBorder pb-2">
        <div>
          <h2 className="text-sm font-semibold text-textMain tracking-wide flex items-center gap-2">
            <Code className="w-4 h-4 text-accentCyan" /> PARSER ENGINEERING WORKBENCH
          </h2>
          <p className="text-[10px] text-textMuted uppercase tracking-wider mt-1 font-mono">Dynamic AI-Assisted Source Onboarding</p>
        </div>
      </div>

      <div className="flex-1 flex flex-col lg:flex-row gap-4 min-h-0">
        {/* Left Side: Input & Analysis */}
        <div className="flex-1 flex flex-col space-y-4 min-h-0">
          
          {/* Input Panel */}
          <div className="bg-darkBg border border-darkBorder rounded flex flex-col shrink-0">
            <div className="px-3 py-2 bg-darkPanel border-b border-darkBorder flex justify-between items-center">
              <span className="text-[10px] font-mono text-textMuted uppercase font-bold">Unknown Source Sample</span>
              <span className="text-[10px] font-mono text-statusWarn bg-statusWarn/10 px-1.5 py-0.5 rounded border border-statusWarn/20">UNMAPPED</span>
            </div>
            <div className="p-3">
              <textarea
                rows={4}
                value={sampleLog}
                onChange={(e) => setSampleLog(e.target.value)}
                className="w-full p-3 bg-darkPanel rounded border border-darkBorder text-xs font-mono text-textMain focus:outline-none focus:border-accentCyan resize-none"
              />
              <div className="mt-3 flex justify-end">
                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="flex items-center gap-1.5 px-3 py-1.5 bg-darkHover hover:bg-darkBorder text-textMain border border-darkBorder rounded text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
                >
                  <Sparkles className="w-3 h-3 text-accentCyan" /> {loading ? 'Processing...' : 'Run Heuristic Analysis'}
                </button>
              </div>
            </div>
          </div>

          {/* Validation & Approval Panel */}
          <div className="flex-1 bg-darkBg border border-darkBorder rounded flex flex-col min-h-0">
             <div className="px-3 py-2 bg-darkPanel border-b border-darkBorder text-[10px] font-mono text-textMuted uppercase font-bold">
              Engineering Pipeline
            </div>
            <div className="flex-1 p-4 flex flex-col justify-center space-y-4">
              
              {!analysis ? (
                <div className="text-center text-[10px] font-mono text-textMuted uppercase tracking-widest">
                  Awaiting source sample for heuristic analysis.
                </div>
              ) : (
                <>
                  <div className="flex items-center justify-between p-3 border border-darkBorder bg-darkPanel rounded">
                    <div>
                      <div className="text-[10px] font-mono text-textMuted uppercase">Step 1: Automated Validation</div>
                      <div className="text-xs font-mono text-textMain mt-1">Test drafted regex against sample</div>
                    </div>
                    <button
                      onClick={handleValidate}
                      disabled={loading || validationResult}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-darkHover hover:bg-darkBorder text-textMain border border-darkBorder rounded text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
                    >
                      <Play className="w-3 h-3 text-accentCyan" /> Validate
                    </button>
                  </div>

                  {validationResult && (
                    <div className="p-3 border border-statusGood bg-statusGood/5 rounded flex items-center gap-2 text-xs font-mono text-statusGood">
                      <CheckCircle2 className="w-4 h-4" /> VALIDATION PASSED ({Object.keys(validationResult.extracted_fields).length} fields extracted)
                    </div>
                  )}

                  <div className="flex items-center justify-between p-3 border border-darkBorder bg-darkPanel rounded">
                    <div>
                      <div className="text-[10px] font-mono text-textMuted uppercase">Step 2: Production Registration</div>
                      <div className="text-xs font-mono text-textMain mt-1">Deploy parser rule to live registry</div>
                    </div>
                    <button
                      onClick={handleApprove}
                      disabled={loading || !validationResult || approvedStatus}
                      className="flex items-center gap-1.5 px-3 py-1.5 bg-accentCyan hover:bg-accentBlue text-white rounded text-[10px] font-mono uppercase font-bold transition-colors disabled:opacity-50"
                    >
                      <Save className="w-3 h-3" /> Approve & Register
                    </button>
                  </div>

                  {approvedStatus && (
                    <div className="p-3 border border-statusGood bg-statusGood/10 rounded flex items-center gap-2 text-xs font-mono text-statusGood">
                      <CheckCircle2 className="w-4 h-4" /> PARSER REGISTERED: {approvedStatus.parser_id}
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>

        {/* Right Side: Analysis Results */}
        <div className="flex-[1.5] bg-darkBg border border-darkBorder rounded flex flex-col min-h-0">
          <div className="px-3 py-2 bg-darkPanel border-b border-darkBorder flex justify-between items-center">
            <span className="text-[10px] font-mono text-textMuted uppercase font-bold">Detected Structure</span>
            {analysis && (
              <span className="text-[10px] font-mono text-statusGood">CONFIDENCE: {Math.round(analysis.overall_confidence * 100)}%</span>
            )}
          </div>
          
          <div className="flex-1 overflow-auto">
            {!analysis ? (
              <div className="flex items-center justify-center h-full text-[10px] font-mono text-textMuted uppercase tracking-widest p-6 text-center">
                Run analysis to detect semantic mappings and generate rules.
              </div>
            ) : (
              <div className="p-0">
                <table className="w-full text-left text-xs whitespace-nowrap">
                  <thead className="bg-darkHover text-[10px] text-textMuted uppercase font-mono tracking-wider sticky top-0 border-b border-darkBorder shadow-sm">
                    <tr>
                      <th className="px-3 py-2 font-semibold">Raw Token</th>
                      <th className="px-3 py-2 font-semibold">Universal Target</th>
                      <th className="px-3 py-2 font-semibold">Sample Value</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-darkBorder">
                    {analysis.suggested_mappings.map((m, idx) => (
                      <tr key={idx} className="hover:bg-darkHover transition-colors">
                        <td className="px-3 py-2 font-mono text-statusWarn font-bold">{m.raw_key}</td>
                        <td className="px-3 py-2 font-mono text-accentCyan font-bold">{m.target_schema_field}</td>
                        <td className="px-3 py-2 font-mono text-textMuted">{m.sample_value}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

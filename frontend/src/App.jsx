import React, { useState, useEffect } from 'react';
import { 
  Home, Activity, Server, Cpu, Database, FileText, Sparkles, 
  RotateCcw, ShieldCheck, GitCommit, Search, ChevronRight, FlaskConical,
  Layers, Sun, Moon
} from 'lucide-react';

import HomePage from './components/HomePage';
import Overview from './components/Overview';
import SourcesView from './components/SourcesView';
import ParserRegistryView from './components/ParserRegistryView';
import EventExplorer from './components/EventExplorer';
import LineageViewer from './components/LineageViewer';
import AIOnboardingStudio from './components/AIOnboardingStudio';
import HistoricalReplayView from './components/HistoricalReplayView';
import TestingSandboxView from './components/TestingSandboxView';

export default function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [selectedLineageEventId, setSelectedLineageEventId] = useState(null);
  
  // Light / Dark Theme State (Default: light mode)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('sarvdrishti_theme') || 'light';
  });

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('sarvdrishti_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  const handleSelectLineage = (eventId) => {
    setSelectedLineageEventId(eventId);
    setActiveTab('lineage');
  };

  const isHome = activeTab === 'home';

  const navItems = [
    { id: 'home', label: 'Home (SIH Portal)', icon: Home },
    { id: 'overview', label: 'Overview', icon: Activity },
    { id: 'sources', label: 'Sources', icon: Server },
    { id: 'parsers', label: 'Parser Registry', icon: Cpu },
    { id: 'explorer', label: 'Event Explorer', icon: Search },
    { id: 'lineage', label: 'Lineage Viewer', icon: GitCommit },
    { id: 'onboarding', label: 'AI Onboarding', icon: Sparkles },
    { id: 'replay', label: 'Historical Replay', icon: RotateCcw },
    { id: 'testing', label: 'Testing Sandbox', icon: FlaskConical },
  ];

  return (
    <div className="min-h-screen bg-darkBg text-textMain flex flex-col font-sans selection:bg-accentCyan selection:text-white transition-colors duration-200">
      {/* Top Bar */}
      <header className="bg-darkPanel border-b border-darkBorder sticky top-0 z-50 px-4 py-2.5 flex items-center justify-between shadow-sm transition-colors">
        <div 
          onClick={() => setActiveTab('home')}
          className="flex items-center gap-3 cursor-pointer hover:opacity-90 transition-opacity"
        >
          <img src="/logo.png" alt="SarvDrishti" className="h-8 object-contain" />
          <div>
            <h1 className="text-sm font-semibold tracking-tight text-textMain flex items-center gap-2 leading-tight">
              SarvDrishti v1.0 
              <span className="text-[10px] px-1.5 py-0.5 rounded font-mono uppercase tracking-wider bg-blue-500/10 text-blue-600 dark:text-blue-400 font-bold border border-blue-500/20">
                Black Pearl
              </span>
            </h1>
            <p className="text-[10px] uppercase tracking-wider font-semibold text-textMuted">
              Unified Log Intelligence Engine • SIH 2026
            </p>
          </div>
        </div>

        {/* View Switcher, Theme Toggle & Status */}
        <div className="flex items-center gap-3 md:gap-4">
          {/* Quick View Switcher */}
          <div className="flex items-center gap-1.5 bg-darkBg border border-darkBorder rounded-lg p-1 text-xs font-medium">
            <button
              onClick={() => setActiveTab('home')}
              className={`px-3 py-1 rounded-md transition-all flex items-center gap-1.5 font-semibold ${
                activeTab === 'home'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-textMuted hover:text-textMain'
              }`}
            >
              <Home className="w-3.5 h-3.5" />
              <span>SIH Home</span>
            </button>
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-3 py-1 rounded-md transition-all flex items-center gap-1.5 font-semibold ${
                activeTab !== 'home'
                  ? 'bg-darkBorder text-textMain shadow-sm'
                  : 'text-textMuted hover:text-textMain'
              }`}
            >
              <Activity className="w-3.5 h-3.5 text-accentCyan" />
              <span>Console Dashboard</span>
            </button>
          </div>

          {/* Theme Toggle Button (Light / Dark) */}
          <button
            onClick={toggleTheme}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-darkBorder bg-darkPanel hover:bg-darkHover text-textMain transition-all text-xs font-semibold shadow-sm"
            title={theme === 'light' ? "Switch to Dark Mode" : "Switch to Light Mode"}
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <>
                <Sun className="w-3.5 h-3.5 text-amber-500 fill-amber-500" />
                <span className="hidden sm:inline font-mono">Light</span>
              </>
            ) : (
              <>
                <Moon className="w-3.5 h-3.5 text-indigo-400 fill-indigo-400" />
                <span className="hidden sm:inline font-mono">Dark</span>
              </>
            )}
          </button>

          {/* Infrastructure Health Badges */}
          <div className="hidden lg:flex items-center gap-4 text-[10px] font-mono tracking-wider font-semibold border-l border-darkBorder pl-4 text-textMuted">
            <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" /> PIPELINE HEALTHY
            </div>
            <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> INGESTION ACTIVE
            </div>
            <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> DATABASE CONNECTED
            </div>
            <div className="pl-2 text-textMuted">
              MODE: <span className="font-bold text-textMain">AIR-GAPPED READY</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex w-full mx-auto p-4 gap-4">
        {/* Navigation Sidebar */}
        <aside className="w-56 bg-darkPanel rounded-xl border border-darkBorder shrink-0 h-fit space-y-0.5 transition-colors shadow-sm">
          <div className="px-3 py-2.5 text-[10px] font-mono font-bold uppercase tracking-widest border-b border-darkBorder mb-1 flex items-center justify-between text-textMuted">
            <span>Navigation</span>
            <span className="text-[9px] px-1.5 py-0.5 rounded font-bold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
              v1.0
            </span>
          </div>

          <div className="px-2 pb-2 space-y-0.5">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600 text-white font-bold shadow-sm'
                      : 'text-textMuted hover:text-textMain hover:bg-darkHover'
                  }`}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-textMuted'}`} />
                    <span>{item.label}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </aside>

        {/* View Content Panel */}
        <main className={`flex-1 min-w-0 transition-colors ${
          isHome 
            ? 'bg-transparent' 
            : 'bg-darkPanel border border-darkBorder rounded-xl p-4 shadow-sm'
        }`}>
          {activeTab === 'home' && <HomePage onNavigate={setActiveTab} />}
          {activeTab === 'overview' && <Overview />}
          {activeTab === 'sources' && <SourcesView />}
          {activeTab === 'parsers' && <ParserRegistryView />}
          {activeTab === 'explorer' && <EventExplorer onSelectLineage={handleSelectLineage} />}
          {activeTab === 'lineage' && <LineageViewer eventId={selectedLineageEventId} />}
          {activeTab === 'onboarding' && <AIOnboardingStudio />}
          {activeTab === 'replay' && <HistoricalReplayView />}
          {activeTab === 'testing' && <TestingSandboxView />}
        </main>
      </div>
    </div>
  );
}

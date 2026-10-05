import os
import subprocess
import base64
from PIL import Image

WORKSPACE = r"e:\sih-blockchain\ULPF"
ARTIFACT_DIR = r"C:\Users\Admin\.gemini\antigravity-ide\brain\1c9d609c-2c61-4e06-85de-e7b790cee2ae"
LOGO_PATH = os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1790783031061.png")

with open(LOGO_PATH, "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Technical Approach - SarvDrishti</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
  
  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    width: 1920px;
    height: 1080px;
    background: #070c18;
    background-image: 
      radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.12) 0%, transparent 40%),
      radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.10) 0%, transparent 40%),
      radial-gradient(circle at 50% 85%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
      linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 100% 100%, 48px 48px, 48px 48px;
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 40px 56px;
    position: relative;
  }}

  /* Top Header */
  .slide-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 20px;
    margin-bottom: 28px;
  }}

  .header-left {{
    display: flex;
    align-items: baseline;
    gap: 20px;
  }}

  .slide-title {{
    font-size: 40px;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #ffffff;
    text-transform: uppercase;
    background: linear-gradient(135deg, #ffffff 60%, #93c5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .slide-subtitle {{
    font-size: 16px;
    font-weight: 500;
    color: #94a3b8;
    letter-spacing: 0.02em;
  }}

  .header-right {{
    display: flex;
    align-items: center;
    gap: 16px;
  }}

  .logo-img {{
    height: 48px;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.4);
  }}

  .team-badge {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 16px;
    border-radius: 9999px;
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(148, 163, 184, 0.2);
    font-size: 14px;
    font-weight: 600;
    color: #e2e8f0;
    backdrop-filter: blur(8px);
  }}

  .team-dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 10px #10b981;
  }}

  /* Main 2-column layout */
  .slide-body {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    flex: 1;
    min-height: 0;
  }}

  /* Section Headings */
  .section-heading {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 20px;
    color: #ffffff;
  }}

  .diamond-bullet {{
    color: #0ea5e9;
    font-size: 20px;
    text-shadow: 0 0 12px rgba(14, 165, 233, 0.8);
  }}

  .underline-heading {{
    position: relative;
    padding-bottom: 6px;
  }}

  .underline-heading::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
    border-radius: 2px;
  }}

  /* Left Column */
  .left-col {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }}

  .tech-bullets-card {{
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-radius: 16px;
    padding: 22px 24px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
  }}

  .tech-bullets-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 11px;
  }}

  .bullet-item {{
    font-size: 14.5px;
    line-height: 1.45;
    color: #cbd5e1;
    display: flex;
    align-items: baseline;
    gap: 10px;
  }}

  .bullet-marker {{
    color: #38bdf8;
    font-size: 10px;
    flex-shrink: 0;
    transform: translateY(-2px);
  }}

  .bullet-label {{
    font-weight: 700;
    color: #38bdf8;
    white-space: nowrap;
  }}

  /* Logos Grid (Bottom-Left) */
  .logos-container {{
    margin-top: 18px;
  }}

  .logos-title {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-bottom: 10px;
  }}

  .logos-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
  }}

  .logo-card {{
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 8px 10px;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s;
  }}

  .logo-card svg {{
    width: 20px;
    height: 20px;
    flex-shrink: 0;
  }}

  .logo-text {{
    font-size: 12.5px;
    font-weight: 600;
    color: #e2e8f0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Right Column (Architecture Diagram) */
  .right-col {{
    display: flex;
    flex-direction: column;
    height: 100%;
  }}

  .arch-container {{
    flex: 1;
    background: rgba(15, 23, 42, 0.65);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 16px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
    position: relative;
  }}

  /* Architecture SVG Diagram */
  .arch-svg {{
    width: 100%;
    height: 100%;
  }}

  /* Footer bar */
  .slide-footer {{
    margin-top: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #475569;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding-top: 10px;
  }}

  .footer-tags {{
    display: flex;
    gap: 16px;
  }}

  .footer-tag {{
    color: #64748b;
  }}
</style>
</head>
<body>

  <!-- Top Header -->
  <div class="slide-header">
    <div class="header-left">
      <h1 class="slide-title">TECHNICAL APPROACH</h1>
      <span class="slide-subtitle">SarvDrishti — Unified Log Intelligence & Deterministic Normalization Platform</span>
    </div>
    <div class="header-right">
      <img src="data:image/png;base64,{logo_b64}" class="logo-img" alt="SarvDrishti Logo">
      <div class="team-badge">
        <span class="team-dot"></span>
        <span>Team Black Pearl</span>
      </div>
    </div>
  </div>

  <!-- Body -->
  <div class="slide-body">
    
    <!-- LEFT HALF: Technology Stack -->
    <div class="left-col">
      <div>
        <div class="section-heading">
          <span class="diamond-bullet">◆</span>
          <span>Technology Stack</span>
        </div>
        
        <div class="tech-bullets-card">
          <ul class="tech-bullets-list">
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Frontend:</span> React 18, Vite 5, Tailwind CSS 3.4, 7-view dashboard (Overview, Sources, Parser Registry, Event Explorer, Lineage Viewer, AI Onboarding Studio, Historical Replay).</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Backend / API:</span> Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy, REST endpoints with Swagger docs.</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Streaming:</span> Apache Kafka (topics: raw-events, dead-letter-log) to decouple ingestion from parsing.</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Database:</span> PostgreSQL 15 with JSONB (raw_logs, normalized_events, field_lineage, parser_registry, source_registry, audit_logs).</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Parsing Engine:</span> Deterministic Regex / Key-Value / JSON parsers, signature-based format auto-detection, versioned Parser Registry.</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">AI Layer:</span> Pluggable AI adapter with an offline heuristic fallback (works with no internet or API key).</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">Security:</span> Pydantic input validation, ORM parameter binding (no SQL injection), no eval(), audit logs for every parser approval.</div>
            </li>
            <li class="bullet-item">
              <span class="bullet-marker">■</span>
              <div><span class="bullet-label">DevOps & Testing:</span> Docker, Docker Compose, Pytest suite, air-gapped deployment.</div>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom-Left: 12 Logos Grid -->
      <div class="logos-container">
        <div class="logos-title">Core Technology Stack & Ecosystem</div>
        <div class="logos-grid">
          <!-- Row 1 -->
          <!-- Python -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#387eb8" d="M63.8 6.5c-29.2 0-27.4 12.7-27.4 12.7l.1 13.1h27.9v3.9H25.3S6.6 34 6.6 63.8c0 29.8 16.3 28.8 16.3 28.8h9.7V79.2s-.5-16.3 16-16.3h27.5s15.5.3 15.5-15V21.5s2.3-15-27.8-15zm-15.5 8.9a4.8 4.8 0 1 1 0 9.7 4.8 4.8 0 0 1 0-9.7z"/>
              <path fill="#ffe052" d="M64.2 121.5c29.2 0 27.4-12.7 27.4-12.7l-.1-13.1H63.6v-3.9h39.1s18.7 2.2 18.7-27.6c0-29.8-16.3-28.8-16.3-28.8h-9.7v13.4s.5 16.3-16 16.3H41.9s-15.5-.3-15.5 15v26.4s-2.3 15 27.8 15zm15.5-8.9a4.8 4.8 0 1 1 0-9.7 4.8 4.8 0 0 1 0 9.7z"/>
            </svg>
            <span class="logo-text">Python</span>
          </div>

          <!-- FastAPI -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <circle cx="64" cy="64" r="60" fill="#009688"/>
              <path fill="#ffffff" d="M69.8 18.3L37 68.6h23.4L54.6 109.7 91 55.4H67.6z"/>
            </svg>
            <span class="logo-text">FastAPI</span>
          </div>

          <!-- React -->
          <div class="logo-card">
            <svg viewBox="-11.5 -10.23174 23 20.46348">
              <circle cx="0" cy="0" r="2.05" fill="#61dafb"/>
              <g stroke="#61dafb" stroke-width="1" fill="none">
                <ellipse rx="11" ry="4.2"/>
                <ellipse rx="11" ry="4.2" transform="rotate(60)"/>
                <ellipse rx="11" ry="4.2" transform="rotate(120)"/>
              </g>
            </svg>
            <span class="logo-text">React</span>
          </div>

          <!-- Vite -->
          <div class="logo-card">
            <svg viewBox="0 0 32 32">
              <path fill="#41d1ff" d="M29.5 5.5L16.7 28.2a1 1 0 0 1-1.8 0L2.5 5.5a1 1 0 0 1 .9-1.5h25.2a1 1 0 0 1 .9 1.5z"/>
              <path fill="#bd34fe" d="M22.8 3.8L16.2 16.2 12.3 8.8l-7.4-4.7z"/>
              <path fill="#ffea83" d="M17.8 11.2h4.5l-6.8 13.8 2.2-7.5h-4.2l2.3-6.3h2z"/>
            </svg>
            <span class="logo-text">Vite</span>
          </div>

          <!-- Tailwind CSS -->
          <div class="logo-card">
            <svg viewBox="0 0 48 48">
              <path fill="#38bdf8" d="M24 10c-5.5 0-9 2.8-10.5 8.3 2.3-1.6 4.9-2.3 7.8-2 3.3.4 5.7 2.8 8.3 5.5C33.8 26.1 38.6 31 48 31c5.5 0 9-2.8 10.5-8.3-2.3 1.6-4.9 2.3-7.8 2-3.3-.4-5.7-2.8-8.3-5.5C38.2 14.9 33.4 10 24 10zM9.5 24C4 24 .5 26.8-1 32.3c2.3-1.6 4.9-2.3 7.8-2 3.3.4 5.7 2.8 8.3 5.5 4.2 4.3 9 9.2 18.4 9.2 5.5 0 9-2.8 10.5-8.3-2.3 1.6-4.9 2.3-7.8 2-3.3-.4-5.7-2.8-8.3-5.5-4.2-4.3-9-9.2-18.4-9.2z"/>
            </svg>
            <span class="logo-text">Tailwind</span>
          </div>

          <!-- Apache Kafka -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <circle cx="64" cy="64" r="58" fill="#231f20"/>
              <path fill="#ffffff" d="M64 25a11 11 0 1 0 0 22 11 11 0 0 0 0-22zm-28 29a11 11 0 1 0 0 22 11 11 0 0 0 0-22zm56 0a11 11 0 1 0 0 22 11 11 0 0 0 0-22zM64 81a11 11 0 1 0 0 22 11 11 0 0 0 0-22z"/>
              <path stroke="#ffffff" stroke-width="6" d="M64 47v34M46 64h36"/>
            </svg>
            <span class="logo-text">Kafka</span>
          </div>

          <!-- Row 2 -->
          <!-- PostgreSQL -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#336791" d="M64.6 15c-27 0-48.9 21.9-48.9 48.9 0 27 21.9 48.9 48.9 48.9s48.9-21.9 48.9-48.9c0-27-21.9-48.9-48.9-48.9zm17.4 34.5c.3 4.2-2.3 9.4-4.8 13.5 3.9 3.5 9.7 7.7 11.2 12.7-5.5.9-10.7-1.3-15-4.5-2.2 4.4-4.8 8.6-7.8 12.3 5.7 3.5 12.6 6.3 14.6 12.7-7.8 1.4-15.2-1.9-21.3-6.4-3.4 3.1-7.4 5.7-11.7 7.7-1.8-6.1 1.7-12.7 5.7-17.7-4.4-3.8-8.3-8.2-11.5-13.1-2.9 5.5-7.5 10.3-13.4 13.5 1.5-7.4 6.7-13.5 12.2-18.4-1.9-4.8-3.1-9.9-3.4-15.1 7.2 2 13.9 5.8 19.3 10.7 4.7-4.5 10.3-8.1 16.5-10.4 3-2 6.6-3.4 10.4-4.2 3.1 3 5.4 6.5 6.4 10.5z"/>
            </svg>
            <span class="logo-text">PostgreSQL</span>
          </div>

          <!-- Docker -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#2496ed" d="M118.8 54.4c-1.3-1-9-6.3-25.7-1.3-.8-6.7-6.2-12-13-13.5l-2.4-.5-.9 2.3c-3.7 9.4-1.5 17.5.3 22-2.2 1.3-5.2 2.6-8.9 3.6-4.5 1.2-10.2 2.1-16.7 2.1H6.8c-1.8 11.6 1.7 23.3 9.4 32.2 9.5 11 23.7 17.4 38.6 17.4 43 0 71.9-25.1 71.9-59.5 0-1.8-.1-3.6-.4-5.3 5.9-3.2 8.4-7.5 8.7-8.1l-6.2 1.1zm-70-13.4h11.7v11.7H48.8V41zm14.7 0h11.7v11.7H63.5V41zm-29.4 0h11.7v11.7H34.1V41zm29.4-14.7h11.7V38H63.5V26.3zm-14.7 0h11.7V38H48.8V26.3zm14.7 29.4h11.7v11.7H63.5V55.7zm-14.7 0h11.7v11.7H48.8V55.7zm-14.7 0h11.7v11.7H34.1V55.7zm-14.7 0h11.7v11.7H19.4V55.7z"/>
            </svg>
            <span class="logo-text">Docker</span>
          </div>

          <!-- SQLAlchemy -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#d71f00" d="M64 12C35.3 12 12 35.3 12 64s23.3 52 52 52 52-23.3 52-52S92.7 12 64 12zm0 18.5c6.5 0 12.3 2.9 16.3 7.6L64 54.4 47.7 38.1C51.7 33.4 57.5 30.5 64 30.5zm-33.5 33.5c0-6.5 2.9-12.3 7.6-16.3l16.3 16.3-16.3 16.3c-4.7-4-7.6-9.8-7.6-16.3zm33.5 33.5c-6.5 0-12.3-2.9-16.3-7.6l16.3-16.3 16.3 16.3c-4 4.7-9.8 7.6-16.3 7.6zm33.5-33.5c0 6.5-2.9 12.3-7.6 16.3L73.6 64l16.3-16.3c4.7 4 7.6 9.8 7.6 16.3z"/>
            </svg>
            <span class="logo-text">SQLAlchemy</span>
          </div>

          <!-- Pydantic -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <circle cx="64" cy="64" r="54" fill="#e92063"/>
              <path fill="#ffffff" d="M46 36h28c11 0 19 8 19 18s-8 18-19 18H58v24H46V36zm12 26h15c4.5 0 8-3.2 8-8s-3.5-8-8-8H58v16z"/>
            </svg>
            <span class="logo-text">Pydantic</span>
          </div>

          <!-- Pytest -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#0a9edc" d="M24 24h36v36H24z"/>
              <path fill="#00d26a" d="M68 24h36v36H68z"/>
              <path fill="#ffb400" d="M24 68h36v36H24z"/>
              <path fill="#ff3838" d="M68 68h36v36H68z"/>
              <circle cx="64" cy="64" r="14" fill="#ffffff"/>
            </svg>
            <span class="logo-text">Pytest</span>
          </div>

          <!-- Linux -->
          <div class="logo-card">
            <svg viewBox="0 0 128 128">
              <path fill="#fbc02d" d="M64 12c-15.5 0-24 13-24 26 0 15 6 22 7 35 1 12-6 19-6 26 0 10 11 17 23 17s23-7 23-17c0-7-7-14-6-26 1-13 7-20 7-35 0-13-8.5-26-24-26z"/>
              <circle cx="56" cy="34" r="4" fill="#212121"/>
              <circle cx="72" cy="34" r="4" fill="#212121"/>
              <path fill="#ff9800" d="M64 42c-5 0-8 3-8 5s3 3 8 3 8-1 8-3-3-5-8-5z"/>
            </svg>
            <span class="logo-text">Linux</span>
          </div>
        </div>
      </div>
    </div>

    <!-- RIGHT HALF: Tech Architecture Flowchart -->
    <div class="right-col">
      <div class="section-heading">
        <span class="underline-heading">Tech Architecture</span>
      </div>

      <div class="arch-container">
        <svg class="arch-svg" viewBox="0 0 880 720" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <!-- Glowing arrow marker -->
            <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8"/>
            </marker>
            <marker id="arrow-green" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#34d399"/>
            </marker>
            <marker id="arrow-rose" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#f43f5e"/>
            </marker>
            <marker id="arrow-purple" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#c084fc"/>
            </marker>
            <filter id="box-glow" x="-20%" y="-20%" width="140%" height="140%">
              <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.5"/>
            </filter>
          </defs>

          <!-- ROW 1: Ingestion Pipeline -->
          
          <!-- Box: Log Sources -->
          <g transform="translate(20, 30)" filter="url(#box-glow)">
            <rect width="180" height="96" rx="14" fill="#1e293b" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="none"/>
            <text x="90" y="32" text-anchor="middle" fill="#fbbf24" font-weight="700" font-size="15" font-family="'Plus Jakarta Sans'">Log Sources</text>
            <line x1="20" y1="44" x2="160" y2="44" stroke="rgba(245, 158, 11, 0.2)" stroke-width="1"/>
            <text x="90" y="62" text-anchor="middle" fill="#94a3b8" font-size="12" font-family="'Plus Jakarta Sans'">• Firewall (Fortinet / ASA)</text>
            <text x="90" y="78" text-anchor="middle" fill="#94a3b8" font-size="12" font-family="'Plus Jakarta Sans'">• Syslog (RFC 5424 / 3164)</text>
            <text x="90" y="94" text-anchor="middle" fill="#94a3b8" font-size="12" font-family="'Plus Jakarta Sans'">• Web Apps (Nginx / JSON)</text>
          </g>

          <!-- Arrow 1: Log Sources -> Ingestion API -->
          <path d="M 200 78 L 295 78" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
          <rect x="212" y="64" width="70" height="20" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
          <text x="247" y="78" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">Raw Logs</text>

          <!-- Box: Ingestion API / Syslog Listener -->
          <g transform="translate(305, 30)" filter="url(#box-glow)">
            <rect width="210" height="96" rx="14" fill="#1e293b" stroke="#0ea5e9" stroke-width="1.8"/>
            <text x="105" y="34" text-anchor="middle" fill="#38bdf8" font-weight="700" font-size="15" font-family="'Plus Jakarta Sans'">Ingestion API / Listener</text>
            <line x1="20" y1="46" x2="190" y2="46" stroke="rgba(14, 165, 233, 0.2)" stroke-width="1"/>
            <text x="105" y="65" text-anchor="middle" fill="#cbd5e1" font-size="12" font-family="'Plus Jakarta Sans'">FastAPI REST + Syslog UDP</text>
            <text x="105" y="82" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Pydantic Schema Validation</text>
          </g>

          <!-- Arrow 2: Ingestion API -> Kafka (raw-events) -->
          <path d="M 515 78 L 610 78" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
          <rect x="532" y="64" width="60" height="20" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
          <text x="562" y="78" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">Publish</text>

          <!-- Box: Kafka (raw-events) -->
          <g transform="translate(620, 30)" filter="url(#box-glow)">
            <rect width="230" height="96" rx="14" fill="#1e293b" stroke="#f43f5e" stroke-width="1.8"/>
            <text x="115" y="34" text-anchor="middle" fill="#fda4af" font-weight="700" font-size="15" font-family="'Plus Jakarta Sans'">Apache Kafka</text>
            <line x1="20" y1="46" x2="210" y2="46" stroke="rgba(244, 63, 94, 0.2)" stroke-width="1"/>
            <text x="115" y="65" text-anchor="middle" fill="#ffffff" font-weight="700" font-size="13" font-family="'JetBrains Mono'">Topic: raw-events</text>
            <text x="115" y="82" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Decoupled Streaming Buffer</text>
          </g>

          <!-- Arrow 3: Kafka -> Worker Engine (downward) -->
          <path d="M 735 126 L 735 190" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
          <rect x="702" y="148" width="68" height="20" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
          <text x="736" y="162" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">Consume</text>

          <!-- ROW 2: Worker Engine + AI Studio + Registry -->
          
          <!-- Box: Worker Engine -->
          <g transform="translate(240, 200)" filter="url(#box-glow)">
            <rect width="610" height="110" rx="16" fill="rgba(30, 41, 59, 0.9)" stroke="#6366f1" stroke-width="2"/>
            <text x="305" y="32" text-anchor="middle" fill="#a5b4fc" font-weight="800" font-size="16" font-family="'Plus Jakarta Sans'">Worker Engine (Deterministic Pipeline)</text>
            
            <!-- 4 Stage Pipeline Blocks inside Worker -->
            <g transform="translate(25, 48)">
              <rect width="125" height="46" rx="8" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
              <text x="62" y="24" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="700" font-family="'Plus Jakarta Sans'">1. Detect</text>
              <text x="62" y="38" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="'Plus Jakarta Sans'">Format Signatures</text>
            </g>
            <path d="M 155 71 L 175 71" stroke="#818cf8" stroke-width="1.5" marker-end="url(#arrow)"/>

            <g transform="translate(180, 48)">
              <rect width="120" height="46" rx="8" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
              <text x="60" y="24" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="700" font-family="'Plus Jakarta Sans'">2. Parse</text>
              <text x="60" y="38" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="'Plus Jakarta Sans'">Regex / KV / JSON</text>
            </g>
            <path d="M 305 71 L 325 71" stroke="#818cf8" stroke-width="1.5" marker-end="url(#arrow)"/>

            <g transform="translate(330, 48)">
              <rect width="120" height="46" rx="8" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
              <text x="60" y="24" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="700" font-family="'Plus Jakarta Sans'">3. Normalize</text>
              <text x="60" y="38" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="'Plus Jakarta Sans'">Universal Schema</text>
            </g>
            <path d="M 455 71 L 475 71" stroke="#818cf8" stroke-width="1.5" marker-end="url(#arrow)"/>

            <g transform="translate(480, 48)">
              <rect width="105" height="46" rx="8" fill="#0f172a" stroke="#818cf8" stroke-width="1"/>
              <text x="52" y="24" text-anchor="middle" fill="#c7d2fe" font-size="12" font-weight="700" font-family="'Plus Jakarta Sans'">4. Validate</text>
              <text x="52" y="38" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="'Plus Jakarta Sans'">Pydantic Rules</text>
            </g>
          </g>

          <!-- Left Side Components: AI Onboarding Studio & Parser Registry -->
          
          <!-- Box: AI Onboarding Studio -->
          <g transform="translate(20, 195)" filter="url(#box-glow)">
            <rect width="180" height="75" rx="14" fill="#1e293b" stroke="#a855f7" stroke-width="1.8"/>
            <text x="90" y="28" text-anchor="middle" fill="#d8b4fe" font-weight="700" font-size="14" font-family="'Plus Jakarta Sans'">AI Onboarding Studio</text>
            <text x="90" y="46" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">LLM + Heuristic Fallback</text>
            <text x="90" y="60" text-anchor="middle" fill="#a855f7" font-size="10" font-weight="600" font-family="'Plus Jakarta Sans'">Zero-eval() Code Gen</text>
          </g>

          <!-- Arrow: AI Studio -> Parser Registry -->
          <path d="M 110 270 L 110 320" stroke="#c084fc" stroke-width="2" marker-end="url(#arrow-purple)"/>
          <rect x="25" y="282" width="168" height="18" rx="5" fill="#0f172a" stroke="#a855f7" stroke-width="1"/>
          <text x="109" y="295" text-anchor="middle" fill="#d8b4fe" font-size="10" font-weight="700" font-family="'Plus Jakarta Sans'">Approved Parser Rules</text>

          <!-- Box: Parser Registry -->
          <g transform="translate(20, 330)" filter="url(#box-glow)">
            <rect width="180" height="85" rx="14" fill="#1e293b" stroke="#8b5cf6" stroke-width="1.8"/>
            <text x="90" y="28" text-anchor="middle" fill="#c4b5fd" font-weight="700" font-size="14" font-family="'Plus Jakarta Sans'">Parser Registry</text>
            <text x="90" y="46" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Versioned Signatures</text>
            <text x="90" y="62" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Regex / KV / JSON Rules</text>
            <text x="90" y="76" text-anchor="middle" fill="#10b981" font-size="10" font-weight="600" font-family="'Plus Jakarta Sans'">Audit Trail Verified</text>
          </g>

          <!-- Arrow: Parser Registry -> Worker Engine -->
          <path d="M 200 372 L 270 372 L 270 320" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrow)"/>
          <rect x="210" y="358" width="105" height="18" rx="5" fill="#0f172a" stroke="#8b5cf6" stroke-width="1"/>
          <text x="262" y="371" text-anchor="middle" fill="#c4b5fd" font-size="10" font-weight="700" font-family="'Plus Jakarta Sans'">Feeds Parsers</text>

          <!-- ROW 3: Splits into PostgreSQL (Valid) & Kafka Dead-Letter (Malformed) -->
          
          <!-- Path Split (a): Worker Engine -> PostgreSQL -->
          <path d="M 430 310 L 430 400" stroke="#34d399" stroke-width="2.5" marker-end="url(#arrow-green)"/>
          <rect x="375" y="340" width="110" height="22" rx="6" fill="#064e3b" stroke="#10b981" stroke-width="1"/>
          <text x="430" y="355" text-anchor="middle" fill="#a7f3d0" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">✓ Valid Events</text>

          <!-- Path Split (b): Worker Engine -> Kafka Dead-Letter -->
          <path d="M 735 310 L 735 400" stroke="#f43f5e" stroke-width="2.5" marker-end="url(#arrow-rose)"/>
          <rect x="682" y="340" width="105" height="22" rx="6" fill="#881337" stroke="#f43f5e" stroke-width="1"/>
          <text x="734" y="355" text-anchor="middle" fill="#fecdd3" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">✗ Malformed</text>

          <!-- Box: PostgreSQL -->
          <g transform="translate(290, 410)" filter="url(#box-glow)">
            <rect width="280" height="110" rx="16" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
            <text x="140" y="30" text-anchor="middle" fill="#6ee7b7" font-weight="800" font-size="16" font-family="'Plus Jakarta Sans'">PostgreSQL 15 (JSONB)</text>
            <line x1="20" y1="42" x2="260" y2="42" stroke="rgba(16, 185, 129, 0.2)" stroke-width="1"/>
            <text x="140" y="60" text-anchor="middle" fill="#e2e8f0" font-size="12" font-family="'Plus Jakarta Sans'">• raw_logs & normalized_events</text>
            <text x="140" y="78" text-anchor="middle" fill="#e2e8f0" font-size="12" font-family="'Plus Jakarta Sans'">• field_lineage & audit_logs</text>
            <text x="140" y="96" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">• parser_registry & source_registry</text>
          </g>

          <!-- Box: Kafka Dead-Letter -->
          <g transform="translate(630, 410)" filter="url(#box-glow)">
            <rect width="210" height="110" rx="16" fill="#1e293b" stroke="#f43f5e" stroke-width="1.8"/>
            <text x="105" y="30" text-anchor="middle" fill="#fda4af" font-weight="700" font-size="15" font-family="'Plus Jakarta Sans'">Kafka Dead-Letter</text>
            <line x1="20" y1="42" x2="190" y2="42" stroke="rgba(244, 63, 94, 0.2)" stroke-width="1"/>
            <text x="105" y="62" text-anchor="middle" fill="#ffffff" font-weight="700" font-size="13" font-family="'JetBrains Mono'">dead-letter-log</text>
            <text x="105" y="80" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="'Plus Jakarta Sans'">Quarantine Isolation</text>
            <text x="105" y="96" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Failure Triage & Alerting</text>
          </g>

          <!-- ROW 4: Replay Service + REST API + Dashboard -->
          
          <!-- Box: Historical Replay Service -->
          <g transform="translate(20, 565)" filter="url(#box-glow)">
            <rect width="220" height="85" rx="14" fill="#1e293b" stroke="#0ea5e9" stroke-width="1.8"/>
            <text x="110" y="28" text-anchor="middle" fill="#38bdf8" font-weight="700" font-size="14" font-family="'Plus Jakarta Sans'">Historical Replay Service</text>
            <text x="110" y="48" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Time-Travel Simulation</text>
            <text x="110" y="66" text-anchor="middle" fill="#cbd5e1" font-size="11" font-family="'Plus Jakarta Sans'">Deterministic Regression Testing</text>
          </g>

          <!-- Arrow: Replay -> Kafka (curves up to Kafka raw-events) -->
          <path d="M 240 607 L 860 607 L 860 85 L 850 85" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="5 4" fill="none" marker-end="url(#arrow)"/>
          <rect x="250" y="595" width="95" height="18" rx="5" fill="#0f172a" stroke="#0ea5e9" stroke-width="1"/>
          <text x="297" y="608" text-anchor="middle" fill="#38bdf8" font-size="10" font-weight="700" font-family="'Plus Jakarta Sans'">Replay Lines</text>

          <!-- Arrow: PostgreSQL -> REST Query API -> React Dashboard -->
          <path d="M 430 520 L 430 565" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow)"/>
          <rect x="368" y="533" width="124" height="20" rx="6" fill="#0f172a" stroke="#38bdf8" stroke-width="1"/>
          <text x="430" y="547" text-anchor="middle" fill="#38bdf8" font-size="11" font-weight="700" font-family="'Plus Jakarta Sans'">REST Query API</text>

          <!-- Box: React Dashboard -->
          <g transform="translate(290, 575)" filter="url(#box-glow)">
            <rect width="280" height="85" rx="14" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
            <text x="140" y="30" text-anchor="middle" fill="#38bdf8" font-weight="800" font-size="16" font-family="'Plus Jakarta Sans'">React 18 Dashboard</text>
            <text x="140" y="50" text-anchor="middle" fill="#cbd5e1" font-size="12" font-family="'Plus Jakarta Sans'">Overview • Sources • Parser Registry</text>
            <text x="140" y="68" text-anchor="middle" fill="#94a3b8" font-size="11" font-family="'Plus Jakarta Sans'">Event Explorer • Lineage • AI Studio • Replay</text>
          </g>

        </svg>
      </div>
    </div>

  </div>

  <!-- Slide Footer -->
  <div class="slide-footer">
    <div class="footer-tags">
      <span class="footer-tag">Smart India Hackathon 2026</span>
      <span class="footer-tag">•</span>
      <span class="footer-tag">Problem Statement: Unified Log Intelligence Platform</span>
      <span class="footer-tag">•</span>
      <span class="footer-tag">Deterministic Parsing & Zero-Eval Security</span>
    </div>
    <div>Team Black Pearl — Confidential & Proprietary</div>
  </div>

</body>
</html>
"""

html_path = os.path.join(WORKSPACE, "technical_approach_slide.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML slide created at {html_path}")

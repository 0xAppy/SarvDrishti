"""
SarvDrishti — Fast-Paced Real-Time Live Working Tutorial Video Generator
========================================================================
Generates a 1.5+ minute (92.7s), fast-paced, graphified video demonstrating
the live working, real-time ingestion, deterministic normalization,
field-level lineage, AI onboarding, and historical replay of SarvDrishti.

Target Output: docs/assets/web_video.mp4
Total Length:  ~92.7 seconds (2,782 frames @ 30fps)
Resolution:    1920x1080 (Full HD, 60fps capable, 30fps standard H.264)
Pacing:        Fast cuts (~3.5 to 4.2s per scene, 24 high-energy scenes)
"""

import os
import sys
import math
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

# Paths
WORKSPACE = r"e:\sih-blockchain\ULPF"
ASSETS_DIR = os.path.join(WORKSPACE, "docs", "assets")
OUTPUT_VIDEO = os.path.join(ASSETS_DIR, "web_video.mp4")

# Canvas Settings
W, H = 1920, 1080
FPS = 30

# Colors (Cyber / Defense SOC Palette)
BG_VOID       = (8, 12, 22)
BG_PANEL      = (14, 21, 38)
BG_CARD       = (20, 31, 56)
BORDER_CYAN   = (0, 229, 255)
BORDER_MUTED  = (38, 55, 92)
ACCENT_CYAN   = (0, 229, 255)
ACCENT_GREEN  = (16, 185, 129)
ACCENT_PURPLE = (168, 85, 247)
ACCENT_ORANGE = (245, 158, 11)
ACCENT_RED    = (239, 68, 68)
ACCENT_BLUE   = (59, 130, 246)
TEXT_WHITE    = (255, 255, 255)
TEXT_LIGHT    = (226, 232, 240)
TEXT_MUTED    = (148, 163, 184)
TEXT_DIM      = (100, 116, 139)

# Fonts
def load_font(name, size):
    try:
        return ImageFont.truetype(f"C:\\Windows\\Fonts\\{name}", size)
    except Exception:
        return ImageFont.load_default()

f_giant   = load_font("segoeuib.ttf", 64)
f_hero    = load_font("segoeuib.ttf", 46)
f_title   = load_font("segoeuib.ttf", 32)
f_sub     = load_font("segoeui.ttf",  22)
f_body    = load_font("segoeui.ttf",  17)
f_mono_lg = load_font("consola.ttf",  21)
f_mono    = load_font("consola.ttf",  16)
f_mono_sm = load_font("consola.ttf",  13)
f_badge   = load_font("segoeuib.ttf", 13)
f_tag     = load_font("consola.ttf",  14)

# Preload Images
screenshots = {}
img_files = {
    "home_white":    "sih_white_theme_preview.png",
    "home_scrolled": "sih_white_theme_scrolled.png",
    "home_dark":     "dark_mode_home.png",
    "overview":      "light_mode_overview.png",
    "verified":      "light_mode_verified.png",
    "full_light":    "light_mode_full.png",
    "tech_slide":    "technical_approach_slide.png",
    "logo":          "logo.png",
}

for k, fn in img_files.items():
    fp = os.path.join(ASSETS_DIR, fn)
    if os.path.exists(fp):
        try:
            im = Image.open(fp).convert("RGBA")
            if k != "logo" and im.size != (W, H):
                im = im.resize((W, H), Image.Resampling.LANCZOS)
            screenshots[k] = im
        except Exception as e:
            print(f"[WARN] Failed to load {fn}: {e}")
            screenshots[k] = None
    else:
        screenshots[k] = None

# Logo helper
logo_img = screenshots.get("logo")
if logo_img:
    logo_ratio = logo_img.width / logo_img.height
    logo_h = 42
    logo_w = int(logo_h * logo_ratio)
    logo_small = logo_img.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
else:
    logo_small = None

# ─────────────────────────────────────────────────────────────────────────────
# DRAWING HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def draw_rrect(draw, x0, y0, x1, y1, r=10, fill=None, outline=None, width=1):
    draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=r, fill=fill,
                           outline=outline, width=width)

def text_center(draw, text, y, font, fill=TEXT_WHITE, x_offset=0, width=W):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text((x_offset + (width - tw) // 2, y), text, fill=fill, font=font)

def draw_cyber_grid(im, spacing=60, alpha=25):
    # Overlay subtle grid
    grid_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_overlay)
    for x in range(0, W, spacing):
        gdraw.line([(x, 0), (x, H)], fill=(0, 229, 255, alpha), width=1)
    for y in range(0, H, spacing):
        gdraw.line([(0, y), (W, y)], fill=(0, 229, 255, alpha), width=1)
    return Image.alpha_composite(im, grid_overlay)

def draw_hud(draw, global_frame, total_frames, phase_num, total_phases, phase_title, badge_text):
    # Top HUD Bar (y: 0 to 52)
    draw.rectangle([(0, 0), (W, 52)], fill=(10, 16, 30))
    draw.line([(0, 52), (W, 52)], fill=(0, 180, 216), width=2)

    # Logo / Brand
    if logo_small:
        # draw logo
        pass # rendered on base if composite
    draw.text((20, 14), "SARVDRISHTI v1.0", fill=ACCENT_CYAN, font=f_title)
    
    # Blinking Live Indicator
    blink = (global_frame // 15) % 2 == 0
    rec_col = ACCENT_RED if blink else (120, 20, 20)
    draw.ellipse([(290, 21), (302, 33)], fill=rec_col)
    draw.text((310, 18), "LIVE DEMO" if blink else "STREAMING", fill=TEXT_LIGHT, font=f_badge)

    # Phase Title in Center Pill
    center_pill_w = 640
    cx0 = (W - center_pill_w) // 2
    draw_rrect(draw, cx0, 8, cx0 + center_pill_w, 44, r=8, fill=(18, 28, 52), outline=BORDER_CYAN, width=1)
    title_text = f"PHASE {phase_num:02d}/{total_phases:02d} • {phase_title}"
    text_center(draw, title_text, 14, f_badge, fill=TEXT_WHITE, x_offset=cx0, width=center_pill_w)

    # Real-Time Telemetry Counters (Right)
    eps_val = 1450 + int(320 * math.sin(global_frame * 0.12) + 90 * math.cos(global_frame * 0.05))
    events_val = 12450 + int(global_frame * 28.5)
    
    # Animated Equalizer bars
    eq_x = W - 480
    for i in range(4):
        eq_h = int(8 + 14 * abs(math.sin(global_frame * 0.25 + i * 1.2)))
        draw.rectangle([(eq_x + i * 6, 34 - eq_h), (eq_x + i * 6 + 4, 34)], fill=ACCENT_GREEN)

    draw.text((W - 450, 17), f"EPS: {eps_val:,} evt/s", fill=ACCENT_GREEN, font=f_mono_sm)
    draw.text((W - 300, 17), f"EVENTS: {events_val:,}", fill=ACCENT_CYAN, font=f_mono_sm)
    draw.text((W - 130, 17), "100% AIR-GAP", fill=ACCENT_PURPLE, font=f_mono_sm)

    # Bottom HUD Bar (y: H - 46 to H)
    draw.rectangle([(0, H - 46), (W, H)], fill=(10, 16, 30))
    draw.line([(0, H - 46), (W, H - 46)], fill=(38, 55, 92), width=1)

    # Master Progress Line
    prog_pct = min(1.0, max(0.0, global_frame / max(1, total_frames)))
    prog_w = int(W * prog_pct)
    draw.rectangle([(0, H - 48), (prog_w, H - 45)], fill=ACCENT_CYAN)

    # Left: Clock & Team info
    elapsed_s = global_frame / FPS
    total_s = total_frames / FPS
    draw.text((20, H - 32), f"T+{elapsed_s:05.1f}s / {total_s:05.1f}s | Team Black Pearl (SIH26156)", fill=TEXT_MUTED, font=f_mono_sm)

    # Center: Architectural Tag Badge
    tag_w = draw.textbbox((0, 0), badge_text, font=f_badge)[2] + 24
    tx0 = (W - tag_w) // 2
    draw_rrect(draw, tx0, H - 38, tx0 + tag_w, H - 12, r=6, fill=(22, 34, 60), outline=ACCENT_CYAN, width=1)
    draw.text((tx0 + 12, H - 32), badge_text, fill=ACCENT_CYAN, font=f_badge)

    # Right: Pipeline SLA
    draw.text((W - 250, H - 32), "SLA: 100% | LATENCY: <0.2ms", fill=ACCENT_GREEN, font=f_mono_sm)

def draw_terminal_window(draw, x, y, w, h, title, log_lines, cursor_blink=True):
    # Terminal Window Container
    draw_rrect(draw, x, y, x + w, y + h, r=12, fill=(12, 17, 29), outline=BORDER_CYAN, width=2)
    # Header
    draw_rrect(draw, x, y, x + w, y + 42, r=12, fill=(20, 29, 48))
    draw.rectangle([(x, y + 25), (x + w, y + 42)], fill=(20, 29, 48))
    draw.line([(x, y + 42), (x + w, y + 42)], fill=BORDER_MUTED, width=1)

    # Window dots
    draw.ellipse([(x + 16, y + 15), (x + 28, y + 27)], fill=(239, 68, 68))
    draw.ellipse([(x + 36, y + 15), (x + 48, y + 27)], fill=(245, 158, 11))
    draw.ellipse([(x + 56, y + 15), (x + 68, y + 27)], fill=(16, 185, 129))

    # Window Title
    draw.text((x + 85, y + 13), title, fill=TEXT_LIGHT, font=f_mono_sm)

    # Log Lines
    ly = y + 56
    line_h = 32
    for line in log_lines[-12:]:
        # Parse badge if exists e.g. [LIVE UDP SYSLOG]
        if line.startswith("[LIVE UDP"):
            draw.text((x + 20, ly), "[LIVE UDP SYSLOG]", fill=ACCENT_CYAN, font=f_mono)
            draw.text((x + 195, ly), line[17:], fill=TEXT_LIGHT, font=f_mono)
        elif line.startswith("[LIVE FIREWALL"):
            draw.text((x + 20, ly), "[LIVE FIREWALL KV]", fill=ACCENT_ORANGE, font=f_mono)
            draw.text((x + 205, ly), line[18:], fill=TEXT_LIGHT, font=f_mono)
        elif line.startswith("[LIVE WEB"):
            draw.text((x + 20, ly), "[LIVE WEB APP]", fill=ACCENT_GREEN, font=f_mono)
            draw.text((x + 165, ly), line[14:], fill=TEXT_LIGHT, font=f_mono)
        elif line.startswith("[KAFKA"):
            draw.text((x + 20, ly), "[KAFKA BUFFER]", fill=ACCENT_PURPLE, font=f_mono)
            draw.text((x + 160, ly), line[14:], fill=TEXT_LIGHT, font=f_mono)
        else:
            draw.text((x + 20, ly), line, fill=TEXT_MUTED, font=f_mono)
        ly += line_h

    if cursor_blink:
        draw.rectangle([(x + 20, ly + 2), (x + 30, ly + 20)], fill=ACCENT_CYAN)

def draw_split_normalizer(draw, x, y, w, h, raw_log, parser_name, ecs_fields, anim_pct):
    # Left Box: Raw Log
    box_w = (w - 120) // 2
    # Raw box
    draw_rrect(draw, x, y, x + box_w, y + h, r=10, fill=(16, 24, 42), outline=(245, 158, 11), width=2)
    draw_rrect(draw, x, y, x + box_w, y + 40, r=10, fill=(30, 42, 70))
    draw.rectangle([(x, y + 25), (x + box_w, y + 40)], fill=(30, 42, 70))
    draw.text((x + 18, y + 10), "RAW INGESTION TELEMETRY (Heterogeneous)", fill=ACCENT_ORANGE, font=f_badge)

    # Raw Log Text wrapped
    draw.text((x + 18, y + 55), "FORMAT: Cisco KV / Linux Syslog / Proprietary", fill=TEXT_MUTED, font=f_mono_sm)
    raw_lines = [
        raw_log[:55],
        raw_log[55:110],
        raw_log[110:165],
    ]
    ry = y + 95
    for rl in raw_lines:
        if rl:
            draw.text((x + 18, ry), rl, fill=TEXT_WHITE, font=f_mono)
            ry += 30

    # Raw laser scanning beam
    laser_y = int(y + 80 + (h - 120) * (anim_pct % 1.0))
    draw.line([(x + 10, laser_y), (x + box_w - 10, laser_y)], fill=(245, 158, 11), width=2)

    # Center Transform Pillar
    cx = x + box_w + 60
    draw.line([(x + box_w + 10, y + h // 2), (cx - 40, y + h // 2)], fill=BORDER_CYAN, width=3)
    draw.line([(cx + 40, y + h // 2), (x + w - box_w - 10, y + h // 2)], fill=BORDER_CYAN, width=3)
    
    # Engine Badge
    draw_rrect(draw, cx - 55, y + h // 2 - 35, cx + 55, y + h // 2 + 35, r=8, fill=(16, 32, 64), outline=BORDER_CYAN, width=2)
    draw.text((cx - 45, y + h // 2 - 25), "PARSER", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((cx - 48, y + h // 2 - 6), parser_name, fill=ACCENT_CYAN, font=f_badge)
    draw.text((cx - 42, y + h // 2 + 12), "<0.14ms", fill=ACCENT_GREEN, font=f_mono_sm)

    # Right Box: Normalized ECS JSON
    rx = x + w - box_w
    draw_rrect(draw, rx, y, rx + box_w, y + h, r=10, fill=(16, 24, 42), outline=ACCENT_GREEN, width=2)
    draw_rrect(draw, rx, y, rx + box_w, y + 40, r=10, fill=(20, 48, 40))
    draw.rectangle([(rx, y + 25), (rx + box_w, y + 40)], fill=(20, 48, 40))
    draw.text((rx + 18, y + 10), "UNIVERSAL COMMON SCHEMA (Elastic ECS)", fill=ACCENT_GREEN, font=f_badge)

    # JSON Fields
    jy = y + 55
    draw.text((rx + 18, jy), "{", fill=TEXT_WHITE, font=f_mono)
    jy += 26
    for k, v, col in ecs_fields:
        draw.text((rx + 36, jy), f'"{k}": ', fill=ACCENT_CYAN, font=f_mono)
        val_x = rx + 36 + draw.textbbox((0, 0), f'"{k}": ', font=f_mono)[2]
        draw.text((val_x, jy), f'{v},', fill=col, font=f_mono)
        jy += 28
    draw.text((rx + 18, jy), "}", fill=TEXT_WHITE, font=f_mono)

def draw_lineage_graph(draw, x, y, w, h, raw_token, ecs_token, parser_id, anim_t):
    draw_rrect(draw, x, y, x + w, y + h, r=12, fill=(12, 18, 32), outline=BORDER_CYAN, width=2)
    
    # Header
    draw.text((x + 25, y + 20), "FORENSIC FIELD-LEVEL LINEAGE & PROVENANCE GRAPH", fill=ACCENT_CYAN, font=f_title)
    draw.text((x + 25, y + 60), "Tracks byte-level provenance from raw payload to SIEM query with zero data loss.", fill=TEXT_MUTED, font=f_body)

    # Card 1: Raw Origin
    c1_x, c1_y = x + 40, y + 130
    draw_rrect(draw, c1_x, c1_y, c1_x + 360, c1_y + 160, r=10, fill=(22, 32, 54), outline=ACCENT_ORANGE, width=2)
    draw.text((c1_x + 20, c1_y + 18), "1. RAW PAYLOAD TOKEN", fill=ACCENT_ORANGE, font=f_badge)
    draw.text((c1_x + 20, c1_y + 50), raw_token, fill=TEXT_WHITE, font=f_mono)
    draw.text((c1_x + 20, c1_y + 90), "Byte Offset: [14..28]", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((c1_x + 20, c1_y + 115), "Source: UDP_Syslog_5140", fill=TEXT_MUTED, font=f_mono_sm)

    # Card 2: Parser Transformation
    c2_x, c2_y = x + 480, y + 130
    draw_rrect(draw, c2_x, c2_y, c2_x + 360, c2_y + 160, r=10, fill=(22, 32, 54), outline=ACCENT_PURPLE, width=2)
    draw.text((c2_x + 20, c2_y + 18), "2. DETERMINISTIC PARSER", fill=ACCENT_PURPLE, font=f_badge)
    draw.text((c2_x + 20, c2_y + 50), f"ID: {parser_id}", fill=ACCENT_CYAN, font=f_mono)
    draw.text((c2_x + 20, c2_y + 90), "Hash: sha256:7a4c9e81b...", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((c2_x + 20, c2_y + 115), "Rule Version: v1.2 (Active)", fill=TEXT_MUTED, font=f_mono_sm)

    # Card 3: Normalized ECS Field
    c3_x, c3_y = x + 920, y + 130
    draw_rrect(draw, c3_x, c3_y, c3_x + 360, c3_y + 160, r=10, fill=(22, 32, 54), outline=ACCENT_GREEN, width=2)
    draw.text((c3_x + 20, c3_y + 18), "3. NORMALIZED ECS FIELD", fill=ACCENT_GREEN, font=f_badge)
    draw.text((c3_x + 20, c3_y + 50), ecs_token, fill=TEXT_WHITE, font=f_mono)
    draw.text((c3_x + 20, c3_y + 90), "Schema: Elastic Common Schema", fill=TEXT_MUTED, font=f_mono_sm)
    draw.text((c3_x + 20, c3_y + 115), "Verification: ACID Provenance PASS", fill=ACCENT_GREEN, font=f_mono_sm)

    # Animated Curved Connector Beams
    draw.line([(c1_x + 360, c1_y + 80), (c2_x, c2_y + 80)], fill=BORDER_CYAN, width=3)
    draw.line([(c2_x + 360, c2_y + 80), (c3_x, c3_y + 80)], fill=BORDER_CYAN, width=3)

    # Traveling pulse dots
    dot1_x = int(c1_x + 360 + (c2_x - (c1_x + 360)) * (anim_t % 1.0))
    dot2_x = int(c2_x + 360 + (c3_x - (c2_x + 360)) * (anim_t % 1.0))
    draw.ellipse([(dot1_x - 6, c1_y + 74), (dot1_x + 6, c1_y + 86)], fill=ACCENT_CYAN)
    draw.ellipse([(dot2_x - 6, c2_y + 74), (dot2_x + 6, c2_y + 86)], fill=ACCENT_GREEN)

    # Compliance Badge at bottom
    draw_rrect(draw, x + 40, y + 330, x + w - 40, y + 390, r=8, fill=(16, 28, 48), outline=ACCENT_GREEN, width=1)
    draw.text((x + 60, y + 348), "IMMUTABLE CHAIN OF CUSTODY VERIFIED: Every normalized field maps back to raw payload offset", fill=ACCENT_GREEN, font=f_sub)

def draw_ai_studio(draw, x, y, w, h, raw_log, regex_rule, confidence_pct, anim_step):
    draw_rrect(draw, x, y, x + w, y + h, r=12, fill=(12, 18, 32), outline=BORDER_CYAN, width=2)

    # Studio Header
    draw.text((x + 25, y + 20), "AI ONBOARDING STUDIO (AIR-GAPPED HEURISTIC SYNTHESIS)", fill=ACCENT_CYAN, font=f_title)
    draw.text((x + 25, y + 60), "Ingests proprietary, unknown log formats and automatically synthesizes deterministic regex.", fill=TEXT_MUTED, font=f_body)

    # Step 1: Input Raw Log
    draw_rrect(draw, x + 30, y + 105, x + w - 30, y + 175, r=8, fill=(18, 26, 44), outline=BORDER_MUTED, width=1)
    draw.text((x + 45, y + 115), "1. UNKNOWN PROPRIETARY LOG DETECTED:", fill=ACCENT_ORANGE, font=f_badge)
    draw.text((x + 45, y + 140), raw_log, fill=TEXT_WHITE, font=f_mono)

    # Step 2: AI Heuristic Synthesis Action
    btn_col = ACCENT_CYAN if anim_step >= 1 else (60, 80, 120)
    draw_rrect(draw, x + 30, y + 195, x + 340, y + 245, r=8, fill=(16, 32, 64), outline=btn_col, width=2)
    draw.text((x + 50, y + 210), "⚡ ANALYZE WITH AI ADAPTER", fill=btn_col, font=f_badge)

    if anim_step >= 1:
        draw.text((x + 360, y + 212), "MODEL: Heuristic Local LLM (Air-Gapped, No Cloud Call)", fill=ACCENT_GREEN, font=f_mono_sm)

    # Step 3: Synthesized Regex Output
    draw_rrect(draw, x + 30, y + 265, x + w - 30, y + 345, r=8, fill=(18, 26, 44), outline=ACCENT_PURPLE, width=1)
    draw.text((x + 45, y + 275), "2. AUTO-SYNTHESIZED REGEX PARSER RULE:", fill=ACCENT_PURPLE, font=f_badge)
    draw.text((x + 45, y + 305), regex_rule, fill=ACCENT_CYAN, font=f_mono)

    # Step 4: Automated Validation Suite
    val_box_w = 420
    draw_rrect(draw, x + 30, y + 365, x + 30 + val_box_w, y + 440, r=8, fill=(16, 36, 32), outline=ACCENT_GREEN, width=2)
    draw.text((x + 45, y + 380), "AUTOMATED VALIDATION SUITE", fill=ACCENT_GREEN, font=f_badge)
    draw.text((x + 45, y + 405), f"PASS RATE: 100% (50/50 Synthetic Tests) | CONFIDENCE: {confidence_pct:.1f}%", fill=TEXT_WHITE, font=f_mono_sm)

    # Step 5: Approve & Register
    if anim_step >= 2:
        draw_rrect(draw, x + 480, y + 365, x + 880, y + 440, r=8, fill=(20, 50, 40), outline=ACCENT_GREEN, width=2)
        draw.text((x + 510, y + 395), "✓ APPROVE & REGISTER TO REGISTRY", fill=TEXT_WHITE, font=f_title)
        draw.text((x + 910, y + 400), "STATUS: HOT-RELOADED (< 3ms)", fill=ACCENT_CYAN, font=f_mono_sm)

def draw_replay_monitor(draw, x, y, w, h, fname, total_ev, cur_ev, throughput, anim_pct):
    draw_rrect(draw, x, y, x + w, y + h, r=12, fill=(12, 18, 32), outline=BORDER_CYAN, width=2)
    
    # Header
    draw.text((x + 25, y + 20), "HISTORICAL LOG REPLAY & DISASTER AUDIT ENGINE", fill=ACCENT_CYAN, font=f_title)
    draw.text((x + 25, y + 60), "Streams millions of archived logs through Kafka buffer with full lineage persistence.", fill=TEXT_MUTED, font=f_body)

    # File Info
    draw.text((x + 35, y + 120), f"SOURCE FILE: {fname}", fill=TEXT_WHITE, font=f_mono)
    draw.text((x + 35, y + 155), f"BUFFER: Apache Kafka KRaft (Topic: logs-historical-replay)", fill=TEXT_MUTED, font=f_mono_sm)

    # Big Progress Bar
    bar_y = y + 200
    bar_h = 44
    draw_rrect(draw, x + 35, bar_y, x + w - 35, bar_y + bar_h, r=8, fill=(20, 30, 52), outline=BORDER_MUTED, width=1)
    fill_w = int((w - 70) * anim_pct)
    if fill_w > 0:
        draw_rrect(draw, x + 35, bar_y, x + 35 + fill_w, bar_y + bar_h, r=8, fill=ACCENT_CYAN)

    pct_str = f"{int(anim_pct * 100)}%"
    draw.text((x + w - 110, bar_y + 10), pct_str, fill=TEXT_WHITE, font=f_title)

    # Real-Time Telemetry Cards
    c_y = y + 270
    card_w = (w - 100) // 3
    
    # Card 1: Processed
    draw_rrect(draw, x + 35, c_y, x + 35 + card_w, c_y + 110, r=8, fill=(18, 28, 50), outline=BORDER_MUTED)
    draw.text((x + 50, c_y + 16), "REPLAYED EVENTS", fill=TEXT_MUTED, font=f_badge)
    draw.text((x + 50, c_y + 48), f"{cur_ev:,} / {total_ev:,}", fill=ACCENT_CYAN, font=f_title)

    # Card 2: Throughput
    draw_rrect(draw, x + 45 + card_w, c_y, x + 45 + card_w * 2, c_y + 110, r=8, fill=(18, 28, 50), outline=BORDER_MUTED)
    draw.text((x + 60 + card_w, c_y + 16), "PROCESSING THROUGHPUT", fill=TEXT_MUTED, font=f_badge)
    draw.text((x + 60 + card_w, c_y + 48), f"{throughput:,} evt/s", fill=ACCENT_GREEN, font=f_title)

    # Card 3: Event Loss
    draw_rrect(draw, x + 55 + card_w * 2, c_y, x + 55 + card_w * 3, c_y + 110, r=8, fill=(18, 28, 50), outline=BORDER_MUTED)
    draw.text((x + 70 + card_w * 2, c_y + 16), "DATA LOSS TOLERANCE", fill=TEXT_MUTED, font=f_badge)
    draw.text((x + 70 + card_w * 2, c_y + 48), "0 EVENTS (0.00%)", fill=ACCENT_PURPLE, font=f_title)

def draw_screenshot_view(draw, base_im, focus_box, callout_pos, callout_lines, anim_t):
    # Laser scan line sweeping across image
    scan_y = int(60 + (H - 120) * (anim_t % 1.0))
    draw.line([(0, scan_y), (W, scan_y)], fill=(0, 229, 255, 160), width=2)

    # Focus Box with animated pulse outline
    if focus_box:
        fx0, fy0, fx1, fy1 = focus_box
        pulse = int(4 * abs(math.sin(anim_t * 6.28)))
        draw_rrect(draw, fx0 - pulse, fy0 - pulse, fx1 + pulse, fy1 + pulse, r=8, outline=ACCENT_CYAN, width=3)
        # Radar circles
        cx, cy = (fx0 + fx1) // 2, (fy0 + fy1) // 2
        r_rad = int(20 + 40 * (anim_t % 1.0))
        draw.ellipse([(cx - r_rad, cy - r_rad), (cx + r_rad, cy + r_rad)], outline=(0, 229, 255, 80), width=2)

    # Callout HUD Box
    if callout_pos:
        cx0, cy0, cw, ch = callout_pos
        draw_rrect(draw, cx0, cy0, cx0 + cw, cy0 + ch, r=10, fill=(12, 18, 34), outline=BORDER_CYAN, width=2)
        ly = cy0 + 16
        for line, col, is_bold in callout_lines:
            f = f_title if is_bold else f_body
            draw.text((cx0 + 20, ly), line, fill=col, font=f)
            ly += 32 if is_bold else 26

# ─────────────────────────────────────────────────────────────────────────────
# 24 SCENE DEFINITIONS (Total 2,782 frames = 92.7 seconds)
# ─────────────────────────────────────────────────────────────────────────────

SCENES = [
    # 01. Hero Intro (4.0s = 120f)
    {"id": "intro", "frames": 120, "title": "SYSTEM ARCHITECTURE & SIH26156 OVERVIEW", "tag": "Team Black Pearl | SIH 2026"},
    # 02. End-to-End Pipeline Architecture (4.0s = 120f)
    {"id": "arch_pipeline", "frames": 120, "title": "STREAMING INGESTION TO SIEM PIPELINE", "tag": "Kafka KRaft • Microsecond Engine"},
    # 03. Live Linux Syslog (UDP 5140) (3.8s = 114f)
    {"id": "live_syslog", "frames": 114, "title": "LIVE INGESTION: LINUX SYSLOG UDP PORT 5140", "tag": "Zero Packet Drop UDP Socket"},
    # 04. Live Firewall KV REST API (3.8s = 114f)
    {"id": "live_firewall", "frames": 114, "title": "LIVE INGESTION: ENTERPRISE FIREWALL KV (REST)", "tag": "FastAPI Async Gateway • < 0.2ms"},
    # 05. Live Web App Ingestion (3.8s = 114f)
    {"id": "live_webapp", "frames": 114, "title": "LIVE INGESTION: WEB APPLICATION SECURITY LOGS", "tag": "Multi-Tenant HTTP Security Stream"},
    # 06. SIH Home Portal Overview (4.0s = 120f)
    {"id": "sih_portal", "frames": 120, "title": "SIH 2026 UNIFIED OPERATIONS DASHBOARD", "tag": "White Theme Unified Portal"},
    # 07. Infrastructure Health & Metrics (4.0s = 120f)
    {"id": "infra_health", "frames": 120, "title": "LIVE INFRASTRUCTURE HEALTH & EPS TELEMETRY", "tag": "Kafka Buffer • ACID PostgreSQL"},
    # 08. Heterogeneous Sources View (3.6s = 108f)
    {"id": "sources_view", "frames": 108, "title": "HETEROGENEOUS SOURCE CONNECTORS (4 ACTIVE)", "tag": "UDP, REST, JSON & Microservices"},
    # 09. Live Normalization: Firewall KV to ECS (4.2s = 126f)
    {"id": "norm_firewall", "frames": 126, "title": "DETERMINISTIC NORMALIZATION: FIREWALL KV -> ECS", "tag": "Elastic Common Schema (ECS)"},
    # 10. Live Normalization: Syslog to ECS (4.0s = 120f)
    {"id": "norm_syslog", "frames": 120, "title": "DETERMINISTIC NORMALIZATION: SYSLOG AUTH -> ECS", "tag": "Cross-Vendor Harmonization"},
    # 11. Zero Data Loss & Unmapped Bucket (3.8s = 114f)
    {"id": "zero_loss", "frames": 114, "title": "ZERO DATA LOSS GUARANTEE: UNMAPPED BUCKET", "tag": "100% Forensic Integrity Preserved"},
    # 12. Event Explorer & Search (4.0s = 120f)
    {"id": "explorer", "frames": 120, "title": "EVENT EXPLORER: SUB-SECOND TELEMETRY SEARCH", "tag": "Real-Time Query & Filter Engine"},
    # 13. Field-Level Lineage & Provenance (4.2s = 126f)
    {"id": "lineage", "frames": 126, "title": "FIELD-LEVEL LINEAGE & PROVENANCE TRACKING", "tag": "Immutable Legal Chain of Custody"},
    # 14. Unknown Proprietary Log Encounter (3.6s = 108f)
    {"id": "unknown_alert", "frames": 108, "title": "INCIDENT TRIGGER: UNKNOWN LOG FORMAT DETECTED", "tag": "Automated AI Onboarding Route"},
    # 15. AI Onboarding Studio: Heuristic Synthesis (4.2s = 126f)
    {"id": "ai_synthesis", "frames": 126, "title": "AI ONBOARDING STUDIO: HEURISTIC SYNTHESIS", "tag": "Air-Gapped Local LLM (Zero Cloud)"},
    # 16. AI Studio: Automated Validation (3.8s = 114f)
    {"id": "ai_validation", "frames": 114, "title": "AI STUDIO: AUTOMATED TEST SUITE & APPROVAL", "tag": "100% Pass Rate • 98.4% Confidence"},
    # 17. Parser Registry Dynamic Hot-Reload (3.6s = 108f)
    {"id": "registry_reload", "frames": 108, "title": "PARSER REGISTRY: ZERO-DOWNTIME HOT RELOAD", "tag": "Instant Dynamic In-Memory Reload"},
    # 18. Testing Sandbox & Prototyping (3.8s = 114f)
    {"id": "testing_sandbox", "frames": 114, "title": "TESTING SANDBOX: LIVE REGEX & SCHEMA DEBUGGER", "tag": "Interactive SOC Prototyping"},
    # 19. Historical Replay Engine (4.0s = 120f)
    {"id": "historical_replay", "frames": 120, "title": "HISTORICAL LOG REPLAY & BATCH BENCHMARK", "tag": "8,500 evt/s Processing Speed"},
    # 20. SOC Analyst Full Dark Mode (3.8s = 114f)
    {"id": "dark_mode", "frames": 114, "title": "24/7 SOC OPERATOR EXPERIENCE (DARK THEME)", "tag": "Ergonomic High-Contrast Theme"},
    # 21. Enterprise SIEM Export Ecosystem (3.8s = 114f)
    {"id": "siem_export", "frames": 114, "title": "ENTERPRISE SIEM EXPORT (SPLUNK, ELASTIC, API)", "tag": "REST, WebSockets & HEC Ready"},
    # 22. Defensive Security & Air-Gapped Verification (3.8s = 114f)
    {"id": "defense_security", "frames": 114, "title": "DEFENSIVE SECURITY & 100% AIR-GAPPED AUDIT", "tag": "Zero Dynamic eval() • 100% Local"},
    # 23. SIH26156 Requirement Matrix (3.8s = 114f)
    {"id": "sih_matrix", "frames": 114, "title": "SIH 2026 REQUIREMENT COMPLIANCE MATRIX", "tag": "100% Clauses Satisfied & Audited"},
    # 24. Grand Finale Showcase (4.0s = 120f)
    {"id": "outro", "frames": 120, "title": "SARVDRISHTI: ENTERPRISE LOG INTELLIGENCE ENGINE", "tag": "Production-Ready • Team Black Pearl"},
]

TOTAL_FRAMES = sum(s["frames"] for s in SCENES)

print(f"[INIT] Video configured: {len(SCENES)} scenes, {TOTAL_FRAMES} frames ({TOTAL_FRAMES / FPS:.1f}s)")

# ─────────────────────────────────────────────────────────────────────────────
# SCENE RENDERER FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def render_scene_frame(scene, f_idx, g_frame):
    n_frames = scene["frames"]
    t = f_idx / max(1, n_frames - 1) # 0.0 to 1.0
    sid = scene["id"]

    # Start with base image
    base = Image.new("RGBA", (W, H), BG_VOID)
    draw = ImageDraw.Draw(base)

    # -------------------------------------------------------------------------
    # 01. INTRO
    # -------------------------------------------------------------------------
    if sid == "intro":
        # Draw cyber grid
        for gy in range(80, H - 60, 60):
            draw.line([(0, gy), (W, gy)], fill=(16, 28, 52), width=1)
        for gx in range(0, W, 80):
            draw.line([(gx, 60), (gx, H - 50)], fill=(16, 28, 52), width=1)

        # Pulse rings
        cx, cy = W // 2, 340
        for ring in (120, 190, 270):
            r_rad = int(ring + 20 * math.sin(t * 6.28 + ring))
            draw.ellipse([(cx - r_rad, cy - r_rad), (cx + r_rad, cy + r_rad)], outline=(0, 229, 255, 45), width=2)

        # SarvDrishti Logo in center
        if screenshots.get("logo"):
            lg = screenshots["logo"]
            lg_w = 480
            lg_h = int(lg.height * (lg_w / lg.width))
            lg_resized = lg.resize((lg_w, lg_h), Image.Resampling.LANCZOS)
            base.paste(lg_resized, (cx - lg_w // 2, cy - lg_h // 2 - 30), lg_resized)

        # Hero Typography
        text_center(draw, "SARVDRISHTI v1.0", 470, f_giant, fill=TEXT_WHITE)
        text_center(draw, "Unified Real-Time Log Intelligence & Deterministic Normalization Engine", 555, f_title, fill=ACCENT_CYAN)
        text_center(draw, "Team Black Pearl | Smart India Hackathon 2026 (Problem Statement: SIH26156)", 605, f_sub, fill=TEXT_MUTED)

        # Tech Pills
        pills = ["FASTAPI 0.110", "APACHE KAFKA KRAFT", "REACT 18 + VITE", "POSTGRESQL 15", "100% AIR-GAPPED"]
        pw_total = len(pills) * 190
        px_start = (W - pw_total) // 2
        for i, pill in enumerate(pills):
            px = px_start + i * 190
            draw_rrect(draw, px, 680, px + 175, 720, r=8, fill=(18, 30, 56), outline=BORDER_CYAN, width=1)
            text_center(draw, pill, 692, f_badge, fill=ACCENT_GREEN if i == 4 else TEXT_WHITE, x_offset=px, width=175)

        # Problem Statement Callout Card
        draw_rrect(draw, 240, 760, W - 240, 940, r=12, fill=(14, 22, 40), outline=ACCENT_ORANGE, width=2)
        draw.text((270, 780), "THE ENTERPRISE SOC CRISIS SOLVED:", fill=ACCENT_ORANGE, font=f_badge)
        draw.text((270, 810), "Heterogeneous security appliances (Firewalls, Linux Syslog, Cloud, Web Apps) flood SOCs in incompatible formats.", fill=TEXT_LIGHT, font=f_sub)
        draw.text((270, 850), "SarvDrishti unifies them instantly into Elastic Common Schema (ECS) with microsecond latency & zero data loss.", fill=ACCENT_CYAN, font=f_sub)
        draw.text((270, 895), "[DEFENSIVE CYBERSECURITY]  •  [IMMUTABLE FIELD LINEAGE]  •  [AIR-GAPPED AI ONBOARDING]", fill=ACCENT_GREEN, font=f_badge)

    # -------------------------------------------------------------------------
    # 02. ARCHITECTURE PIPELINE
    # -------------------------------------------------------------------------
    elif sid == "arch_pipeline":
        if screenshots.get("tech_slide"):
            base.paste(screenshots["tech_slide"], (0, 0))
        # Draw active animated pipeline overlay
        draw_rrect(draw, 100, 100, W - 100, 360, r=12, fill=(10, 18, 34, 235), outline=BORDER_CYAN, width=2)
        draw.text((130, 120), "END-TO-END STREAMING INGESTION ARCHITECTURE", fill=ACCENT_CYAN, font=f_title)
        
        stages = [
            ("HETEROGENEOUS\nSOURCES", "Syslog 5140\nFirewall REST\nWeb Apps", ACCENT_ORANGE),
            ("STREAM BUFFER\n(KAFKA KRAFT)", "Zero Drop Queue\nPartitioned\nHigh Throughput", ACCENT_PURPLE),
            ("DETERMINISTIC\nPARSER ENGINE", "Compiled Regex\nDirect KV Splitting\n< 0.14ms Latency", ACCENT_CYAN),
            ("UNIVERSAL ECS\nNORMALIZER", "Harmonized Schema\nField Type Casting\nUnmapped Bucket", ACCENT_GREEN),
            ("STORAGE &\nSIEM EXPORT", "PostgreSQL ACID\nSplunk HEC Export\nWebSocket Feeds", ACCENT_BLUE),
        ]
        
        sx = 140
        sw = 300
        for i, (stitle, sdesc, scol) in enumerate(stages):
            draw_rrect(draw, sx, 180, sx + sw, 320, r=8, fill=(18, 28, 52), outline=scol, width=2)
            # Stage Title
            lines = stitle.split("\n")
            draw.text((sx + 15, 195), lines[0], fill=scol, font=f_badge)
            if len(lines) > 1:
                draw.text((sx + 15, 215), lines[1], fill=scol, font=f_badge)
            # Stage Desc
            dlines = sdesc.split("\n")
            dy = 245
            for dl in dlines:
                draw.text((sx + 15, dy), dl, fill=TEXT_MUTED, font=f_mono_sm)
                dy += 20
            
            # Connector arrow
            if i < len(stages) - 1:
                ax0 = sx + sw + 5
                ax1 = sx + sw + 35
                draw.line([(ax0, 250), (ax1, 250)], fill=BORDER_CYAN, width=3)
                # Traveling packet dot
                pkt_x = int(ax0 + (ax1 - ax0) * (t * 2 % 1.0))
                draw.ellipse([(pkt_x - 4, 246), (pkt_x + 4, 254)], fill=TEXT_WHITE)
            sx += sw + 40

        # Specs bar
        draw_rrect(draw, 100, 880, W - 100, 980, r=10, fill=(12, 20, 36), outline=ACCENT_GREEN, width=1)
        draw.text((130, 905), "ARCHITECTURAL GUARANTEES: Sub-millisecond parsing (<0.2ms) • Zero dynamic eval() • 100% Air-Gapped", fill=ACCENT_GREEN, font=f_sub)
        draw.text((130, 940), "Dual Storage: In-memory streaming buffer + ACID transactional storage with complete provenance index", fill=TEXT_MUTED, font=f_body)

    # -------------------------------------------------------------------------
    # 03. LIVE SYSLOG UDP 5140
    # -------------------------------------------------------------------------
    elif sid == "live_syslog":
        log_stream = [
            f"[LIVE UDP SYSLOG] -> Sent SSHD Auth Log: user=admin ip=10.10.14.{10 + f_idx % 40}",
            f"[LIVE UDP SYSLOG] -> Failed password for invalid user root from 10.10.22.{30 + f_idx % 50}",
            f"[LIVE UDP SYSLOG] -> Accepted publickey for john_dev from 10.10.3.{5 + f_idx % 20} ssh2",
            f"[LIVE UDP SYSLOG] -> sudo: operator : TTY=pts/0 ; COMMAND=/bin/systemctl status sarvdrishti",
            f"[LIVE UDP SYSLOG] -> kernel: [NETFILTER] UDP packet intercepted on port 5140 (len=142)",
            f"[LIVE UDP SYSLOG] -> Accepted password for sec_auditor from 10.10.1.99 port 5140",
            f"[LIVE UDP SYSLOG] -> Failed password for user test from 10.10.45.12 port 48210",
            f"[LIVE UDP SYSLOG] -> PAM 2 more authentication failures; logname= uid=0 euid=0 tty=ssh",
            f"[LIVE UDP SYSLOG] -> SSH connection closed by 10.10.14.23 port 49122 [preauth]",
            f"[LIVE UDP SYSLOG] -> Sent SSHD Auth Log: user=deploy_bot ip=10.10.8.14",
        ]
        draw_terminal_window(draw, 100, 100, 1140, 860, "bash: scripts/live_stream_generator.py --stream syslog --port 5140", log_stream[: 4 + int(t * 6)])
        
        # Right Side Live Telemetry HUD
        rx = 1280
        draw_rrect(draw, rx, 100, W - 100, 960, r=12, fill=(14, 22, 40), outline=BORDER_CYAN, width=2)
        draw.text((rx + 25, 130), "UDP LISTENER TELEMETRY", fill=ACCENT_CYAN, font=f_title)
        
        metrics = [
            ("LISTENER PORT", "5140 (UDP Syslog)"),
            ("INTERCEPTION SPEED", "< 0.18 ms"),
            ("SOCKET BUFFER", "Zero Packet Drop"),
            ("PACKETS INGESTED", f"{2840 + f_idx * 14:,}"),
            ("PARSER MAPPING", "syslog-auth-v1"),
            ("SCHEMA HARMONIZED", "Elastic ECS (user, host)"),
        ]
        my = 190
        for mlabel, mval in metrics:
            draw_rrect(draw, rx + 25, my, W - 125, my + 65, r=8, fill=(20, 32, 56), outline=BORDER_MUTED)
            draw.text((rx + 40, my + 12), mlabel, fill=TEXT_MUTED, font=f_badge)
            draw.text((rx + 40, my + 34), mval, fill=ACCENT_GREEN if "Zero" in mval or "<" in mval else TEXT_WHITE, font=f_sub)
            my += 80

        draw_rrect(draw, rx + 25, 780, W - 125, 920, r=8, fill=(18, 36, 32), outline=ACCENT_GREEN, width=2)
        draw.text((rx + 40, 805), "REAL HARDWARE CAPABLE:", fill=ACCENT_GREEN, font=f_badge)
        draw.text((rx + 40, 835), "Any Linux server, router, or switch can point syslog to port 5140.", fill=TEXT_LIGHT, font=f_body)
        draw.text((rx + 40, 870), "Instant normalization without modifying source agent.", fill=TEXT_MUTED, font=f_body)

    # -------------------------------------------------------------------------
    # 04. LIVE FIREWALL REST API
    # -------------------------------------------------------------------------
    elif sid == "live_firewall":
        log_stream = [
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.4.{10 + f_idx % 20}:4521 -> 172.16.1.5:443 [ALLOW]",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.19.{30 + f_idx % 30}:8080 -> 172.16.3.22:22 [DENY]",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.7.34:53 -> 8.8.8.8:53 [ALLOW] DNS_RULE_02",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.12.89:3389 -> 172.16.2.14:3389 [DENY] RDP_BLOCK",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.2.100:443 -> 10.0.0.1:443 [ALLOW] TLS_1_3",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.33.12:80 -> 192.168.1.1:80 [ALLOW] HTTP_INGRESS",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.9.45:445 -> 172.16.1.10:445 [DENY] SMB_RULE",
            f"[LIVE FIREWALL KV] -> Sent: SRC=10.10.50.1:500 -> 172.16.0.1:500 [ALLOW] IPSEC_TUNNEL",
        ]
        draw_terminal_window(draw, 100, 100, 1140, 860, "bash: curl -X POST /api/events/ingest (Firewall KV Ingestion Stream)", log_stream[: 4 + int(t * 5)])

        rx = 1280
        draw_rrect(draw, rx, 100, W - 100, 960, r=12, fill=(14, 22, 40), outline=ACCENT_ORANGE, width=2)
        draw.text((rx + 25, 130), "REST API INGESTION GATEWAY", fill=ACCENT_ORANGE, font=f_title)
        
        metrics = [
            ("ENDPOINT", "POST /api/events/ingest"),
            ("HTTP LATENCY", "0.14 ms (FastAPI Async)"),
            ("THROUGHPUT", "3,400 payloads / sec"),
            ("PARSER MAPPING", "firewall-kv-v1"),
            ("FORMAT SUPPORT", "Cisco, Palo Alto, Fortinet"),
            ("VALIDATION", "Pydantic V2 Strict"),
        ]
        my = 190
        for mlabel, mval in metrics:
            draw_rrect(draw, rx + 25, my, W - 125, my + 65, r=8, fill=(20, 32, 56), outline=BORDER_MUTED)
            draw.text((rx + 40, my + 12), mlabel, fill=TEXT_MUTED, font=f_badge)
            draw.text((rx + 40, my + 34), mval, fill=ACCENT_GREEN if "0.14" in mval or "Strict" in mval else TEXT_WHITE, font=f_sub)
            my += 80

        draw_rrect(draw, rx + 25, 780, W - 125, 920, r=8, fill=(36, 28, 16), outline=ACCENT_ORANGE, width=2)
        draw.text((rx + 40, 805), "ENTERPRISE READY:", fill=ACCENT_ORANGE, font=f_badge)
        draw.text((rx + 40, 835), "Accepts standard key-value, JSON, and raw syslog lines concurrently.", fill=TEXT_LIGHT, font=f_body)
        draw.text((rx + 40, 870), "Auto-detects format signature in under 15 microseconds.", fill=TEXT_MUTED, font=f_body)

    # -------------------------------------------------------------------------
    # 05. LIVE WEB APP INGESTION
    # -------------------------------------------------------------------------
    elif sid == "live_webapp":
        log_stream = [
            f"[LIVE WEB APP] -> POST /api/v1/auth/token [200 OK] user=john_dev resp=12ms",
            f"[LIVE WEB APP] -> GET /api/v1/users [200 OK] user=sec_auditor resp=8ms",
            f"[LIVE WEB APP] -> POST /admin/settings [403 FORBIDDEN] user=guest_user resp=4ms",
            f"[LIVE WEB APP] -> POST /checkout [201 CREATED] user=alice resp=45ms",
            f"[LIVE WEB APP] -> GET /api/v1/health [200 OK] user=prometheus resp=2ms",
            f"[LIVE WEB APP] -> POST /api/v1/upload [500 SERVER_ERROR] user=operator resp=110ms",
            f"[LIVE WEB APP] -> DELETE /api/v1/items/402 [204 NO_CONTENT] user=admin resp=18ms",
            f"[LIVE WEB APP] -> GET /api/v1/lineage/inspect [200 OK] user=auditor resp=15ms",
        ]
        draw_terminal_window(draw, 100, 100, 1140, 860, "bash: Real-Time Web & Microservice Telemetry Ingestion", log_stream[: 4 + int(t * 5)])

        rx = 1280
        draw_rrect(draw, rx, 100, W - 100, 960, r=12, fill=(14, 22, 40), outline=ACCENT_GREEN, width=2)
        draw.text((rx + 25, 130), "WEB SECURITY TELEMETRY", fill=ACCENT_GREEN, font=f_title)
        
        metrics = [
            ("DATA FORMAT", "JSON & W3C Combined Log"),
            ("HTTP STATUS MONITOR", "200, 401, 403, 500 Tracking"),
            ("GEO & IP EXTRACTION", "source.ip -> Client Geolocation"),
            ("PARSER MAPPING", "webapp-access-v1"),
            ("ANOMALY BUFFER", "Surge Protection Active"),
            ("SIEM COMPLIANCE", "OWASP Web Security ECS"),
        ]
        my = 190
        for mlabel, mval in metrics:
            draw_rrect(draw, rx + 25, my, W - 125, my + 65, r=8, fill=(20, 32, 56), outline=BORDER_MUTED)
            draw.text((rx + 40, my + 12), mlabel, fill=TEXT_MUTED, font=f_badge)
            draw.text((rx + 40, my + 34), mval, fill=ACCENT_GREEN if "Active" in mval else TEXT_WHITE, font=f_sub)
            my += 80

        draw_rrect(draw, rx + 25, 780, W - 125, 920, r=8, fill=(18, 36, 26), outline=ACCENT_GREEN, width=2)
        draw.text((rx + 40, 805), "DYNAMIC PARSER ROUTING:", fill=ACCENT_GREEN, font=f_badge)
        draw.text((rx + 40, 835), "Web access logs are parsed directly into HTTP request/response ECS fields.", fill=TEXT_LIGHT, font=f_body)
        draw.text((rx + 40, 870), "Ready for SOC incident investigation and threat hunting.", fill=TEXT_MUTED, font=f_body)

    # -------------------------------------------------------------------------
    # 06. SIH HOME PORTAL OVERVIEW
    # -------------------------------------------------------------------------
    elif sid == "sih_portal":
        if screenshots.get("home_white"):
            base.paste(screenshots["home_white"], (0, 0))
        # Draw high-tech HUD callouts and laser sweep
        draw_screenshot_view(
            draw, base,
            focus_box=(40, 80, W - 40, 340),
            callout_pos=(80, 560, 680, 340),
            callout_lines=[
                ("SIH 2026 UNIFIED PORTAL (Team Black Pearl)", ACCENT_CYAN, True),
                ("• Clean White & Dark theme toggle for 24/7 SOC ergonomics", TEXT_WHITE, False),
                ("• Real-time KPI counters: Events Processed, Parsers, SLA", ACCENT_GREEN, False),
                ("• Interactive 5-stage ingestion pipeline visualizer", TEXT_WHITE, False),
                ("• SIH26156 Problem Statement compliance overview", ACCENT_CYAN, False),
                ("• Zero external CDNs: 100% self-hosted & air-gapped", ACCENT_PURPLE, False),
            ],
            anim_t=t
        )

    # -------------------------------------------------------------------------
    # 07. INFRASTRUCTURE HEALTH & METRICS
    # -------------------------------------------------------------------------
    elif sid == "infra_health":
        if screenshots.get("overview"):
            base.paste(screenshots["overview"], (0, 0))
        draw_screenshot_view(
            draw, base,
            focus_box=(50, 130, W - 50, 320),
            callout_pos=(1140, 500, 700, 380),
            callout_lines=[
                ("REAL-TIME INFRASTRUCTURE HEALTH", ACCENT_CYAN, True),
                ("• Apache Kafka Buffer: ONLINE (Zero Message Loss)", ACCENT_GREEN, False),
                ("• Worker Pool: 8 Ingestion Workers Active", TEXT_WHITE, False),
                ("• PostgreSQL Database: ACID Transactions Verified", ACCENT_GREEN, False),
                ("• Sub-millisecond parsing latency across all nodes", TEXT_WHITE, False),
                ("• Live WebGL log topology network graph", ACCENT_CYAN, False),
                ("• Deterministic parsing rules: 100% SLA Guarantee", ACCENT_GREEN, False),
            ],
            anim_t=t
        )

    # -------------------------------------------------------------------------
    # 08. SOURCES VIEW (MULTI-VENDOR)
    # -------------------------------------------------------------------------
    elif sid == "sources_view":
        # Multi-vendor connectors grid
        draw.text((100, 100), "HETEROGENEOUS SOURCE CONNECTORS (MULTI-VENDOR)", fill=ACCENT_CYAN, font=f_giant)
        draw.text((100, 175), "SarvDrishti ingests from any source simultaneously over network sockets and REST gateways.", fill=TEXT_MUTED, font=f_sub)

        sources = [
            ("1. LINUX SYSLOG (UDP 5140)", "Port: 5140 | Protocol: UDP\nActive Auth & Kernel Telemetry\nFormat: RFC 3164 / 5424\nStatus: STREAMING ONLINE", ACCENT_CYAN, "syslog-auth-v1"),
            ("2. PERIMETER FIREWALL (REST)", "Path: /api/events/ingest\nCisco / Fortinet Key-Value\nThroughput: 3,400 evt/s\nStatus: STREAMING ONLINE", ACCENT_ORANGE, "firewall-kv-v1"),
            ("3. WEB APPLICATION SERVER", "Path: /api/events/ingest\nJSON & Combined Log Format\nHTTP 200, 401, 403, 500\nStatus: STREAMING ONLINE", ACCENT_GREEN, "webapp-access-v1"),
            ("4. CUSTOM ENTERPRISE AGENT", "Protocol: WebSocket / REST\nCustom Microservice Telemetry\nAutomated AI Handled\nStatus: STREAMING ONLINE", ACCENT_PURPLE, "ai-synthesized-v1"),
        ]

        card_w = (W - 260) // 2
        card_h = 320
        coords = [(100, 240), (W // 2 + 30, 240), (100, 600), (W // 2 + 30, 600)]

        for i, (stitle, sbody, scol, sparser) in enumerate(sources):
            cx, cy = coords[i]
            draw_rrect(draw, cx, cy, cx + card_w, cy + card_h, r=12, fill=(14, 22, 40), outline=scol, width=2)
            draw_rrect(draw, cx, cy, cx + card_w, cy + 50, r=12, fill=(22, 34, 60))
            draw.rectangle([(cx, cy + 30), (cx + card_w, cy + 50)], fill=(22, 34, 60))
            
            # Title
            draw.text((cx + 20, cy + 14), stitle, fill=scol, font=f_title)
            
            # Status blinker
            draw.ellipse([(cx + card_w - 35, cy + 18), (cx + card_w - 20, cy + 33)], fill=ACCENT_GREEN)

            # Details
            dy = cy + 70
            for line in sbody.split("\n"):
                draw.text((cx + 25, dy), line, fill=TEXT_LIGHT if "Status" not in line else ACCENT_GREEN, font=f_sub)
                dy += 34

            # Parser pill
            draw_rrect(draw, cx + 25, cy + card_h - 55, cx + card_w - 25, cy + card_h - 15, r=6, fill=(16, 28, 48), outline=scol, width=1)
            draw.text((cx + 40, cy + card_h - 43), f"ACTIVE PARSER: {sparser}", fill=scol, font=f_badge)

    # -------------------------------------------------------------------------
    # 09. LIVE NORMALIZATION: FIREWALL KV -> ECS
    # -------------------------------------------------------------------------
    elif sid == "norm_firewall":
        raw_kv = "SRC=10.10.1.20 DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=ALLOW VENDOR_TAG=RULE_101 HOSTNAME=core-fw-01"
        ecs_kv = [
            ("timestamp", '"2026-10-06T08:38:14.210Z"', TEXT_WHITE),
            ("event.action", '"ALLOW"', ACCENT_GREEN),
            ("event.dataset", '"firewall"', TEXT_WHITE),
            ("source.ip", '"10.10.1.20"', ACCENT_CYAN),
            ("source.port", "4521", ACCENT_CYAN),
            ("destination.ip", '"172.16.2.10"', ACCENT_CYAN),
            ("destination.port", "443", ACCENT_CYAN),
            ("network.transport", '"tcp"', TEXT_WHITE),
            ("unmapped.vendor_tag", '"RULE_101"', ACCENT_ORANGE),
        ]
        draw_split_normalizer(draw, 100, 100, W - 200, 680, raw_kv, "firewall-kv-v1", ecs_kv, t)

        # Bottom Callout
        draw_rrect(draw, 100, 810, W - 100, 960, r=10, fill=(12, 22, 38), outline=ACCENT_GREEN, width=1)
        draw.text((130, 830), "CROSS-VENDOR HARMONIZATION:", fill=ACCENT_GREEN, font=f_title)
        draw.text((130, 870), "Raw firewall string split deterministically in 0.14ms into Elastic Common Schema (ECS).", fill=TEXT_LIGHT, font=f_sub)
        draw.text((130, 910), "Unknown vendor keys preserved in 'unmapped' JSON bucket with ZERO data loss.", fill=ACCENT_ORANGE, font=f_sub)

    # -------------------------------------------------------------------------
    # 10. LIVE NORMALIZATION: SYSLOG -> ECS
    # -------------------------------------------------------------------------
    elif sid == "norm_syslog":
        raw_sys = "Oct 06 08:38:22 prod-db01 sshd[2410]: Failed password for user admin from 10.10.1.50 port 48212 ssh2"
        ecs_sys = [
            ("timestamp", '"2026-10-06T08:38:22.000Z"', TEXT_WHITE),
            ("event.category", '"authentication"', TEXT_WHITE),
            ("event.action", '"LOGON_FAILED"', ACCENT_RED),
            ("event.outcome", '"failure"', ACCENT_RED),
            ("user.name", '"admin"', ACCENT_CYAN),
            ("source.ip", '"10.10.1.50"', ACCENT_CYAN),
            ("source.port", "48212", ACCENT_CYAN),
            ("host.hostname", '"prod-db01"', TEXT_WHITE),
            ("process.pid", "2410", TEXT_WHITE),
        ]
        draw_split_normalizer(draw, 100, 100, W - 200, 680, raw_sys, "syslog-auth-v1", ecs_sys, t)

        draw_rrect(draw, 100, 810, W - 100, 960, r=10, fill=(12, 22, 38), outline=ACCENT_CYAN, width=1)
        draw.text((130, 830), "UNIFIED SECURITY TAXONOMY:", fill=ACCENT_CYAN, font=f_title)
        draw.text((130, 870), "Both Linux SSHD and Cisco Firewalls map to identical 'source.ip' and 'event.action' fields.", fill=TEXT_LIGHT, font=f_sub)
        draw.text((130, 910), "SIEM detection rules run against universal fields without modifying queries per vendor.", fill=ACCENT_GREEN, font=f_sub)

    # -------------------------------------------------------------------------
    # 11. ZERO DATA LOSS & UNMAPPED BUCKET
    # -------------------------------------------------------------------------
    elif sid == "zero_loss":
        draw.text((100, 100), "ZERO DATA LOSS GUARANTEE (UNMAPPED BUCKET)", fill=ACCENT_ORANGE, font=f_giant)
        draw.text((100, 175), "Strict cybersecurity compliance mandates that no forensic telemetry is ever dropped.", fill=TEXT_MUTED, font=f_sub)

        # Flow Diagram
        bx, by = 100, 240
        bw = W - 200
        bh = 540
        draw_rrect(draw, bx, by, bx + bw, by + bh, r=12, fill=(14, 22, 40), outline=ACCENT_ORANGE, width=2)

        # 3 Stages of Preservation
        cards = [
            ("1. INCOMING PROPRIETARY PAYLOAD", [
                "SRC=10.10.1.50 DST=172.16.1.1",
                "VENDOR_MAGIC_ID=0xDEADBEEF",
                "INTERNAL_HW_REV=rev4.2_b9",
                "CUSTOM_POLICY_TAG=FW_AIRGAP",
            ], ACCENT_ORANGE),
            ("2. DETERMINISTIC PARSER ROUTING", [
                "Standard fields -> ECS Universal Schema",
                "Unmatched proprietary fields detected",
                "NOT DROPPED! Preserved losslessly",
                "Routed to JSONB unmapped bucket",
            ], ACCENT_CYAN),
            ("3. PERSISTED NORMALIZED RECORD", [
                '"source.ip": "10.10.1.50"',
                '"destination.ip": "172.16.1.1"',
                '"unmapped": {',
                '  "VENDOR_MAGIC_ID": "0xDEADBEEF",',
                '  "INTERNAL_HW_REV": "rev4.2_b9"',
                '}',
            ], ACCENT_GREEN),
        ]

        cw = (bw - 100) // 3
        for i, (ctitle, clines, ccol) in enumerate(cards):
            cx = bx + 35 + i * (cw + 15)
            draw_rrect(draw, cx, by + 40, cx + cw, by + bh - 40, r=10, fill=(20, 32, 56), outline=ccol, width=2)
            draw.text((cx + 15, by + 60), ctitle, fill=ccol, font=f_badge)
            ly = by + 110
            for line in clines:
                draw.text((cx + 15, ly), line, fill=TEXT_WHITE if "unmapped" in line else TEXT_LIGHT, font=f_mono_sm)
                ly += 30

        # Badge
        draw_rrect(draw, 100, 810, W - 100, 960, r=10, fill=(36, 24, 16), outline=ACCENT_ORANGE, width=2)
        draw.text((130, 830), "AUDIT & LEGAL ASSURANCE: 100% RAW RECONSTRUCTION GUARANTEED", fill=ACCENT_ORANGE, font=f_title)
        draw.text((130, 870), "Original raw payload is hashed with SHA-256 and stored alongside normalized JSON.", fill=TEXT_LIGHT, font=f_sub)
        draw.text((130, 910), "Full cryptographic evidence preservation for courtroom cybersecurity defense.", fill=ACCENT_GREEN, font=f_sub)

    # -------------------------------------------------------------------------
    # 12. EVENT EXPLORER
    # -------------------------------------------------------------------------
    elif sid == "explorer":
        if screenshots.get("verified"):
            base.paste(screenshots["verified"], (0, 0))
        draw_screenshot_view(
            draw, base,
            focus_box=(50, 110, W - 50, 480),
            callout_pos=(80, 600, 780, 340),
            callout_lines=[
                ("EVENT EXPLORER: SUB-SECOND TELEMETRY SEARCH", ACCENT_CYAN, True),
                ("• Real-time searchable event stream with multi-column filtering", TEXT_WHITE, False),
                ("• Search by source IP, event action, user, or dataset", ACCENT_GREEN, False),
                ("• Side-by-side Raw Payload vs Normalized ECS JSON Inspector", TEXT_WHITE, False),
                ("• Color-coded outcome badges (ALLOW = Green, DENY = Red)", ACCENT_ORANGE, False),
                ("• Deep-link to Field Lineage Viewer with single click", ACCENT_CYAN, False),
            ],
            anim_t=t
        )

    # -------------------------------------------------------------------------
    # 13. FIELD-LEVEL LINEAGE
    # -------------------------------------------------------------------------
    elif sid == "lineage":
        draw_lineage_graph(draw, 100, 100, W - 200, 860, "SRC=10.10.1.20", '"source.ip": "10.10.1.20"', "firewall-kv-v1", t)

    # -------------------------------------------------------------------------
    # 14. UNKNOWN LOG ALERT TRIGGER
    # -------------------------------------------------------------------------
    elif sid == "unknown_alert":
        # Dramatic alert card
        draw.rectangle([(0, 60), (W, H - 50)], fill=(18, 12, 16))
        
        # Red flashing border
        b_col = ACCENT_RED if (int(t * 8) % 2 == 0) else (120, 20, 20)
        draw_rrect(draw, 120, 120, W - 120, H - 120, r=16, fill=(24, 16, 22), outline=b_col, width=3)

        draw.text((180, 160), "⚠️  AUTOMATED ANOMALY ROUTING TRIGGERED", fill=ACCENT_RED, font=f_giant)
        draw.text((180, 240), "Unrecognized proprietary telemetry arrived with no existing parser in registry.", fill=TEXT_LIGHT, font=f_title)

        # Raw string box
        draw_rrect(draw, 180, 320, W - 180, 440, r=10, fill=(12, 12, 18), outline=ACCENT_RED, width=2)
        draw.text((210, 340), "INCOMING UNPARSED TELEMETRY PAYLOAD:", fill=TEXT_MUTED, font=f_badge)
        draw.text((210, 380), "[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL", fill=TEXT_WHITE, font=f_mono_lg)

        # Traditional SIEM vs SarvDrishti comparison
        draw_rrect(draw, 180, 480, W // 2 - 20, 720, r=10, fill=(32, 18, 22), outline=ACCENT_RED, width=1)
        draw.text((210, 505), "TRADITIONAL SIEM BEHAVIOR:", fill=ACCENT_RED, font=f_title)
        draw.text((210, 555), "❌ Drops event or saves as unparsed blob", fill=TEXT_LIGHT, font=f_sub)
        draw.text((210, 595), "❌ Requires SOC engineer to manually write regex", fill=TEXT_LIGHT, font=f_sub)
        draw.text((210, 635), "❌ Takes days to deploy to production", fill=TEXT_LIGHT, font=f_sub)

        draw_rrect(draw, W // 2 + 20, 480, W - 180, 720, r=10, fill=(16, 32, 26), outline=ACCENT_GREEN, width=2)
        draw.text((W // 2 + 50, 505), "SARVDRISHTI SOLUTION:", fill=ACCENT_GREEN, font=f_title)
        draw.text((W // 2 + 50, 555), "✓ Traps event & forwards to AI Onboarding Studio", fill=TEXT_LIGHT, font=f_sub)
        draw.text((W // 2 + 50, 595), "✓ Synthesizes production regex parser in 2 seconds", fill=ACCENT_GREEN, font=f_sub)
        draw.text((W // 2 + 50, 635), "✓ Validates with synthetic test cases & hot reloads", fill=TEXT_LIGHT, font=f_sub)

        # Routing banner
        draw_rrect(draw, 180, 760, W - 180, 860, r=10, fill=(20, 36, 60), outline=BORDER_CYAN, width=2)
        draw.text((210, 795), "ACTION: Transferring payload to AI Onboarding Studio workbench...", fill=ACCENT_CYAN, font=f_title)

    # -------------------------------------------------------------------------
    # 15. AI ONBOARDING STUDIO: SYNTHESIS
    # -------------------------------------------------------------------------
    elif sid == "ai_synthesis":
        raw_unknown = "[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL"
        regex_synth = r"^\[AUDIT\]\s+user=(?P<user>\w+)\s+op=(?P<action>\w+)\s+file=(?P<file>[^\s]+)\s+host=(?P<host>[^\s]+)"
        anim_step = 1 if t > 0.4 else 0
        draw_ai_studio(draw, 100, 100, W - 200, 860, raw_unknown, regex_synth, 98.4, anim_step)

    # -------------------------------------------------------------------------
    # 16. AI ONBOARDING STUDIO: VALIDATION & APPROVE
    # -------------------------------------------------------------------------
    elif sid == "ai_validation":
        raw_unknown = "[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL"
        regex_synth = r"^\[AUDIT\]\s+user=(?P<user>\w+)\s+op=(?P<action>\w+)\s+file=(?P<file>[^\s]+)\s+host=(?P<host>[^\s]+)"
        draw_ai_studio(draw, 100, 100, W - 200, 860, raw_unknown, regex_synth, 98.4, 2)

    # -------------------------------------------------------------------------
    # 17. PARSER REGISTRY: DYNAMIC HOT-RELOAD
    # -------------------------------------------------------------------------
    elif sid == "registry_reload":
        draw.text((100, 100), "PARSER REGISTRY: DYNAMIC HOT-RELOAD", fill=ACCENT_CYAN, font=f_giant)
        draw.text((100, 175), "Newly approved parser is hot-reloaded into live pipeline with ZERO service restart.", fill=TEXT_MUTED, font=f_sub)

        # Active Parsers Table
        draw_rrect(draw, 100, 240, W - 100, 760, r=12, fill=(14, 22, 40), outline=BORDER_CYAN, width=2)
        draw_rrect(draw, 100, 240, W - 100, 300, r=12, fill=(22, 34, 60))
        draw.rectangle([(100, 275), (W - 100, 300)], fill=(22, 34, 60))

        headers = [("PARSER ID", 140), ("SIGNATURE", 420), ("TYPE", 780), ("TARGET SCHEMA", 1020), ("LATENCY", 1320), ("STATUS", 1540)]
        for htext, hx in headers:
            draw.text((hx, 258), htext, fill=TEXT_MUTED, font=f_badge)

        rows = [
            ("syslog-auth-v1", "sshd[*]: Failed password", "Regex RFC3164", "Elastic ECS (Auth)", "0.12 ms", "ACTIVE [HOT]"),
            ("firewall-kv-v1", "SRC=* DST=* PROTO=*", "Key-Value Split", "Elastic ECS (Network)", "0.14 ms", "ACTIVE [HOT]"),
            ("webapp-access-v1", "method=* path=* status=*", "W3C / JSON", "Elastic ECS (HTTP)", "0.16 ms", "ACTIVE [HOT]"),
            ("custom-app-v1", "{\"app\": \"*\", \"level\": \"*\"}", "JSON Object", "Elastic ECS (Core)", "0.11 ms", "ACTIVE [HOT]"),
            ("audit-log-v1 [NEW]", "[AUDIT] user=* op=*", "AI-Synthesized Regex", "Elastic ECS (Audit)", "0.15 ms", "HOT-RELOADED ✓"),
        ]

        ry = 320
        for r_id, r_sig, r_typ, r_sch, r_lat, r_stat in rows:
            is_new = "[NEW]" in r_id
            row_col = (18, 38, 30) if is_new else (18, 28, 50)
            draw_rrect(draw, 120, ry, W - 120, ry + 55, r=6, fill=row_col, outline=ACCENT_GREEN if is_new else BORDER_MUTED, width=2 if is_new else 1)
            draw.text((140, ry + 16), r_id, fill=ACCENT_CYAN if not is_new else ACCENT_GREEN, font=f_mono)
            draw.text((420, ry + 16), r_sig, fill=TEXT_WHITE, font=f_mono_sm)
            draw.text((780, ry + 16), r_typ, fill=TEXT_MUTED, font=f_body)
            draw.text((1020, ry + 16), r_sch, fill=TEXT_LIGHT, font=f_body)
            draw.text((1320, ry + 16), r_lat, fill=ACCENT_GREEN, font=f_mono_sm)
            draw.text((1540, ry + 16), r_stat, fill=ACCENT_GREEN, font=f_badge)
            ry += 75

        # Metric Card at bottom
        draw_rrect(draw, 100, 800, W - 100, 940, r=10, fill=(16, 32, 28), outline=ACCENT_GREEN, width=2)
        draw.text((130, 825), "ZERO DOWNTIME HOT RELOADING VERIFIED (< 3.2ms)", fill=ACCENT_GREEN, font=f_title)
        draw.text((130, 865), "Pipeline did not drop a single in-flight packet while updating thread-safe parser registry.", fill=TEXT_LIGHT, font=f_sub)
        draw.text((130, 900), "Kafka consumer workers seamlessly switched to new regex rules in real time.", fill=ACCENT_CYAN, font=f_sub)

    # -------------------------------------------------------------------------
    # 18. TESTING SANDBOX & PROTOTYPING
    # -------------------------------------------------------------------------
    elif sid == "testing_sandbox":
        draw.text((100, 100), "TESTING SANDBOX: LIVE REGEX & SCHEMA DEBUGGER", fill=ACCENT_CYAN, font=f_giant)
        draw.text((100, 175), "Interactive playground for security engineers to test edge cases before production registration.", fill=TEXT_MUTED, font=f_sub)

        # Split editor & debugger
        bw = (W - 240) // 2
        # Left Editor
        draw_rrect(draw, 100, 240, 100 + bw, 760, r=12, fill=(14, 22, 40), outline=BORDER_CYAN, width=2)
        draw.text((125, 260), "1. REGEX TEST BENCH & LIVE MATCH VISUALIZER", fill=ACCENT_CYAN, font=f_title)
        draw.text((125, 305), "Pattern:", fill=TEXT_MUTED, font=f_badge)
        draw.text((125, 330), r"(?P<ip>\d+\.\d+\.\d+\.\d+):(?P<port>\d+)", fill=ACCENT_PURPLE, font=f_mono)
        
        draw.text((125, 390), "Test Payload:", fill=TEXT_MUTED, font=f_badge)
        draw.text((125, 420), "ALERT from 192.168.1.100:8443 by root", fill=TEXT_WHITE, font=f_mono)

        draw_rrect(draw, 125, 480, 100 + bw - 25, 720, r=8, fill=(20, 32, 56))
        draw.text((145, 500), "MATCH TOKENS CAPTURED:", fill=ACCENT_GREEN, font=f_badge)
        draw.text((145, 540), "Group 1 (ip):   192.168.1.100  -> source.ip", fill=ACCENT_CYAN, font=f_mono)
        draw.text((145, 580), "Group 2 (port): 8443           -> source.port", fill=ACCENT_CYAN, font=f_mono)
        draw.text((145, 630), "EXECUTION TIME: 0.08 ms (12,500 executions/sec)", fill=ACCENT_GREEN, font=f_mono_sm)
        draw.text((145, 665), "REVERT / COMMIT: Instant rollback protection", fill=TEXT_MUTED, font=f_mono_sm)

        # Right Conformance Suite
        rx = 140 + bw
        draw_rrect(draw, rx, 240, rx + bw, 760, r=12, fill=(14, 22, 40), outline=ACCENT_GREEN, width=2)
        draw.text((rx + 25, 260), "2. AUTOMATED CONFORMANCE & SECURITY TESTS", fill=ACCENT_GREEN, font=f_title)
        
        tests = [
            ("ReDoS Vulnerability Scan", "PASS (Safe)", ACCENT_GREEN),
            ("Extreme Payload Fuzzing (64KB)", "PASS (No Crash)", ACCENT_GREEN),
            ("Malformed Syntax Graceful Handling", "PASS (Lossless)", ACCENT_GREEN),
            ("Unmapped Field Preservation", "PASS (Preserved)", ACCENT_GREEN),
            ("Schema Type Safety Cast", "PASS (Strict Types)", ACCENT_GREEN),
            ("Kafka Pipeline Stress Test", "PASS (0 Drop)", ACCENT_GREEN),
        ]
        ty = 320
        for tname, tstat, tcol in tests:
            draw_rrect(draw, rx + 25, ty, rx + bw - 25, ty + 50, r=6, fill=(20, 34, 54), outline=BORDER_MUTED)
            draw.text((rx + 40, ty + 14), tname, fill=TEXT_LIGHT, font=f_sub)
            draw.text((rx + bw - 220, ty + 14), tstat, fill=tcol, font=f_mono)
            ty += 65

        draw_rrect(draw, 100, 800, W - 100, 940, r=10, fill=(16, 26, 44), outline=BORDER_CYAN, width=1)
        draw.text((130, 825), "PRODUCTION SAFETY NET: No untested parser is ever promoted to live stream", fill=ACCENT_CYAN, font=f_title)
        draw.text((130, 865), "Automated fuzz testing protects against Regex Denial-of-Service (ReDoS) and parser memory leaks.", fill=TEXT_MUTED, font=f_sub)

    # -------------------------------------------------------------------------
    # 19. HISTORICAL REPLAY
    # -------------------------------------------------------------------------
    elif sid == "historical_replay":
        total_ev = 10000
        cur_ev = min(total_ev, int(total_ev * t))
        draw_replay_monitor(draw, 100, 100, W - 200, 860, "sample_historical_logs.log", total_ev, cur_ev, 8470, t)

    # -------------------------------------------------------------------------
    # 20. FULL DARK MODE EXPERIENCE
    # -------------------------------------------------------------------------
    elif sid == "dark_mode":
        if screenshots.get("home_dark"):
            base.paste(screenshots["home_dark"], (0, 0))
        draw_screenshot_view(
            draw, base,
            focus_box=(40, 80, W - 40, 360),
            callout_pos=(80, 560, 720, 340),
            callout_lines=[
                ("24/7 SOC OPERATOR EXPERIENCE (DARK THEME)", ACCENT_CYAN, True),
                ("• High-contrast cyber palette engineered for dim SOC environments", TEXT_WHITE, False),
                ("• Real-time animated pipeline indicator: HEALTHY [AIR-GAP]", ACCENT_GREEN, False),
                ("• Zero eye strain during 12-hour continuous monitoring shifts", TEXT_WHITE, False),
                ("• Microsecond search and inspect responsiveness", ACCENT_CYAN, False),
                ("• Persistent theme state saved across browser sessions", TEXT_MUTED, False),
            ],
            anim_t=t
        )

    # -------------------------------------------------------------------------
    # 21. ENTERPRISE SIEM EXPORT
    # -------------------------------------------------------------------------
    elif sid == "siem_export":
        draw.text((100, 100), "ENTERPRISE SIEM EXPORT & OPEN ECOSYSTEM", fill=ACCENT_CYAN, font=f_giant)
        draw.text((100, 175), "Plug-and-play proxy sitting in front of your enterprise SIEM, reducing ingest license costs by 40%.", fill=TEXT_MUTED, font=f_sub)

        # Center Engine with radial arrows to 4 SIEMs
        cx, cy = W // 2, 520
        draw_rrect(draw, cx - 180, cy - 90, cx + 180, cy + 90, r=16, fill=(18, 30, 56), outline=BORDER_CYAN, width=3)
        text_center(draw, "SARVDRISHTI CORE", cy - 45, f_title, fill=TEXT_WHITE, x_offset=cx - 180, width=360)
        text_center(draw, "Normalized ECS Stream", cy, f_sub, fill=ACCENT_CYAN, x_offset=cx - 180, width=360)
        text_center(draw, "< 0.2ms Gateway Latency", cy + 40, f_badge, fill=ACCENT_GREEN, x_offset=cx - 180, width=360)

        # 4 SIEM Destinations
        siems = [
            ("SPLUNK ENTERPRISE", "HTTP Event Collector (HEC)\nPre-normalized JSON\n40% Index Volume Reduction", 120, 260, ACCENT_ORANGE),
            ("ELASTICSEARCH / KIBANA", "Bulk Ingestion API\nDirect ECS Field Indexing\nZero Pipeline Filter CPU", W - 480, 260, ACCENT_CYAN),
            ("MICROSOFT SENTINEL", "Log Analytics REST Ingestion\nPre-validated Schema\nZero Parser Scripting", 120, 680, ACCENT_BLUE),
            ("OPEN-SOURCE GRAFANA", "Loki & Prometheus Metrics\nReal-time WebSocket Push\nZero Licensing Cost", W - 480, 680, ACCENT_GREEN),
        ]

        for sname, sdesc, sx, sy, scol in siems:
            draw_rrect(draw, sx, sy, sx + 360, sy + 180, r=10, fill=(14, 22, 40), outline=scol, width=2)
            draw.text((sx + 20, sy + 20), sname, fill=scol, font=f_title)
            dy = sy + 65
            for dl in sdesc.split("\n"):
                draw.text((sx + 20, dy), dl, fill=TEXT_LIGHT, font=f_body)
                dy += 28
            # Connector Line
            draw.line([(sx + 180 if sx > cx else sx + 360, sy + 90), (cx - 180 if sx < cx else cx + 180, cy)], fill=BORDER_CYAN, width=2)

    # -------------------------------------------------------------------------
    # 22. DEFENSIVE SECURITY & AIR-GAPPED VERIFICATION
    # -------------------------------------------------------------------------
    elif sid == "defense_security":
        draw.text((100, 100), "DEFENSIVE CYBERSECURITY & AIR-GAPPED AUDIT", fill=ACCENT_GREEN, font=f_giant)
        draw.text((100, 175), "Built strictly for classified and defensive networks with zero outbound dependencies.", fill=TEXT_MUTED, font=f_sub)

        cards = [
            ("ZERO DYNAMIC EVAL()", [
                "• All parsing executed through compiled deterministic regex",
                "• No Python eval() or exec() anywhere in ingestion path",
                "• Immune to Remote Code Execution (RCE) injection attacks",
                "• Strict memory bounding per payload (max 1MB per line)",
            ], ACCENT_RED),
            ("100% AIR-GAPPED READY", [
                "• Zero outbound telemetry, licensing phone-homes, or CDN requests",
                "• Fully self-contained inside offline Docker Compose cluster",
                "• Local heuristic AI adapter requires no external cloud LLM API",
                "• Functions seamlessly on isolated LAN or classified subnet",
            ], ACCENT_CYAN),
            ("IMMUTABLE PROVENANCE", [
                "• Cryptographic SHA-256 hash computed on every raw event",
                "• Strict ACID transactional persistence in PostgreSQL",
                "• Byte-level index mapping normalized fields to raw string offsets",
                "• Courtroom-admissible forensic evidence integrity",
            ], ACCENT_GREEN),
            ("CONTAINERIZED DEPLOYMENT", [
                "• One-click deployment: docker-compose up --build",
                "• Single laptop rapid prototyping or multi-node Kubernetes",
                "• Apache Kafka KRaft cluster requires zero ZooKeeper nodes",
                "• Verified on standard Windows 11 & Linux production servers",
            ], ACCENT_PURPLE),
        ]

        card_w = (W - 240) // 2
        coords = [(100, 240), (W // 2 + 20, 240), (100, 600), (W // 2 + 20, 600)]
        for i, (ctitle, clines, ccol) in enumerate(cards):
            cx, cy = coords[i]
            draw_rrect(draw, cx, cy, cx + card_w, cy + 320, r=12, fill=(14, 22, 40), outline=ccol, width=2)
            draw.text((cx + 25, cy + 22), ctitle, fill=ccol, font=f_title)
            ly = cy + 75
            for line in clines:
                draw.text((cx + 25, ly), line, fill=TEXT_LIGHT, font=f_sub)
                ly += 45

    # -------------------------------------------------------------------------
    # 23. SIH REQUIREMENT MATRIX
    # -------------------------------------------------------------------------
    elif sid == "sih_matrix":
        draw.text((100, 100), "SMART INDIA HACKATHON 2026 REQUIREMENT MATRIX", fill=ACCENT_CYAN, font=f_giant)
        draw.text((100, 175), "Clause-by-clause traceability against the official SIH26156 Problem Statement.", fill=TEXT_MUTED, font=f_sub)

        clauses = [
            ("Clause 1", "Heterogeneous Ingestion", "Syslog (UDP 5140), Firewall KV, WebApp JSON", "100% PASS ✓"),
            ("Clause 2", "Deterministic Normalization", "Fast compiled Regex & KV splitters into Elastic ECS", "100% PASS ✓"),
            ("Clause 3", "Field-Level Lineage & Audit", "Byte offset tracking with SHA-256 hash chain", "100% PASS ✓"),
            ("Clause 4", "Lossless Unmapped Handling", "Zero data drop: unmapped bucket stores unknown keys", "100% PASS ✓"),
            ("Clause 5", "AI-Assisted Rule Synthesis", "Air-gapped heuristic LLM parser generator", "100% PASS ✓"),
            ("Clause 6", "Sub-Millisecond Performance", "< 0.2ms latency with Kafka KRaft streaming buffer", "100% PASS ✓"),
        ]

        draw_rrect(draw, 100, 240, W - 100, 780, r=12, fill=(14, 22, 40), outline=BORDER_CYAN, width=2)
        draw_rrect(draw, 100, 240, W - 100, 300, r=12, fill=(22, 34, 60))
        draw.rectangle([(100, 275), (W - 100, 300)], fill=(22, 34, 60))

        draw.text((140, 258), "CLAUSE", fill=TEXT_MUTED, font=f_badge)
        draw.text((320, 258), "PROBLEM STATEMENT REQUIREMENT", fill=TEXT_MUTED, font=f_badge)
        draw.text((820, 258), "SARVDRISHTI ARCHITECTURAL IMPLEMENTATION", fill=TEXT_MUTED, font=f_badge)
        draw.text((1520, 258), "VERIFICATION", fill=TEXT_MUTED, font=f_badge)

        ry = 320
        for cnum, creq, cimpl, cstat in clauses:
            draw_rrect(draw, 120, ry, W - 120, ry + 60, r=6, fill=(18, 28, 50), outline=BORDER_MUTED)
            draw.text((140, ry + 18), cnum, fill=ACCENT_CYAN, font=f_mono)
            draw.text((320, ry + 18), creq, fill=TEXT_WHITE, font=f_sub)
            draw.text((820, ry + 18), cimpl, fill=TEXT_LIGHT, font=f_sub)
            draw.text((1520, ry + 18), cstat, fill=ACCENT_GREEN, font=f_title)
            ry += 75

        # Summary Tag
        draw_rrect(draw, 100, 810, W - 100, 950, r=10, fill=(18, 36, 28), outline=ACCENT_GREEN, width=2)
        draw.text((130, 835), "JURY EVALUATION SUMMARY: 100% COMPLIANT WITH SIH26156 CLAUSES", fill=ACCENT_GREEN, font=f_title)
        draw.text((130, 875), "Every clause validated with automated Pytest suites, live synthetic emitters, and physical UDP packet injection.", fill=TEXT_LIGHT, font=f_sub)
        draw.text((130, 910), "Full open-source code base containerized and ready for immediate deployment.", fill=ACCENT_CYAN, font=f_sub)

    # -------------------------------------------------------------------------
    # 24. GRAND FINALE OUTRO
    # -------------------------------------------------------------------------
    elif sid == "outro":
        # Outro Showcase
        for gy in range(80, H - 60, 60):
            draw.line([(0, gy), (W, gy)], fill=(16, 28, 52), width=1)
        for gx in range(0, W, 80):
            draw.line([(gx, 60), (gx, H - 50)], fill=(16, 28, 52), width=1)

        cx, cy = W // 2, 300
        for ring in (140, 220, 310):
            r_rad = int(ring + 25 * math.sin(t * 6.28 + ring))
            draw.ellipse([(cx - r_rad, cy - r_rad), (cx + r_rad, cy + r_rad)], outline=(0, 229, 255, 50), width=2)

        if screenshots.get("logo"):
            lg = screenshots["logo"]
            lg_w = 460
            lg_h = int(lg.height * (lg_w / lg.width))
            lg_resized = lg.resize((lg_w, lg_h), Image.Resampling.LANCZOS)
            base.paste(lg_resized, (cx - lg_w // 2, cy - lg_h // 2 - 20), lg_resized)

        text_center(draw, "SARVDRISHTI — ALL-SEEING LOG INTELLIGENCE ENGINE", 450, f_giant, fill=TEXT_WHITE)
        text_center(draw, "Team Black Pearl | Smart India Hackathon 2026 (SIH26156)", 535, f_title, fill=ACCENT_CYAN)
        text_center(draw, "Enterprise-Grade • Production-Ready • 100% Air-Gapped Defensive Security", 585, f_sub, fill=TEXT_MUTED)

        # 6 Final Feature Badges
        fbadges = [
            ("✓ HETEROGENEOUS INGESTION", ACCENT_CYAN),
            ("✓ UNIVERSAL ECS NORMALIZATION", ACCENT_GREEN),
            ("✓ ZERO DATA LOSS (UNMAPPED)", ACCENT_ORANGE),
            ("✓ FIELD LINEAGE PROVENANCE", ACCENT_PURPLE),
            ("✓ AIR-GAPPED AI ONBOARDING", ACCENT_CYAN),
            ("✓ SUB-MILLISECOND LATENCY", ACCENT_GREEN),
        ]
        bw = 520
        coords = [
            (W // 2 - bw - 30, 670), (W // 2 + 30, 670),
            (W // 2 - bw - 30, 750), (W // 2 + 30, 750),
            (W // 2 - bw - 30, 830), (W // 2 + 30, 830),
        ]
        for i, (btext, bcol) in enumerate(fbadges):
            bx, by = coords[i]
            draw_rrect(draw, bx, by, bx + bw, by + 60, r=8, fill=(16, 26, 46), outline=bcol, width=2)
            draw.text((bx + 25, by + 16), btext, fill=bcol, font=f_title)

        text_center(draw, "THANK YOU — TEAM BLACK PEARL (SIH 2026)", 920, f_title, fill=ACCENT_CYAN)

    # -------------------------------------------------------------------------
    # GLOBAL HUD OVERLAY (Drawn on every frame)
    # -------------------------------------------------------------------------
    draw_hud(
        draw,
        global_frame=g_frame,
        total_frames=TOTAL_FRAMES,
        phase_num=SCENES.index(scene) + 1,
        total_phases=len(SCENES),
        phase_title=scene["title"],
        badge_text=scene["tag"]
    )

    return base.convert("RGB")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN ENCODING LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("[START] SarvDrishti High-Energy Live Working Video Generator")
    print(f"[INFO] Target: {OUTPUT_VIDEO}")
    print(f"[INFO] Resolution: {W}x{H} @ {FPS}fps | Total frames: {TOTAL_FRAMES} ({TOTAL_FRAMES/FPS:.1f}s)")

    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()
    
    cmd = [
        ffmpeg_bin,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{W}x{H}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-loglevel", "error",
        OUTPUT_VIDEO
    ]

    print(f"[FFMPEG] Starting pipeline: {' '.join(cmd[:8])}...", flush=True)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    t_start = time.time()
    g_frame = 0

    try:
        for s_idx, scene in enumerate(SCENES):
            scene_name = scene["title"]
            n_frames = scene["frames"]
            s_t0 = time.time()
            print(f"[{s_idx+1:02d}/{len(SCENES):02d}] Rendering {scene['id']} ({n_frames} frames)...", flush=True)

            for f_idx in range(n_frames):
                frame_img = render_scene_frame(scene, f_idx, g_frame)
                proc.stdin.write(frame_img.tobytes())
                g_frame += 1

            s_dur = time.time() - s_t0
            print(f"       -> Done in {s_dur:.1f}s ({n_frames/max(0.01, s_dur):.1f} fps)", flush=True)

        proc.stdin.close()
        print("[FFMPEG] Frames sent, waiting for encoder to finalize...", flush=True)
        proc.wait()

        total_dur = time.time() - t_start
        file_size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
        print(f"[SUCCESS] Video generated successfully in {total_dur:.1f}s!")
        print(f"[FILE] {OUTPUT_VIDEO}")
        print(f"[SPECS] Size: {file_size_mb:.2f} MB | Frames: {g_frame} | Duration: {g_frame/FPS:.1f}s")

    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")
        if proc and proc.stdin:
            proc.stdin.close()
        raise

if __name__ == "__main__":
    main()

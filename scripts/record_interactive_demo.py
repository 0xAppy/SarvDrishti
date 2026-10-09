"""
Interactive Video Recorder for SarvDrishti Platform
Automates high-resolution Chrome browser interactions across all modules:
- SIH Portal & KPIs (Theme toggling)
- Interactive Jury Testbench (Live normalization)
- Console Overview & Telemetry (EPS, pipeline metrics, 3D visualizer)
- Log Sources Fleet (Perimeter, UDP Syslog, Web, AI Staging)
- Deterministic Parser Registry (Regex, KV, JSON)
- Live Event Explorer & Schema Inspector (Universal schema, raw payload)
- Field Lineage & Token Audit Trail (Forensic provenance)
- AI Onboarding Studio (Analyze -> Validate -> Register)
- Testing Sandbox Benchmarks & Verification

Target total duration: Exactly 90.0 seconds (1.5 minutes)
"""

import os
import sys
import time
import math
import subprocess
import shutil
from playwright.sync_api import sync_playwright
import imageio_ffmpeg

WORKSPACE = r"e:\sih-blockchain\ULPF"
RECORD_DIR = os.path.join(WORKSPACE, "scripts", "temp_raw_recording")
FINAL_MP4_PUBLIC = os.path.join(WORKSPACE, "frontend", "public", "web_video.mp4")
FINAL_MP4_DOCS = os.path.join(WORKSPACE, "docs", "assets", "web_video.mp4")
FINAL_MP4_ARTIFACT = r"C:\Users\Admin\.gemini\antigravity-ide\brain\8bdcee30-d478-44e8-b9fa-9aa92129e73a\web_video.mp4"

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def inject_cursor(page):
    page.evaluate("""
    () => {
        if (document.getElementById('demo-cursor')) return;
        const cursor = document.createElement('div');
        cursor.id = 'demo-cursor';
        cursor.style.position = 'fixed';
        cursor.style.width = '24px';
        cursor.style.height = '24px';
        cursor.style.borderRadius = '50%';
        cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.65)';
        cursor.style.border = '2.5px solid #ffffff';
        cursor.style.boxShadow = '0 0 15px rgba(0, 229, 255, 0.9), 0 0 5px rgba(0,0,0,0.5)';
        cursor.style.pointerEvents = 'none';
        cursor.style.zIndex = '999999';
        cursor.style.transition = 'transform 0.12s ease-out, background-color 0.15s ease, width 0.15s ease, height 0.15s ease';
        cursor.style.top = '100px';
        cursor.style.left = '100px';
        cursor.style.transform = 'translate(-50%, -50%)';

        const dot = document.createElement('div');
        dot.style.position = 'absolute';
        dot.style.width = '6px';
        dot.style.height = '6px';
        dot.style.borderRadius = '50%';
        dot.style.backgroundColor = '#ffffff';
        dot.style.top = '50%';
        dot.style.left = '50%';
        dot.style.transform = 'translate(-50%, -50%)';
        cursor.appendChild(dot);

        document.body.appendChild(cursor);

        window.__cursorX = 100;
        window.__cursorY = 100;

        window.__moveCursor = (x, y) => {
            window.__cursorX = x;
            window.__cursorY = y;
            cursor.style.left = x + 'px';
            cursor.style.top = y + 'px';
        };

        window.__clickCursor = () => {
            cursor.style.transform = 'translate(-50%, -50%) scale(0.7)';
            cursor.style.backgroundColor = 'rgba(239, 68, 68, 0.9)';
            cursor.style.borderColor = '#ffedd5';
            setTimeout(() => {
                cursor.style.transform = 'translate(-50%, -50%) scale(1)';
                cursor.style.backgroundColor = 'rgba(0, 229, 255, 0.65)';
                cursor.style.borderColor = '#ffffff';
            }, 180);
        };
    }
    """)

def smooth_move(page, target_x, target_y, steps=25, sleep_time=0.015):
    cur = page.evaluate("() => ({ x: window.__cursorX || 100, y: window.__cursorY || 100 })")
    start_x, start_y = cur['x'], cur['y']
    for i in range(1, steps + 1):
        t = i / steps
        # Smooth ease in-out curve
        ease = t * t * (3.0 - 2.0 * t)
        cx = start_x + (target_x - start_x) * ease
        cy = start_y + (target_y - start_y) * ease
        page.evaluate(f"window.__moveCursor({cx}, {cy})")
        time.sleep(sleep_time)

def move_and_click(page, selector, wait_after=1.0, text_match=None):
    try:
        inject_cursor(page)
        elem = page.locator(selector)
        if text_match:
            elem = page.get_by_text(text_match, exact=False).first
        else:
            elem = elem.first
        
        elem.scroll_into_view_if_needed(timeout=3000)
        box = elem.bounding_box()
        if box:
            target_x = box['x'] + box['width'] / 2
            target_y = box['y'] + box['height'] / 2
            smooth_move(page, target_x, target_y, steps=20, sleep_time=0.012)
            page.evaluate("window.__clickCursor()")
            elem.click(timeout=3000)
        else:
            elem.click(timeout=3000)
    except Exception as e:
        print(f"[WARN] move_and_click error on {selector}: {e}")
    time.sleep(wait_after)

def smooth_scroll(page, start_y, end_y, steps=30, sleep_time=0.02):
    for i in range(1, steps + 1):
        t = i / steps
        ease = t * t * (3.0 - 2.0 * t)
        cy = start_y + (end_y - start_y) * ease
        page.evaluate(f"window.scrollTo(0, {cy})")
        time.sleep(sleep_time)

def run_recording():
    os.makedirs(RECORD_DIR, exist_ok=True)
    # Clear old webm
    for f in os.listdir(RECORD_DIR):
        if f.endswith('.webm'):
            try: os.remove(os.path.join(RECORD_DIR, f))
            except: pass

    print("Launching Chromium browser with screen recording...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=True,
            args=[
                "--start-maximized",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--window-size=1920,1080"
            ]
        )
        
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=RECORD_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )

        page = context.new_page()
        # Initialize dark theme by default in localStorage
        page.add_init_script("""
            localStorage.setItem('sarvdrishti_theme', 'dark');
        """)

        print("Navigating to http://localhost:3000?recording=true ...")
        page.goto("http://localhost:3000?recording=true", wait_until="networkidle")
        time.sleep(1.0)
        inject_cursor(page)

        start_time = time.time()
        print("--- STARTING 90-SECOND LIVE INTERACTIVE WALKTHROUGH ---")

        # ---------------------------------------------------------------------
        # 1. 00:00 - 00:10 (10s) | SIH Portal & Adaptive Theming
        # ---------------------------------------------------------------------
        print("[00:00] Act 1: SIH 2026 Portal & Hero Overview")
        smooth_move(page, 450, 180, steps=25)
        time.sleep(1.5)

        # Move to theme toggle button - show Light Mode
        print("Toggling theme to Light Mode...")
        move_and_click(page, "button[title*='Mode'], button[aria-label='Toggle theme']", wait_after=2.0)
        inject_cursor(page)
        
        # Toggle back to Dark Mode
        print("Toggling theme back to High-Contrast Dark Mode...")
        move_and_click(page, "button[title*='Mode'], button[aria-label='Toggle theme']", wait_after=1.5)
        inject_cursor(page)

        # Hover over KPI ribbon
        smooth_move(page, 960, 310, steps=20)
        time.sleep(2.0)

        # ---------------------------------------------------------------------
        # 2. 00:10 - 00:22 (12s) | Interactive Jury Testbench
        # ---------------------------------------------------------------------
        print("[00:10] Act 2: Interactive Jury Testbench Live Normalization")
        smooth_scroll(page, 0, 420, steps=22)
        inject_cursor(page)
        time.sleep(0.5)

        # Preset 1: Fortinet Firewall (Fixed selector)
        print("Testing Preset: Fortinet Firewall...")
        move_and_click(page, "button:has-text('Fortinet Firewall')", wait_after=2.2)
        inject_cursor(page)

        # Preset 2: Linux Syslog RFC 5424
        print("Testing Preset: Linux Syslog RFC 5424...")
        move_and_click(page, "button:has-text('Linux Syslog RFC 5424')", wait_after=2.2)
        inject_cursor(page)

        # Preset 3: Nginx Web Access
        print("Testing Preset: Nginx Web Access...")
        move_and_click(page, "button:has-text('Nginx Web Access')", wait_after=2.2)
        inject_cursor(page)

        # Preset 4: Unrecognized Zero-Day Log
        print("Testing Preset: Unrecognized Zero-Day Log...")
        move_and_click(page, "button:has-text('Unrecognized Zero-Day Log')", wait_after=2.5)
        inject_cursor(page)

        # ---------------------------------------------------------------------
        # 3. 00:22 - 00:32 (10s) | Console Dashboard & Overview
        # ---------------------------------------------------------------------
        print("[00:22] Act 3: Console Dashboard & System Telemetry")
        smooth_scroll(page, 420, 0, steps=20)
        inject_cursor(page)
        
        move_and_click(page, "button:has-text('Launch Operator Console')", wait_after=2.0)
        inject_cursor(page)

        # Hover over metrics cards & visualizer
        smooth_move(page, 400, 240, steps=15)
        time.sleep(1.5)
        smooth_move(page, 850, 240, steps=15)
        time.sleep(1.5)
        smooth_move(page, 1200, 240, steps=15)
        time.sleep(3.0)

        # ---------------------------------------------------------------------
        # 4. 00:32 - 00:42 (10s) | Ingestion Fleet & Log Sources
        # ---------------------------------------------------------------------
        print("[00:32] Act 4: Ingestion Fleet Management")
        move_and_click(page, "aside button:has-text('Sources')", wait_after=2.0)
        inject_cursor(page)

        # Hover over firewall endpoint row
        smooth_move(page, 600, 220, steps=18)
        time.sleep(2.0)
        # Hover over syslog UDP row
        smooth_move(page, 600, 270, steps=18)
        time.sleep(2.0)
        # Hover over AI staging row
        smooth_move(page, 600, 360, steps=18)
        time.sleep(2.5)

        # ---------------------------------------------------------------------
        # 5. 00:42 - 00:52 (10s) | Deterministic Parser Registry
        # ---------------------------------------------------------------------
        print("[00:42] Act 5: Deterministic Parser Registry")
        move_and_click(page, "aside button:has-text('Parser Registry')", wait_after=2.0)
        inject_cursor(page)

        # Hover over parser table entries
        smooth_move(page, 550, 230, steps=15)
        time.sleep(2.0)
        smooth_move(page, 550, 310, steps=15)
        time.sleep(2.5)
        smooth_move(page, 1300, 230, steps=15)
        time.sleep(2.0)

        # ---------------------------------------------------------------------
        # 6. 00:52 - 01:04 (12s) | Live Event Explorer & Schema Inspector
        # ---------------------------------------------------------------------
        print("[00:52] Act 6: Live Event Explorer & Schema Inspector")
        move_and_click(page, "aside button:has-text('Event Explorer')", wait_after=2.0)
        inject_cursor(page)

        # Click on top event row
        print("Selecting event row to inspect payload...")
        move_and_click(page, "table tbody tr", wait_after=2.5)
        inject_cursor(page)

        # Inspect Event Details Inspector panel
        smooth_move(page, 900, 750, steps=20)
        time.sleep(2.5)

        # Click Trace Lineage in the inspector header
        print("Triggering Trace Lineage for inspected event...")
        move_and_click(page, "button:has-text('Trace Lineage')", wait_after=2.0)
        inject_cursor(page)

        # ---------------------------------------------------------------------
        # 7. 01:04 - 01:16 (12s) | Field Lineage & Audit Trail
        # ---------------------------------------------------------------------
        print("[01:04] Act 7: End-to-End Field Lineage & Audit Trail")
        time.sleep(1.5)
        inject_cursor(page)

        # Hover over untouched raw payload
        smooth_move(page, 700, 190, steps=18)
        time.sleep(2.0)

        # Click through extracted fields list on left
        fields = page.locator("div:has-text('Extracted Fields') + div > div")
        field_count = fields.count()
        print(f"Extracted fields found: {field_count}")
        if field_count > 1:
            try:
                second_field = fields.nth(1)
                box = second_field.bounding_box()
                if box:
                    smooth_move(page, box['x'] + box['width']/2, box['y'] + box['height']/2, steps=15)
                    page.evaluate("window.__clickCursor()")
                    second_field.click()
            except Exception as e:
                print("Field click warning:", e)
        time.sleep(2.5)
        inject_cursor(page)

        # Hover over the provenance mapping card
        smooth_move(page, 1100, 480, steps=20)
        time.sleep(3.0)

        # ---------------------------------------------------------------------
        # 8. 01:16 - 01:28 (12s) | AI-Assisted Source Onboarding Studio
        # ---------------------------------------------------------------------
        print("[01:16] Act 8: AI-Assisted Source Onboarding Studio")
        move_and_click(page, "aside button:has-text('AI Onboarding')", wait_after=2.0)
        inject_cursor(page)

        # Step 1: Run Heuristic Analysis
        print("Clicking 'Run Heuristic Analysis'...")
        move_and_click(page, "button:has-text('Run Heuristic Analysis')", wait_after=2.5)
        inject_cursor(page)

        # Step 2: Validate
        print("Clicking 'Validate'...")
        move_and_click(page, "button:has-text('Validate')", wait_after=2.5)
        inject_cursor(page)

        # Step 3: Approve & Register
        print("Clicking 'Approve & Register'...")
        move_and_click(page, "button:has-text('Approve & Register')", wait_after=2.0)
        inject_cursor(page)

        # ---------------------------------------------------------------------
        # 9. 01:28 - 01:30 (2s) | Testing Sandbox Verification & Wrap-up
        # ---------------------------------------------------------------------
        print("[01:28] Act 9: Testing Sandbox Verification & System Ready")
        move_and_click(page, "aside button:has-text('Testing Sandbox')", wait_after=1.5)
        inject_cursor(page)
        time.sleep(1.0)

        total_elapsed = time.time() - start_time
        print(f"Recorded sequence completed in {total_elapsed:.2f} seconds.")
        if total_elapsed < 91.0:
            remaining = 91.0 - total_elapsed
            print(f"Holding screen for {remaining:.2f}s to guarantee full 90-second recording...")
            time.sleep(remaining)

        context.close()
        browser.close()

    # Find the recorded webm file
    webm_files = [os.path.join(RECORD_DIR, f) for f in os.listdir(RECORD_DIR) if f.endswith('.webm')]
    if not webm_files:
        raise RuntimeError("No recorded webm file found in RECORD_DIR!")
    
    # Pick the newest webm file
    webm_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    raw_video = webm_files[0]
    print(f"Raw Playwright recording saved at: {raw_video}")

    # Process and encode with ffmpeg to exactly 90.0 seconds (1.5 minutes)
    post_process_video(raw_video)

def post_process_video(input_webm):
    print("--- POST-PROCESSING VIDEO TO EXACTLY 90.0 SECONDS (1.5 MIN) ---")
    
    # We want exact duration 90.0 seconds at 30 fps (2700 frames)
    # Using ffmpeg with high-quality H.264 profile
    os.makedirs(os.path.dirname(FINAL_MP4_PUBLIC), exist_ok=True)
    os.makedirs(os.path.dirname(FINAL_MP4_DOCS), exist_ok=True)
    os.makedirs(os.path.dirname(FINAL_MP4_ARTIFACT), exist_ok=True)

    # Let's inspect raw duration using ffprobe or ffmpeg
    cmd_probe = [
        FFMPEG_EXE, "-i", input_webm
    ]
    probe_proc = subprocess.run(cmd_probe, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    print("Probe output summary:")
    for line in probe_proc.stderr.splitlines():
        if "Duration" in line or "Video:" in line:
            print("  ", line.strip())

    # Filter to ensure exactly 90s duration and smooth 30fps H.264
    cmd_encode = [
        FFMPEG_EXE, "-y",
        "-i", input_webm,
        "-t", "90.0",
        "-vf", "fps=30,scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-movflags", "+faststart",
        FINAL_MP4_PUBLIC
    ]

    print("Running ffmpeg command:")
    print(" ".join(cmd_encode))
    res = subprocess.run(cmd_encode, capture_output=True, text=True)
    if res.returncode != 0:
        print("[ERROR] FFmpeg failed:", res.stderr)
        raise RuntimeError("FFmpeg encode failed!")

    print(f"[SUCCESS] Exported video to: {FINAL_MP4_PUBLIC}")
    print(f"Size: {os.path.getsize(FINAL_MP4_PUBLIC):,} bytes")

    # Copy to docs/assets and artifacts
    shutil.copyfile(FINAL_MP4_PUBLIC, FINAL_MP4_DOCS)
    print(f"Copied to {FINAL_MP4_DOCS}")
    shutil.copyfile(FINAL_MP4_PUBLIC, FINAL_MP4_ARTIFACT)
    print(f"Copied to {FINAL_MP4_ARTIFACT}")

if __name__ == "__main__":
    run_recording()

import os
import subprocess
import glob
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

WORKSPACE = r"e:\sih-blockchain\ULPF"
ARTIFACT_DIR = r"C:\Users\Admin\.gemini\antigravity-ide\brain\1c9d609c-2c61-4e06-85de-e7b790cee2ae"
OUTPUT_VIDEO_WORKSPACE = os.path.join(WORKSPACE, "web_video.mp4")
OUTPUT_VIDEO_ARTIFACT = os.path.join(ARTIFACT_DIR, "web_video.mp4")

# Screenshots list
SCREENSHOT_PATHS = [
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783506029.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783562407.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783617770.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783675378.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783749794.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783780823.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783840471.png"),
    os.path.join(ARTIFACT_DIR, ".tempmediaStorage", "media_1790783898302.png"),
]

SCENE_META = [
    {
        "title": "MODULE 1: Real-Time Telemetry & System Overview",
        "desc": "Live Metrics: 32,971 Events Ingested | 99.99% Parsing Accuracy | Zero Packet Drops",
        "tag": "TELEMETRY & STATUS"
    },
    {
        "title": "MODULE 2: Log Source Fleet Management",
        "desc": "Active Multi-Source Ingestion: Network Firewalls, Linux Syslog RFC 5424, and Microservice Web Apps",
        "tag": "INGESTION FLEET"
    },
    {
        "title": "MODULE 3: Deterministic & Signature Parser Registry",
        "desc": "Audited Parser Registry: Deterministic Regex, Key-Value & JSON parsers with versioning & zero eval()",
        "tag": "PARSER REGISTRY"
    },
    {
        "title": "MODULE 4: Live Event Explorer & Schema Inspector",
        "desc": "High-Throughput Normalized Event Stream with field inspection, search filtering, and raw payload audit",
        "tag": "EVENT EXPLORER"
    },
    {
        "title": "MODULE 5: End-to-End Field Lineage & Schema Mapping",
        "desc": "Interactive Lineage Graph: Complete audit traceability from raw ingress byte offsets to ECS schema",
        "tag": "FIELD LINEAGE"
    },
    {
        "title": "MODULE 6: AI-Assisted Parser Onboarding Studio",
        "desc": "Pluggable LLM rule generator with deterministic offline heuristic fallback for air-gapped environments",
        "tag": "AI ONBOARDING"
    },
    {
        "title": "MODULE 7: Historical Replay & Time-Travel Simulation",
        "desc": "Lossless replay engine for regression testing, schema evolution validation, and incident recreation",
        "tag": "HISTORICAL REPLAY"
    },
    {
        "title": "PRODUCTION ARCHITECTURE: SarvDrishti Engine Online",
        "desc": "Decoupled Kafka Streaming + PostgreSQL JSONB + React 18 UI | Team Black Pearl (SIH 2026)",
        "tag": "SYSTEM ONLINE"
    }
]

LOGO_PATH = os.path.join(ARTIFACT_DIR, ".user_uploaded", "media_1790783031061.png")
logo_img = None
if os.path.exists(LOGO_PATH):
    try:
        logo_img = Image.open(LOGO_PATH).convert("RGBA")
        logo_img = logo_img.resize((140, 52), Image.Resampling.LANCZOS)
    except Exception as e:
        print("Logo load error:", e)

# Fonts
font_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
font_desc = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 15)
font_badge = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 13)
font_tag = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 14)

font_intro_main = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 56)
font_intro_sub = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 24)
font_intro_team = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 20)

WIDTH = 1920
HEIGHT = 1080
TOP_BAR_H = 55
BOTTOM_BAR_H = 72
CONTENT_H = HEIGHT - TOP_BAR_H - BOTTOM_BAR_H  # 953

def create_top_bar():
    bar = Image.new("RGB", (WIDTH, TOP_BAR_H), (11, 15, 25))
    draw = ImageDraw.Draw(bar)
    # Bottom separator line
    draw.line([(0, TOP_BAR_H - 1), (WIDTH, TOP_BAR_H - 1)], fill=(30, 41, 59), width=1)
    
    # Left brand
    draw.text((24, 14), "SarvDrishti", fill=(255, 255, 255), font=font_title)
    draw.text((160, 20), "Unified Log Intelligence Engine", fill=(148, 163, 184), font=font_desc)
    
    # Right team badge
    badge_text = "Team Black Pearl | SIH 2026"
    draw.rounded_rectangle([(WIDTH - 300, 11), (WIDTH - 24, 43)], radius=16, fill=(30, 41, 59), outline=(56, 189, 248), width=1)
    # Green live dot
    draw.ellipse([(WIDTH - 285, 23), (WIDTH - 275, 33)], fill=(16, 185, 129))
    draw.text((WIDTH - 262, 17), badge_text, fill=(226, 232, 240), font=font_badge)
    
    if logo_img:
        # Paste small logo
        logo_small = logo_img.resize((90, 34), Image.Resampling.LANCZOS)
        bar.paste(logo_small, (540, 10), logo_small)
        
    return bar

def create_bottom_bar(meta):
    bar = Image.new("RGB", (WIDTH, BOTTOM_BAR_H), (11, 15, 25))
    draw = ImageDraw.Draw(bar)
    # Top separator line
    draw.line([(0, 0), (WIDTH, 0)], fill=(30, 41, 59), width=1)
    
    # Tag badge
    tag = meta.get("tag", "SYSTEM")
    draw.rounded_rectangle([(24, 14), (160, 42)], radius=6, fill=(15, 23, 42), outline=(14, 165, 233), width=1)
    draw.text((34, 20), tag, fill=(56, 189, 248), font=font_tag)
    
    # Title & Desc
    draw.text((180, 12), meta.get("title", ""), fill=(255, 255, 255), font=font_title)
    draw.text((180, 42), meta.get("desc", ""), fill=(148, 163, 184), font=font_desc)
    
    # Right status indicator
    draw.text((WIDTH - 240, 26), "PIPELINE: ACTIVE (KAFKA + PG)", fill=(52, 211, 153), font=font_badge)
    
    return bar

top_bar = create_top_bar()

def render_scene_frame(img_path, meta):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (7, 12, 24))
    
    # Screenshot content
    if os.path.exists(img_path):
        screen = Image.open(img_path).convert("RGB")
        if screen.size != (WIDTH, CONTENT_H):
            screen = screen.resize((WIDTH, CONTENT_H), Image.Resampling.LANCZOS)
        canvas.paste(screen, (0, TOP_BAR_H))
    
    # Top Bar
    canvas.paste(top_bar, (0, 0))
    
    # Bottom Bar
    bot_bar = create_bottom_bar(meta)
    canvas.paste(bot_bar, (0, HEIGHT - BOTTOM_BAR_H))
    
    return canvas

def render_intro_card():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (7, 12, 24))
    draw = ImageDraw.Draw(canvas)
    
    # Draw background grid
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=(15, 23, 42), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=(15, 23, 42), width=1)
        
    # Large Logo if available
    if os.path.exists(LOGO_PATH):
        try:
            big_logo = Image.open(LOGO_PATH).convert("RGBA")
            big_logo = big_logo.resize((480, 180), Image.Resampling.LANCZOS)
            canvas.paste(big_logo, ((WIDTH - 480) // 2, 240), big_logo)
        except Exception:
            pass
            
    # Title text
    title = "SarvDrishti"
    bbox = draw.textbbox((0,0), title, font=font_intro_main)
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, 450), title, fill=(255, 255, 255), font=font_intro_main)
    
    subtitle = "Next-Generation Unified Log Intelligence & Deterministic Normalization Engine"
    bbox2 = draw.textbbox((0,0), subtitle, font=font_intro_sub)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - w2) // 2, 530), subtitle, fill=(56, 189, 248), font=font_intro_sub)
    
    team = "Team Black Pearl  •  Smart India Hackathon 2026"
    bbox3 = draw.textbbox((0,0), team, font=font_intro_team)
    w3 = bbox3[2] - bbox3[0]
    draw.text(((WIDTH - w3) // 2, 600), team, fill=(148, 163, 184), font=font_intro_team)
    
    # Pill features
    features = "✓ Kafka Decoupled Streaming   ✓ 99.99% Parsing SLA   ✓ Zero-eval() AI Studio   ✓ Air-Gapped Ready"
    bbox4 = draw.textbbox((0,0), features, font=font_desc)
    w4 = bbox4[2] - bbox4[0]
    draw.rounded_rectangle([((WIDTH - w4) // 2 - 24, 670), ((WIDTH + w4) // 2 + 24, 715)], radius=12, fill=(15, 23, 42), outline=(37, 99, 235), width=1)
    draw.text(((WIDTH - w4) // 2, 683), features, fill=(226, 232, 240), font=font_desc)
    
    return canvas

def render_outro_card():
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (7, 12, 24))
    draw = ImageDraw.Draw(canvas)
    
    # Draw background grid
    for x in range(0, WIDTH, 60):
        draw.line([(x, 0), (x, HEIGHT)], fill=(15, 23, 42), width=1)
    for y in range(0, HEIGHT, 60):
        draw.line([(0, y), (WIDTH, y)], fill=(15, 23, 42), width=1)
        
    title = "System Operational & Production-Ready"
    bbox = draw.textbbox((0,0), title, font=font_intro_main)
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, 360), title, fill=(16, 185, 129), font=font_intro_main)
    
    subtitle = "SarvDrishti — Unified Log Intelligence Engine"
    bbox2 = draw.textbbox((0,0), subtitle, font=font_intro_sub)
    w2 = bbox2[2] - bbox2[0]
    draw.text(((WIDTH - w2) // 2, 450), subtitle, fill=(255, 255, 255), font=font_intro_sub)
    
    team = "Engineered with pride by Team Black Pearl"
    bbox3 = draw.textbbox((0,0), team, font=font_intro_team)
    w3 = bbox3[2] - bbox3[0]
    draw.text(((WIDTH - w3) // 2, 520), team, fill=(56, 189, 248), font=font_intro_team)
    
    specs = "Python 3.10+ • FastAPI • React 18 • Kafka • PostgreSQL 15 JSONB • Docker"
    bbox4 = draw.textbbox((0,0), specs, font=font_desc)
    w4 = bbox4[2] - bbox4[0]
    draw.text(((WIDTH - w4) // 2, 580), specs, fill=(148, 163, 184), font=font_desc)
    
    return canvas

print("Pre-rendering scenes...")
scenes = []
# 0: Intro
scenes.append(render_intro_card())

# 1-8: Modules
for path, meta in zip(SCREENSHOT_PATHS, SCENE_META):
    scenes.append(render_scene_frame(path, meta))

# 9: Outro
scenes.append(render_outro_card())

print(f"Total scenes to animate: {len(scenes)}")

# Launch FFmpeg pipe
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
fps = 30
hold_frames = 65    # ~2.2s per scene
fade_frames = 10    # ~0.33s crossfade transition

cmd = [
    ffmpeg_exe,
    "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(fps),
    "-i", "-",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-crf", "19",
    "-pix_fmt", "yuv420p",
    OUTPUT_VIDEO_WORKSPACE
]

print(f"Encoding video to {OUTPUT_VIDEO_WORKSPACE}...")
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

total_frames = 0
for idx in range(len(scenes)):
    cur_scene = scenes[idx]
    next_scene = scenes[idx + 1] if idx + 1 < len(scenes) else None
    
    # Hold frames
    cur_bytes = cur_scene.tobytes()
    for _ in range(hold_frames):
        proc.stdin.write(cur_bytes)
        total_frames += 1
        
    # Crossfade frames
    if next_scene:
        for f in range(fade_frames):
            alpha = (f + 1) / (fade_frames + 1)
            blended = Image.blend(cur_scene, next_scene, alpha)
            proc.stdin.write(blended.tobytes())
            total_frames += 1

proc.stdin.close()
proc.wait()

print(f"Video encoded successfully! Total frames: {total_frames}, duration: {total_frames/fps:.1f}s")

# Copy to artifact dir
import shutil
shutil.copy(OUTPUT_VIDEO_WORKSPACE, OUTPUT_VIDEO_ARTIFACT)
print(f"Copied to artifact dir: {OUTPUT_VIDEO_ARTIFACT}")

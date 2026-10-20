import os
import sys
import json
import subprocess
import re

import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def find_ffmpeg():
    # 1. System PATH
    found = shutil.which("ffmpeg")
    if found:
        return found
    # 2. Local Winget Gyan.FFmpeg installation
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    if local_appdata:
        winget_path = os.path.join(local_appdata, "Microsoft", "WinGet", "Packages")
        if os.path.exists(winget_path):
            for root, dirs, files in os.walk(winget_path):
                if "ffmpeg.exe" in files:
                    return os.path.join(root, "ffmpeg.exe")
    return "ffmpeg"

FFMPEG_BIN = find_ffmpeg()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MP3_DIR = os.path.join(SCRIPT_DIR, "nhac_mp3_goc")
OGG_DIR = os.path.join(SCRIPT_DIR, "music")
PLAYLIST_FILE = os.path.join(SCRIPT_DIR, "playlist.json")

REPO_USER = "thaihuy1101"
REPO_NAME = "Kho_nhac"
CDN_BASE = f"https://cdn.jsdelivr.net/gh/{REPO_USER}/{REPO_NAME}@main"

os.makedirs(MP3_DIR, exist_ok=True)
os.makedirs(OGG_DIR, exist_ok=True)

def clean_slug(name):
    s = name.lower()
    s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(r'[ìíịỉĩ]', 'i', s)
    s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(r'[đ]', 'd', s)
    s = re.sub(r'[^a-z0-9_-]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s or "song"

def generate_keywords(name):
    clean = name.replace("_", " ").replace("-", " ")
    words = clean.split()
    kws = [clean.lower()]
    for w in words:
        if len(w) >= 2 and w.lower() not in kws:
            kws.append(w.lower())
    # Add unaccented keywords (slug words) so searches without accents always match
    slug = clean_slug(name).replace("_", " ")
    if slug not in kws:
        kws.append(slug)
    for sw in slug.split():
        if len(sw) >= 2 and sw not in kws:
            kws.append(sw)
    return kws

def main():
    print("==================================================")
    print("   BỘ CHUYỂN ĐỔI NHẠC TỰ ĐỘNG CHO ESP32 XIAOZHI   ")
    print("==================================================")

    # 1. Tải playlist.json hiện tại nếu có
    playlist_data = {"playlist": []}
    if os.path.exists(PLAYLIST_FILE):
        try:
            with open(PLAYLIST_FILE, "r", encoding="utf-8") as f:
                playlist_data = json.load(f)
        except Exception as e:
            print(f"[!] Không đọc được playlist.json cũ: {e}, sẽ tạo mới.")

    existing_ids = {item.get("id"): item for item in playlist_data.get("playlist", [])}

    # 2. Quét thư mục nhac_mp3_goc/
    mp3_files = [f for f in os.listdir(MP3_DIR) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
    if not mp3_files:
        print("[!] Không tìm thấy file nhạc MP3 nào trong thư mục nhac_mp3_goc/")
        print("    -> Hãy chép các file bài hát .mp3 vào thư mục: nhac_mp3_goc/")
        return

    print(f"[*] Tìm thấy {len(mp3_files)} bài hát cần xử lý.")

    for filename in mp3_files:
        base_name, _ = os.path.splitext(filename)
        slug_id = clean_slug(base_name)
        ogg_filename = f"{slug_id}.ogg"
        ogg_path = os.path.join(OGG_DIR, ogg_filename)
        input_path = os.path.join(MP3_DIR, filename)

        print(f"\n[>] Đang chuyển đổi: {filename} -> {ogg_filename}...")
        
        # Chuyển đổi bằng ffmpeg sang 16kHz mono Opus chuẩn của Xiaozhi
        cmd = [
            FFMPEG_BIN, "-y", "-i", input_path,
            "-c:a", "libopus",
            "-ar", "16000",
            "-ac", "1",
            "-b:a", "32k",
            ogg_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            print(f"[X] Lỗi chuyển đổi file: {filename}")
            continue

        file_size_kb = os.path.getsize(ogg_path) // 1024
        print(f"    [OK] Đã tạo {ogg_filename} ({file_size_kb} KB)")

        # Cập nhật playlist
        display_name = base_name.replace("_", " ").replace("-", " ").title()
        song_entry = {
            "id": slug_id,
            "name": display_name,
            "keywords": generate_keywords(base_name),
            "file": f"music/{ogg_filename}",
            "url": f"{CDN_BASE}/music/{ogg_filename}"
        }

        existing_ids[slug_id] = song_entry

    playlist_data["playlist"] = list(existing_ids.values())

    with open(PLAYLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(playlist_data, f, ensure_ascii=False, indent=2)

    print("\n[OK] Đã cập nhật thành công playlist.json!")
    print(f"[*] Tổng số bài hát hiện tại trong kho: {len(playlist_data['playlist'])}")

if __name__ == "__main__":
    main()

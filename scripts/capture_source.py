#!/usr/bin/env python3
"""Capture a source so it can still be checked if the link dies.

For a given source_id in data/sources.csv:
  1. asks the Wayback Machine to snapshot the live URL (Save Page Now)
  2. renders the page to PDF with headless Chrome/Edge, straight into captures/
  3. writes archive_url + captured_file + captured_at back into sources.csv

Usage:
    python scripts/capture_source.py S0037
    python scripts/capture_source.py S0037 --no-archive     # skip Wayback
    python scripts/capture_source.py --all-missing          # batch, slow

Why both: the archive protects against link rot; the local PDF protects against
paywalls, geo-blocking, and the archive itself being unavailable in a decade.
"""
import csv, os, sys, subprocess, shutil, datetime, tempfile, urllib.parse, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "sources.csv")
CAP = os.path.join(ROOT, "captures")

BROWSERS = [
    r"C:/Program Files/Google/Chrome/Application/chrome.exe",
    r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
    r"C:/Program Files/Microsoft/Edge/Application/msedge.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

def find_browser():
    env = os.environ.get("HERMES_BROWSER")
    if env and os.path.exists(env): return env
    for b in BROWSERS:
        if os.path.exists(b): return b
    for name in ("chrome", "msedge", "chromium"):
        p = shutil.which(name)
        if p: return p
    return None

def wayback(url):
    try:
        out = subprocess.run(
            ["curl", "-sL", "--max-time", "90", "-A", "Mozilla/5.0", "https://web.archive.org/save/" + url,
             "-o", os.devnull, "-w", "%{url_effective}"],
            capture_output=True, text=True, timeout=120)
        u = (out.stdout or "").strip()
        if "web.archive.org/web/" in u:
            return u
    except Exception as e:
        print("  wayback failed:", e)
    return ""

def render(browser, url, pdf_path):
    tmp = tempfile.mkdtemp(prefix="cap_")
    cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
           f"--user-data-dir={tmp}", "--virtual-time-budget=12000",
           "--no-pdf-header-footer", f"--print-to-pdf={pdf_path}", url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=150)
        return os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000
    except Exception as e:
        print("  render failed:", e)
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def capture(rows, row, browser, do_archive=True):
    url = (row.get("url") or "").strip()
    sid = row["source_id"]
    if not url.startswith("http"):
        print(f"{sid}: no URL — capture this manually (print/photo/scan) and set captured_file")
        return False
    os.makedirs(CAP, exist_ok=True)
    stamp = datetime.date.today().isoformat()
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", urllib.parse.urlparse(url).netloc)[:40]
    name = f"{sid}_{stamp}_{safe}.pdf"
    path = os.path.join(CAP, name)
    ok = render(browser, url, path)
    print(f"{sid}: {'PDF saved ' + name if ok else 'PDF FAILED'}")
    if ok: row["captured_file"] = f"captures/{name}"
    if do_archive:
        snap = wayback(url)
        if snap:
            row["archive_url"] = snap
            print(f"{sid}: archived -> {snap}")
        else:
            print(f"{sid}: wayback gave no snapshot")
    if ok or row.get("archive_url"):
        row["captured_at"] = stamp
        return True
    return False

def main(argv):
    if not os.path.exists(SRC):
        print("data/sources.csv not found"); return 1
    rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
    browser = find_browser()
    if not browser:
        print("No Chrome/Edge found. Set HERMES_BROWSER to a browser executable."); return 1
    print("browser:", browser)

    if "--all-missing" in argv:
        todo = [r for r in rows if not r.get("archive_url") and (r.get("url") or "").startswith("http")]
        print(f"{len(todo)} sources to capture (this will take a while)")
    else:
        ids = [a for a in argv if re.fullmatch(r"S\d{4}", a)]
        if not ids:
            print(__doc__); return 1
        todo = [r for r in rows if r["source_id"] in ids]

    # Reuse a capture that already exists for the same URL (another row may have archived it).
    existing = {}
    for r in rows:
        if r.get("captured_file"):  # only a real file counts; an archive link alone is not a capture
            existing.setdefault((r.get("url") or "").strip(), r)

    # Group by unique URL: a shared aggregator page must be fetched once, not once per record.
    groups = {}
    for r in todo:
        groups.setdefault((r.get("url") or "").strip(), []).append(r)
    print(f"{len(todo)} source rows -> {len(groups)} unique URLs")

    n = 0
    for url, grp in groups.items():
        if url in existing:
            src = existing[url]
            for r in grp:
                r["captured_file"] = src.get("captured_file", "")
                r["archive_url"] = src.get("archive_url", "")
                r["captured_at"] = src.get("captured_at", "")
            print(f"reused existing capture for {len(grp)} row(s): {url[:70]}")
            n += 1
            continue
        lead = grp[0]
        if capture(rows, lead, browser, do_archive="--no-archive" not in argv):
            n += 1
            for other in grp[1:]:
                other["captured_file"] = lead.get("captured_file", "")
                other["archive_url"] = lead.get("archive_url", "")
                other["captured_at"] = lead.get("captured_at", "")
            if len(grp) > 1:
                print(f"  applied to {len(grp)} source rows sharing this URL")

    fields = list(rows[0].keys())
    with open(SRC, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"\ncaptured/archived {n} of {len(todo)}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

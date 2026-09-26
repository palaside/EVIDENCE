# -*- coding: utf-8 -*-
"""
DIGITAL EVIDENCE SILENT HEARTBEAT SUITE (tick.py)
"""
import time
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "tools" / "tick.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def heartbeat():
    tick_count = 0
    while True:
        tick_count += 1
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        if tick_count % 20 == 0 or tick_count == 1:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] HEARTBEAT tick #{tick_count} - Evidence Silent Daemon Active\n")
        time.sleep(2)

if __name__ == "__main__":
    heartbeat()

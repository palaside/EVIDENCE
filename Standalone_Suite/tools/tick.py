#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Silent Background Daemon & File Watcher for DIGITAL EVIDENCE
Runs quietly with Windows startup.
"""
import time
import os
import sys
from pathlib import Path

LOG_FILE = Path(__file__).parent / "tick.log"

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def main():
    log("DIGITAL EVIDENCE Silent Background Daemon Started (Heartbeat Mode)")
    tick_count = 0
    while True:
        tick_count += 1
        if tick_count % 20 == 0:
            log(f"HEARTBEAT: Daemon active at tick {tick_count}")
        time.sleep(5)

if __name__ == "__main__":
    main()

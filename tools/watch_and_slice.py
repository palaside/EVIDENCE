# -*- coding: utf-8 -*-
"""
WATCH & SLICE DAEMON (watchandslice engine)
- Polls config.json and data sources every 2 seconds (interval = 2000ms)
- Automatically triggers incremental slicing and live sandbox updates
- Runs silently with 0 terminal windows when launched by VBS
"""
import os
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from tools.scaffold_agent import generate_sandbox_bundle, log_event, CONFIG_PATH

POLL_INTERVAL = 2.0 # 2 seconds per skill rule
WATCH_FILES = [
    CONFIG_PATH,
    BASE_DIR / "Folder_Out" / "Evidence_Slips_Master_Unique_560.xlsx",
    BASE_DIR / "Folder_Out" / "Evidence_Chat_Master_Combined_Vol1_to_3_Slip_Index.json"
]

def get_mtimes():
    mtimes = {}
    for p in WATCH_FILES:
        if p.exists():
            mtimes[str(p)] = p.stat().st_mtime
    return mtimes

def main():
    log_event("Watch & Slice Daemon initialized (2-second interval heartbeat).")
    # Initial build pass
    try:
        generate_sandbox_bundle()
    except Exception as e:
        log_event(f"Initial build error: {e}")
        
    last_mtimes = get_mtimes()
    
    while True:
        try:
            time.sleep(POLL_INTERVAL)
            current_mtimes = get_mtimes()
            
            # Check for changes
            changed = False
            for k, mtime in current_mtimes.items():
                if k not in last_mtimes or mtime != last_mtimes[k]:
                    log_event(f"Change detected in {Path(k).name} -> Triggering slice update")
                    changed = True
                    break
                    
            if changed:
                last_mtimes = current_mtimes
                generate_sandbox_bundle()
        except KeyboardInterrupt:
            log_event("Watch & Slice Daemon stopped by user.")
            break
        except Exception as e:
            log_event(f"Watch & Slice loop error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()

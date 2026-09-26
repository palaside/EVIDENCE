# -*- coding: utf-8 -*-
"""
DIGITAL EVIDENCE ROOT SERVER LAUNCHER
"""
import sys
import io

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from core.backend_server import main

if __name__ == "__main__":
    main()


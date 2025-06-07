# rehash.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rehash.py

🚀 CLI wrapper entrypoint for tools.rehash.main
"""

import sys
from pathlib import Path

# 🧭 Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rehash.cli import main

if __name__ == "__main__":
    main()

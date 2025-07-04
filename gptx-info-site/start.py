#!/usr/bin/env python3
"""
Railway startup script for GPTX Exchange.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the application
if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    # Use os.system to run uvicorn with the correct module path
    cmd = f"uvicorn gptx.main:app --host 0.0.0.0 --port {port} --log-level info"
    os.system(cmd)
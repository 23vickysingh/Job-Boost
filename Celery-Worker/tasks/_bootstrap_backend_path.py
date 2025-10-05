import sys
import os

# Add BackEnd to sys.path for local imports
BACKEND_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../BackEnd'))
if BACKEND_PATH not in sys.path:
    sys.path.insert(0, BACKEND_PATH)

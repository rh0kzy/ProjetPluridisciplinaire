import sys
import traceback

try:
    import Edit
    print("Import successful!")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

import sys
from datetime import datetime

def main():
    print("[LOG PROCESSOR] Siap menerima log melalui pipe.", flush=True)

    for line in sys.stdin:
        line = line.rstrip("\n")
        if line:
            print(f"[LOG DITERIMA] {line}", flush=True)

    print("[LOG PROCESSOR] Pipe ditutup.", flush=True)

if __name__ == "__main__":
    main()

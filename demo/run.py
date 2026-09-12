"""ASE Demo Runner — one command to start everything.

Usage:
    python demo/run.py              # start server + dashboard on :8000
    python demo/run.py --port 9000  # custom port
    python demo/run.py --demo       # force demo mode (no wallet needed)

What it does:
    1. Checks for .env / wallet
    2. Starts the ASE backend server on the given port
    3. Serves the dashboard from dashboard/dist/
    4. Prints the URL to open in a browser
"""
import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
DASHBOARD_DIST = ROOT / "dashboard" / "dist"


def check_env():
    """Check if .env exists and has a private key."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return False, "No .env file found"
    
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line.startswith("ASE_PRIVATE_KEY=") and len(line) > 20:
            return True, "Wallet configured"
    
    return False, "ASE_PRIVATE_KEY not set in .env"


def check_dashboard():
    """Check if dashboard is built."""
    if DASHBOARD_DIST.exists() and (DASHBOARD_DIST / "index.html").exists():
        return True, "Dashboard built"
    return False, "Dashboard not built — run: cd dashboard && npm run build"


def main():
    parser = argparse.ArgumentParser(description="ASE Demo Runner")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--demo", action="store_true", help="Force demo mode")
    args = parser.parse_args()

    print("=" * 60)
    print("  ASE — the word that acts")
    print("  ETHOnline 2026 Demo Runner")
    print("=" * 60)
    print()

    # Check dashboard
    dash_ok, dash_msg = check_dashboard()
    if not dash_ok:
        print(f"  [!] {dash_msg}")
        print()
        print("  Building dashboard...")
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=str(ROOT / "dashboard"),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  Dashboard build failed:\n{result.stderr}")
            sys.exit(1)
        print("  Dashboard built successfully.")
    else:
        print(f"  [ok] {dash_msg}")

    # Check wallet
    if not args.demo:
        wallet_ok, wallet_msg = check_env()
        if wallet_ok:
            print(f"  [ok] {wallet_msg}")
            mode = "LIVE"
        else:
            print(f"  [!] {wallet_msg}")
            print("  Starting in DEMO mode (no live transactions)")
            mode = "DEMO"
    else:
        print("  [ok] Demo mode forced")
        mode = "DEMO"

    print()
    print(f"  Port:     {args.port}")
    print(f"  Mode:     {mode}")
    print(f"  Dashboard: serving from dashboard/dist/")
    print()
    print(f"  Open:     http://localhost:{args.port}")
    print()
    print("-" * 60)
    print("  API endpoints:")
    print(f"    GET  /api/state       → agent state")
    print(f"    GET  /api/activity    → event log")
    print(f"    POST /api/cycle       → run one agent cycle")
    print(f"    GET  /api/status      → online status")
    print("-" * 60)
    print()
    print("  Press Ctrl+C to stop.")
    print()

    # Start the server
    sys.path.insert(0, str(ROOT / "src"))
    os.chdir(str(ROOT))
    
    from ase.server import main as server_main
    sys.argv = ["ase-server", "--port", str(args.port), "--host", args.host]
    try:
        server_main()
    except KeyboardInterrupt:
        print("\n  Shutting down.")


if __name__ == "__main__":
    main()

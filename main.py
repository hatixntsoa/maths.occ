import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from ui.app import create_app

def main():
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    print(f"\n  CS Maths  →  http://localhost:{port}\n")
    app.run(host="0.0.0.0", debug=True, port=port)

if __name__ == "__main__":
    main()

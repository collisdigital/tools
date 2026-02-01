from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
import uvicorn
import os
import sys

# Configuration
serve_dir = os.environ.get("SERVE_DIR", "dist")

# Ensure directory exists
if not os.path.exists(serve_dir):
    print(f"Error: '{serve_dir}' directory not found. Do you need to run 'just build'?")
    sys.exit(1)

routes = [
    Mount('/', app=StaticFiles(directory=serve_dir, html=True), name='static'),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 8000))
    print(f"Serving directory '{serve_dir}' at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

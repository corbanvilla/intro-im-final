import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uvicorn
from starlette.responses import Response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include routers for content and controls
from app.api.content import router as content_router
from app.api.controls import router as controls_router

# Set path to client files
client_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../client"))
print(client_path)

# Include API routers with /api prefix
app.include_router(content_router, prefix="/api")
app.include_router(controls_router, prefix="/api")

# Serve static files under correct subdirectories
app.mount(
    "/libraries",
    StaticFiles(directory=os.path.join(client_path, "libraries")),
    name="libraries",
)

# Custom StaticFiles to disable caching
class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 200:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

app.mount(
    "/code", NoCacheStaticFiles(directory=os.path.join(client_path, "code")), name="code"
)

app.mount(
    "/assets", NoCacheStaticFiles(directory=os.path.join(client_path, "assets")), name="assets"
)

# Manual route for index.html
@app.get("/")
@app.get("/index.html")
async def serve_index():
    return FileResponse(os.path.join(client_path, "index.html"))


# Entry point for running the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

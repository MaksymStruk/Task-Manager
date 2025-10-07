from fastapi.middleware.cors import CORSMiddleware

def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200", "http://frontend:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

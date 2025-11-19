"""Flask application factory for LineGuard."""

from flask import Flask


def create_app() -> Flask:
    """Application factory for the LineGuard API."""
    app = Flask(__name__)

    @app.get("/health")
    def health_check():
        """Simple endpoint for uptime monitoring."""
        return {"status": "ok"}

    return app


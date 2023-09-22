from opm_app import OpmApp
from flet import app, Page
import os
from opm.app.logging.configure_logging import configure_logging
from loguru import logger


def get_assets_uploads_url(with_parent_dir: bool = False):
    uploads_parent_dir = "assets"
    uploads_dir = "uploads"
    if with_parent_dir:
        return f"{uploads_parent_dir}/{uploads_dir}"
    return uploads_dir


async def main(page: Page):
    """Entry point of the app"""
    env = os.getenv("APP_ENV")
    if env is None:
        env = "prod"
        os.environ["APP_ENV"] = env

    configure_logging(env=env)
    logger.info(f"Entry point of the app. Env: {env}")

    app = OpmApp(page)
    await app.build()


if __name__ == "__main__":
    app(
        name="Op-M Console",
        target=main,
        assets_dir="opm/app/assets",
        upload_dir=get_assets_uploads_url(with_parent_dir=True),
    )

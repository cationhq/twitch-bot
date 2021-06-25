from os import environ
from pathlib import Path

from dotenv import load_dotenv
from twitchio.ext import commands


class Bot(commands.Bot):
    """The bot implementation."""

    def __init__(self, **kwargs):
        """Initialize the bot settings."""

        load_dotenv()

        initial_channels = list(
            filter(None, environ.get("INITIAL_CHANNELS").split(","))
        )

        super().__init__(
            token=environ.get("TOKEN"),
            client_secret=environ.get("CLIENT_SECRET"),
            prefix=environ.get("PREFIX"),
            initial_channels=initial_channels,
            **kwargs,
        )

        self._load_extensions()

    def _load_extensions(self) -> None:  # pragma: no cover
        """Load all extensions from exts path."""

        path = Path(__file__).parent / "exts"
        for resource in path.iterdir():
            if resource.is_file() and resource.name.endswith(".py"):
                self.load_module(f"app.exts.{resource.name[:-3]}")

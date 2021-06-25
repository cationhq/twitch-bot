from os import environ
from unittest.mock import patch

from faker import Faker
from twitchio.ext import commands
from ward import test

from app.bot import Bot

faker = Faker()


@test("should create the bot with corret parameters")
def _():

    token = faker.sha256()
    client_secret = faker.sha256()
    prefix = faker.word()
    initial_channels = faker.word()

    with patch.object(commands.Bot, "__init__") as twitchio_bot, patch(
        "app.bot.load_dotenv"
    ) as load_dotenv, patch.object(
        Bot, "_load_extensions"
    ) as load_extensions, patch.dict(
        environ,
        {
            "TOKEN": token,
            "CLIENT_SECRET": client_secret,
            "PREFIX": prefix,
            "INITIAL_CHANNELS": initial_channels,
        },
    ):
        Bot()

        load_extensions.assert_called_once()
        load_dotenv.assert_called_once()
        twitchio_bot.assert_called_once_with(
            token=token,
            client_secret=client_secret,
            prefix=prefix,
            initial_channels=[initial_channels],
        )

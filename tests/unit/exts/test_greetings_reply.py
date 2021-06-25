from unittest.mock import AsyncMock, MagicMock, patch

from faker import Faker
from ward import each, fixture, test

from app.exts.greetings import Greetings, greeting_from_message

faker = Faker()


@fixture
def message():
    message = AsyncMock()
    message.echo = False
    return message


@test(
    "should return none when message content is not a greeting",
    tags=["greeting_from_message"],
)
def _():
    message = MagicMock()
    message.content = faker.word()

    assert greeting_from_message(message) is None


@test(
    "should return none when message content have more than a greeting",
    tags=["greeting_from_message"],
)
def _(greeting=each("Bom dia", "Boa tarde", "Boa noite")):
    message = MagicMock()
    message.content = f"{greeting}, {faker.user_name()}"

    assert greeting_from_message(message) is None


@test(
    "should return the greeting when message content have just greeting",
    tags=["greeting_from_message"],
)
def _(greeting=each("Bom dia", "Boa tarde", "Boa noite")):
    message = MagicMock()
    message.content = greeting

    assert greeting == greeting_from_message(message)


# class TestGreetingsCog:
#     @pytest.fixture
#     def message(self, mocker):
#         message = mocker.AsyncMock()
#         message.echo = False
#         return message

#     @pytest.mark.asyncio


@test(
    "should not reply when message is echo",
    tags=["grettings_cog"],
)
async def _():
    bot = MagicMock()
    message = MagicMock()
    message.echo = True

    await Greetings(bot).event_message(message)

    message.channel.send.assert_not_called()


@test(
    "should not reply when message is not a greeting",
    tags=["grettings_cog"],
)
async def _(message=message):
    bot = MagicMock()

    with patch(
        "app.exts.greetings.greeting_from_message",
        return_value=None,
    ) as greeting_from_message:
        await Greetings(bot).event_message(message)

        message.channel.send.assert_not_called()
        greeting_from_message.assert_called_once_with(message)


@test(
    "should reply when message content is a greeting",
    tags=["grettings_cog"],
)
async def _(message=message):
    bot = MagicMock()
    username = faker.user_name()
    greeting = faker.word(ext_word_list=["Bom dia", "Boa tarde", "Boa noite"])

    with patch(
        "app.exts.greetings.greeting_from_message",
        return_value=greeting,
    ) as greeting_from_message:
        message.author.name = username

        await Greetings(bot).event_message(message)

        expected_reply = f"{greeting} para você também {username}! TwitchUnity"
        message.channel.send.assert_called_once_with(expected_reply)
        greeting_from_message.assert_called_once_with(message)

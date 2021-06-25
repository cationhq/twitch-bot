import re
import typing as t

from twitchio import Message
from twitchio.ext import commands

from ..bot import Bot

GREETING_PATTERN = (
    r"^[B|b](([o|a]|m)+)\s+([D|d]|[T|t]|[N|n])(i+a+|a+rde+|o+i+te+)"
)

GREETING_REGEX = re.compile(GREETING_PATTERN)
REPLY = "{greeting} para você também {user}! TwitchUnity"


def greeting_from_message(message: Message) -> t.Optional[t.Text]:
    """
    Get the greeting from a message content.

    Args:
        message: the message to verify the content.

    Returns:
        The greeting content, if it matches the GREETING_PATTERN.
        Othewise, None.
    """
    greetings = GREETING_REGEX.match(message.content)

    if (
        greetings
        and (greeting := greetings.group())
        and greeting == message.content
    ):
        return greeting


class Greetings(commands.Cog):
    """Handle the greeting messages on chat."""

    def __init__(self, bot: Bot) -> None:
        """Initialize the cog."""
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message: Message) -> None:
        """Handle the received message."""
        if message.echo:
            return

        if greeting := greeting_from_message(message):
            reply = REPLY.format(
                greeting=greeting,
                user=message.author.name,
            )
            await message.channel.send(reply)


def prepare(bot):  # noqa
    bot.add_cog(Greetings(bot))

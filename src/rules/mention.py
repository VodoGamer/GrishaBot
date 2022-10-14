import re
from typing import Iterable

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

MENTION_PATTERN = (
    r"(?i)^{word}\s+(?P<action>.*)\[(?P<type>club|public|id)(?P<id>\d*)\|(?P<text>.+)\]"
)


class HasUserMention(ABCRule[Message]):
    def __init__(self, commands: Iterable[str] | str, can_reply: bool = True) -> None:
        self.commands = [commands] if isinstance(commands, str) else commands
        self.can_reply = can_reply

    async def check(self, event: Message):
        for command in self.commands:
            if self.can_reply and event.reply_message:
                if event.text.lower().startswith(command):
                    return {
                        "user_id": event.reply_message.from_id,
                        "action": event.text[len(command) + 1:],
                    }
            pattern = re.compile(MENTION_PATTERN.format(word=command))
            match = pattern.search(event.text.lower())
            if match:
                match_id = int(match.groupdict()["id"])
                return {
                    "user_id": match_id if match.groupdict()["type"] == "id" else -match_id,
                    "action": match.groupdict()["action"],
                }

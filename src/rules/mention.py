import re
from typing import Iterable

from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule


class HasUserMention(ABCRule[Message]):
    def __init__(
        self, commands: Iterable[str] | str, args_count: int = -1, can_reply: bool = True
    ) -> None:
        self.commands = [commands] if isinstance(commands, str) else commands
        self.args_count = f"{args_count}" if args_count >= 0 else "{0,}"
        self.can_reply = can_reply

    async def check(self, event: Message):
        for command in self.commands:
            if self.can_reply and event.reply_message:
                regex = r"^{word}\s+((?:\w+\s*){args})$"
                match = self._match(regex, command, event.reply_message.text)
                if match:
                    groups = match.groups()
                    return {"args": groups[0], "user_id": event.reply_message.from_id}
            regex = r"^{word}\s+((?:\w+\s){args})\[(club|id)(\d+)\|(.+)\]$"
            match = self._match(regex, command, event.text)
            if match:
                groups = match.groups()
                return {
                    "args": groups[0],
                    "user_id": int(groups[2]) if groups[1] == "id" else -int(groups[2]),
                }
        return False

    def _match(self, regex: str, command: str, text: str):
        return re.match(regex.format(word=command, args=self.args_count), text)

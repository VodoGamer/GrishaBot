from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule


class HasPhotoRule(ABCRule[Message]):
    async def check(self, event: Message) -> bool:
        if not event.reply_message:
            if event.attachments:
                return bool(
                    attachment.type.value == "photo"
                    for attachment in event.attachments
                )
            return False
        if not event.reply_message.attachments:
            return False
        return bool(
            attachment.type.value == "photo"
            for attachment in event.reply_message.attachments
        )

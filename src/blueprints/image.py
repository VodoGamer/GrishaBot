import io

from vkbottle.bot import Blueprint, Message
from vkbottle.http.aiohttp import AiohttpClient
from vkbottle.tools import PhotoMessageUploader

from src.images.black_white import BlackWhite
from src.images.dem import Demotivator
from src.images.djpeg import Djpeg
from src.images.edvais import Edvais
from src.images.kek import Kek
from src.images.low_bit import LowBits
from src.images.zhmyx import Zmhyx
from src.rules.photo import HasPhotoRule

bp = Blueprint("image")
image_link = str


@bp.on.message(HasPhotoRule(), text=".кек")
async def kek(message: Message):
    await make_meme(message, Kek())


@bp.on.message(HasPhotoRule(), text=[".кеклол", ".лолкек"])
async def kek_lol(message: Message):
    await make_meme(message, Kek(lol=True))


@bp.on.message(HasPhotoRule(), text=[".зерно", ".чб"])
async def black_white(message: Message):
    await make_meme(message, BlackWhite())


@bp.on.message(HasPhotoRule(), text=[".10бит", ".10bit"])
async def ten_bits(message: Message):
    await make_meme(message, LowBits(8))


@bp.on.message(HasPhotoRule(), text=[".8бит", ".8bit"])
async def eight_bits(message: Message):
    await make_meme(message, LowBits(12))


@bp.on.message(HasPhotoRule(), text=[".жпег"])
async def djpeg(message: Message):
    await make_meme(message, Djpeg())


@bp.on.message(HasPhotoRule(), regex=r"^\.дем\s+(.+)(?:\n(.+))?$")
async def demotivator(message: Message, match):
    await make_meme(message, Demotivator(match[0], match[1]))


@bp.on.message(HasPhotoRule(), regex=r"^\.эдвайс\s+(.+)(?:\n(.+))?$")
async def edvais(message: Message, match):
    await make_meme(message, Edvais(match[0], match[1]))


@bp.on.message(HasPhotoRule(), text=[".жмых"])
async def zhmyx(message: Message):
    await make_meme(message, Zmhyx())


async def make_meme(
    message: Message,
    mem_class: (Kek | BlackWhite | LowBits | Djpeg | Demotivator | Edvais | Zmhyx),
):
    requst = await AiohttpClient().request_content(get_max_size_image(message))
    bytes_image = io.BytesIO()
    bytes_image.write(requst)

    result_image = await PhotoMessageUploader(bp.api).upload(
        mem_class.make(bytes_image), peer_id=message.peer_id
    )
    if isinstance(result_image, str):
        await message.answer(attachment=result_image)


def get_max_size_image(message: Message) -> image_link:
    if message.attachments:
        photo = message.attachments[0].photo
    else:
        photo = message.reply_message.attachments[0].photo  # type: ignore
    if photo and photo.sizes:
        image_pixels = photo.sizes[0].width * photo.sizes[0].height
        image_url = photo.sizes[0].url
        for image in photo.sizes:
            if image.width * image.height > image_pixels:
                image_pixels = image.width * image.height
                image_url = image.url
        return image_url
    raise ValueError()

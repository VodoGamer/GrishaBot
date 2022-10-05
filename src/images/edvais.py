import io

from PIL import Image, ImageDraw, ImageFont


class Edvais:
    def __init__(
        self,
        top_text: str = "",
        bottom_text: str = "",
        font_size: int = 40,
        font: str = "impact.ttf",
    ) -> None:
        self.top_text = top_text
        self.bottom_text = bottom_text
        self.font_size = font_size
        self.font = font

    def make(self, file: io.BytesIO) -> bytes:
        image = Image.open(file).convert("RGB")
        self._add_text(self.top_text, image, image.height / 90)
        if self.bottom_text:
            self._add_text(
                self.bottom_text, image, image.height - image.height / 13
            )
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

    def _add_text(self, text: str, image: Image.Image, height: int | float):
        font = ImageFont.truetype(self.font, self.font_size)
        draw = ImageDraw.Draw(image)
        font_size = draw.textlength(text, font)
        while font_size > image.width - 100:
            font = ImageFont.truetype(self.font, self.font_size)
            font_size = draw.textlength(text, font)
            self.font_size -= 1

        draw.text(
            ((image.width - font_size) / 2, height),
            text,
            font=font,
            stroke_width=3,
            stroke_fill="black",
        )

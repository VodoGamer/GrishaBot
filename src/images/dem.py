import io

from PIL import Image, ImageDraw, ImageFont, ImageOps


class Demotivator:
    # https://github.com/Infqq/simpledemotivators/blob/main/simpledemotivators/Demotivator.py
    def __init__(
        self,
        top_text="",
        bottom_text="",
        fill_color: str = "black",
        top_size: int = 80,
        bottom_size: int = 60,
    ):
        self.top_text = top_text
        self.bottom_text = bottom_text
        self.font_name: str = "times.ttf"
        self.font_color: str = "white"
        self.fill_color = fill_color
        self.top_size = top_size
        self.bottom_size = bottom_size

    def make(self, file: io.BytesIO) -> bytes:
        img = Image.new("RGB", (1280, 1024), color=self.fill_color)
        img_border = Image.new("RGB", (1060, 720), color="black")
        border = ImageOps.expand(img_border, border=2, fill="#ffffff")
        user_img = Image.open(file).convert("RGBA").resize((1050, 710))
        width = user_img.size[0]
        img.paste(border, (111, 96))
        img.paste(user_img, (118, 103))
        drawer = ImageDraw.Draw(img)

        """
        Подбираем оптимальный размер шрифта
        Добавляем текст в шаблон для демотиватора
        """
        font_1 = self._test_font(self.top_size, width, self.top_text)
        size_1 = font_1.getbbox(self.top_text)
        drawer.text(
            ((1280 - size_1[2]) / 2, 840),
            self.top_text,
            fill=self.font_color,
            font=font_1,
        )

        if self.bottom_text:
            font_2 = self._test_font(self.bottom_size, width, self.bottom_text)
            size_2 = font_2.getbbox(self.bottom_text)
            drawer.text(
                ((1280 - size_2[2]) / 2, 930),
                self.bottom_text,
                fill=self.font_color,
                font=font_2,
            )

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

    def _test_font(self, size, width, text):
        font = ImageFont.truetype(
            font=self.font_name, size=size, encoding="UTF-8"
        )
        text_width = font.getlength(text)

        while text_width >= (width + 250) - 20:
            font = ImageFont.truetype(
                font=self.font_name, size=size, encoding="UTF-8"
            )
            text_width = font.getlength(text)
            size -= 1
        return font

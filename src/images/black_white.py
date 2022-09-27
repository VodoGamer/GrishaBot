import io

from PIL import Image


class BlackWhite():
    def make(self, file: io.BytesIO) -> bytes:
        image = Image.open(file).convert("1")
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

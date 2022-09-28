import io

from PIL import Image


class Djpeg:
    def make(self, file: io.BytesIO) -> bytes:
        image = Image.open(file)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, quality=1, format='jpeg')
        return img_byte_arr.getvalue()

import io

from PIL import Image, ImageOps


class Kek:
    def __init__(self, black_white: bool = False, lol: bool = False) -> None:
        self.bit = "1" if black_white else "RGB"
        self._lol = lol

    def make(self, file: io.BytesIO) -> bytes:
        image = Image.open(file)
        if self._lol:
            image = ImageOps.mirror(image)
        width_crop = round(image.width / 2)

        crop = ImageOps.crop(image, (width_crop, 0, 0, 0))

        empty = Image.new(self.bit, (crop.width * 2, crop.height))
        empty.paste(ImageOps.mirror(crop))
        empty.paste(crop, (crop.width, 0))
        img_byte_arr = io.BytesIO()
        empty.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

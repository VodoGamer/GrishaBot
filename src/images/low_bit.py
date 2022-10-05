import io

from PIL import Image


class LowBits:
    def __init__(self, pixel_size: int) -> None:
        self.pixel_size = pixel_size

    def make(self, file: io.BytesIO) -> bytes:
        image = Image.open(file).convert("RGB")
        image = image.resize(
            (
                image.size[0] // self.pixel_size,
                image.size[1] // self.pixel_size,
            ),
            Image.Resampling.NEAREST,
        )
        image = image.resize(
            (image.size[0] * self.pixel_size, image.size[1] * self.pixel_size),
            Image.Resampling.NEAREST,
        )

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        return img_byte_arr.getvalue()

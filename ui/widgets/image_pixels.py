from rich_pixels import Pixels
from textual.widgets import Static

class ImagePixels(Static):

    def render(self):
        pixels = Pixels.from_image_path("./assets/folder.png", resize=(10, 10))
        return pixels
from textual.widgets import Static
from textual.widget import Widget

class BoxMessage(Widget):

    def __init__(self, message: str, is_centered: bool = True, **kwargs) -> None:
        super().__init__(**kwargs)
        self.message = message
        self.is_centered = is_centered

    def compose(self):
        if self.is_centered:
            with Static(classes="box-full-center"):
                yield Static(self.message, classes="box-message")
        else:
            yield Static(self.message, classes="box-message")
                
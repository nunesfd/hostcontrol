from textual import on
from textual.screen import ModalScreen
from textual.containers import Container
from textual.widgets import Label, Button, Static, Markdown
from typing_extensions import Literal

AlertVariant = Literal["default", "primary", "success", "warning", "error"]

class Alert(ModalScreen):

    def __init__(self, message: str, title: str = None, btn_ok="OK"):
        super().__init__()
        self.classes = "modal alert"
        self.title = title
        self.message = message
        self.btn_ok = btn_ok
        
    def compose(self):
        with Container(classes="container"):
            if self.title:
                yield Label(self.title, classes="modal-title")
                # yield Rule(line_style="dashed")
            yield Markdown(self.message)
            with Static(classes="modal-buttons center"):
                yield Button(self.btn_ok, id="ok") 

    # def key_escape(self, event) -> None:
    #     event.stop()
    #     self.dismiss("no")

    @on(Button.Pressed)
    def on_button_pressed(self, event):
        self.dismiss(event.button.id)
        
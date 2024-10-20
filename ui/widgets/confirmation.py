from textual import on
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Label, Button, Rule

class Confirmation(ModalScreen):

    def __init__(self, question: str, title: str = None, btn_confirm="Confirm", btn_cancel="Cancel"):
        super().__init__()
        self.classes = "modal confirmation"
        self.title = title
        self.question = question
        self.btn_confirm = btn_confirm
        self.btn_cancel = btn_cancel
        
    def compose(self):
        with Container(classes="container"):
            if self.title:
                yield Label(self.title, classes="modal-title")
                yield Rule(line_style="dashed")
            yield Label(self.question, classes="modal-question")
            with Horizontal(classes="modal-buttons"):
                yield Button(self.btn_cancel, variant="error", id="no")
                yield Vertical()
                yield Button(self.btn_confirm, variant="success", id="yes")

    def key_escape(self, event) -> None:
        event.stop()
        self.dismiss("no")

    def key_right(self, event) -> None:
        event.stop()
        self.focus_next()

    def key_left(self, event) -> None:
        event.stop()
        self.focus_next()

    @on(Button.Pressed)
    def on_button_pressed(self, event):
        self.dismiss(event.button.id)
        
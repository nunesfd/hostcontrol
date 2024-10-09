from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Label, Button, Markdown, Static

from config import config

MESSAGE_INFO = f"""\
# 📜 About the System
**{config.APP_NAME}** is a simple and effective tool for developers, designed to streamline the management of the hosts file. Organize your hosts into groups and easily enable or disable blocks, making your workflow more agile and efficient!

# 👨 About the Developer
- **Name**: Flávio Nunes
- **Email**: [admflaviodouglas@gmail.com](admflaviodouglas@gmail.com)
- **GitHub**: [github.com/nunesfd](https://github.com/nunesfd)
"""

class AboutMainView(ModalScreen):
    def __init__(self):
        super().__init__()
        self.classes = "modal about"
    
    def compose(self):
        with Container(classes="container"):
            yield Markdown(MESSAGE_INFO)
            with Static(classes="modal-buttons center"):
                yield Button("Close", id="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-btn":
            self.dismiss()
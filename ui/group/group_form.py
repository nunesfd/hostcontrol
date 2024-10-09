import logging
from textual import on
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Label, Button, Input, Rule

from models.group import Group
from repositories.group_repository import GroupRepository
from shared.exception import ValidationException

class GroupFormView(ModalScreen):

    def __init__(self, update_group:Group=None):
        super().__init__()
        self.classes = "modal group-form"
        self.update_group = update_group
        
        if self.update_group is None:
            self.title = "NEW GROUP"
        else:
            self.title = "UPDATE GROUP"

    def on_mount(self):
        if self.update_group is not None:
            self.group_input.value = self.update_group.name
        
    def compose(self):
        self.group_input = Input(placeholder="Group Name", id="f_group_name")
        with Container(classes="container"):
            yield Label(self.title, classes="modal-title")
            yield Rule(line_style="dashed")
            yield self.group_input
            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel (esc)", variant="error", id="cancel")
                yield Vertical()
                yield Button("Save (enter)", variant="success", id="save")

    def key_escape(self) -> None:
        self.close() 

    def key_enter(self) -> None:
        self.save()      

    @on(Button.Pressed)
    def on_button_pressed(self, event):
        if event.button.id == "cancel":
            self.close()
            return
        
        self.save()


    def save(self):
        group_name = self.group_input.value.strip()
        
        if not group_name:
            self.app.notify("Group name cannot be empty", severity="error")
            return
        
        # logging.info(group_name)
        repo = GroupRepository()

        try:
            if self.update_group is not None:
                repo.update_group(self.update_group.id, name=group_name)
            else:
                repo.create_group(name=group_name, hosts_status="active")
            
            self.dismiss(True)

        except ValidationException as e:
            self.app.notify(title="Error", message=e.message, severity="error")

        except Exception as e:
            self.app.notify(title="Error", message=f"Failed to save group: {str(e)}", severity="error")
        

    def close(self):
        self.dismiss(False)
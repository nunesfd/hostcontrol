import logging
from textual import on
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Label, Button, Input, Rule

from repositories.group_repository import GroupRepository
from repositories.host_repository import HostRepository
from shared.exception import ValidationException

class HostFormView(ModalScreen):

    def __init__(self, group_id, group_name, update_id=0):
        super().__init__()
        self.classes = "modal host-form"
        self.group_id = group_id
        self.group_name = group_name
        self.update_id = update_id

    def on_mount(self):
        if self.update_id > 0:
            host = HostRepository().get_host_by_id(self.update_id)
            if host:
                self.ip_input.value = host.ip_address
                self.host_input.value = host.hostname
        
    def compose(self):
        self.ip_input = Input(placeholder="IP", classes="ip-address-input")
        self.host_input = Input(placeholder="Host", classes="host-input")
        with Container(classes="container"):
            yield Label("NEW HOST - " + self.group_name, classes="modal-title")
            yield Rule(line_style="dashed")
            with Vertical():
                yield self.ip_input
                yield self.host_input

            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel(esc)", variant="error", id="cancel")
                yield Vertical()
                yield Button("Save(enter)", variant="success", id="save")

    def key_escape(self, event):
        event.stop()
        self.close()

    def key_enter(self):
        focused_widget = self.focused
        if focused_widget == self.ip_input:
            self.focus_next()
        else:
            self.save()

    @on(Button.Pressed)
    def on_button_pressed(self, event):
        if event.button.id == "cancel":
            self.close()
            return
        
        self.save()
        
        
    def close(self):
        self.dismiss(False)

    def save(self):
        ip = self.ip_input.value.strip()

        if not ip:
            self.app.notify("IP cannot be empty", severity="error")
            return
        
        host = self.host_input.value.strip()
        if not host:
            self.app.notify("Host cannot be empty", severity="error")
            return
        
        repoHost = HostRepository()
        repoGroup = GroupRepository()

        try:
            if self.update_id > 0:
                repoHost.update_host(host_id=self.update_id, ip_address=ip, hostname=host)
            else:
                repoHost.create_host(ip_address=ip, hostname=host, group_id=self.group_id)
                repoGroup.update_total_hosts(self.group_id)
            # host_id = repo.create_host(ip_address=ip, hostname=host, group_id=self.group_id)
            # host = repo.get_host_by_id(host_id)
            # self.app.notify("New host added", title="Success", severity="success")
            self.dismiss(True)

        except ValidationException as e:
            self.app.notify(title="Error", message=e.message, severity="error")

        except Exception as e:
            self.app.notify(title="Error", message=f"Failed to save host: {str(e)}", severity="error")

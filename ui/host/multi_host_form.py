import logging
from textual import on
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Label, Button, Input, Rule, TextArea

from repositories.group_repository import GroupRepository
from repositories.host_repository import HostRepository
from shared.exception import ValidationException

class MultiHostFormView(ModalScreen):

    def __init__(self, group_id, group_name, update_id=0):
        super().__init__()
        self.classes = "modal multi-host-form"
        self.group_id = group_id
        self.group_name = group_name
        self.update_id = update_id
        
    def compose(self):
        self.hosts_input = TextArea(show_line_numbers=True, classes="host-input")
        with Container(classes="container"):
            yield Label("ADD MULTIPLE HOSTS - " + self.group_name, classes="modal-title")
            yield Rule(line_style="dashed")
            yield Label(" [bold yellow]line example:[/bold yellow] 127.0.0.1 test.com.br")
            yield self.hosts_input

            with Horizontal(classes="modal-buttons"):
                yield Button("Cancel(esc)", variant="error", id="cancel")
                yield Vertical()
                yield Button("Save(enter)", variant="success", id="save")

    def key_escape(self, event):
        event.stop()
        self.close()

    @on(Button.Pressed)
    def on_button_pressed(self, event):
        if event.button.id == "cancel":
            self.close()
            return
        
        self.save()
        
        
    def close(self):
        self.dismiss(False)

    def get_hosts_list(self):
        hosts = self.hosts_input.text.strip()
        hosts_list = []
        for line in hosts.strip().splitlines():
            parts = line.split()
            if len(parts) >= 2:
                hosts_list.append(parts)
            elif len(parts) == 1:
                hosts_list.append([parts[0], ""])

        return hosts_list

    def save(self):
        hosts = self.get_hosts_list()

        if len(hosts) == 0:
            self.app.notify("Hosts cannot be empty", severity="error")
            return
        
        repoHost = HostRepository()
        repoGroup = GroupRepository()
        total_success = 0
        errors = []

        for index, host_line in enumerate(hosts):
            try:
                current_line = index + 1

                if len(host_line) > 2:
                    raise ValidationException(f"Invalid line")

                ip = host_line[0]
                host = host_line[1]
                repoHost.create_host(ip_address=ip, hostname=host, group_id=self.group_id)
                total_success += 1
            except ValidationException as e:
                errors.append(f"[bold red]Line:[/bold red]{current_line} [yellow]{host_line}[/yellow] - {e.message}")
            except Exception as e:
                errors.append(f"Failed to save host: {str(e)}")

        if len(errors) > 0:
            self.app.notify(title="Error", message="\n".join(errors), severity="error")

        if total_success > 0:
            repoGroup.update_total_hosts(self.group_id)
            self.dismiss(True)

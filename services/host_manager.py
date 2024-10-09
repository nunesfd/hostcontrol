import re
import os

from config import config
from models.host_file import HostFile
from typing import List

class HostsManager:

    LINE_BREAK = os.linesep 
    START_BLOCK = "# BEGIN:"
    END_BLOCK = "# END"

    MATH_BEGIN = r"# BEGIN:(\d+)"

    def __init__(self):
        self.filename = config.get_hosts_path()

    def _parseHostsToBlockWriter(self, group_id: str, group_name: str, hosts: List[HostFile]):
        return f"{self.START_BLOCK}{group_id} - {group_name}{self.LINE_BREAK}"+f"{self.LINE_BREAK}".join([f"{host.ip_address} {host.hostname}" for host in hosts])+f"{self.LINE_BREAK}{self.END_BLOCK}"

    def create_or_replace_hosts(self, group_id: int, group_name: str, hosts: List[HostFile]):
        start, end, content = self.get_position_of_block(group_id)
        new_content = self._parseHostsToBlockWriter(group_id, group_name, hosts)
        
        if start is None:
            self.write_new_block(new_content=new_content)
            return

        if start is not None and end is not None:
            self.write_replaced_block(old_content=content, new_content=new_content)
            return

        raise Exception("Failed to create or replace hosts")


    def remove_hosts(self, group_id: int):
        start, end, content = self.get_position_of_block(group_id)
        if start is not None and end is not None:
            self.write_replaced_block(old_content=content, new_content=None)

    def check_start_group(self, row):
        match = re.match(self.MATH_BEGIN, row)
        if match is not None:
            return int(match.group(1))
        else:
            return None

    def get_position_of_block(self, find_group_id: int):
         
         start_position = None
         end_position = None
         content = "" 

         with open(self.filename, 'r') as file:
            for position, row in enumerate(file):
                if start_position is None:
                    groupId = self.check_start_group(row.strip())
                    if groupId == int(find_group_id):
                        start_position = position
                        content+= row
                    continue

                if end_position is None:
                    content+= row
                    if row.strip() == '# END':
                        end_position = position
                    continue
                break

         return start_position, end_position, content
    
    def clear_line_break(self, content: str) -> str:
        return re.sub(r'(\r\n|\r|\n){3,}', self.LINE_BREAK+self.LINE_BREAK, content)

    def _write(self, old_content, new_content):
        with open(self.filename, 'r+') as file:
            original_content = file.read()

            if old_content is None:
                new_content_file = original_content + self.LINE_BREAK + new_content + self.LINE_BREAK
            elif new_content is None:
                new_content_file = original_content.replace(old_content, "")
            else:
                new_content_file = original_content.replace(old_content, new_content + self.LINE_BREAK)

            new_content_file = self.clear_line_break(new_content_file)
            
            file.seek(0)
            file.write(new_content_file)
            file.truncate() 

    def write_new_block(self, new_content):
        self._write(old_content=None, new_content=new_content)

    def write_replaced_block(self, old_content, new_content):
        self._write(old_content=old_content, new_content=new_content)

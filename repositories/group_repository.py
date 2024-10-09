from datetime import datetime
import logging
import sqlite3
from models.group import Group, GroupHostsStatus
from repositories.repository import Repository
from shared.exception import ValidationException



class GroupRepository(Repository):

    def validate_unique_group_name(self, group_name: str, diff_group_id: int = None):
        if self.exist_group_with_name(group_name, diff_group_id):
            raise ValidationException("Group name already exists")


    def update_total_hosts(self, group_id):
        query = '''UPDATE groups 
                SET total_hosts = (SELECT count(*) FROM hosts_file WHERE group_id = ?) 
                WHERE id = ?'''
        self._execute(query, (group_id, group_id))

    def create_group(self, name, hosts_status:GroupHostsStatus="active"):
        name = name.strip()
        self.validate_unique_group_name(name)

        query = '''INSERT INTO groups (created_at, name, hosts_status) 
                   VALUES (?, ?, ?)'''
        self._execute(query, (datetime.now().isoformat(), name, hosts_status))

    def update_hosts_status(self, group_id, hosts_status: GroupHostsStatus):
        self._execute('''UPDATE groups SET hosts_status = ? WHERE id = ?''', (hosts_status, group_id))

    def update_group(self, group_id, name=None):
        name = name.strip()
        self.validate_unique_group_name(group_name=name, diff_group_id=group_id)
        self._execute('''UPDATE groups SET name = ? WHERE id = ?''', (name, group_id))

    def delete_group(self, group_id):
        self._execute('''DELETE FROM groups WHERE id = ?''', (group_id,))


    def list_groups(self):
        query = '''SELECT id, created_at, name, hosts_status, total_hosts FROM groups'''
        return [Group(*row) for row in self._execute(query, fetch=True)]
    
    def get_group_by_id(self, group_id: int):
        query = '''SELECT id, created_at, name, hosts_status, total_hosts 
                FROM groups 
                WHERE id = ?'''
        result = self._execute(query, (group_id,), fetch=True)
        return Group(*result[0]) if result else None
    
    def exist_group_with_name(self, name: str, diff_group_id: int = None) -> bool:
        query = '''SELECT id FROM groups WHERE name LIKE ?'''
        params = [name]
        
        if diff_group_id is not None:
            query += ' AND id != ?'
            params.append(diff_group_id)
        
        query += ' LIMIT 1'
        result = self._execute(query, tuple(params), fetch=True)
        return bool(result)


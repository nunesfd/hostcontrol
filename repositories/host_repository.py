from datetime import datetime
import sqlite3

from models.host_file import HostFile
from repositories.repository import Repository
from shared.exception import ValidationException
from shared.network_validator import is_valid_hostname, is_valid_ip


class HostRepository(Repository):

    def validate_ip_and_hostname(self, ip_address, hostname):
        if is_valid_ip(ip_address) == False:
            raise ValidationException("Invalid IP address")
        
        if is_valid_hostname(hostname) == False:
            raise ValidationException("Invalid hostname")

    def create_host(self, ip_address, hostname, group_id=None):

        self.validate_ip_and_hostname(ip_address, hostname)

        query = '''INSERT INTO hosts_file (ip_address, hostname, created_at, group_id) 
                   VALUES (?, ?, ?, ?)'''
        return self._execute(query, (ip_address, hostname, datetime.now().isoformat(), group_id), lastId=True)

    def update_host(self, host_id, ip_address=None, hostname=None):
        self.validate_ip_and_hostname(ip_address, hostname)
        self._execute('''UPDATE hosts_file SET ip_address = ?, hostname = ? WHERE id = ?''', (ip_address, hostname, host_id))

    def delete_host(self, host_id):
        self._execute('''DELETE FROM hosts_file WHERE id = ?''', (host_id,))

    def delete_host_by_group_id(self, group_id):
        self._execute('''DELETE FROM hosts_file WHERE group_id = ?''', (group_id,))

    def list_hosts(self):
        query = '''SELECT id, ip_address, hostname, created_at, group_id FROM hosts_file'''
        return [HostFile(*row) for row in self._execute(query, fetch=True)]
    
    def get_host_by_id(self, host_id):
        query = '''SELECT id, ip_address, hostname, created_at, group_id 
                   FROM hosts_file 
                   WHERE id = ?'''
        result = self._execute(query, (host_id,), fetch=True)
        
        # Retorna o HostFile correspondente ao ID ou None se não encontrado
        return HostFile(*result[0]) if result else None
    
    def list_hosts_by_group_id(self, group_id: int):
        query = '''SELECT id, ip_address, hostname, created_at, group_id 
                FROM hosts_file 
                WHERE group_id = ?'''  # Adiciona a cláusula WHERE para filtrar pelo group_id
        return [HostFile(*row) for row in self._execute(query, (group_id,), fetch=True)]


    def get_host_by_id(self, host_id):
        query = '''SELECT id, ip_address, hostname, created_at, group_id 
                   FROM hosts_file WHERE id = ?'''
        result = self._execute(query, (host_id,), fetch=True)
        if result:
            return HostFile(*result[0])
        return None

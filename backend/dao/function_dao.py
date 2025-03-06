from typing import Optional, Dict, List
from .base_dao import BaseDAO


class FunctionDAO(BaseDAO):
    """函数存储专用操作类"""

    def __init__(self):
        super().__init__("stored_functions")

    def add_function(self, rule_name: str, function_name: str, code: str) -> bool:
        """添加新函数"""
        query = """
        INSERT INTO stored_functions 
        (rule_name, function_name, function_code)
        VALUES (%s, %s, %s)
        """
        return self._execute_write(query, (rule_name, function_name, code))

    def get_by_rule(self, rule_name: str) -> Optional[Dict]:
        """通过规则名称获取函数"""
        query = "SELECT * FROM stored_functions WHERE rule_name = %s"
        result = self._execute_read(query, (rule_name,))
        return result[0] if result else None

    def get_by_name(self, function_name: str) -> Optional[Dict]:
        """通过函数名称获取"""
        query = "SELECT * FROM stored_functions WHERE function_name = %s"
        result = self._execute_read(query, (function_name,))
        return result[0] if result else None

    def update_code(self, identifier: str, new_code: str, by_name: bool = False) -> bool:
        """更新函数代码"""
        field = "function_name" if by_name else "rule_name"
        query = f"UPDATE stored_functions SET function_code = %s WHERE {field} = %s"
        return self._execute_write(query, (new_code, identifier))

    def delete(self, identifier: str, by_name: bool = False) -> bool:
        """删除函数"""
        field = "function_name" if by_name else "rule_name"
        query = f"DELETE FROM stored_functions WHERE {field} = %s"
        return self._execute_write(query, (identifier,))

    def list_all(self) -> List[Dict]:
        """列出所有函数"""
        return self._execute_read("SELECT rule_name, function_name, function_code, created_at FROM stored_functions")
    
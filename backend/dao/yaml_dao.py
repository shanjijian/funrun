from typing import Optional, Dict, List
from .base_dao import BaseDAO


class YamlDAO(BaseDAO):
    """YAML配置专用操作类"""

    def __init__(self):
        super().__init__("stored_yamls")

    def add_yaml(self, rule_name: str, yaml_name: str, content: str) -> bool:
        """添加新配置"""
        query = """
        INSERT INTO stored_yamls 
        (rule_name, yaml_name, yaml_code)
        VALUES (%s, %s, %s)
        """
        return self._execute_write(query, (rule_name, yaml_name, content))

    def get_by_rule(self, rule_name: str) -> Optional[Dict]:
        """通过规则名称获取"""
        query = "SELECT * FROM stored_yamls WHERE rule_name = %s"
        result = self._execute_read(query, (rule_name,))
        return result[0] if result else None

    def get_by_name(self, yaml_name: str) -> Optional[Dict]:
        """通过配置名称获取"""
        query = "SELECT * FROM stored_yamls WHERE yaml_name = %s"
        result = self._execute_read(query, (yaml_name,))
        return result[0] if result else None

    def update_content(self, identifier: str, new_content: str, by_name: bool = False) -> bool:
        """更新配置内容"""
        field = "yaml_name" if by_name else "rule_name"
        query = f"UPDATE stored_yamls SET yaml_code = %s WHERE {field} = %s"
        return self._execute_write(query, (new_content, identifier))

    def delete(self, identifier: str, by_name: bool = False) -> bool:
        """删除配置"""
        field = "yaml_name" if by_name else "rule_name"
        query = f"DELETE FROM stored_yamls WHERE {field} = %s"
        return self._execute_write(query, (identifier,))

    def list_all(self) -> List[Dict]:
        """列出所有配置"""
        return self._execute_read("SELECT rule_name, yaml_name, yaml_code, created_at FROM stored_yamls")

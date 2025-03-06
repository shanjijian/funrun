
import re
from typing import Any, Dict
import yaml
from backend.dao.yaml_dao import YamlDAO


class YamlExecutor:
    """YAML配置执行器"""

    def __init__(self):
        self.dao = YamlDAO()
        self._yaml_cache: Dict[str, Any] = {}

    def execute_by_rule(self, rule_name: str, data: Any) -> str:
        """通过规则名称执行函数"""
        yaml_data = self.dao.get_by_rule(rule_name)
        if not yaml_data:
            return f"未找到YAML配置：{rule_name}"
        yaml_rules = yaml_data.get('yaml_code', [])
        rules = yaml.safe_load(yaml_rules).get('rules', [])
        return self._match_yaml(rules, data)

    def execute_by_name(self, yaml_name: str, data: Any) -> str:
        """加载并解析YAML配置，并根据输入的内容进行匹配"""
        # 从数据库获取 YAML 配置
        yaml_data = self.dao.get_by_name(yaml_name)
        if not yaml_data:
            return f"未找到YAML配置：{yaml_name}"
        yaml_rules = yaml_data.get('yaml_code', [])
        rules = yaml.safe_load(yaml_rules).get('rules', [])
        return self._match_yaml(rules, data)

    def _match_yaml(self, rules, data) -> str:
        """加载 YAML 配置并匹配数据"""
        for rule in rules:
            # 检查每个规则中的条件是否匹配
            if all(re.search(condition['match'], data.get(condition['field'], ''))
                   for condition in rule.get('condition', [])):
                return f"匹配成功：{rule['name']}"
        return "未匹配任何规则"

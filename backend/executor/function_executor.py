from typing import Any, Tuple

from backend.core.conf import settings
from backend.dao.function_dao import FunctionDAO


class FunctionExecutor:
    """函数执行器"""

    def __init__(self):
        self.dao = FunctionDAO()
        self.required_libraries = settings.REQUIRED_LIBRARIES

    def execute_by_rule(self, rule_name: str, data: Any) -> str:
        """通过规则名称执行函数"""
        func_record = self.dao.get_by_rule(rule_name)
        if not func_record:
            return f"未找到规则：'{rule_name}'"
        return self._execute_function(func_record, data)

    def execute_by_name(self, function_name: str, data: Any) -> str:
        """通过函数名称执行函数"""
        func_record = self.dao.get_by_name(function_name)
        if not func_record:
            return f"未找到函数：'{function_name}'"
        return self._execute_function(func_record, data)

    def _import_libraries(self, global_env: dict):
        """导入所有需要的库到执行环境"""
        for lib in self.required_libraries:
            try:
                module = __import__(lib)  # 动态导入库
                global_env[lib] = module  # 将库添加到执行环境中
            except ImportError as e:
                return None, f"Error importing library '{lib}': {str(e)}"
        return global_env, ""

    def _execute_code(self, code_str: str, function_name: str) -> Tuple[Any, str]:
        """编译并验证代码"""
        try:
            code = compile(code_str, '<string>', 'exec')  # 编译为可执行代码
        except SyntaxError as e:
            return None, f"Syntax error: {e.msg} at line {e.lineno}"

        local_env = {}
        global_env = globals()  # 使用全局环境

        # 导入所需的库
        global_env, error = self._import_libraries(global_env)
        if error:
            return None, error

        try:
            exec(code, global_env, local_env)  # 执行代码
        except Exception as e:
            return None, f"Execution error: {str(e)}"

        if function_name not in local_env:
            return None, f"Function '{function_name}' not defined in code"

        return local_env[function_name], ""

    def _execute_function(self, func_record: dict, data: Any) -> str:
        """执行函数通用逻辑"""
        code_str = func_record['function_code']
        func_name = func_record['function_name']
        # 编译获取函数对象
        func, error = self._execute_code(code_str, func_name)
        if error:
            return error

        # 执行目标函数
        try:
            result = func(data)
            return result
        except Exception as e:
            return f"Function runtime error: {str(e)}"

import yaml
import re


def match_yaml(data, yaml_content):
    """加载 YAML 配置并匹配数据"""
    rules = yaml.safe_load(yaml_content).get('rules', [])

    for rule in rules:
        # 检查每个规则中的条件是否匹配
        if all(re.search(condition['match'], data.get(condition['field'], ''))
               for condition in rule.get('condition', [])):
            print(f"匹配成功: {rule['name']}")
        else:
            print(f"未匹配: {rule['name']}")


if __name__ == "__main__":
    # 输入数据
    input_data = {
        "httpRspHeader": "HTTP/1.1 504 Gateway Timeout",
        "httpRspBody": "Timeout: timeout"
    }

    # YAML 配置
    yaml_content = """
rules:
  - name: "Timeout Error Rule"
    description: "Match timeout error in the response"
    condition:
      - field: "httpRspHeader"
        match: ".*504.*Timeout.*"
      - field: "httpRspBody"
        match: ".*Timeout.*"
    """

    # 执行匹配
    match_yaml(input_data, yaml_content)


def es_dsl_verification(data):
    try:
        alarm_info_filter = data
        # 从字典中提取相关数据
        http_req_body = alarm_info_filter.get("httpReqBody", "")
        if not http_req_body:
            return "缺少 httpReqBody"

        # 解析 HTTP 请求体为 JSON
        try:
            query_dsl = json.loads(http_req_body)
        except json.JSONDecodeError:
            return "httpReqBody 无法解析为 JSON"

        # 校验规则逻辑
        # 1. 检查是否包含 aggregations 字段
        if "aggregations" not in query_dsl:
            return "未包含 aggregations 字段"

        # 2. 检查是否包含 query.bool.filter 字段
        query = query_dsl.get("query", {})
        if not isinstance(query, dict) or "bool" not in query or "filter" not in query["bool"]:
            return "未包含 query.bool.filter 字段"
        # 3. 校验 filter 中的内容
        filters = query["bool"]["filter"]
        if not isinstance(filters, list):
            return "filter 字段不是列表"

        # 规则：检查是否存在 range 和 terms 相关内容
        range_found = any("range" in f for f in filters if isinstance(f, dict))
        terms_found = any("terms" in f for f in filters if isinstance(f, dict))

        if range_found and terms_found:
            return True
        else:
            return False

    except Exception as e:
        return "异常错误：{str(e)}"

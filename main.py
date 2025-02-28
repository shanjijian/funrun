from common.log import log
from dao.function_dao import FunctionDAO
from executor.function_executor import FunctionExecutor
from executor.yaml_executor import YamlExecutor

if __name__ == "__main__":
    functools = FunctionDAO()
    executor = FunctionExecutor()

    data = {"data": {"ruleName": "SQL注入攻击_注入点探测",
                     "httpReqHeader": "POST /ebus/rio/logkit/api/search HTTP/1.1\r\nUser-Agent: Go-http-client/1.1\r\nContent-Length: 584\r\nContent-Type: application/json\r\nKbn-Xsrf: kibana\r\nX-Tif-Nonce: 0100007f:01940736acbc:019de1\r\nX-Tif-Paasid: rio\r\nx-forwarded-for: 127.0.0.1\r\nx-real-ip: 127.0.0.1\r\nx-proxy-by: gateagent\r\nHost: 173.16.153.243:8080\r\nX-Tif-Timestamp: 1735287811\r\nX-Tif-Signature: D6934576CF23C3E7D614C9FB4387F226711854AB06BEE6FCB143CD54A75643A7\r\nconnection: close\r\nAccept-Encoding: gzip\r\n\r\n",
                     "httpReqBody": "{\"aggregations\":{\"Monitor\":{\"aggregations\":{\"err_cnt\":{\"filter\":{\"query_string\":{\"query\":\"(_exists_:errorInfo) OR (statusCode:\\u003e=400)\"}}},\"total_cnt\":{\"value_count\":{\"field\":\"_id\"}}},\"date_histogram\":{\"field\":\"@timestamp\",\"format\":\"yyyy-MM-dd HH:mm:ss\",\"interval\":\"1y\",\"time_zone\":\"Asia/Shanghai\"}}},\"query\":{\"bool\":{\"_name\":\"Monitor\",\"filter\":[{\"range\":{\"@timestamp\":{\"format\":\"epoch_second\",\"from\":1727633437,\"include_lower\":true,\"include_upper\":true,\"to\":1735287500}}},{\"terms\":{\"acctype\":[\"sub\"]}},{\"terms\":{\"paasid\":[\"guangdongshengzhanjiangnongkendieryiyuan\"]}}]}},\"size\":0}",
                     "httpRspHeader": "HTTP/1.1 504 Gateway Timeout\r\nx-proxy-by: Tif-APIGate\r\ncontent-type: text/html; charset=utf-8\r\nconnection: close\r\nDate: Fri, 27 Dec 2024 08:24:31 GMT\r\nContent-Length: 16\r\n",
                     "httpRspBody": "Timeout: timeout"}}
    result = executor.execute_by_name("es_dsl_verification", data)
    log.info(f"结果: {result}")

    # 测试YAML配置
    input_data = {
        "ruleName": "SQLu6ce8u5165u653bu51fb_u6ce8u5165u70b9u63a2u6d4b",
        "httpReqHeader": "POST /ebus/rio/logkit/api/search HTTP/1.1User-Agent: Go-http-client/1.1Content-Length: 584Content-Type: application/jsonKbn-Xsrf: kibanaX-Tif-Nonce: 0100007f:01940736acbc:019de1X-Tif-Paasid: riox-forwarded-for: 127.0.0.1x-real-ip: 127.0.0.1x-proxy-by: gateagentHost: 173.16.153.243:8080X-Tif-Timestamp: 1735287811X-Tif-Signature: D6934576CF23C3E7D614C9FB4387F226711854AB06BEE6FCB143CD54A75643A7connection: closeAccept-Encoding: gzip",
        "httpReqBody": "{\"aggregations\":{\"Monitor\":{\"aggregations\":{\"err_cnt\":{\"filter\":{\"query_string\":{\"query\":\"(_exists_:errorInfo) OR (statusCode:\\u003e=400)\"}}},\"total_cnt\":{\"value_count\":{\"field\":\"_id\"}}},\"date_histogram\":{\"field\":\"@timestamp\",\"format\":\"yyyy-MM-dd HH:mm:ss\",\"interval\":\"1y\",\"time_zone\":\"Asia/Shanghai\"}}},\"query\":{\"bool\":{\"_name\":\"Monitor\",\"filter\":[{\"range\":{\"@timestamp\":{\"format\":\"epoch_second\",\"from\":1727633437,\"include_lower\":true,\"include_upper\":true,\"to\":1735287500}}},{\"terms\":{\"acctype\":[\"sub\"]}},{\"terms\":{\"paasid\":[\"guangdongshengzhanjiangnongkendieryiyuan\"]}}]}},\"size\":0}",
        "httpRspHeader": "HTTP/1.1 504 Gateway Timeoutx-proxy-by: Tif-APIGatecontent-type: text/html; charset=utf-8connection: closeDate: Fri, 27 Dec 2024 08:24:31 GMTContent-Length: 16",
        "httpRspBody": "Timeout: timeout"
    }
    result = YamlExecutor().execute_by_rule('test', input_data)
    log.info(f"结果: {result}")

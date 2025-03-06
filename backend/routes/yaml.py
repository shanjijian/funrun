import json

from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Optional

import logging
from backend.common.log import log
from backend.dao.yaml_dao import YamlDAO
from backend.executor.yaml_executor import YamlExecutor

router = APIRouter()

# 初始化 DAO 和 执行器
yaml_dao = YamlDAO()
yaml_executor = YamlExecutor()


@router.post("/yaml/execute")
async def execute_yaml(
        rule_name: str = Body(..., embed=True),
        input_data: str = Body(..., embed=True)
):
    try:
        # 将字符串类型的 input_data 转换为字典
        data_dict = json.loads(input_data)

        # 执行指定规则的 YAML 配置
        result = yaml_executor.execute_by_rule(rule_name, data_dict)
        log.info(f"规则 {rule_name} 执行结果: {result}")

        return {"status": "success", "rule": rule_name, "result": result}

    except Exception as e:
        log.error(f"规则 {rule_name} 执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"执行失败: {str(e)}")


@router.post("/yaml/add")
async def add_yaml(
        rule_name: str = Body(...),
        yaml_name: str = Body(...),
        yaml_code: str = Body(...)
):
    """添加新 YAML 配置"""
    success = yaml_dao.add_yaml(rule_name, yaml_name, yaml_code)
    if success:
        return {"status": "success", "message": "YAML 配置添加成功"}
    raise HTTPException(status_code=500, detail="YAML 配置添加失败")


@router.get("/yaml/rule/{rule_name}")
async def get_yaml_by_rule(rule_name: str) -> Optional[Dict]:
    """通过规则名称获取 YAML 配置"""
    result = yaml_dao.get_by_rule(rule_name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="未找到对应规则的 YAML 配置")


@router.get("/yaml/name/{yaml_name}")
async def get_yaml_by_name(yaml_name: str) -> Optional[Dict]:
    """通过 YAML 配置名称获取"""
    result = yaml_dao.get_by_name(yaml_name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="未找到对应名称的 YAML 配置")


@router.put("/yaml/update")
async def update_yaml_content(
        identifier: str = Body(...),
        new_code: str = Body(...),
        by_name: bool = Body(False)
):
    """更新 YAML 配置内容"""
    success = yaml_dao.update_content(identifier, new_code, by_name)
    if success:
        return {"status": "success", "message": "YAML 配置更新成功"}
    raise HTTPException(status_code=500, detail="更新失败")


@router.delete("/yaml/delete")
async def delete_yaml(
        identifier: str = Body(...),
        by_name: bool = Body(False)
):
    """删除 YAML 配置"""
    success = yaml_dao.delete(identifier, by_name)
    if success:
        return {"status": "success", "message": "YAML 配置删除成功"}
    raise HTTPException(status_code=500, detail="删除失败")


@router.get("/yaml/list", response_model=List[Dict])
async def list_yamls():
    """列出所有 YAML 配置"""
    return yaml_dao.list_all()

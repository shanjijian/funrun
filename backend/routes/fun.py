import json

from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Optional

import logging
from backend.common.log import log
from backend.dao.function_dao import FunctionDAO
from backend.executor.function_executor import FunctionExecutor

router = APIRouter()

# 初始化 DAO 和 执行器
functools = FunctionDAO()
executor = FunctionExecutor()


@router.post("/execute")
async def execute_verification(
        rule_name: str = Body(..., embed=True),
        input_data: str = Body(..., embed=True)
):
    try:
        # 将字符串类型的 data 转换为字典
        data_dict = json.loads(input_data)

        # 执行指定任务
        result = executor.execute_by_name(rule_name, data_dict)
        log.info(f"任务 {rule_name} 执行结果: {result}")

        return {"status": "success", "task": rule_name, "result": result}

    except Exception as e:
        log.error(f"任务 {rule_name} 执行失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"执行失败: {str(e)}")


@router.post("/functions/add")
async def add_function(
        rule_name: str = Body(...),
        function_name: str = Body(...),
        function_code: str = Body(...)
):
    """添加新函数"""
    success = functools.add_function(rule_name, function_name, function_code)
    if success:
        return {"status": "success", "message": "函数添加成功"}
    raise HTTPException(status_code=500, detail="函数添加失败")


@router.get("/functions/rule/{rule_name}")
async def get_function_by_rule(rule_name: str) -> Optional[Dict]:
    """通过规则名称获取函数"""
    result = functools.get_by_rule(rule_name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="未找到对应规则的函数")


@router.get("/functions/name/{function_name}")
async def get_function_by_name(function_name: str) -> Optional[Dict]:
    """通过函数名称获取"""
    result = functools.get_by_name(function_name)
    if result:
        return result
    raise HTTPException(status_code=404, detail="未找到对应名称的函数")


@router.put("/functions/update")
async def update_function_code(
        identifier: str = Body(...),
        new_code: str = Body(...),
        by_name: bool = Body(False)
):
    """更新函数代码"""
    success = functools.update_code(identifier, new_code, by_name)
    if success:
        return {"status": "success", "message": "代码更新成功"}
    raise HTTPException(status_code=500, detail="更新失败")


@router.delete("/functions/delete")
async def delete_function(
        identifier: str = Body(...),
        by_name: bool = Body(False)
):
    """删除函数"""
    success = functools.delete(identifier, by_name)
    if success:
        return {"status": "success", "message": "函数删除成功"}
    raise HTTPException(status_code=500, detail="删除失败")


@router.get("/functions/list", response_model=List[Dict])
async def list_functions():
    """列出所有函数"""
    return functools.list_all()

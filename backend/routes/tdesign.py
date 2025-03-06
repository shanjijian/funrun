from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from random import randint, choice
from datetime import datetime

router = APIRouter()


# 模拟数据生成函数
def generate_mock_list(count, template):
    return [template(i) for i in range(1, count + 1)]


# 获取采购列表
@router.get("/api/get-purchase-list")
def get_purchase_list():
    data = generate_mock_list(randint(1, 100), lambda i: {
        "index": f"S20201228115950{randint(100, 999)}",
        "pdName": "Macbook",
        "pdNum": "p_tmp_60a637cd0d",
        "purchaseNum": randint(1, 100),
        "adminName": "财务部111",
        "updateTime": datetime.now().strftime("%H:%M:%S"),
        "pdType": "电子产品",
    })
    return {"code": 0, "data": {"list": data}}


# 获取列表
@router.get("/api/get-list")
def get_list():
    data = generate_mock_list(randint(1, 100), lambda i: {
        "index": i,
        "status": randint(0, 4),
        "no": f"BH00{randint(1, 100):02d}",
        "name": f"某市办公用品采购项目",
        "paymentType": randint(0, 1),
        "contractType": randint(0, 2),
        "updateTime": datetime.now().strftime("%H:%M:%S"),
        "amount": f"{randint(10, 500)},000,000",
        "adminName": "管理员",
    })
    return {"code": 0, "data": {"list": data}}


# 获取用户详情
@router.get("/api/detail-basic")
def get_detail_basic():
    return {
        "code": 0,
        "data": {
            "name": "td_20023747",
            "loginType": "Web",
            "currentRole": "Admin",
            "rightsList": "通用权限",
            "userStatus": "启用",
            "language": "简体中文",
            "timeZone": "(GMT+08:00)中国时区—北京（Asia/Beijing）",
        },
    }


# 获取卡片列表
@router.get("/api/get-card-list")
def get_card_list():
    banners = [
        "https://tdesign.gtimg.com/starter/cloud-db.jpg",
        "https://tdesign.gtimg.com/starter/cloud-server.jpg",
        "https://tdesign.gtimg.com/starter/ssl.jpg",
        "https://tdesign.gtimg.com/starter/t-sec.jpg",
        "https://tdesign.gtimg.com/starter/face-recognition.jpg",
    ]
    names = ["人脸识别", "SSL证书", "CVM", "云数据库", "T-Sec 云防火墙"]
    descriptions = [
        "提供人脸检测与分析、人脸比对等服务。",
        "云硬盘提供数据块级存储服务。",
        "SSL证书管理与申请。",
        "腾讯安全云防火墙，SaaS化防火墙产品。",
        "云数据库MySQL，提供安全可靠的数据库服务。",
    ]
    data = generate_mock_list(randint(48, 50), lambda i: {
        "index": i,
        "isSetup": bool(randint(0, 1)),
        "type": randint(1, 5),
        "banner": choice(banners),
        "name": choice(names),
        "description": choice(descriptions),
    })
    return {"code": 0, "data": {"list": data}}


# 获取项目列表
@router.get("/api/get-project-list")
def get_project_list():
    admins = ["顾娟", "常刚", "郑洋"]
    project_names = [
        "沧州市办公用品采购项目", "红河哈尼族彝族自治州办公用品采购项目", "铜川市办公用品采购项目",
        "陇南市办公用品采购项目", "六安市办公用品采购项目"
    ]
    data = generate_mock_list(randint(1, 50), lambda i: {
        "index": i,
        "adminPhone": f"+86 135{randint(1000, 9999)}{randint(1000, 9999)}",
        "updateTime": datetime.now().strftime("%H:%M:%S"),
        "adminName": choice(admins),
        "name": choice(project_names),
    })
    return {"code": 0, "data": {"list": data}}


# 处理POST请求
class PostRequest(BaseModel):
    name: str


@router.post("/api/post")
def post_data(request: PostRequest):
    return {"code": 0, "data": {"name": request.name}}


# 获取菜单列表
@router.get("/api/get-menu-list-i18n")
def get_menu_list():
    return {
        "code": 0,
        "data": {
            "list": [
                {
                    "path": "/list",
                    "name": "list",
                    "component": "LAYOUT",
                    "redirect": "/list/base",
                    "meta": {"title": {"zh_CN": "列表页", "en_US": "List"}, "icon": "view-list"},
                    "children": [
                        {"path": "base", "name": "ListBase", "component": "/list/base/index",
                         "meta": {"title": {"zh_CN": "基础列表页", "en_US": "Base List"}}},
                        {"path": "card", "name": "ListCard", "component": "/list/card/index",
                         "meta": {"title": {"zh_CN": "卡片列表页", "en_US": "Card List"}}},
                    ],
                }
            ]
        },
    }

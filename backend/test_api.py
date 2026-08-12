"""川香小馆 API 自测脚本 —— 需后端已启动（uvicorn :8000）。

用法：cd backend && uv run python test_api.py
用标准库 urllib，避免 PowerShell 的编码坑；中文请求/校验全程 UTF-8。
"""

import json
import sys
import urllib.error
import urllib.request

BASE = "http://localhost:8000"

passed = 0
failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"  [PASS] {name}")
    else:
        failed += 1
        print(f"  [FAIL] {name} -> {detail}")


def req(method, path, body=None):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    r = urllib.request.Request(
        BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if body is not None else {},
    )
    try:
        with urllib.request.urlopen(r, timeout=10) as resp:
            raw = resp.read()
            status = resp.status
    except urllib.error.HTTPError as e:
        status = e.code
        raw = e.read()
    try:
        payload = json.loads(raw.decode("utf-8")) if raw else None
    except Exception:
        payload = None
    return status, payload


print("=== 1. 分类 ===")
status, cats = req("GET", "/api/menu/categories")
check(
    "GET /api/menu/categories -> 200, 6 项",
    status == 200 and len(cats) == 6,
    f"status={status} count={len(cats) if cats else 0}",
)

print("=== 2. 菜品 ===")
status, dishes = req("GET", "/api/menu/dishes")
d7 = next((d for d in dishes if d["id"] == "d7"), None)
check(
    "GET /api/menu/dishes -> 200, 18 项",
    status == 200 and len(dishes) == 18,
    f"status={status} count={len(dishes) if dishes else 0}",
)
check(
    "字段 camelCase 对齐 (d7.soldOut=True, monthlySales=180)",
    d7 is not None and d7["soldOut"] is True and d7["monthlySales"] == 180,
    f"d7={d7}",
)

print("=== 3. 分类下菜品 ===")
status, c1 = req("GET", "/api/menu/categories/c1/dishes")
check(
    "GET /api/menu/categories/c1/dishes -> 200, 4 项",
    status == 200 and len(c1) == 4,
    f"status={status} count={len(c1) if c1 else 0}",
)

print("=== 4. 提交订单 (d1x2 + d14x1, 期望 67) ===")
remark = "接口自测-加辣"
status, order = req(
    "POST",
    "/api/orders",
    {
        "items": [{"dishId": "d1", "quantity": 2}, {"dishId": "d14", "quantity": 1}],
        "remark": remark,
    },
)
order_id = order["id"] if order else None
check(
    "POST /api/orders -> 201, totalPrice=67",
    status == 201 and order is not None and order["totalPrice"] == 67,
    f"status={status} order={order}",
)
check(
    "订单 items=2 且 remark 中文回显",
    order is not None and len(order["items"]) == 2 and order["remark"] == remark,
    f"remark={order.get('remark') if order else None}",
)

print("=== 5. 订单列表 ===")
status, orders = req("GET", "/api/orders")
check(
    "GET /api/orders 含新订单",
    status == 200 and any(o["id"] == order_id for o in orders),
    f"count={len(orders) if orders else 0}",
)

print("=== 6. 订单详情 ===")
status, detail = req("GET", f"/api/orders/{order_id}")
check(
    "GET /api/orders/{id} 与提交一致",
    status == 200 and detail["id"] == order_id and detail["totalPrice"] == 67,
    f"detail={detail}",
)

print("=== 7. 标记完成 ===")
status, _ = req("PATCH", f"/api/orders/{order_id}/complete")
check("PATCH /api/orders/{id}/complete -> 200", status == 200, f"status={status}")

print("=== 8. 完成态确认 ===")
status, after = req("GET", f"/api/orders/{order_id}")
check(
    "GET 后 status=completed",
    status == 200 and after["status"] == "completed",
    f"status={after.get('status') if after else None}",
)

print("=== 9. 异常场景 ===")
s, _ = req("POST", "/api/orders", {"items": [], "remark": ""})
check("POST 空 items -> 400", s == 400, f"status={s}")
s, _ = req("POST", "/api/orders", {"items": [{"dishId": "nope", "quantity": 1}]})
check("POST 不存在菜品 -> 400", s == 400, f"status={s}")
s, _ = req("GET", "/api/orders/NO0-not-exist")
check("GET 不存在订单 -> 404", s == 404, f"status={s}")
s, _ = req("PATCH", "/api/orders/NO0-not-exist/complete")
check("PATCH 不存在订单 -> 404", s == 404, f"status={s}")

print()
print(f"=== 结果: PASS {passed} / FAIL {failed} ===")
sys.exit(1 if failed else 0)

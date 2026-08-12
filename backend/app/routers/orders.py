"""订单接口：下单、列表、详情、标记完成。金额由服务端按菜单价计算。"""

import time
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..database import get_connection

router = APIRouter(prefix="/api/orders", tags=["orders"])


class OrderItemIn(BaseModel):
    dishId: str
    quantity: int = Field(gt=0)


class OrderIn(BaseModel):
    items: list[OrderItemIn]
    remark: str = ""


def _get_order(conn, order_id: str) -> dict | None:
    row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if row is None:
        return None
    items = conn.execute(
        "SELECT dish_id, quantity FROM order_items WHERE order_id = ?", (order_id,)
    ).fetchall()
    return {
        "id": row["id"],
        "items": [{"dishId": r["dish_id"], "quantity": r["quantity"]} for r in items],
        "totalPrice": row["total_price"],
        "status": row["status"],
        "remark": row["remark"],
        "createdAt": row["created_at"],
    }


@router.post("", status_code=201)
def create_order(payload: OrderIn) -> dict:
    if not payload.items:
        raise HTTPException(status_code=400, detail="订单不能为空")

    conn = get_connection()
    try:
        total_price = 0.0
        for it in payload.items:
            row = conn.execute(
                "SELECT price FROM dishes WHERE id = ?", (it.dishId,)
            ).fetchone()
            if row is None:
                raise HTTPException(status_code=400, detail=f"菜品不存在: {it.dishId}")
            total_price += row["price"] * it.quantity

        order_id = f"NO{int(time.time() * 1000)}"
        created_at = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "INSERT INTO orders (id, total_price, status, remark, created_at)"
            " VALUES (?, ?, 'pending', ?, ?)",
            (order_id, total_price, payload.remark, created_at),
        )
        conn.executemany(
            "INSERT INTO order_items (order_id, dish_id, quantity) VALUES (?, ?, ?)",
            [(order_id, it.dishId, it.quantity) for it in payload.items],
        )
        conn.commit()
    finally:
        conn.close()

    conn = get_connection()
    try:
        order = _get_order(conn, order_id)
    finally:
        conn.close()
    return order


@router.get("")
def list_orders(status: str | None = None) -> list[dict]:
    conn = get_connection()
    try:
        if status:
            rows = conn.execute(
                "SELECT id FROM orders WHERE status = ? ORDER BY created_at DESC",
                (status,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id FROM orders ORDER BY created_at DESC"
            ).fetchall()
        orders = [_get_order(conn, r["id"]) for r in rows]
    finally:
        conn.close()
    return orders


@router.get("/{order_id}")
def read_order(order_id: str) -> dict:
    conn = get_connection()
    try:
        order = _get_order(conn, order_id)
    finally:
        conn.close()
    if order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order


@router.patch("/{order_id}/complete")
def complete_order(order_id: str) -> dict:
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,)
        )
        conn.commit()
    finally:
        conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"ok": True}

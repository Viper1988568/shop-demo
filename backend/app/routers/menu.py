"""菜单只读接口：分类、菜品。返回 camelCase，与前端类型契约对齐。"""

from fastapi import APIRouter
from ..database import get_connection

router = APIRouter(prefix="/api/menu", tags=["menu"])


def _dish_to_json(row) -> dict:
    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "categoryId": row["category_id"],
        "description": row["description"],
        "image": row["image"],
        "monthlySales": row["monthly_sales"],
        "spicyLevel": row["spicy_level"],
        "soldOut": bool(row["sold_out"]),
    }


@router.get("/categories")
def list_categories() -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, name FROM categories ORDER BY id").fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]


@router.get("/dishes")
def list_dishes() -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM dishes ORDER BY id").fetchall()
    finally:
        conn.close()
    return [_dish_to_json(r) for r in rows]


@router.get("/categories/{category_id}/dishes")
def list_dishes_by_category(category_id: str) -> list[dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM dishes WHERE category_id = ? ORDER BY id", (category_id,)
        ).fetchall()
    finally:
        conn.close()
    return [_dish_to_json(r) for r in rows]

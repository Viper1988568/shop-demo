"""SQLite 连接、建表与种子数据。

数据契约见前端 src/types/index.ts；本文件的分类/菜品 seed 由 src/mock/index.ts
迁移而来，字段命名保持数据库风格（snake_case），路由层负责转成 camelCase 契约。
"""

import sqlite3
from pathlib import Path

# backend/shop.db —— 首次启动自动创建
DB_PATH = Path(__file__).resolve().parent.parent / "shop.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id   TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dishes (
    id            TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    price         REAL NOT NULL,
    category_id   TEXT NOT NULL REFERENCES categories(id),
    description   TEXT NOT NULL,
    image         TEXT NOT NULL,
    monthly_sales INTEGER NOT NULL,
    spicy_level   TEXT NOT NULL,
    sold_out      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    id          TEXT PRIMARY KEY,
    total_price REAL NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    remark      TEXT NOT NULL DEFAULT '',
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL REFERENCES orders(id),
    dish_id  TEXT NOT NULL,
    quantity INTEGER NOT NULL
);
"""

CATEGORIES = [
    ("c1", "招牌必点"),
    ("c2", "热菜"),
    ("c3", "凉菜"),
    ("c4", "汤类"),
    ("c5", "主食"),
    ("c6", "饮品"),
]

# (id, name, price, category_id, description, image, monthly_sales, spicy_level, sold_out)
DISHES = [
    ("d1", "宫保鸡丁", 32, "c1", "经典川菜，鸡丁花生爆炒，咸甜微辣", "🍗", 320, "微辣", 0),
    ("d2", "水煮鱼", 58, "c1", "麻辣鲜香，鱼片嫩滑", "🐟", 268, "中辣", 0),
    ("d3", "回锅肉", 36, "c1", "肥而不腻，香辣下饭", "🥩", 210, "微辣", 0),
    ("d4", "毛血旺", 52, "c1", "鸭血毛肚，麻辣过瘾", "🍲", 156, "特辣", 0),
    ("d5", "鱼香肉丝", 30, "c2", "酸甜微辣，肉丝滑嫩", "🥕", 300, "微辣", 0),
    ("d6", "麻婆豆腐", 22, "c2", "麻辣鲜嫩烫，下饭神器", "🍳", 280, "中辣", 0),
    ("d7", "干煸四季豆", 24, "c2", "干香爽脆，今日已售罄", "🫘", 180, "不辣", 1),
    ("d8", "糖醋里脊", 38, "c2", "外酥里嫩，酸甜开胃", "🥓", 140, "不辣", 0),
    ("d9", "拍黄瓜", 12, "c3", "爽口解腻", "🥒", 350, "不辣", 0),
    ("d10", "口水鸡", 28, "c3", "麻辣红油，鸡肉嫩滑", "🍗", 220, "中辣", 0),
    ("d11", "夫妻肺片", 26, "c3", "卤香入味，麻辣鲜香", "🥩", 160, "中辣", 0),
    ("d12", "番茄蛋花汤", 12, "c4", "酸甜暖胃", "🍅", 240, "不辣", 0),
    ("d13", "酸辣汤", 14, "c4", "酸辣开胃，料足味浓", "🥣", 130, "微辣", 0),
    ("d14", "米饭", 3, "c5", "东北五常大米", "🍚", 800, "不辣", 0),
    ("d15", "扬州炒饭", 18, "c5", "粒粒分明，配料丰富", "🍛", 190, "不辣", 0),
    ("d16", "手工水饺(12只)", 20, "c5", "现包现煮，皮薄馅大", "🥟", 170, "不辣", 0),
    ("d17", "酸梅汤", 6, "c6", "冰镇解辣", "🧃", 400, "不辣", 0),
    ("d18", "王老吉", 8, "c6", "降火凉茶", "🥤", 360, "不辣", 0),
]


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """建表（幂等）并写入种子数据。应用启动时调用一次。"""
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        # INSERT OR IGNORE：主键已存在则跳过，重复启动不重复插入
        conn.executemany(
            "INSERT OR IGNORE INTO categories (id, name) VALUES (?, ?)", CATEGORIES
        )
        conn.executemany(
            """INSERT OR IGNORE INTO dishes
               (id, name, price, category_id, description, image,
                monthly_sales, spicy_level, sold_out)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            DISHES,
        )
        conn.commit()
    finally:
        conn.close()

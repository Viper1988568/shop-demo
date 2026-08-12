/**
 * 数据契约 —— 与将来后端接口对齐的唯一依据。
 * 第一阶段由 api/ 层返回本地 mock 数据实现这些契约；
 * 后续接入后端时只改 api/ 内部实现，类型与页面不变。
 */

export interface Category {
  id: string
  name: string
}

export type SpicyLevel = '不辣' | '微辣' | '中辣' | '特辣'

export interface Dish {
  id: string
  name: string
  /** 单价，单位：元 */
  price: number
  categoryId: string
  description: string
  /** 菜品图片：mock 阶段为 emoji 占位，接入后端后为图片 URL */
  image: string
  /** 月售数量 */
  monthlySales: number
  spicyLevel: SpicyLevel
  soldOut: boolean
}

export interface CartItem {
  dishId: string
  quantity: number
}

export type OrderStatus = 'pending' | 'completed'

export interface Order {
  id: string
  items: CartItem[]
  totalPrice: number
  status: OrderStatus
  remark: string
  createdAt: string
}

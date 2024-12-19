布料销售管理系统 - 开发与部署指南
一、开发环境要求
1. 基础环境
Python 3.8+
MySQL 5.7+
PyQt6
Git (可选，用于版本控制)
2. Python 依赖包
  pip install PyQt6
  pip install pymysql
  pip install openpyxl
二、项目结构
├── main.py              # 主程序入口
├── models.py            # 数据模型
├── database.py          # 数据库连接
├── config.py            # 配置文件
├── test_db.py          # 数据库测试
└── dialogs/            # 对话框模块
    ├── customer_edit_dialog.py
    ├── customer_orders_dialog.py
    ├── customer_select_dialog.py
    ├── order_detail_dialog.py
    ├── order_edit_dialog.py
    ├── order_item_dialog.py
    ├── payment_dialog.py
    └── payment_method_dialog.py
三、数据库设置
-- 创建客户表
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建订单表
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'partial_paid', 'paid') DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 创建订单项目表
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    meters DECIMAL(10,2) NOT NULL,
    rolls INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- 创建支付记录表
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- 创建支付方式表
CREATE TABLE payment_methods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

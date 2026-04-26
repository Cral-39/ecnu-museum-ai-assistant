-- MySQL 8.0 建表语句
-- 华东师大博物馆AI智能导览系统

-- 用户表
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    `password` VARCHAR(32) NOT NULL COMMENT '密码(MD5加密)',
    `role` ENUM('user', 'admin') DEFAULT 'user' COMMENT '角色:普通用户/管理员',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 文物表
CREATE TABLE IF NOT EXISTS `artifacts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '文物ID',
    `name` VARCHAR(100) NOT NULL COMMENT '文物名称',
    `description` TEXT COMMENT '文物描述',
    `image_url` VARCHAR(255) COMMENT '图片URL',
    `three_d_url` VARCHAR(255) COMMENT '3D/官网链接',
    `category` VARCHAR(50) COMMENT '类别:古钱币/青铜器/书画/陶瓷/标本等',
    `collection` VARCHAR(50) COMMENT '所属馆藏:历史文物馆/生物标本馆/古钱币馆等',
    `era` VARCHAR(50) COMMENT '所属年代',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文物表';

-- 展览表
CREATE TABLE IF NOT EXISTS `exhibitions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '展览ID',
    `title` VARCHAR(100) NOT NULL COMMENT '展览标题',
    `description` TEXT COMMENT '展览描述',
    `start_date` DATE COMMENT '开始日期',
    `end_date` DATE COMMENT '结束日期',
    `location` VARCHAR(100) COMMENT '展览地点',
    `highlights` TEXT COMMENT '展览亮点',
    `image_url` VARCHAR(255) COMMENT '展览图片URL',
    `status` ENUM('upcoming', 'ongoing', 'ended') DEFAULT 'ongoing' COMMENT '展览状态',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='展览表';

-- 咨询记录表
CREATE TABLE IF NOT EXISTS `consultations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '咨询记录ID',
    `user_id` INT COMMENT '用户ID',
    `question` TEXT NOT NULL COMMENT '用户问题',
    `answer` TEXT COMMENT 'AI回答',
    `artifact_id` INT COMMENT '关联文物ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '咨询时间',
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL,
    FOREIGN KEY (`artifact_id`) REFERENCES `artifacts`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='咨询记录表';

-- 搜索统计表(用于热门搜索Top5)
CREATE TABLE IF NOT EXISTS `search_stats` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `keyword` VARCHAR(100) NOT NULL COMMENT '搜索关键词',
    `search_count` INT DEFAULT 1 COMMENT '搜索次数',
    `last_searched` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '最后搜索时间',
    UNIQUE KEY `idx_keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='搜索统计表';

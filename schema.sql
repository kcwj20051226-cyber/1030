-- ========================================================
-- 專案名稱：廢墟版活動報名平台 (基本款)
-- 資料庫結構與初始化腳本 (MySQL / MariaDB 版)
-- ========================================================

-- 建立資料庫 (若不存在)
CREATE DATABASE IF NOT EXISTS `activity_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `activity_db`;

-- 清理舊資料表 (依照外鍵相依順序)
DROP TABLE IF EXISTS `registrations`;
DROP TABLE IF EXISTS `events`;

-- --------------------------------------------------------
-- 資料表 1: events (活動資料表)
-- 符合需求：
-- 1. 新增新的活動
-- 2. 列出可報名的活動清單
-- --------------------------------------------------------
CREATE TABLE `events` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '活動唯一識別碼 (Primary Key)',
    `title` VARCHAR(150) NOT NULL COMMENT '活動名稱 / 主題',
    `description` TEXT NULL COMMENT '活動詳細內容說明',
    `event_date` DATETIME NOT NULL COMMENT '活動開始日期與時間',
    `location` VARCHAR(255) NOT NULL DEFAULT '線上' COMMENT '活動地點或會議連結',
    `max_participants` INT NOT NULL DEFAULT 50 COMMENT '人數上限 (0 代表不限人數)',
    `status` ENUM('OPEN', 'CLOSED', 'CANCELLED') NOT NULL DEFAULT 'OPEN' COMMENT '狀態：OPEN(可報名), CLOSED(已額滿/截止), CANCELLED(已取消)',
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '活動建立時間',
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '最後更新時間'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='活動資訊表';

-- --------------------------------------------------------
-- 資料表 2: registrations (報名清單資料表)
-- 符合需求：
-- 1. 填寫報名表 (姓名、連絡電話)
-- 2. 送出完成報名
-- 3. 查看活動的報名清單
-- --------------------------------------------------------
CREATE TABLE `registrations` (
    `id` INT AUTO_INCREMENT PRIMARY KEY COMMENT '報名紀錄唯一序號 (Primary Key)',
    `event_id` INT NOT NULL COMMENT '關聯之活動 ID (Foreign Key)',
    `name` VARCHAR(100) NOT NULL COMMENT '報名者姓名',
    `phone` VARCHAR(30) NOT NULL COMMENT '連絡電話',
    `email` VARCHAR(150) NULL COMMENT '電子郵件 (選填)',
    `note` TEXT NULL COMMENT '備註需求 (選填)',
    `registered_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '報名送出時間',
    CONSTRAINT `fk_registrations_event`
        FOREIGN KEY (`event_id`)
        REFERENCES `events` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='報名紀錄資料表';

-- --------------------------------------------------------
-- 索引設計 (提升查詢效能)
-- --------------------------------------------------------
CREATE INDEX `idx_events_status_date` ON `events` (`status`, `event_date`);
CREATE INDEX `idx_registrations_event_id` ON `registrations` (`event_id`);

-- --------------------------------------------------------
-- 測試種子資料 (Seed Data)
-- 供小組成員匯入後立即進行介面與 API 開發測試
-- --------------------------------------------------------
INSERT INTO `events` (`id`, `title`, `description`, `event_date`, `location`, `max_participants`, `status`) VALUES
(1, '廢墟探險與攝影入門實作', '探索城市廢墟美學，學習低光源環境下的光影構圖。', '2026-11-15 14:00:00', '舊松山菸廠園區', 25, 'OPEN'),
(2, '全端網頁開發入門工作坊', '教導如何使用 Git 協作與建置活動報名系統前端與後端。', '2026-11-20 09:30:00', '綜合科技大樓 301 電腦教室', 40, 'OPEN'),
(3, '校園星空夜景野營體驗', '因預約已滿，目前已截止報名。', '2026-12-05 18:00:00', '學校後山草坪', 15, 'CLOSED');

INSERT INTO `registrations` (`event_id`, `name`, `phone`, `email`, `note`) VALUES
(1, '陳小美', '0912-345-678', 'may@example.com', '需要自備手電筒嗎？'),
(1, '林大同', '0922-987-654', 'tatung@example.com', '準時出席'),
(2, '王志強', '0933-111-222', 'john@example.com', '希望學習 MySQL 連線'),
(2, '張雅婷', '0955-444-333', 'yating@example.com', '使用筆電參加');

-- `first`.custom_parameter definition

CREATE TABLE `custom_parameter` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key_name` varchar(255) NOT NULL COMMENT '参数键',
  `value` text NOT NULL COMMENT '参数值',
  `description` text COMMENT '参数描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放自定义参数信息';


-- `first`.database_info definition

CREATE TABLE `database_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '数据库标识名',
  `environment` varchar(32) NOT NULL COMMENT '环境标识:sit,uat',
  `host` varchar(255) NOT NULL COMMENT '数据库主机地址',
  `port` int NOT NULL COMMENT '数据库端口',
  `username` varchar(255) NOT NULL COMMENT '用户名',
  `password` varchar(255) NOT NULL COMMENT '密码（加密存储）',
  `db_name` varchar(255) NOT NULL COMMENT '数据库名',
  `description` text COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据库相关信息';


-- `first`.`domain` definition

CREATE TABLE `domain` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '名称',
  `code` varchar(255) NOT NULL COMMENT '接口唯一code',
  `environment` varchar(32) NOT NULL COMMENT '环境标识:sit,uat',
  `domain` varchar(255) NOT NULL COMMENT '域名',
  `description` text COMMENT '接口描述',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_environment_unique` (`code`,`environment`) COMMENT 'code和环境唯一约束'
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='接口域名表';


-- `first`.endpoint definition

CREATE TABLE `endpoint` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '名称',
  `code` varchar(255) NOT NULL COMMENT '接口唯一code',
  `method` varchar(32) NOT NULL COMMENT 'HTTP 请求方法:get,post',
  `domain_code` varchar(32) NOT NULL COMMENT '域名code',
  `path` varchar(255) NOT NULL COMMENT '接口路径',
  `description` text COMMENT '接口描述',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `code_unique` (`code`) COMMENT 'code唯一约束'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='接口基本信息表';


-- `first`.report definition

CREATE TABLE `report` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint NOT NULL COMMENT '任务 ID',
  `version` bigint NOT NULL COMMENT '版本号',
  `status` int NOT NULL COMMENT '执行状态',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放测试报告信息';


-- `first`.report_detail definition

CREATE TABLE `report_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `report_id` bigint NOT NULL COMMENT '测试报告 ID',
  `content_type` varchar(50) NOT NULL COMMENT '内容类型（如日志、截图）',
  `content` mediumblob COMMENT '内容数据（如日志文本、截图文件）',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存储用例执行产生的日志或截图信息';


-- `first`.repository definition

CREATE TABLE `repository` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '仓库名称',
  `url` text NOT NULL COMMENT 'Git 仓库地址',
  `branch` varchar(255) DEFAULT 'main' COMMENT '分支',
  `description` text COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放 Git 仓库地址';


-- `first`.repository_detail definition

CREATE TABLE `repository_detail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `repository_id` bigint NOT NULL COMMENT '仓库id',
  `url` text NOT NULL COMMENT 'Git 仓库地址',
  `branch` varchar(255) NOT NULL COMMENT '分支',
  `version` bigint DEFAULT NULL COMMENT '版本号',
  `is_latest` tinyint(1) DEFAULT '0' COMMENT '是否为最新版本',
  `task_num` int DEFAULT '0' COMMENT '任务数量',
  `description` text COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放 Git 仓库地址';


-- `first`.schedule definition

CREATE TABLE `schedule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `task_id` bigint NOT NULL COMMENT '任务 ID',
  `cron_expression` varchar(255) NOT NULL COMMENT 'CRON 表达式',
  `enabled` tinyint(1) DEFAULT '1' COMMENT '是否启用',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放任务的定时信息';


-- `first`.task definition

CREATE TABLE `task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `version` bigint NOT NULL COMMENT '版本号',
  `file_path` varchar(255) NOT NULL COMMENT '文件路径',
  `func_name` varchar(64) NOT NULL COMMENT '方法名称',
  `cron_expression` varchar(255) NOT NULL COMMENT 'CRON 表达式',
  `description` text COMMENT '描述',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='存放任务信息';
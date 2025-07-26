use first;

CREATE TABLE if not exists endpoint
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL COMMENT '名称',
    code        VARCHAR(255) NOT NULL COMMENT '接口唯一code',
    method      VARCHAR(32)  NOT NULL COMMENT 'HTTP 请求方法:get,post',
    domain_code VARCHAR(32)  NOT NULL COMMENT '域名code',
    path        VARCHAR(255) NOT NULL COMMENT '接口路径',
    description TEXT         NULL DEFAULT NULL COMMENT '接口描述',
    is_active   BOOLEAN           DEFAULT TRUE COMMENT '是否启用',
    created_at  TIMESTAMP         DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  TIMESTAMP         DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY code_unique (code) COMMENT 'code唯一约束'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='接口基本信息表';

CREATE TABLE if not exists domain
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL COMMENT '名称',
    code        VARCHAR(255) NOT NULL COMMENT '接口唯一code',
    environment VARCHAR(32)  NOT NULL COMMENT '环境标识:sit,uat',
    domain      VARCHAR(255) NOT NULL COMMENT '域名',
    description TEXT         NULL DEFAULT NULL COMMENT '接口描述',
    created_at  TIMESTAMP         DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  TIMESTAMP         DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY code_environment_unique (code, environment) COMMENT 'code和环境唯一约束'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='接口域名表';

CREATE TABLE database_info
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL COMMENT '数据库标识名',
    environment VARCHAR(32)  NOT NULL COMMENT '环境标识:sit,uat',
    host        VARCHAR(255) NOT NULL COMMENT '数据库主机地址',
    port        INT          NOT NULL COMMENT '数据库端口',
    username    VARCHAR(255) NOT NULL COMMENT '用户名',
    password    VARCHAR(255) NOT NULL COMMENT '密码（加密存储）',
    db_name     VARCHAR(255) NOT NULL COMMENT '数据库名',
    description TEXT COMMENT '描述',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='数据库相关信息';

CREATE TABLE custom_parameter
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    key_name    VARCHAR(255) NOT NULL COMMENT '参数键',
    value       TEXT         NOT NULL COMMENT '参数值',
    description TEXT COMMENT '参数描述',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存放自定义参数信息';

CREATE TABLE repository
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL COMMENT '仓库名称',
    url         TEXT         NOT NULL COMMENT 'Git 仓库地址',
    branch      VARCHAR(255) DEFAULT 'main' COMMENT '分支',
    description TEXT COMMENT '描述',
    created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存放 Git 仓库地址';

CREATE TABLE repository_detail
(
    id            BIGINT AUTO_INCREMENT PRIMARY KEY,
    repository_id BIGINT       NOT NULL COMMENT '仓库id',
    url           TEXT         NOT NULL COMMENT 'Git 仓库地址',
    branch        VARCHAR(255) NOT NULL COMMENT '分支',
    version       BIGINT COMMENT '版本号',
    is_latest     BOOLEAN  DEFAULT FALSE COMMENT '是否为最新版本',
    task_num      INT(128) DEFAULT 0 COMMENT '任务数量',
    description   TEXT COMMENT '描述',
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at    DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT'存放 Git 仓库地址';

CREATE TABLE task
(
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    version         BIGINT       NOT NULL COMMENT '版本号',
    file_path       VARCHAR(255) NOT NULL COMMENT '文件路径',
    func_name       VARCHAR(64)  NOT NULL COMMENT '方法名称',
    cron_expression VARCHAR(255) NOT NULL COMMENT 'CRON 表达式',
    description     TEXT COMMENT '描述',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存放任务信息';

CREATE TABLE schedule
(
    id              BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id         BIGINT       NOT NULL COMMENT '任务 ID',
    cron_expression VARCHAR(255) NOT NULL COMMENT 'CRON 表达式',
    enabled         BOOLEAN  DEFAULT TRUE COMMENT '是否启用',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存放任务的定时信息';

CREATE TABLE report
(
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id    BIGINT NOT NULL COMMENT '任务 ID',
    version    BIGINT NOT NULL COMMENT '版本号',
    status     int(4) NOT NULL COMMENT '执行状态',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '执行时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存放测试报告信息';

CREATE TABLE report_detail
(
    id           BIGINT AUTO_INCREMENT PRIMARY KEY,
    report_id    BIGINT      NOT NULL COMMENT '测试报告 ID',
    content_type VARCHAR(50) NOT NULL COMMENT '内容类型（如日志、截图）',
    content      MEDIUMBLOB COMMENT '内容数据（如日志文本、截图文件）',
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='存储用例执行产生的日志或截图信息';

CREATE TABLE user
(
    id         BIGINT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(64) NOT NULL COMMENT '账号',
    password   VARCHAR(128) NOT NULL COMMENT '密码',
    salt       VARCHAR(32) COMMENT '加盐值',
    role       INT         NOT NULL COMMENT '角色',
    created_at DATETIME  DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_unicode_ci  COMMENT='用户信息';


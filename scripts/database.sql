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
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='接口基本信息表';

CREATE TABLE if not exists domain
(
    id          BIGINT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(255) NOT NULL COMMENT '名称',
    code        VARCHAR(255) NOT NULL COMMENT '接口唯一code',
    environment VARCHAR(32)  NOT NULL COMMENT '环境标识:sit,uat',
    domain      VARCHAR(255) NOT NULL COMMENT '域名',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY code_environment_unique (code, environment) COMMENT 'code和环境唯一约束'
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4 COMMENT ='接口域名表';

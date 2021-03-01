create table user
(
	id bigint auto_increment,
	phone varchar(32) null comment '手机号码',
	email varchar(255) null comment '邮箱',
	`password` varchar(128) not null DEFAULT '' comment '密码',
	nickname varchar(128) not null DEFAULT '' comment '昵称',
	head_img_url varchar(256) not null DEFAULT '' comment '头像地址',
	type int not null DEFAULT 0 comment '用户类型',
	`status` int not null DEFAULT 1 comment '账户状态 # 0: 冻结 1: 激活',
	token varchar(256) not null DEFAULT '' comment '用户登陆token',
	create_time datetime not null DEFAULT NOW() comment '创建时间',
	update_time datetime not null DEFAULT NOW() comment '更新时间',
	constraint user_pk primary key (id)
) comment '用户表';
CREATE UNIQUE INDEX user_phone_unique ON user(phone);
CREATE UNIQUE INDEX user_email_unique ON user(email);
CREATE INDEX user_nickname ON user(nickname);


create table role
(
	id bigint auto_increment,
	`name` varchar(32) not null DEFAULT '' comment '角色名',
	description varchar(255) not null DEFAULT '' comment '描述',
	create_time datetime not null DEFAULT NOW() comment '创建时间',
	update_time datetime not null DEFAULT NOW() comment '更新时间',
	constraint role_pk primary key (id)
) comment '角色表';

create table platform
(
	id bigint auto_increment,
	`name` varchar(32) not null DEFAULT '' comment '平台名',
	description varchar(255) not null DEFAULT '' comment '描述',
	`key` varchar(255) null comment '平台Key',
	create_time datetime not null DEFAULT NOW() comment '创建时间',
	update_time datetime not null DEFAULT NOW() comment '更新时间',
	constraint role_pk primary key (id)
) comment '平台表';

create table menu
(
	id bigint auto_increment,
	`name` varchar(32) not null DEFAULT '' comment '菜单名称',
	description varchar(255) not null DEFAULT '' comment '描述',
	`key` varchar(255) null comment '菜单Key',
	parent_id bigint DEFAULT 0 comment '父级菜单ID',
	platform_id bigint DEFAULT 0 comment '平台ID',
	menu_url varchar(1024) null comment '菜单图片地址',
	create_time datetime not null DEFAULT NOW() comment '创建时间',
	update_time datetime not null DEFAULT NOW() comment '更新时间',
	constraint menu_pk primary key (id)
) comment '菜单表';
CREATE UNIQUE INDEX menu_key_unique ON menu(`key`);

create table permission
(
	id bigint auto_increment,
	`name` varchar(32) not null DEFAULT '' comment '权限名称',
	`key` varchar(255) null comment '权限Key',
	create_time datetime not null DEFAULT NOW() comment '创建时间',
	update_time datetime not null DEFAULT NOW() comment '更新时间',
	constraint permission_pk primary key (id)
) comment '权限表';
CREATE UNIQUE INDEX permission_key_unique ON permission(`key`);


SET FOREIGN_KEY_CHECKS = 0;

drop database if exists pt_csust;

create database pt_csust;

drop table if exists homework;
create table `homework` (
	`id` bigint unsigned not null auto_increment comment 'id',
    `title` varchar(255) not null comment '作业标题',
    `publish_time` datetime comment '发布时间',
    `end_time` datetime comment '截止时间',
    `content` varchar(255) comment '作业内容',
    `is_publish_reminder` tinyint comment '是否已进行发布提醒',
    `is_deadline_reminder_first` tinyint unsigned default 0 comment '是否已进行第一次截止提醒',
    `is_deadline_reminder_second` tinyint unsigned default 0 comment '是否已进行第二次截止提醒',
    `course_id` bigint unsigned not null comment '课程id',
    primary key (`id`) using btree,
    constraint FK_COURSE_ID foreign key (`course_id`) references `course`(`id`)
) engine=InnoDB default charset=utf8;

drop table if exists course;
create table `course` (
	`id` bigint unsigned not null auto_increment comment 'id',
    `course_name` varchar(50) comment '课程名',
    primary key (`id`) using btree
) engine=InnoDB default charset=utf8;

set FOREIGN_KEY_CHECKS = 1;
/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : localhost
 Source Database       : wechat_game

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : utf-8

 Date: 07/05/2017 23:48:05 PM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `attack_log`
-- ----------------------------
DROP TABLE IF EXISTS `attack_log`;
CREATE TABLE `attack_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `attacker` int(11) NOT NULL COMMENT '攻击者ID',
  `attacked` int(11) NOT NULL COMMENT '被攻击者的ID',
  `damage` int(11) NOT NULL DEFAULT '0' COMMENT '伤害',
  `attack_type` int(11) NOT NULL DEFAULT '0' COMMENT '伤害类型',
  `attack_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '攻击时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `chat_log`
-- ----------------------------
DROP TABLE IF EXISTS `chat_log`;
CREATE TABLE `chat_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `msg_id` bigint(20) DEFAULT NULL,
  `nickname` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '谁发的',
  `content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `actual_nick_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '',
  `group_name` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '',
  `received_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '接收的时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=746 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `kill_log`
-- ----------------------------
DROP TABLE IF EXISTS `kill_log`;
CREATE TABLE `kill_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `killer` int(11) NOT NULL COMMENT '杀手',
  `killed` int(11) NOT NULL COMMENT '被杀的',
  `kill_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '击杀时间',
  `damage` double NOT NULL DEFAULT '0' COMMENT '伤害值',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `prop`
-- ----------------------------
DROP TABLE IF EXISTS `prop`;
CREATE TABLE `prop` (
  `id` int(11) NOT NULL COMMENT 'prop',
  `prop_name` varchar(256) NOT NULL DEFAULT '' COMMENT '道具名称',
  `prop_type` int(5) NOT NULL DEFAULT '0' COMMENT '道具类型，1:攻击Buff、2:死后Buff、3:自用Buff、4:被动Buff',
  `prop_desc` varchar(256) NOT NULL DEFAULT '' COMMENT '道具描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Table structure for `user`
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '本数据库生成的id',
  `userName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '账号',
  `nickName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `remarkName` varchar(256) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '备注的昵称',
  `displayName` varchar(256) CHARACTER SET utf8mb4 NOT NULL DEFAULT '' COMMENT '群名字',
  `hp` bigint(20) unsigned NOT NULL DEFAULT '10000' COMMENT '血量',
  `maxHp` int(11) NOT NULL DEFAULT '500' COMMENT '最大血量',
  `power` int(11) unsigned NOT NULL DEFAULT '10' COMMENT '体力，一点体力攻击一次',
  `level` int(11) NOT NULL DEFAULT '1' COMMENT '等级',
  `exp` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '经验值',
  `groupUserName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '' COMMENT '群聊ID，每次登陆都会变',
  `groupNickName` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '群聊名称',
  `minDamage` int(11) NOT NULL DEFAULT '0' COMMENT '最小伤害',
  `maxDamage` int(11) NOT NULL DEFAULT '10' COMMENT '最大伤害',
  `lastAttack` int(2) NOT NULL DEFAULT '0' COMMENT '上次攻击的时间',
  `attack_num` int(5) NOT NULL DEFAULT '0' COMMENT '攻击次数',
  `critical_pro` double(9,2) NOT NULL DEFAULT '0.20' COMMENT '暴击概率',
  `critical_times` int(11) NOT NULL DEFAULT '2' COMMENT '暴击倍数',
  `acctack_buff` int(11) NOT NULL DEFAULT '0' COMMENT '攻击buff',
  `dead_buff` int(11) NOT NULL DEFAULT '0' COMMENT '死后buff',
  `usr_buff` int(11) NOT NULL DEFAULT '0' COMMENT '自用buff',
  `pass_buff` int(11) NOT NULL DEFAULT '0' COMMENT '被动buff',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_index` (`nickName`,`remarkName`,`displayName`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;

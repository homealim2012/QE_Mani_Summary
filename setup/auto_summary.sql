/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50710
Source Host           : localhost:3306
Source Database       : db

Target Server Type    : MYSQL
Target Server Version : 50710
File Encoding         : 65001

Date: 2020-04-26 19:12:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `result`
-- ----------------------------
DROP TABLE IF EXISTS `result`;
CREATE TABLE `result` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(40) DEFAULT NULL,
  `group` varchar(255) DEFAULT NULL,
  `result_name` varchar(255) DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `dataset` varchar(100) DEFAULT NULL,
  `method` varchar(255) DEFAULT NULL,
  `variable` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `other_vars` text,
  `ROUGE-1-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-1-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-1-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-2-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-2-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-2-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-3-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-3-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-3-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-4-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-4-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-4-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-L-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-L-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-L-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-W-1.2-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-W-1.2-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-W-1.2-F` decimal(10,5) DEFAULT NULL,
  `ROUGE-SU4-P` decimal(10,5) DEFAULT NULL,
  `ROUGE-SU4-R` decimal(10,5) DEFAULT NULL,
  `ROUGE-SU4-F` decimal(10,5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of result
-- ----------------------------

/*
 Navicat Premium Dump SQL

 Source Server         : tetst
 Source Server Type    : MySQL
 Source Server Version : 80300 (8.3.0)
 Source Host           : localhost:3306
 Source Schema         : pereformance-report

 Target Server Type    : MySQL
 Target Server Version : 80300 (8.3.0)
 File Encoding         : 65001

 Date: 25/05/2024 16:24:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test_data
-- ----------------------------
DROP TABLE IF EXISTS `test_data`;
CREATE TABLE `test_data` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `platform` varchar(50) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `test_type` varchar(50) NOT NULL,
  `version` varchar(50) NOT NULL,
  `test_category` varchar(100) NOT NULL,
  `test_value` int NOT NULL,
  `value_unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of test_data
-- ----------------------------
BEGIN;
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (28, 'Apls', 'dev', '开机时序', 'V1', 'GVM kernel start', 4925, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (29, 'Apls', 'dev', '开机时序', 'V1', 'Start alps-bootanimation', 9436, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (30, 'Apls', 'dev', '开机时序', 'V1', 'Start alps HUD', 9980, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (31, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_start', 6086, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (32, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_preload_start', 6970, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (33, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_preload_end', 8439, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (34, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_system_run', 8836, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (35, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_pms_start', 10078, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (36, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_pms_system_scan_start', 10318, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (37, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_pms_data_scan_start', 10759, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (38, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_pms_scan_end', 10798, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (39, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_pms_ready', 10991, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (40, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_ams_ready', 12867, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (41, 'Apls', 'dev', '开机时序', 'V1', 'boot_progress_enable_screen', 15709, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (42, 'Apls', 'dev', '开机时序', 'V2', 'GVM kernel start', 3925, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (43, 'Apls', 'dev', '开机时序', 'V2', 'Start alps-bootanimation', 8436, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (44, 'Apls', 'dev', '开机时序', 'V2', 'Start alps HUD', 8980, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (45, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_start', 4086, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (46, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_preload_start', 4970, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (47, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_preload_end', 4439, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (48, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_system_run', 4836, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (49, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_pms_start', 4078, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (50, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_pms_system_scan_start', 4318, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (51, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_pms_data_scan_start', 4759, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (52, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_pms_scan_end', 4798, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (53, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_pms_ready', 4991, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (54, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_ams_ready', 4867, 'ms');
INSERT INTO `test_data` (`id`, `platform`, `branch`, `test_type`, `version`, `test_category`, `test_value`, `value_unit`) VALUES (55, 'Apls', 'dev', '开机时序', 'V2', 'boot_progress_enable_screen', 4709, 'ms');
COMMIT;

DROP TABLE IF EXISTS `versions`;
CREATE TABLE `versions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

BEGIN;
INSERT INTO `versions` (`id`, `name`) VALUES (1, 'V1');
INSERT INTO `versions` (`id`, `name`) VALUES (2, 'V2');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

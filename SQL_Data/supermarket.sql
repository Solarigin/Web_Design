/*
 Navicat Premium Data Transfer

 Source Server         : DB_Design
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : localhost:3306
 Source Schema         : supermarket

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 14/10/2024 08:33:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `role` enum('Admin','Warehouse','CustomerManager') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'admin', 'password123', 'Admin');
INSERT INTO `admin` VALUES (2, 'warehouse_user', 'password456', 'Warehouse');
INSERT INTO `admin` VALUES (3, 'customer_user', 'password789', 'CustomerManager');

-- ----------------------------
-- Table structure for tb_customer
-- ----------------------------
DROP TABLE IF EXISTS `tb_customer`;
CREATE TABLE `tb_customer`  (
  `Cid` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CcompanyName` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CcompanySName` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CcompanyAddress` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CcompanyPhone` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Cemail` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `CName` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `CtelPhone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `other` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Cid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_customer
-- ----------------------------
INSERT INTO `tb_customer` VALUES ('C001', 'Company A', 'CA', '9234 Elm St', '1234567890', 'contact@companya.com', 'John Doe', '0987654321', 'Note 1');
INSERT INTO `tb_customer` VALUES ('C002', 'Company B', 'CB', '5678 Oak St', '1234567891', 'contact@companyb.com', 'Jane Smith', '0987654322', 'Note 2');
INSERT INTO `tb_customer` VALUES ('C003', 'Company C', 'CC', '9101 Pine St', '1234567892', 'contact@companyc.com', 'Michael Johnson', '0987654323', 'Note 3');
INSERT INTO `tb_customer` VALUES ('C004', 'Company D', 'CD', '1213 Maple St', '1234567893', 'contact@companyd.com', 'Emily Davis', '0987654324', 'Note 4');
INSERT INTO `tb_customer` VALUES ('C005', 'Company E', 'CE', '1415 Birch St', '1234567894', 'contact@companye.com', 'Chris Lee', '0987654325', 'Note 5');
INSERT INTO `tb_customer` VALUES ('C006', 'Company F', 'CF', '1617 Cedar St', '1234567895', 'contact@companyf.com', 'Patricia Brown', '0987654326', 'Note 6');
INSERT INTO `tb_customer` VALUES ('C007', 'Company G', 'CG', '1819 Walnut St', '1234567896', 'contact@companyg.com', 'Linda White', '0987654327', 'Note 7');
INSERT INTO `tb_customer` VALUES ('C008', 'Company H', 'CH', '2021 Ash St', '1234567897', 'contact@companyh.com', 'Robert Martin', '0987654328', 'Note 8');
INSERT INTO `tb_customer` VALUES ('C009', 'Company I', 'CI', '2223 Spruce St', '1234567898', 'contact@companyi.com', 'Barbara Clark', '0987654329', 'Note 9');
INSERT INTO `tb_customer` VALUES ('C010', 'Company J', 'CJ', '2425 Chestnut St', '1234567899', 'contact@companyj.com', 'James Lewis', '0987654330', 'Note 10');
INSERT INTO `tb_customer` VALUES ('C011', 'XiaoLi', 'DY', 'aaaa', '44444444444', 'FuRong@qq.com', 'Rick5Offical', '45454', 'ZZZ');
INSERT INTO `tb_customer` VALUES ('C012', 'XXX', 'XX', 'XXX', '1425424', 'FuRong@qq.com', 'John Doe', '914341999', 'XXXX');

-- ----------------------------
-- Table structure for tb_employee
-- ----------------------------
DROP TABLE IF EXISTS `tb_employee`;
CREATE TABLE `tb_employee`  (
  `Eid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `EName` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `EPas` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Elevel` varchar(2) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `EtelPhone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ESalary` int(11) NULL DEFAULT NULL,
  `other` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Eid`) USING BTREE,
  INDEX `Eid`(`Eid` ASC) USING BTREE,
  INDEX `Eid_2`(`Eid` ASC) USING BTREE,
  INDEX `Eid_3`(`Eid` ASC) USING BTREE,
  INDEX `Eid_4`(`Eid` ASC) USING BTREE,
  INDEX `Eid_5`(`Eid` ASC) USING BTREE,
  INDEX `Eid_6`(`Eid` ASC) USING BTREE,
  INDEX `Eid_7`(`Eid` ASC) USING BTREE,
  INDEX `Eid_8`(`Eid` ASC) USING BTREE,
  INDEX `Eid_9`(`Eid` ASC) USING BTREE,
  INDEX `Eid_10`(`Eid` ASC) USING BTREE,
  INDEX `Eid_11`(`Eid` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_employee
-- ----------------------------
INSERT INTO `tb_employee` VALUES ('E001', 'Alice', 'pass1', '1', '1234567890', 50000, 'Note 1');
INSERT INTO `tb_employee` VALUES ('E002', 'Bob', 'pass2', '2', '1234567891', 52000, 'Note 2');
INSERT INTO `tb_employee` VALUES ('E003', 'Charlie', 'pass3', '1', '1234567892', 51000, 'Note 3');
INSERT INTO `tb_employee` VALUES ('E004', 'David', 'pass4', '3', '1234567893', 53000, 'Note 4');
INSERT INTO `tb_employee` VALUES ('E005', 'Eve', 'pass5', '2', '1234567894', 54000, 'Note 5');
INSERT INTO `tb_employee` VALUES ('E006', 'Frank', 'pass6', '1', '1234567895', 50000, 'Note 6');
INSERT INTO `tb_employee` VALUES ('E007', 'Grace', 'pass7', '3', '1234567896', 55000, 'Note 7');
INSERT INTO `tb_employee` VALUES ('E008', 'Hank', 'pass8', '2', '1234567897', 52000, 'Note 8');
INSERT INTO `tb_employee` VALUES ('E009', 'Ivy', 'pass9', '1', '1234567898', 51000, 'Note 9');
INSERT INTO `tb_employee` VALUES ('E010', 'Jack', 'pass10', '3', '1234567899', 53000, 'Note 10');

-- ----------------------------
-- Table structure for tb_good
-- ----------------------------
DROP TABLE IF EXISTS `tb_good`;
CREATE TABLE `tb_good`  (
  `Gid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `GName` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `GPay` float NOT NULL,
  `Cid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `GIntroduction` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `other` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Gid`) USING BTREE,
  INDEX `Cid`(`Cid` ASC) USING BTREE,
  INDEX `Gid`(`Gid` ASC) USING BTREE,
  INDEX `Gid_2`(`Gid` ASC) USING BTREE,
  INDEX `Gid_3`(`Gid` ASC) USING BTREE,
  INDEX `Gid_4`(`Gid` ASC) USING BTREE,
  CONSTRAINT `tb_good` FOREIGN KEY (`Cid`) REFERENCES `tb_customer` (`Cid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_good
-- ----------------------------
INSERT INTO `tb_good` VALUES ('G001', 'Good 1', 10, 'C001', 'Introduction 1', 'NOTE 1');
INSERT INTO `tb_good` VALUES ('G002', 'Good 2', 20, 'C002', 'Introduction 2', 'Note 2');
INSERT INTO `tb_good` VALUES ('G003', 'Good 3', 30, 'C003', 'Introduction 3', 'Note 3');
INSERT INTO `tb_good` VALUES ('G004', 'Good 4', 40, 'C004', 'Introduction 4', 'Note 4');
INSERT INTO `tb_good` VALUES ('G005', 'Good 5', 50, 'C005', 'Introduction 5', 'Note 5');
INSERT INTO `tb_good` VALUES ('G006', 'Good 6', 60, 'C006', 'Introduction 6', 'Note 6');
INSERT INTO `tb_good` VALUES ('G007', 'Good 7', 70, 'C007', 'Introduction 7', 'Note 7');
INSERT INTO `tb_good` VALUES ('G008', 'Good 8', 80, 'C008', 'Introduction 8', 'Note 8');
INSERT INTO `tb_good` VALUES ('G009', 'Good 9', 90, 'C009', 'Introduction 9', 'Note 9');
INSERT INTO `tb_good` VALUES ('G010', 'Good 10', 100, 'C010', 'Introduction 10', 'Note 10');
INSERT INTO `tb_good` VALUES ('G011', 'iphone 16 pro max', 999, 'C010', 'New iphone', 'very expensive');

-- ----------------------------
-- Table structure for tb_pay_detail
-- ----------------------------
DROP TABLE IF EXISTS `tb_pay_detail`;
CREATE TABLE `tb_pay_detail`  (
  `PDid` int(15) NOT NULL,
  `Pid` int(15) NOT NULL,
  `Gid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Pcount` int(11) NOT NULL,
  `GPay` float NOT NULL,
  `total` float NOT NULL,
  `other` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`PDid`) USING BTREE,
  INDEX `Pid`(`Pid` ASC) USING BTREE,
  INDEX `Gid`(`Gid` ASC) USING BTREE,
  CONSTRAINT `tb_pay_detail1` FOREIGN KEY (`Pid`) REFERENCES `tb_pay_main` (`pid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tb_pay_detail2` FOREIGN KEY (`Gid`) REFERENCES `tb_good` (`gid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_pay_detail
-- ----------------------------
INSERT INTO `tb_pay_detail` VALUES (1, 1, 'G001', 10, 10, 100, 'Note 1');
INSERT INTO `tb_pay_detail` VALUES (2, 2, 'G002', 20, 20, 400, 'Note 2');
INSERT INTO `tb_pay_detail` VALUES (3, 3, 'G003', 30, 30, 900, 'Note 3');
INSERT INTO `tb_pay_detail` VALUES (4, 4, 'G004', 40, 40, 1600, 'Note 4');
INSERT INTO `tb_pay_detail` VALUES (5, 5, 'G005', 50, 50, 2500, 'Note 5');
INSERT INTO `tb_pay_detail` VALUES (6, 6, 'G006', 60, 60, 3600, 'Note 6');
INSERT INTO `tb_pay_detail` VALUES (7, 7, 'G007', 70, 70, 4900, 'Note 7');
INSERT INTO `tb_pay_detail` VALUES (8, 8, 'G008', 80, 80, 6400, 'Note 8');
INSERT INTO `tb_pay_detail` VALUES (9, 9, 'G009', 90, 90, 8100, 'Note 9');
INSERT INTO `tb_pay_detail` VALUES (10, 10, 'G010', 100, 100, 10000, 'Note 10');

-- ----------------------------
-- Table structure for tb_pay_main
-- ----------------------------
DROP TABLE IF EXISTS `tb_pay_main`;
CREATE TABLE `tb_pay_main`  (
  `Pid` int(11) NOT NULL,
  `Eid` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Pcount` int(11) NOT NULL,
  `Ptotal` float NOT NULL,
  `Pdate` varchar(8) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `other` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Pid`) USING BTREE,
  INDEX `Eid`(`Eid` ASC) USING BTREE,
  INDEX `Pid`(`Pid` ASC) USING BTREE,
  INDEX `Pid_2`(`Pid` ASC) USING BTREE,
  INDEX `Pid_3`(`Pid` ASC) USING BTREE,
  INDEX `Pid_4`(`Pid` ASC) USING BTREE,
  CONSTRAINT `tb_pay_main` FOREIGN KEY (`Eid`) REFERENCES `tb_employee` (`eid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_pay_main
-- ----------------------------
INSERT INTO `tb_pay_main` VALUES (1, 'E001', 10, 100, '20230101', 'Note 1');
INSERT INTO `tb_pay_main` VALUES (2, 'E002', 20, 400, '20230102', 'Note 2');
INSERT INTO `tb_pay_main` VALUES (3, 'E003', 30, 900, '20230103', 'Note 3');
INSERT INTO `tb_pay_main` VALUES (4, 'E004', 40, 1600, '20230104', 'Note 4');
INSERT INTO `tb_pay_main` VALUES (5, 'E005', 50, 2500, '20230105', 'Note 5');
INSERT INTO `tb_pay_main` VALUES (6, 'E006', 60, 3600, '20230106', 'Note 6');
INSERT INTO `tb_pay_main` VALUES (7, 'E007', 70, 4900, '20230107', 'Note 7');
INSERT INTO `tb_pay_main` VALUES (8, 'E008', 80, 6400, '20230108', 'Note 8');
INSERT INTO `tb_pay_main` VALUES (9, 'E009', 90, 8100, '20230109', 'Note 9');
INSERT INTO `tb_pay_main` VALUES (10, 'E010', 100, 10000, '20230110', 'Note 10');

-- ----------------------------
-- Procedure structure for AddCustomer
-- ----------------------------
DROP PROCEDURE IF EXISTS `AddCustomer`;
delimiter ;;
CREATE PROCEDURE `AddCustomer`(IN Cid VARCHAR(10),
    IN CcompanyName VARCHAR(30),
    IN CcompanySName VARCHAR(10),
    IN CcompanyAddress VARCHAR(40),
    IN CcompanyPhone VARCHAR(15),
    IN Cemail VARCHAR(30),
    IN Cname VARCHAR(30),
    IN CtelPhone VARCHAR(11),
    IN other VARCHAR(30))
BEGIN
    INSERT INTO tb_customer (Cid, CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, Cname, CtelPhone, other)
    VALUES (Cid, CcompanyName, CcompanySName, CcompanyAddress, CcompanyPhone, Cemail, Cname, CtelPhone, other);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteCustomer
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteCustomer`;
delimiter ;;
CREATE PROCEDURE `DeleteCustomer`(IN Cid VARCHAR(10))
BEGIN
    DELETE FROM tb_customer WHERE Cid = Cid;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetAllCustomers
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetAllCustomers`;
delimiter ;;
CREATE PROCEDURE `GetAllCustomers`()
BEGIN
    SELECT * FROM tb_customer;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateCustomer
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateCustomer`;
delimiter ;;
CREATE PROCEDURE `UpdateCustomer`(IN Cid VARCHAR(10),
    IN CcompanyName VARCHAR(30),
    IN CcompanySName VARCHAR(10),
    IN CcompanyAddress VARCHAR(40),
    IN CcompanyPhone VARCHAR(15),
    IN Cemail VARCHAR(30),
    IN Cname VARCHAR(30),
    IN CtelPhone VARCHAR(11),
    IN other VARCHAR(30))
BEGIN
    UPDATE tb_customer 
    SET CcompanyName = CcompanyName, 
        CcompanySName = CcompanySName,
        CcompanyAddress = CcompanyAddress,
        CcompanyPhone = CcompanyPhone,
        Cemail = Cemail,
        Cname = Cname,
        CtelPhone = CtelPhone,
        other = other
    WHERE Cid = Cid;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_good
-- ----------------------------
DROP TRIGGER IF EXISTS `before_good_insert_GPay`;
delimiter ;;
CREATE TRIGGER `before_good_insert_GPay` BEFORE INSERT ON `tb_good` FOR EACH ROW BEGIN
    IF NEW.GPay < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品单价不能为负数';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_good
-- ----------------------------
DROP TRIGGER IF EXISTS `before_good_update_GPay`;
delimiter ;;
CREATE TRIGGER `before_good_update_GPay` BEFORE UPDATE ON `tb_good` FOR EACH ROW BEGIN
    IF NEW.GPay < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品单价不能为负!';
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_good
-- ----------------------------
DROP TRIGGER IF EXISTS `after_good_update_GPay`;
delimiter ;;
CREATE TRIGGER `after_good_update_GPay` AFTER UPDATE ON `tb_good` FOR EACH ROW BEGIN
    IF NEW.GPay != OLD.GPay THEN
        SET @skip_trigger = TRUE;
        UPDATE tb_pay_detail SET GPay = NEW.GPay WHERE Gid = NEW.Gid;
        SET @skip_trigger = FALSE;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_detail
-- ----------------------------
DROP TRIGGER IF EXISTS `after_detail_update_PtANDPc`;
delimiter ;;
CREATE TRIGGER `after_detail_update_PtANDPc` AFTER UPDATE ON `tb_pay_detail` FOR EACH ROW BEGIN
    UPDATE tb_pay_main
    SET Ptotal = (SELECT SUM(total) FROM tb_pay_detail WHERE Pid = NEW.Pid),
        Pcount = (SELECT SUM(Pcount) FROM tb_pay_detail WHERE Pid = NEW.Pid)
    WHERE Pid = NEW.Pid;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_detail
-- ----------------------------
DROP TRIGGER IF EXISTS `after_detail_delete_PidExist`;
delimiter ;;
CREATE TRIGGER `after_detail_delete_PidExist` AFTER DELETE ON `tb_pay_detail` FOR EACH ROW BEGIN
    DECLARE PidExist INT;
    SELECT COUNT(Pid) INTO PidExist
    FROM tb_pay_main
    WHERE Pid = OLD.Pid;
    IF PidExist != 0 THEN
        UPDATE tb_pay_main
        SET Ptotal = Ptotal - OLD.total,
            Pcount = Pcount - OLD.Pcount
        WHERE Pid = OLD.Pid;
    END IF;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_detail
-- ----------------------------
DROP TRIGGER IF EXISTS `before_detail_insert_fetchedPrice`;
delimiter ;;
CREATE TRIGGER `before_detail_insert_fetchedPrice` BEFORE INSERT ON `tb_pay_detail` FOR EACH ROW BEGIN
    -- 声明一个浮点类型的变量，用于存储从tb_good表中获取的商品单价
    DECLARE fetched_price FLOAT;
    
    -- 检查插入的新记录中的Pcount（商品总数）是否为负数，如果是，则抛出一个错误，终止插入操作
    IF NEW.Pcount < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品总数不能为负!';
    END IF;

    -- 检查插入的新记录中的GPay（商品单价）是否为负数，如果是，则抛出一个错误，终止插入操作
    IF NEW.GPay < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品单价不能为负!';
    END IF;

    -- 检查插入的新记录中的total（总价）是否为负数，如果是，则抛出一个错误，终止插入操作
    IF NEW.total < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '总价不能为负!';
    END IF;

    -- 从tb_good表中选择Gid等于新插入记录的Gid的商品单价，并将其存储在变量fetched_price中
    SELECT GPay INTO fetched_price FROM tb_good WHERE Gid = NEW.Gid;

    -- 检查新插入记录的GPay是否与从tb_good表中获取的商品单价不一致，如果不一致，则将新记录的GPay设置为fetched_price
    IF NEW.GPay != fetched_price THEN
        SET NEW.GPay = fetched_price;
    END IF;

    -- 计算新插入记录的总价，公式为Pcount乘以GPay，并将其设置到新记录的total字段中
    SET NEW.total = NEW.Pcount * NEW.GPay;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_detail
-- ----------------------------
DROP TRIGGER IF EXISTS `before_detail_update_fetchedPrice`;
delimiter ;;
CREATE TRIGGER `before_detail_update_fetchedPrice` BEFORE UPDATE ON `tb_pay_detail` FOR EACH ROW BEGIN
    DECLARE fetched_price FLOAT;
    
    IF NEW.Pcount < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品总数不能为负数';
    END IF;

    IF NEW.GPay < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品单价不能为负数';
    END IF;

    IF NEW.total < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '总价不能为负数';
    END IF;

    SELECT GPay INTO fetched_price FROM tb_good WHERE Gid = NEW.Gid;

    IF NEW.GPay != fetched_price THEN
        SET NEW.GPay = fetched_price;
    END IF;

    SET NEW.total = NEW.Pcount * NEW.GPay;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_detail
-- ----------------------------
DROP TRIGGER IF EXISTS `after_detail_insert_PtANDPc`;
delimiter ;;
CREATE TRIGGER `after_detail_insert_PtANDPc` AFTER INSERT ON `tb_pay_detail` FOR EACH ROW BEGIN
    UPDATE tb_pay_main
    SET Ptotal = (SELECT SUM(total) FROM tb_pay_detail WHERE Pid = NEW.Pid),
        Pcount = (SELECT SUM(Pcount) FROM tb_pay_detail WHERE Pid = NEW.Pid)
    WHERE Pid = NEW.Pid;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_main
-- ----------------------------
DROP TRIGGER IF EXISTS `before_main_insert_NEWID`;
delimiter ;;
CREATE TRIGGER `before_main_insert_NEWID` BEFORE INSERT ON `tb_pay_main` FOR EACH ROW BEGIN
    SET NEW.Pcount = 0;
    SET NEW.Ptotal = 0;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table tb_pay_main
-- ----------------------------
DROP TRIGGER IF EXISTS `before_main_update_total`;
delimiter ;;
CREATE TRIGGER `before_main_update_total` BEFORE UPDATE ON `tb_pay_main` FOR EACH ROW BEGIN
    -- 声明一个整数类型的变量，用于存储从tb_pay_detail表中获取的商品数量总和
    DECLARE detail_total_count INT;
    -- 声明一个浮点类型的变量，用于存储从tb_pay_detail表中获取的总价总和
    DECLARE detail_total_amount FLOAT;

    -- 从tb_pay_detail表中选择Pid等于新记录Pid的商品数量总和和总价总和
    -- 如果SUM(Pcount)或SUM(total)为NULL，则使用0代替
    SELECT COALESCE(SUM(Pcount), 0), COALESCE(SUM(total), 0)
    INTO detail_total_count, detail_total_amount
    FROM tb_pay_detail
    WHERE Pid = NEW.Pid;

    -- 检查更新的新记录中的Pcount（商品数量）是否为负数，如果是，则抛出一个错误，终止更新操作
    IF NEW.Pcount < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '商品数量不能为负数';
    END IF;
    -- 检查更新的新记录中的Ptotal（总价）是否为负数，如果是，则抛出一个错误，终止更新操作
    IF NEW.Ptotal < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '总价不能为负数';
    END IF;

    -- 检查新记录的Pcount是否与从tb_pay_detail表中获取的商品数量总和不一致，如果不一致，则抛出一个错误，终止更新操作
    IF NEW.Pcount != detail_total_count THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '不匹配的商品数量在采购主表与采购明细表中';
    END IF;
    -- 检查新记录的Ptotal是否与从tb_pay_detail表中获取的总价总和不一致，如果不一致，则抛出一个错误，终止更新操作
    IF NEW.Ptotal != detail_total_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '不匹配的总价总和在采购主表与采购明细表中';
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

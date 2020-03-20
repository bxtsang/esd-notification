drop schema if exists notifications;
Create schema notifications;
use notifications;

DROP TABLE IF EXISTS `promotions`;
CREATE TABLE `promotions` (
  `code` varchar(12) NOT NULL,
  `discount` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `redemptions` int(11) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `message` varchar(300) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `applicability`;
CREATE TABLE `applicability` (
  `code` varchar(12) NOT NULL,
  `customer_tier` int NOT NULL,
  PRIMARY KEY (`code`,`customer_tier`),
  CONSTRAINT `applicability_fk1` FOREIGN KEY (`code`) REFERENCES `promotions` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



DROP TABLE IF EXISTS `redeem`;
CREATE TABLE `redeem` (
  `user_id` int NOT NULL,
  `code` varchar(12) NOT NULL,
  PRIMARY KEY (`user_id`,`code`),
  CONSTRAINT `redeem_fk1` FOREIGN KEY (`code`) REFERENCES `promotions` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DELIMITER $$

CREATE TRIGGER deduct_redemption AFTER
INSERT
ON redeem FOR EACH ROW
BEGIN
	declare num int;
    set num = (select redemptions from promotions where code = new.code) - 1;
    update promotions set redemptions = num where code = new.code;
END$$

DELIMITER ;
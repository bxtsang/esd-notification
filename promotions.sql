drop schema if exists notifications;
Create schema notifications;
use notifications;

DROP TABLE IF EXISTS `promotions`;
CREATE TABLE `promotions` (
  `code` varchar(10) NOT NULL,
  `discount` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `redemptions` int(11) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  'message' varchar(300) NOT NULL,
  PRIMARY KEY (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `promotions` VALUES ('sleepy',20,'name of promotion',100,'2020-03-08','2020-03-10', 'this is the message that should be sent out to the customers');


DROP TABLE IF EXISTS `applicability`;
CREATE TABLE `applicability` (
  `code` varchar(10) NOT NULL,
  `customer_type` varchar(45) NOT NULL,
  PRIMARY KEY (`code`,`customer_type`),
  CONSTRAINT `applicability_fk1` FOREIGN KEY (`code`) REFERENCES `promotions` (`code`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `applicability` VALUES ('sleepy','gold'),('sleepy','new'),('sleepy','old'),('sleepy','platinum');


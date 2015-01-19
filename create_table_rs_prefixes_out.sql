SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `rs_prefixes_out` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `custid` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `prefix` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `protocol` int(11) DEFAULT NULL,
  `irrdb` int(11) DEFAULT NULL,
  `rs_origin` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`custid`) REFERENCES `cust` (`id`),
  KEY `IDX_29FA9871DA0209B9` (`custid`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=505755 ;
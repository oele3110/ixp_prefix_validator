CREATE TABLE IF NOT EXISTS `rs_rpki_validation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rs_prefix_id` int(11) NOT NULL,
  `validity` varchar(255),
  `info` varchar(255),
  PRIMARY KEY (`id`)
)
CREATE TABLE IF NOT EXISTS `rs_rpki_validation` (
  `rs_prefix_id` int(11) NOT NULL,
  `validity` varchar(255),
  `info` varchar(255),
  PRIMARY KEY (`rs_prefix_id`),
  FOREIGN KEY (`rs_prefix_id`) REFERENCES `rs_prefixes` (`id`)
)
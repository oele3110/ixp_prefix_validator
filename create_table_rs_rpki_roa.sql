CREATE TABLE IF NOT EXISTS `rs_rpki_roa` (
  `rs_prefix_id` int(11) NOT NULL,
  `asn` int(11),
  `prefix` varchar(16),
  `max` int(11),
  `min` int(11),
  PRIMARY KEY (`rs_prefix_id`,`asn`,`prefix`,`max`,`min`),
  FOREIGN KEY (`rs_prefix_id`) REFERENCES `rs_prefixes` (`id`)
)
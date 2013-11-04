znc-mysql
=========
a python plugin for znc to log all communication to a mysql database

(Only tested against 0.206)

#### installation instructions
* Create a database with the name `irclogs` and the table `channel_log` as described below
* copy the sql.py to znc modules-folder
* In `Your Settings` activate the sql-plugin and enter the username and password as arguments separated by a space

#### sql tables
```sql
CREATE TABLE `channel_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` enum('MODE','UNBAN','BAN','KICK','VOICE','DEVOICE','OP','DEOP','NICK','ME','SAY','JOIN','PART','QUIT','TOPIC') DEFAULT NULL,
  `channel` char(64) DEFAULT NULL,
  `host` char(128) DEFAULT NULL,
  `user` char(32) DEFAULT NULL,
  `user_mode` char(1) DEFAULT NULL,
  `target_user` char(32) DEFAULT NULL,
  `message` text, `date` datetime DEFAULT NULL,
  `source` enum('mirc','xchat') DEFAULT NULL,
  PRIMARY KEY (`id`), KEY `channel_index` (`channel`),
  KEY `user_index` (`user`) 
) ENGINE=MyISAM AUTO_INCREMENT=2518095 DEFAULT CHARSET=utf8

```

#### dependencies
* MySQLdb
* znc python plugin

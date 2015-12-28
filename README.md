znc-mysql
=========
a python plugin for znc to log all communication to a mysql database

(Only tested against znc 1.2 and PyMySQL 0.6)

#### installation instructions
* Create a database with the name `irclogs` and the table `channel_log` as described below
* copy the sql.py to znc modules-folder
* In `Your Settings` activate the sql-plugin and enter the username, password and host as arguments separated in this format `username:password@host`

#### sql tables
```sql
CREATE TABLE `channel_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` enum('MODE','UNBAN','BAN','KICK','VOICE','DEVOICE','OP','DEOP','NICK','ME','SAY','JOIN','PART','QUIT','TOPIC') DEFAULT NULL,
  `network` char(64) DEFAULT NULL,
  `channel` char(64) DEFAULT NULL,
  `host` char(128) DEFAULT NULL,
  `user` char(32) DEFAULT NULL,
  `ident` char(32) DEFAULT NULL,
  `user_mode` char(1) DEFAULT NULL,
  `target_user` char(32) DEFAULT NULL,
  `message` text,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `channel_index` (`channel`),
  KEY `user_index` (`user`) 
) ENGINE=MyISAM AUTO_INCREMENT=2518095 DEFAULT CHARSET=utf8

```

#### dependencies
* PyMySQL
* znc python plugin

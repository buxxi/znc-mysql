import znc,pymysql,re
from datetime import datetime
from contextlib import closing

class sql(znc.Module):
	module_types = [znc.CModInfo.GlobalModule]
	has_args = True
	description = "Log all channels to a MySQL/MariaDB database"

	def OnOp(self, user, target_user, channel, noChange):
		self.insert("OP", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), target_user.GetNick(), None, str(self.GetNetwork()))
		return True

	def OnDeop(self, user, target_user, channel, noChange):
		self.insert("DEOP", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), target_user.GetNick(), None, str(self.GetNetwork()))
		return True

	def OnVoice(self, user, target_user, channel, noChange):
		self.insert("VOICE", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), target_user.GetNick(), None, str(self.GetNetwork()))
		return True

	def OnDevoice(self, user, target_user, channel, noChange):
		self.insert("DEVOICE", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), target_user.GetNick(), None, str(self.GetNetwork()))
		return True

	def OnMode(self, user, channel, mode, argument, added, noChange):
		mode = chr(mode)
		code = "MODE"
		if mode == "b":
			code = "BAN" if added else "UNBAN"
		else:
			sign = "+" if added else "-"
			argument = "{0}{1} {2}".format(sign, mode, argument)

		self.insert(code, channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, argument, str(self.GetNetwork()))
		return True

	def OnQuit(self, user, message, channels):
		for channel in channels:
			self.insert("QUIT", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, message, str(self.GetNetwork()))
		return True

	def OnNick(self, user, new_nick, channels):
		for channel in channels:
			self.insert("NICK", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), new_nick, None, str(self.GetNetwork()))
		return True

	def OnKick(self, user, target_nick, channel, message):
		self.insert("KICK", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), target_nick, message, str(self.GetNetwork()))
		return True

	def OnJoin(self, user, channel):
		self.insert("JOIN", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, None, str(self.GetNetwork()))
		return True

	def OnPart(self, user, channel, message):
		self.insert("PART", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, message, str(self.GetNetwork()))
		return True

	def OnUserAction (self, target, message):
		(channel, user) = self.resolveTarget(target)
		if channel == None:
			return True

		return self.OnChanAction(user, channel, message)

	def OnUserMsg (self, target, message):
		(channel, user) = self.resolveTarget(target)
		if channel == None:
			return True

		return self.OnChanMsg(user, channel, message)

	def OnChanAction(self, user, channel, message):
		self.insert("ME", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, message.s, str(self.GetNetwork()))
		return True

	def OnChanMsg(self, user, channel, message):
		self.insert("SAY", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), self.findMode(channel, user), datetime.now(), None, message.s, str(self.GetNetwork()))
		return True

	def OnTopic(self, user, channel, message):
		self.insert("TOPIC", channel.GetName(), user.GetHost(), user.GetNick(), user.GetIdent(), None, datetime.now(), None, message.s, str(self.GetNetwork()))
		return True

	def OnLoad(self, args, message):
		match = re.search("(.*?):(.*?)@(.*)", args)
		if match:
			self.username = match.group(1)
			self.password = match.group(2)
			self.host = match.group(3)
			return True
		else:
			return False

	def findMode(self, channel, user):
		realUser = channel.FindNick(user.GetNick())
		if not realUser:
			return None
		return chr(realUser.GetPermChar())

	def resolveTarget(self, target):
		target = target.s
		channel = self.GetNetwork().FindChan(target)
		if channel == None:
			return (None, None)
		user = self.GetNetwork().GetIRCNick()
		return (channel, user)

	def insert(self, code, channel, host, user, ident, user_mode, date, target_user, message, network):
		try:
			with closing(pymysql.connect (host = self.host, user = self.username, passwd = self.password, db = "irclogs", use_unicode=True, charset='utf8mb4')) as conn:
				with closing(conn.cursor()) as cursor:
					sql = "INSERT INTO channel_log (code, channel, host, user, ident, user_mode, date, target_user, message, network) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					if message is not None:
						message = message.encode('utf-8').decode('utf-8', 'replace')
					cursor.execute (sql, [code, channel[1:], host, user, ident, user_mode, date.isoformat(), target_user, message, network])
		except Exception as e:
			self.PutModule("Could not save {0} to database caused by: {1} {2}".format(code, type(e), str(e)))

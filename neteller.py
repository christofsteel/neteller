#!/usr/bin/env python
import http.cookiejar
import urllib
import argparse
import getpass
from pyquery import PyQuery as pq

class NetellerRequest:
	def __init__(self):
		self.cookiejar = http.cookiejar.CookieJar()
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookiejar))
		loginpage = pq(url="https://member.neteller.com", opener=self.opener.open)
		self.securityToken = loginpage("#loginForm #securityToken").attr('value')
		self.secureId = ""

	def login(self, user, password):
		params = urllib.parse.urlencode({'accountId': user, 'password': password, 'securityToken': self.securityToken}, )
		return self.opener.open("https://member.neteller.com/session/create", params.encode('utf-8'))

	def getBalance(self):
		startpage = pq(url = "https://member.neteller.com/account", opener=self.opener.open)
		return startpage(".balance-yes").text()

	def getCreditCard(self):
		if not self.secureId:
			self.secureId = getpass.getpass("Security ID: ")
		params = urllib.parse.urlencode({"secureId": self.secureId, 'securityToken': nr.securityToken}).encode("utf-8")
		resp = self.opener.open("https://member.neteller.com/virtualCardPlus/generateCard", params)
		html = resp.read()
		phtml = pq(html)
		cc = phtml('.vdc-cc').text()
		cvv = phtml('.vdc-cvv').text()
		expires = phtml('.vdc-expiry').text()
		return cc + " " + cvv + " " + expires



if __name__ == "__main__":
	nr = NetellerRequest()
	user = input("Username: ")
	password = getpass.getpass()
	nr.login(user, password)
	print(nr.getBalance())
	print(nr.getCreditCard())

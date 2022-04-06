import requests
import re
import time
import threading
import json
from multiprocessing import Queue
from bs4 import BeautifulSoup as bs

class FreeProxy:
	def __init__(self):
		self.refresh_time = 600
		self.squeue = Queue(1000)
		self.get_proxy_list()

	def clear_list(self):
		try:
			while True:
				proxy = self.squeue.get_nowait()
		except:
			pass

	def get_proxy_list(self):
		self.clear_list()
		page = requests.get("https://free-proxy-list.net/")
		soup = bs(page.text, "html.parser")
		elements = soup.select('textarea.form-control')
		ips1 = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', elements[0].text)

		page = requests.get("https://www.us-proxy.org/")
		soup = bs(page.text, "html.parser")
		elements = soup.select('textarea.form-control')
		ips2 = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', elements[0].text)

		page = requests.get(
			"https://proxylist.geonode.com/api/proxy-list?limit=1000&page=1&sort_by=lastChecked&sort_type=desc")
		json_object = json.loads(page.text)
		ips3 = []
		for j in json_object['data']:
			ip = "{}:{}".format(j['ip'], j['port'])
			ips3.append(ip)

		merged_list = list(set(ips1 + ips2 + ips3))
		print(" ---------- ")
		print(len(merged_list))
		try:
			for p in merged_list:
				self.squeue.put_nowait(p)
		except:
			pass

		print('---refresh proxy list---')
		threading.Timer(self.refresh_time, self.get_proxy_list).start()

	def get_next_proxy(self):
		proxy = ''
		while True:
			try:
				proxy = self.squeue.get_nowait()
				break
			except:
				time.sleep(0.005)
				continue
		return proxy


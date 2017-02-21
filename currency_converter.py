from bs4 import BeautifulSoup
import logging
import urllib2

class CurrencyConverter:

	def __init__(self):
		self.url = "http://www.bna.com.ar/"
	# 	self.supported_conversions = {'USD':['ARS'], 'ARS':['USD']}

	# def convert(self, origin_curreny, destination_currency, amount):
	# 	if (origin_currency in self.supported_conversions):
	# 		if (destination_currency in self.supported_conversions[origin_currency]):
	# 			ratio = self.ratio_to_ars()
	# 			return amount
		
	def convert_to_ars(self, amount):
		ratio = self.ratio_to_ars()
		return [(amount * ratio), ratio]

	def ratio_to_ars(self):
		logging.info("Making request to " + self.url)
		response = urllib2.urlopen(self.url)
		soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
		return float(soup.find("table", class_ = 'table cotizacion').find('td', class_ = 'tit').parent.findChildren()[-1].text.replace(",","."))
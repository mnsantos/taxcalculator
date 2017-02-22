from bs4 import BeautifulSoup
import logging
import urllib2
import datetime

class CurrencyConverter:

  def __init__(self):
    self.url = "http://www.bna.com.ar/"
    self.ratios = dict()
    self.ratios[datetime.date(2017,2,21)] = 15.8
  #   self.supported_conversions = {'USD':['ARS'], 'ARS':['USD']}

  # def convert(self, origin_curreny, destination_currency, amount):
  #   if (origin_currency in self.supported_conversions):
  #     if (destination_currency in self.supported_conversions[origin_currency]):
  #       ratio = self.ratio_to_ars()
  #       return amount
    
  def convert_to_ars(self, amount, date):
    today = datetime.datetime.now()
    if date in self.ratios:
      ratio = self.ratios[date]
    else:
      if date < today.date():
        raise Exception("No se encuentra cotizacion para " + str(date))
      elif date == today:
        ratio = self.ratio_usd_to_ars()
        self.ratios[date] = ratio
    return [(amount * ratio), ratio]

  def ratio_usd_to_ars(self):
    logging.info("Making request to " + self.url)
    response = urllib2.urlopen(self.url)
    soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
    return float(soup.find("table", class_ = 'table cotizacion').find('td', class_ = 'tit').parent.findChildren()[-1].text.replace(",","."))
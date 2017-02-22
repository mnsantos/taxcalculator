from bs4 import BeautifulSoup
import logging
import urllib2
import datetime
import logging

logger = logging.getLogger(__name__)

class CurrencyConverter:

  def __init__(self, ratios):
    self.url = "http://www.bna.com.ar/"
    self.ratios = ratios
    
  def convert_to_ars(self, amount, date):
    logger.info("Buscando cotizacion para el dia " + str(date))
    today = datetime.datetime.now()
    if date in self.ratios:
      ratio = self.ratios[date]
    else:
      if date < today.date():
        raise Exception("No se encuentra cotizacion para " + str(date))
      elif date == today.date():
        ratio = self.ratio_usd_to_ars()
        self.ratios[date] = ratio
    return [(amount * ratio), ratio]

  def ratio_usd_to_ars(self):
    logging.info("Buscando cotizacion en la pagina del banco nacion...")
    response = urllib2.urlopen(self.url)
    soup = BeautifulSoup(response, 'html.parser', from_encoding="utf-8")
    return float(soup.find("table", class_ = 'table cotizacion').find('td', class_ = 'tit').parent.findChildren()[-1].text.replace(",","."))
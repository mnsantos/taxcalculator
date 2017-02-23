import logging
from currency_converter import CurrencyConverter
import datetime
from datetime import timedelta

class Calculator:

  def __init__(self, currency_converter=CurrencyConverter(dict())):
    self.currency_converter = currency_converter

  def calculate(self, params):
    respuesta = ''
    precio_pesos = 0
    if (params.moneda == 'USD'):
      res = self.currency_converter.convert_to_ars(params.precio, params.fecha + timedelta(days=-1))
      ratio = res[1]
      precio_pesos = res[0]
      respuesta = respuesta + 'Cotizacion utilizada: ' + str(ratio) + '. Monto en pesos: $' + str(precio_pesos) +'\n'
    else:
      precio_pesos = params.precio
    if params.iti:
      if params.reemplazo:
        respuesta = respuesta + 'NO paga ITI ya que hace uso de reemplazo.\n'
      else:
        respuesta = respuesta + 'Paga ITI ya que NO hace uso de reemplazo. Monto: $' + str(precio_pesos * 0.015) + ' (1.5% de ' + str(precio_pesos) + ').\n'
      respuesta = respuesta + 'NO paga IG.\n'
    else:
      respuesta = respuesta + 'NO paga ITI.\n'
      if params.ganancias:
        if params.vf > precio_pesos:
          respuesta = respuesta + 'Paga IG. Monto: $' + str(params.vf * 0.03) + ' (3% de ' + str(params.vf) + ' (VF)).\n'
        else:
          respuesta = respuesta + 'Paga IG. Monto: $' + str(precio_pesos * 0.03) + ' (3% de ' + str(precio_pesos) + ').\n'
      else:
        respuesta = respuesta + 'NO paga IG.\n'
    if params.otra_propiedad:
      if precio_pesos >= params.vf and precio_pesos >= params.vir:
        respuesta = respuesta + 'Paga SELLOS. Monto: $' + str(precio_pesos * 0.036) + ' (3.6% de ' + str(precio_pesos) + ').\n'
      elif params.vf >= precio_pesos and params.vf >= params.vir:
        respuesta = respuesta + 'Paga SELLOS. Monto: $' + str(params.vf * 0.036) + ' (3.6% de ' + str(params.vf) + ' (VF)).\n'
      else:
        respuesta = respuesta + 'Paga SELLOS. Monto: $' + str(params.vir * 0.036) + ' (3.6% de ' + str(params.vir) + ' (VIR)).\n'        
    else:
      if precio_pesos < 975000:
        respuesta = respuesta + 'NO Paga SELLOS dado que no supera $' + str(975000) + '.\n'
      else:
        if precio_pesos >= params.vf and precio_pesos >= params.vir:
          respuesta = respuesta + 'Paga SELLOS. Monto: $' + str((precio_pesos - 975000) * 0.036) + ' (3.6% de ' + str(precio_pesos) + ' - 975000).\n'
        elif params.vf >= precio_pesos and params.vf >= params.vir:
          respuesta = respuesta + 'Paga SELLOS. Monto: $' + str((params.vf - 975000) * 0.036) + ' (3.6% de ' + str(params.vf) + ' (VF) - 975000).\n'
        else:
          respuesta = respuesta + 'Paga SELLOS. Monto: $' + str((params.vir - 975000) * 0.036) + ' (3.6% de ' + str(params.vir) + ' (VIR) - 975000).\n'   
    return respuesta

  def can_calculate(self, params):
    date = params.fecha
    today = datetime.datetime.now()
    tomorrow = today.date() + timedelta(days=1)
    if params.moneda == 'ARS' or date < tomorrow or (date == tomorrow and today.hour > 15):
      return True
    else:
      return False
          



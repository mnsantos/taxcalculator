import logging
from currency_converter import CurrencyConverter

class Calculator:

	def __init__(self):
		self.MONTO_FIJO = 975000
		self.currency_converter = CurrencyConverter()

	def calculate(self, params):
		respuesta = ''
		precio_vf_vir = params.sello_tax
		precio_pesos = 0
		if (params.moneda == 'USD'):
			res = self.currency_converter.convert_to_ars(params.precio)
			ratio = res[1]
			precio_pesos = res[0]
			respuesta = respuesta + 'Cotizacion utilizada: ' + str(ratio) + ' (' + str(params.fecha) + '). Monto en pesos: $' + str(precio_pesos) +'\n'
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
				respuesta = respuesta + 'Paga IG. Monto: $' + str(precio_pesos * 0.03) + ' (3% de ' + str(precio_pesos) + ').\n'
			else:
				##ACA que hacemos??
				respuesta = respuesta + 'NO paga IG.\n'
		if params.otraPropiedad:
			if precio_pesos > precio_vf_vir:
				respuesta = respuesta + 'Paga SELLOS. Monto: $' + str(precio_pesos * 0.036) + ' (3.6% de ' + str(precio_pesos) + ').\n'
			else:
				respuesta = respuesta + 'Paga SELLOS. Monto: $' + str(precio_vf_vir * 0.036) + ' (3.6% de ' + str(precio_vf_vir) + ').\n'
		else:
			if precio_pesos < self.MONTO_FIJO:
				respuesta = respuesta + 'NO Paga SELLOS. dado que no supera $' + str(self.MONTO_FIJO) + '.\n'
			else:
				monto_respuesta = ''
				monto = precio_vf_vir - self.MONTO_FIJO
				monto_respuesta = monto_respuesta + 'Monto: $' + str(monto * 0.036) + ' (3.6% de VF/VIR - ' + str(self.MONTO_FIJO) + ')'
				respuesta = respuesta + 'Paga SELLOS. ' + monto_respuesta
		return respuesta



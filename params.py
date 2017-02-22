class Params:

  def __init__(self):
    self.ig = False
    self.iti = False
    self.reemplazo = False
    self.otraPropiedad = False
    self.ganancias = False
    self.moneda = ''
    self.precio = 0
    self.fecha = ''
    self.tipo = ''
    self.sello_tax = 0
    self.id = 0
    self.chat_id = 0

  def __repr__(self):
    return 'ig: ' + str(self.ig) + \
    ', iti: ' + str(self.iti) + \
    ', reemplazo: ' + str(self.reemplazo) + \
    ', otraPropiedad: ' + str(self.otraPropiedad) + \
    ', ganancias: ' + str(self.ganancias) + \
    ', moneda: ' + str(self.moneda) + \
    ', precio: ' + str(self.precio) + \
    ', fecha: ' + str(self.fecha) + \
    ', VIR/VF: ' + str(self.sello_tax) + \
    ', tipo: ' + str(self.tipo) + \
    ', id: ' + str(self.id) + \
    ', chat_id: ' + str(self.chat_id)
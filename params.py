class Params:

  def __init__(self):
    self.iti = False
    self.reemplazo = False
    self.otra_propiedad = False
    self.ganancias = False
    self.moneda = ''
    self.precio = 0
    self.fecha = ''
    self.tipo = ''
    self.vir = 0
    self.vf = 0
    self.id = 0
    self.chat_id = 0

  def __repr__(self):
    return ', iti: ' + str(self.iti) + \
    ', reemplazo: ' + str(self.reemplazo) + \
    ', otra_propiedad: ' + str(self.otra_propiedad) + \
    ', ganancias: ' + str(self.ganancias) + \
    ', moneda: ' + str(self.moneda) + \
    ', precio: ' + str(self.precio) + \
    ', fecha: ' + str(self.fecha) + \
    ', VIR: ' + str(self.vir) + \
    ', VF: ' + str(self.vf) + \
    ', tipo: ' + str(self.tipo) + \
    ', id: ' + str(self.id) + \
    ', chat_id: ' + str(self.chat_id)
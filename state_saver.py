import pickle
import logging

class StateSaver:

  def __init__(self):
    self.data_path = 'data.pickle'
    self.ids_path = 'ids.pickle'
    self.ratios_path = 'ratios_file.pickle'

  def save(self, data, ids, ratios):
    with open(self.data_path, 'wb') as data_file:
      pickle.dump(data, data_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(self.ids_path, 'wb') as ids_file:
      pickle.dump(ids, ids_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(self.ratios_path, 'wb') as ratios_file:
      pickle.dump(ratios, ratios_file, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('data.pickle', 'wb') as data_file:
    #   pickle.dump(data, data, protocol=pickle.HIGHEST_PROTOCOL)

  def load(self):
    with open(self.data_path, 'rb') as data_file:
      data = pickle.load(data_file)
    with open(self.ids_path, 'rb') as ids_file:
      ids = pickle.load(ids_file)
    with open(self.ratios_path, 'rb') as ratios_file:
      ratios = pickle.load(ratios_file)
    return data, ids, ratios
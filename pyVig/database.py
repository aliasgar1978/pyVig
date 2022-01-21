


import pandas as pd



class Data():
	def __init__(self, data_file):
		self.data_file = data_file

	def read(self, sheet_name):
		self.df = pd.read_excel(self.data_file, sheet_name=sheet_name).fillna("")

class DeviceData(Data):

	def add_description(self):
		cols = (self.df.ip_address, self.df.device_model, self.df.serial_number)
		self.df['description'] = self.df.hostname
		for col in cols:
			self.df.description += "\n"+col


class CableMatrixData(Data):
	pass


# DD = DeviceData(data_file)
# DD.read("Devices")
# DD.add_description()
# # print(DD.df)

# CMD = CableMatrixData(data_file)
# CMD.read("CableMatrix")
# print(CMD.df)

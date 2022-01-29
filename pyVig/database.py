

import pandas as pd
from math import tanh, degrees

from pyVig.maths import df_with_slops_and_angles
from pyVig.static import REMARKS_COLUMNS_TO_MERGE

class Data():
	def __init__(self, data_file):
		self.data_file = data_file

	def read(self, sheet_name):
		self.df = pd.read_excel(self.data_file, sheet_name=sheet_name).fillna("")



class DeviceData(Data):

	def add_description(self):
		cols = [ self.df[x] for x in REMARKS_COLUMNS_TO_MERGE]
		# cols = (self.df.ip_address, self.df.device_model, self.df.serial_number)
		self.df['description'] = self.df.hostname
		for col in cols:
			self.df.description += "\n"+col




def merged_df_on_hostname(devices_df, cablemtx_df, hostname_col_hdr, sortby):
	cablemtx_df['hostname'] = cablemtx_df[hostname_col_hdr]
	cablemtx_df = cablemtx_df.reset_index()
	return pd.merge(cablemtx_df, devices_df, 
		on=["hostname",], 
		sort="False", 
		).fillna("").sort_values(sortby)

class CableMatrixData(Data):

	def filter_eligible_cables_only(self):
		self.df = self.df[ self.df.include == "y"]

	def calc_slop(self, DD):
		dev_df = DD.df.reset_index()
		df2a = merged_df_on_hostname(dev_df, self.df, 'dev_a', 'index_x')
		df2b = merged_df_on_hostname(dev_df, self.df, 'dev_b', 'index_y')
		mdf = pd.merge(df2a, df2b, on=["dev_a", "dev_b"])
		mdf = mdf[mdf.index_x_x==mdf.index_x_y]		
		self.df = df_with_slops_and_angles(mdf, 'y_x', 'y_y', 'x_x', 'x_y')



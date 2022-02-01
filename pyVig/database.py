
# -----------------------------------------------------------------------------------
import pandas as pd
from math import tanh, degrees

from pyVig.maths import df_with_slops_and_angles
# -----------------------------------------------------------------------------------

class Data():
	def __init__(self, data_file):
		self.data_file = data_file

	def read(self, sheet_name):
		self.df = pd.read_excel(self.data_file, sheet_name=sheet_name).fillna("")


# -----------------------------------------------------------------------------------

def add_description(description, col_desc):
	if col_desc.empty:
		description += col_desc  
	return description

class DeviceData(Data):

	def add_description(self, columns_to_merge):
		cols = [ self.df[x] for x in columns_to_merge]
		# cols = (self.df.ip_address, self.df.device_model, self.df.serial_number)
		self.df['description'] = self.df.hostname
		for col in cols:
			if col.empty: continue
			# self.df['description'].apply(add_description, col)
			self.df.description += "\n"+col

	def plane_coordinate_columns(self, x=None, y=None):
		if x:
			try:
				self.df["x"] = self.df[x]
			except:
				raise ValueError("Undefined x-column")
		if y:
			try:
				self.df["y"] = self.df[y]
			except:
				raise ValueError("Undefined y-column")

# -----------------------------------------------------------------------------------

def merged_df_on_hostname(devices_df, cablemtx_df, hostname_col_hdr, sortby):
	cablemtx_df['hostname'] = cablemtx_df[hostname_col_hdr]
	cablemtx_df = cablemtx_df.reset_index()
	return pd.merge(cablemtx_df, devices_df, 
		on=["hostname",], 
		sort="False", 
		).fillna("").sort_values(sortby)

# -----------------------------------------------------------------------------------
class CableMatrixData(Data):

	def filter_eligible_cables_only(self):
		if "include" in self.df.columns:
			self.df = self.df[ self.df.include == "y"]

	def calc_slop(self, DD):
		dev_df = DD.df.reset_index()
		df2a = merged_df_on_hostname(dev_df, self.df, 'dev_a', 'index_x')
		df2b = merged_df_on_hostname(dev_df, self.df, 'dev_b', 'index_y')
		mdf = pd.merge(df2a, df2b, on=["dev_a", "dev_b"])
		mdf = mdf[mdf.index_x_x==mdf.index_x_y]		
		self.df = df_with_slops_and_angles(mdf, 'y_x', 'y_y', 'x_x', 'x_y')

	def filter(self, **kwargs):
		for k, v in kwargs.items():
			self.df = self.df[self.df[k] == v]


# -----------------------------------------------------------------------------------


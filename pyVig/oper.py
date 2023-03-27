
import pandas as pd
import nettoolkit as nt
from .devices import AdevDevices, device_df_drop_empty_duplicates, update_var_df_details_to_table_df
from .cablings import ADevCablings
from .maths import CalculateXY
from .general import *

# --------------------------------------------- 
# Data Frame Generator
# --------------------------------------------- 
class DFGen():

	def __init__(self, files):
		self.files = files
		self.default_stencil = None
		self.default_x_spacing = 3.5
		self.default_y_spacing = 2
		self.line_pattern_style_separation_on = None
		self.line_pattern_style_shift_no = 2
		self.func_dict = {}
		self.var_func_dict = {}
		self.blank_dfs()

	def blank_dfs(self):
		self.devices_merged_df = pd.DataFrame({'hostname':[]})
		self.cabling_merged_df = pd.DataFrame({'a_device':[]})

	def update_attributes(self, **kwargs):
		for k, v in kwargs.items():
			if v:
				self.__dict__[k] = v

	def update_functions(self, **kwargs):
		for k, v in kwargs.items():
			self.func_dict[k] = v

	def update_var_functions(self, **kwargs):
		for k, v in kwargs.items():
			self.var_func_dict[k] = v

	def iterate_over_files(self):
		self.DCT = {}
		for file in self.files:
			DCT = DF_ConverT(file, self.default_stencil, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
			DCT.get_self_details(self.var_func_dict)
			DCT.convert(self.func_dict)
			self.update_devices_df(DCT, file)
			self.update_cabling_df(DCT, file)
			self.DCT[DCT.hostname] = DCT

		self.devices_merged_df = device_df_drop_empty_duplicates(self.devices_merged_df)
		self.devices_merged_df = update_var_df_details_to_table_df(self.devices_merged_df, self.DCT, self.var_func_dict)
		self.calculate_cordinates()

	def update_devices_df(self, DCT, file):
		ddf = DCT.update_devices()
		#
		# ddf_dev = DCT.update_device_self_detils(self.func_dict)
		# ddf = pd.concat([ddf, ddf_dev], axis=0, join='outer')
		#
		self.devices_merged_df = pd.concat([self.devices_merged_df, ddf], axis=0, join='outer')

	def update_cabling_df(self, DCT, file):
		cdf = DCT.update_cablings(**self.__dict__)
		#
		self.cabling_merged_df = pd.concat([self.cabling_merged_df, cdf], axis=0, join='outer')

	def calculate_cordinates(self):
		CXY = CalculateXY(self.devices_merged_df, self.default_x_spacing, self.default_y_spacing)
		CXY.calc()
		self.df_dict = {'Devices': CXY.df, 'Cablings': self.cabling_merged_df }



# --------------------------------------------- 
# Data Frame Converter
# --------------------------------------------- 
class DF_ConverT():

	def __init__(self, file, 
		default_stencil, 
		line_pattern_style_separation_on, 
		line_pattern_style_shift_no,
		):
		self.file = file
		self.full_df = nt.read_xl(file)
		file = file.split("/")[-1].split("\\")[-1]
		# self.hierarchical_order = get_hierarchical_order(file)
		# self.device_type = get_sw_type(file)
		self.self_device = file.split("-clean")[0].split(".")[0]
		#
		self.stencils = default_stencil
		self.line_pattern_style_separation_on = line_pattern_style_separation_on
		self.line_pattern_style_shift_no = line_pattern_style_shift_no


	def get_self_details(self, var_func_dict):
		self.var_func_dict = var_func_dict
		for k,  f in var_func_dict.items():
			v = f(self.full_df['var'])
			if not v: v = 'N/A'
			self.__dict__[k] = v

	def convert(self, func_dict):

		# vlan
		vlan_df = get_vlan_if_up(self.full_df['vlan'])
		vlan_df = get_vlan_if_relevants(vlan_df)
		self.vlan_df = vlan_df

		# physical
		df = get_physical_if_up(self.full_df['physical'])
		df = get_physical_if_relevants(df)
		#
		df = self.update_devices_df_pattern_n_custom_func(df, func_dict)
		#
		self.u_ph_df = df


	def update_devices_df_pattern_n_custom_func(self, df, func_dict, test=False):
		for k, f in func_dict.items():
			df[k] = f(df)
		#
		self.patterns = get_patterns(df, self.line_pattern_style_separation_on, self.line_pattern_style_shift_no)
		df = update_pattern(df, self.patterns, self.line_pattern_style_separation_on)
		#
		return df


	def update_cablings(self, **default_dic):
		self.C = ADevCablings(self.self_device, **default_dic)
		for k, v in self.u_ph_df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.C.add_to_cablings(**kwargs)
		df = self.C.cabling_dataframe()
		return df

	def update_devices(self):
		self.D = AdevDevices(self.stencils, self.var_func_dict, self.full_df['var'])
		self.D.int_df = self.update_devices_for(df=self.u_ph_df, dic=self.D.devices)
		self.D.add_vlan_info(self.vlan_df)
		return self.D.merged_df

	def update_device_self_detils(self, func_dict):
		self_device_df = self.D.get_self_device_df()
		self_dev_df = self.update_devices_for(df=self_device_df, dic=self.D.self_device)
		self_dev_df = self.update_devices_df_pattern_n_custom_func(self_dev_df, func_dict, True)
		return self_dev_df

	def update_devices_for(self, df, dic):

		for k, v in df.iterrows():
			kwargs = {}
			for x, y in v.items():
				kwargs[x] = y
			self.D.add_to_devices(what=dic, **kwargs)

		u_df = device_df_drop_empty_duplicates(dic)
		return u_df



# --------------------------------------------- 

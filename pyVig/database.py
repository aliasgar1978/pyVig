"""database activities"""

# -----------------------------------------------------------------------------------
import pandas as pd

from pyVig.maths import df_with_slops_and_angles
from .general import *

# -----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------

class Data():
	'''
	Parent class defining device and connectors.
	'''

	def __init__(self, **kwargs):
		"""Initialize the object

		Args:
			data_file (str): file name of excel database containing devices and cabling details.
		"""		
		self.kwargs = kwargs
		self.data_file = kwargs['data_file']
		self.read(self.sheet_name)

	def add_kwargs_attributes(self):
		for k, v in self.kwargs.items():
			self.add_attribute(k, v)

	def add_optional_columnnames_attributes(self):
		for k, v in self.optional_columns.items():
			self.add_attribute(k, v)

	def add_attribute(self, attr_name, attr_value):
		if attr_name:
			self.__dict__[attr_name] = attr_value

	def read(self, sheet_name):
		"""read data from given excel sheet and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		self.df = pd.read_excel(self.data_file, sheet_name=sheet_name).fillna("")


# -----------------------------------------------------------------------------------


class DeviceData(Data):
	"""Devices Data Object Building
	"""		
	format_columns = {	'iconWidth': 2.5, 
						'iconHeight': 1,
	}

	optional_columns = {'stencil': DEFAULT_STENCIL,
						'item': None,
	}
	x = 'x-axis'
	y = 'y-axis'
	default_stencil = None
	sheet_name = 'Devices'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_format_columnnames_attributes()
		self.add_optional_columnnames_attributes()
		self.add_kwargs_attributes()

	def add_format_columnnames_attributes(self):
		for k, v in self.format_columns.items():
			self.add_attribute(k, v)

	def read(self, sheet_name):
		"""read data from given excel sheet containing device data and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		super().read(sheet_name)


	def add_description(self, columns_to_merge):
		"""add a description column to dataframe, which will be output of merged data of provided columns

		Args:
			columns_to_merge (iterable): provide list/set/tuple of column names to be merged in a single
			description column.

		Raises:
			ValueError: Raises error if Mandtory hostname column is missing.
		"""		
		cols = []
		for x in columns_to_merge:
			try:
				cols.append(self.df[x])
			except:
				print(f"column `{x}` is missing in input file")
		try:
			self.df['description'] = self.df.hostname
		except:
			raise ValueError("Missing mandatory column `hostname` ")

		for col in cols:
			if col.empty:  continue
			self.df.description += "\n"+ col.str.strip().fillna("invalid datatype")


# -----------------------------------------------------------------------------------

def merged_df_on_hostname(devices_df, cablemtx_df, hostname_col_hdr, sortby):
	"""merge two dataframes by matching hostname column

	Args:
		devices_df (DataFrame): Devices details dataframe
		cablemtx_df (DataFrame): Cabling details dataframe
		hostname_col_hdr (str): column name of hostname from cabling dataframe to be merge with
		sortby (str): adhoc column name on which data to be sorted

	Raises:
		ValueError: Raise Exception if hostname column missing.

	Returns:
		DataFrame: merged DataFrame
	"""		
	try:
		cablemtx_df['hostname'] = cablemtx_df[hostname_col_hdr]
	except:
		raise ValueError(f"Missing mandatory column `{hostname_col_hdr}`")
	cablemtx_df = cablemtx_df.reset_index()
	return pd.merge(cablemtx_df, devices_df, 
		on=["hostname",], 
		sort="False", 
		).fillna("").sort_values(sortby)

# -----------------------------------------------------------------------------------
class CableMatrixData(Data):
	"""Cabling Data Object Building
	"""		

	optional_columns = {'connector_type': DEFAULT_CONNECTOR_TYPE,
						'color': DEFAULT_LINE_COLOR,
						'weight': DEFAULT_LINE_WT,
						'pattern': DEFAULT_LINE_PATTERN,
						# 'angle': "straight",
						'aport': "",
	}
	dev_a = 'a_device'
	dev_b = 'b_device'
	sheet_name = 'Cablings'

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.add_optional_columnnames_attributes()
		self.add_kwargs_attributes()

	def read(self, sheet_name):
		"""read data from given excel sheet containing cabling data and set dataframe for the object.

		Args:
			sheet_name (str): Excel sheet name
		"""		
		super().read(sheet_name)


	# optional
	def filter_eligible_cables_only(self):
		"""optional filter: filters DataFrame for the column `include` with values as `y`
		"""				
		if "include" in self.df.columns:
			self.df = self.df[ self.df.include == "y"]

	# optional
	def filter(self, **kwargs):
		"""filter the dataframe for given column:value
		multiple kwargs act as 'and' operation.
		"""		
		for k, v in kwargs.items():
			self.df = self.df[self.df[k] == v]

	# mandatory
	def calc_slop(self, DD):
		"""calculate the slop and angle of the two end points and add it in respective column
		in dataframe.

		Args:
			DD (DeviceData): DeviceData object
		"""		
		dev_df = DD.df.reset_index()
		df2a = merged_df_on_hostname(dev_df, self.df, self.dev_a, 'index_x')
		df2b = merged_df_on_hostname(dev_df, self.df, self.dev_b, 'index_y')
		mdf = pd.merge(df2a, df2b, on=[self.dev_a, self.dev_b])
		mdf = mdf[mdf.index_x_x==mdf.index_x_y]		
		yx = DD.y + "_x"
		yy = DD.y + "_y"
		xx = DD.x + "_x"
		xy = DD.x + "_y"
		self.df = df_with_slops_and_angles(mdf, yx, yy, xx, xy)


# -----------------------------------------------------------------------------------


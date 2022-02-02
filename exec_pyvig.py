
# -----------------------------------------------------------------------------------
import os

from pyVig.stencils import get_list_of_stencils
from pyVig.database import DeviceData, CableMatrixData
from pyVig.entities import ItemObjects, Connectors
from pyVig.visio import VisioObject

# -----------------------------------------------------------------------------------

# --------------------  Static inputs  -------------------- #
stencil_folder = "C:/Users/al202t/Desktop/Short-Cuts/04.     #~~~ IGA-PJT ~~~#/01. - OWN Projects/IGA/100. Help Docs/Stencil/"
op_file = "output.vsdx"

COLUMNS_TO_BE_MERGED_WITH_HOSTNAME = [
	'device_model',
	'serial_number',
	'ip_address',
	'blg_hubroom',
	# 'rack_details',

	# update and/or add More as needed.
	# re-order them as required in output.
]

######## Multiple test databases #########
data_file = 'data/data.xlsx'
# data_file = "data/data - MTP - IBM.xlsx"
# data_file = "data/data - MTP - KYN.xlsx"

# -----------------------------------------------------------------------------------
#  Executions
# -----------------------------------------------------------------------------------

#---------------------------
# device database operations
#---------------------------
devices_data = DeviceData(
	data_file,
	sheet_name="Devices",
	x="x-axis",
	y="y-axis",
	# stencil_colname="stencils",
	device_type_colname="device_type",
	default_stencil="Network and Peripherals",
	)

# // Device Description containing columns //
devices_data.add_description(COLUMNS_TO_BE_MERGED_WITH_HOSTNAME)

#---------------------------------
# cabling database operations
#---------------------------------

### Initialize/Create CM_DATA object
cable_matrix_data = CableMatrixData(
	data_file,									# mandatory: file name (with full path)
	sheet_name="Cablings",						# mandatory: tab/sheet name
	a_device_colname="a_device",				# mandatory: a side device of cable
	b_device_colname="b_device",				# mandatory: b side device of cable
	a_device_port_colname="a_device_port",
	connector_type_colname="connector_type",
	cable_color_colname="color",
	cable_weight_colname="weight",
	cable_line_pattern_colname="pattern",
	)

### [Optional] data filter mechanism
# cable_matrix_data.filter_eligible_cables_only()	# Apply filter for 'include' column containing 'x'
# cable_matrix_data.filter(draw_type="x")	# Apply if to filter a particular column=records

### [Mandatory] method to be executed to get the connector slop/angles
cable_matrix_data.calc_slop(devices_data)		# calculate cable slop/angle

# -----------------------------------------------------------------------------------

#------------------------
# visio app operations
#------------------------
stencils = get_list_of_stencils(
	folder=stencil_folder, 
	devices_data=devices_data,
	)

with VisioObject(stencils=stencils, outputFile=op_file) as v:
	print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
	# ----------------------------------------------------------------------------------
	print("Dropping Devices...")
	item_objects = ItemObjects(v, devices_data, cable_matrix_data, filterOnCables=False)
	# ----------------------------------------------------------------------------------
	print("Connecting Devices...")
	Connectors(cable_matrix_data, item_objects)
	# ----------------------------------------------------------------------------------
	print("Resizing Page...")
	v.fit_to_draw(item_objects.page_height, item_objects.page_width)
	# ----------------------------------------------------------------------------------
	print("Finished with drawing, Save the file as necessary.")
# -----------------------------------------------------------------------------------

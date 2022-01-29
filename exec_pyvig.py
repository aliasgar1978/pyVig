
# -----------------------------------------------------------------------------------
import os

from pyVig.stencils import get_list_of_stencils
from pyVig.database import DeviceData, CableMatrixData
from pyVig import VisioObject, ItemObjects, Connectors

# -----------------------------------------------------------------------------------

# Static inputs
stencil_folder = os.path.abspath(os.getcwd()) + "\\pyVig\\stencils\\"
op_file = "output.vsdx"
stencil_icons_dict = {
	'L3_SW': "Master.35",
	'L2_SW': "Master.38",
	'ROUTER': "Master.39",
	'LINE': 'line',
	'AP': 'Wireless access point',
	'LAN': 'Ethernet',
	'SERVER': 'Server',
	'FIREWALL': 'Firewall',
	'PRINTER': 'Printer',
	'MODEM': 'Modem',
	'': None,
}

REMARKS_COLUMNS_TO_MERGE = [
	'ip_address',
	'device_model',
	'serial_number',

	# Add More as needed.
	# Resequence as required in output.
]

######## Multiple test databases #########
# data_file = 'data/data.xlsx'
# data_file = 'data/data - vod.xlsx'
data_file = "data/data - MTP.xlsx"

# -----------------------------------------------------------------------------------
#  Executions
# -----------------------------------------------------------------------------------

# database operations
devices_data = DeviceData(data_file)
devices_data.read("Devices")
devices_data.add_description(REMARKS_COLUMNS_TO_MERGE)

cable_matrix_data = CableMatrixData(data_file)
cable_matrix_data.read("CableMatrix")
cable_matrix_data.filter_eligible_cables_only()
cable_matrix_data.calc_slop(devices_data)
# -----------------------------------------------------------------------------------

# visio operations
stencils = get_list_of_stencils(stencil_folder)
with VisioObject(stencils=stencils, outputFile=op_file) as v:
	print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
	#
	print("Dropping Devices...")
	devices_details = (dev for i, dev in devices_data.df.iterrows())
	item_objects = ItemObjects(v, stencil_icons_dict, devices_details, cable_matrix_data.df)
	#
	print("Connecting Devices...")
	connectors = (connector for i, connector in cable_matrix_data.df.iterrows())
	Connectors(connectors, item_objects)
	#
	print("Resizing Page...")
	v.fit_to_draw(item_objects.page_height, item_objects.page_width)
	#
	print("Finished with drawing, Save the file as necessary.")

# -----------------------------------------------------------------------------------

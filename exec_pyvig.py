# -----------------------------------------------------------------------------------
import os

from pyVig.stencils import get_list_of_stencils
from pyVig.database import DeviceData, CableMatrixData
from pyVig.entities import ItemObjects, Connectors
from pyVig.visio import VisioObject

# -----------------------------------------------------------------------------------

# Static inputs
# stencil_folder = os.path.abspath(os.getcwd()) + "\\pyVig\\stencils\\"
stencil_folder = "C:\\Users\\al202t\\Desktop\\Short-Cuts\\04.     #~~~ IGA-PJT ~~~#\\01. - OWN Projects\\IGA\\100. Help Docs\\Stencil\\"
op_file = "output.vsdx"

REMARKS_COLUMNS_TO_MERGE = [
	'device_model',
	# 'ip_address',
	# 'serial_number',
	# 'blg_hubroom',
	# 'rack_details',

	# Add More as needed.
	# Resequence as required in output.
]

######## Multiple test databases #########
data_file = 'data/data.xlsx'
# data_file = 'data/data - vod.xlsx'
# data_file = "data/data - MTP.xlsx"
# data_file = "data/data - MTP - KYN.xlsx"

# -----------------------------------------------------------------------------------
#  Executions
# -----------------------------------------------------------------------------------

#---------------------------
# device database operations
#---------------------------
devices_data = DeviceData(data_file)
devices_data.read("Devices")				# 'Devices' is tab on Excel file
devices_data.plane_coordinate_columns(		# decide the x,y column names
	x="x", 
	y="y")	 
devices_data.add_description(REMARKS_COLUMNS_TO_MERGE)	# Device Description containing columns

#---------------------------------
# cable-matrix database operations
#---------------------------------
cable_matrix_data = CableMatrixData(data_file)
cable_matrix_data.read("CableMatrix")		# 'CableMatrix' is tab on Excel file
cable_matrix_data.filter_eligible_cables_only()	# Apply filter for 'include' column containing 'x'
cable_matrix_data.filter(draw_type="core")	# Apply if to filter a particular column=records
cable_matrix_data.calc_slop(devices_data)		# calculate cable slop/angle
# -----------------------------------------------------------------------------------

#------------------------
# visio app operations
#------------------------
stencils = get_list_of_stencils(stencil_folder, devices_data)

with VisioObject(stencils=stencils, outputFile=op_file) as v:
	print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
	#
	print("Dropping Devices...")
	devices_details = (dev for i, dev in devices_data.df.iterrows())
	item_objects = ItemObjects(v, devices_details, cable_matrix_data.df)
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

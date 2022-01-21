
from visio import device, VisioObject
from static import op_file
from stencils import *
from database import DeviceData, CableMatrixData

# -----------------------------------------------------------------------------------
data_file = 'data.xlsx'

DD = DeviceData(data_file)
DD.read("Devices")
DD.add_description()

CMD = CableMatrixData(data_file)
CMD.read("CableMatrix")


stencils = get_list_of_stencils(stencil_folder)
devices = {}
with VisioObject(stencils=stencils, outputFile=op_file) as V:
	for i, dev in DD.df.iterrows():
		devices[dev.hostname] = device(
			dev.stencil, V, stencil_icons[dev.dev_type], dev.x, dev.y)
		devices[dev.hostname].description(dev.description)

	for i, dev in CMD.df.iterrows():		
		devices[dev.dev_a].connect( devices[dev.dev_b], dev.conn_type )




# -----------------------------------------------------------------------------------

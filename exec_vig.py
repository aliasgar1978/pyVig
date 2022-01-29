import os
# from pyVig.visio import device, VisioObject
# from pyVig.static import op_file
from pyVig import VisioObject, device
from pyVig.stencils import stencil_icons, get_list_of_stencils
from pyVig.database import DeviceData, CableMatrixData

stencil_folder = os.path.abspath(os.getcwd()) + "\\pyVig\\stencils\\"
op_file = "output.vsdx"
# # -----------------------------------------------------------------------------------
# data_file = 'data.xlsx'
# data_file = 'data - vod.xlsx'
data_file = "data - MTP.xlsx"

DD = DeviceData(data_file)
DD.read("Devices")
DD.add_description()

CMD = CableMatrixData(data_file)
CMD.read("CableMatrix")
CMD.filter_eligible_cables_only()
CMD.calc_slop(DD)


# # # -----------------------------------------------------------------------------------
stencils = get_list_of_stencils(stencil_folder)

devices = {}
x_coordinates= []
y_coordinates= []

with VisioObject(stencils=stencils, outputFile=op_file) as V:
	print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
	for i, dev in DD.df.iterrows():
		if not ((dev.hostname == CMD.df.dev_a).any() 
				or (dev.hostname == CMD.df.dev_b).any() ):
			continue

		x_coordinates.append(dev.x)
		y_coordinates.append(dev.y)
		stencil = dev.stencil if dev.stencil else "Network and Peripherals"
		devices[dev.hostname] = device(						# drop device
			stencil=stencil, 
			visObj=V, 
			item=stencil_icons[dev.dev_type], 
			x=dev.x, 
			y=dev.y)
		devices[dev.hostname].description(dev.description)	# description of device

	for i, connector in CMD.df.iterrows():
		if connector.dev_a and connector.dev_b:
			angle = connector.angle_straight_connector if connector.conn_type_x == "straight" else connector.angle_angled_connector 
			devices[connector.dev_a].connect(devices[connector.dev_b], 	# connect these two devices
				connector_type=connector.conn_type_x, 
				angle=angle, 
				aport=connector.dev_a_port_y,
				color=connector.color_x,
				weight=connector.weight_x,
				pattern=connector.pattern_x,
				)

	height = max(y_coordinates) - min(y_coordinates) + 2
	width = max(x_coordinates) - min(x_coordinates) + 3
	V.fit_to_draw(height, width)
	print("Finished with drawing, Save the file as necessary.")


# # # -----------------------------------------------------------------------------------

# y1,x1 = 10,1
# y11,x11 = 10,8
# y12,x12 = 1,8
# y13,x13 = 1,1

# y2,x2 = 5,5

# V = VisioObject(stencils=stencils, outputFile=op_file)
# d1 = device( "Network and Peripherals", V, stencil_icons['L3_SW'], y1,x1)
# d2 = device( "Network and Peripherals", V, stencil_icons['L3_SW'], y2,x2)
# d11 = device( "Network and Peripherals", V, stencil_icons['L3_SW'], y11,x11)
# d12 = device( "Network and Peripherals", V, stencil_icons['L3_SW'], y12,x12)
# d13 = device( "Network and Peripherals", V, stencil_icons['L3_SW'], y13,x13)

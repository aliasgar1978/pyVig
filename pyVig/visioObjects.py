
# -----------------------------------------------------------------------------------

from nettoolkit import Multi_Execution

from pyVig.visio import device

# -----------------------------------------------------------------------------------
#  Visio Objects / Items
# -----------------------------------------------------------------------------------
class ItemObjects(Multi_Execution):

	def __init__(self, 
		visObj, 
		stencil_icons_dict,
		devices_details, 
		cable_matrid_df
		):
		self.visObj = visObj
		self.stencil_icons_dict = stencil_icons_dict
		self.devices_details = devices_details
		self.cable_matrid_df = cable_matrid_df
		self.devices = {}
		self.x_coordinates = []
		self.y_coordinates = []
		super().__init__(self.devices_details)
		self.start(multi_thread=False)

	def __getitem__(self, k): return self.devices[k]

	@property
	def top_most(self): return max(self.y_coordinates)
	@property
	def bottom_most(self): return min(self.y_coordinates)
	@property
	def left_most(self): return min(self.x_coordinates)
	@property
	def right_most(self): return max(self.x_coordinates)
	@property
	def page_height(self): return self.top_most - self.bottom_most + 2
	@property
	def page_width(self): return self.right_most - self.left_most + 3
	
	def execute(self, dev):
		# filter to only drop connected devices.
		if not ((dev.hostname == self.cable_matrid_df.dev_a).any() 
				or (dev.hostname == self.cable_matrid_df.dev_b).any() ):
			return None
		# -- start drops ---
		self.x_coordinates.append(dev.x)
		self.y_coordinates.append(dev.y)
		stencil = dev.stencil if dev.stencil else "Network and Peripherals"
		self.devices[dev.hostname] = device(						# drop device
			stencil=stencil, 
			visObj=self.visObj, 
			item=self.stencil_icons_dict[dev.dev_type], 
			x=dev.x, 
			y=dev.y)
		self.devices[dev.hostname].description(dev.description)	# description of device


# -----------------------------------------------------------------------------------
#  Visio Connectors
# -----------------------------------------------------------------------------------
class Connectors(Multi_Execution):

	def __init__(self, connectors, devices):
		self.connectors = connectors
		self.devices = devices
		super().__init__(self.connectors)
		self.start(multi_thread=False)

	def execute(self, connector):
		if connector.dev_a and connector.dev_b:
			# decide text angle on line
			angle = connector.angle_straight_connector if connector.conn_type_x == "straight" else connector.angle_angled_connector 
			# connect these two devices
			self.devices[connector.dev_a].connect(self.devices[connector.dev_b],
				connector_type=connector.conn_type_x, 
				angle=angle, 
				aport=connector.dev_a_port_y,
				color=connector.color_x,
				weight=connector.weight_x,
				pattern=connector.pattern_x,
			)

# -----------------------------------------------------------------------------------

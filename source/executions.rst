CLI Execution Instructions
===========================

pyVig package
--------------

.. automodule:: pyVig
   :members:
   :undoc-members:
   :show-inheritance:


Execution steps
---------------------------

Import necessary modules::

	import os
	from copy import deepcopy
	from pyVig.stencils import get_list_of_stencils
	from pyVig.database import DeviceData, CableMatrixData
	from pyVig.entities import ItemObjects, Connectors
	from pyVig.visio import VisioObject




Cabling database operations function::

	def cabling_data_operations(dic):
		cable_matrix_data = CableMatrixData(
			dic['data_file'],		# mandatory: file name (with full path)
			sheet_name=dic['cabling_sheet_name'],		# mandatory: tab/sheet name
			a_device_colname=dic['a_device_col'],		# mandatory: a side device of cable
			b_device_colname=dic['b_device_col'],		# mandatory: b side device of cable
			a_device_port_colname=dic['a_device_port_col'],
			connector_type_colname=dic['connector_type_col'],
			cable_color_colname=dic['color_col'],
			cable_weight_colname=dic['weight_col'],
			cable_line_pattern_colname=dic['pattern_col'],)

		return cable_matrix_data


Device database operations function::

	def device_data_operations(dic):
		devices_data = DeviceData(
			dic['data_file'],
			sheet_name=dic['devices_sheet_name'],
			x=dic['x-coordinates_col'],
			y=dic['y-coordinates_col'],
			stencil_colname=dic['stencils_col'],
			device_type_colname=dic['device_type_col'],
			default_stencil=dic['default_stencil'], )

		devices_data.add_description(dic['cols_to_merge'])
		return devices_data



Visio app operations functions::

	def visio_operations(dic, devices_data, cable_matrix_data, stencils):
		with VisioObject(stencils=stencils, outputFile=dic['op_file']) as v:
			print("Visio Drawing Inprogress, Do not close Visio Drawing while its running...")
			if dic['sheet_filters']:
				for kv in dic['sheet_filters'].items():
					if isinstance(kv[1], str):
						repeat_for_filter(v, devices_data, cable_matrix_data, 
							dic, kv[0], kv[1], kv[0])
					elif isinstance(kv[1], (list, tuple, set)):
						for _kv in kv[1]:
							repeat_for_filter(v, devices_data, cable_matrix_data, 
								dic, kv[0], _kv, kv[0] + '_' + _kv)
			else:
				visio_page_operation(v, devices_data, cable_matrix_data, {}, dic)
		return None


	def repeat_for_filter(v, devices_data, cable_matrix_data, 
		dic, filt_key, filt_value, page_key):
		flt ={filt_key:filt_value}
		cmd = deepcopy(cable_matrix_data)
		visio_page_operation(v, devices_data, cmd, flt, dic, page_key=page_key)


	def visio_page_operation(v, devices_data, cable_matrix_data, flt, dic, page_key=None):
		if dic['filter_on_include_col']:
			cable_matrix_data.filter_eligible_cables_only()	# [Optional]
		if dic['is_sheet_filter']:
			cable_matrix_data.filter(**flt)		# [Optional] column=records
		cable_matrix_data.calc_slop(devices_data)	# [Mandatory] calculate cable slop/angle
		if flt:
			v.insert_new_page(page_key)
		else:
			v.insert_new_page("PhysicalDrawing")
		item_objects = ItemObjects(v, devices_data, cable_matrix_data, 
			filterOnCables=dic['filter_on_cable'])
		Connectors(cable_matrix_data, item_objects)
		v.fit_to_draw(item_objects.page_height, item_objects.page_width)



Main Execution Function::

	def main(dic):
		devices_data = device_data_operations(dic)
		cable_matrix_data = cabling_data_operations(dic)
		stencils = get_list_of_stencils(
			folder=dic['stencil_folder'], 
			devices_data=devices_data, 
		)
		visio_operations(dic, devices_data, cable_matrix_data, stencils)
		return None


Define Variables:

.. code-block:: python
	:emphasize-lines: 5,6,36,37

	# Define all necessary input variables.
	dic = {

		# Mandatory
		'stencil_folder': '/fullpath_stencil_folder',
		'data_file': '/fullpath/data_file',

		# Optional
		'default_stencil': 'Network and Peripherals',
		'op_file': 'None',

		# Optional / if differ from actual database
		'devices_sheet_name': 'Devices',
		'x-coordinates_col': 'x-axis',
		'y-coordinates_col': 'y-axis',
		'stencils_col': 'stencils',
		'device_type_col': 'device_type',

		# Optional / if differ from actual database
		'cabling_sheet_name': 'Cablings',
		'a_device_col': 'a_device',
		'a_device_port_col': 'a_device_port',
		'b_device_col': 'b_device',
		'color_col': 'color',
		'connector_type_col': 'connector_type',
		'weight_col': 'weight',
		'pattern_col': 'pattern',

		# Optional / if differ from actual database
		'cols_to_merge': ['LIST_OF_COLUMNS_NAMES_TO_BE_MERGED_WITH_HOSTNAME',],
		'filter_on_cable': True,
		'filter_on_include_col': False,
		'is_sheet_filter': True,

		'sheet_filters': {
			'draw_type': ('core', 'dist', 'building-a',),
			'dist': 'x',
			# Add more filter / tabs as necessary.... },
	}


Execute Now::

	main(dic)



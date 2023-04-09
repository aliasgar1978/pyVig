Way1: CLI Execution with manual Excel Database preparation
==========================================================


Follow below steps for Command Line Execution steps
Copy python commands to a .py file for repeatative use.


----------------------------

Prepare Excel
----------------------

   #. Excel Database should contain two tabs **Devices**, **Cablings**.
   #. Refer to ``Databse Sample`` section for more details on Excel database requirements.
   #. :download:`Sample <samples/Excel-pyvig-sample.xlsx>`. pyVig readable Sample Excel file with Devices and Cablings Tab.


Prepare your code
------------------------------

	.. code-block:: python
	
		# --------------------------------------------------------------------------------------
		# 1. Import package
		# 2. Call pyVig with necessary inputs ( you can remove optional, undesired inputs )
		# --------------------------------------------------------------------------------------
		from pyVig import pyVig
		pyVig(
			# Mandatory
			stencil_folder = '/fullpath_stencil_folder',
			data_file = '/fullpath/data_file',

			# Optional - inputs
			default_stencil = 'Network and Peripherals',    #(default: None)
			op_file = 'filename.vsdx',    # (default: None)

			devices_sheet_name = 'Devices',    # (default: 'Deviecs')
			x-coordinates_col = 'x-axis',    # (default: 'x-axis')
			y-coordinates_col = 'y-axis',    # (default: 'y-axis')
			stencils_col = 'stencil',    # (default: 'stencil')
			device_type_col = 'item',    # (default: 'item')

			cabling_sheet_name = 'Cablings',    #(default: 'Cablings')
			a_device_col = 'a_device',    # (default: 'a_device')
			b_device_col = 'b_device',    # (default: 'b_device')

			# Optional - Devices tab columns to be merged to form device description 
			cols_to_merge = ['COLUMNS_TO_BE_MERGED_WITH_HOSTNAME', 'IP', 'SERIAL', ... ],

			# Optional - Device icon formatting 
			device_format_columns = {
				'iconHeight': 1,    # sets default iconHeight (default: 1)
				'iconWidth': 2.5,    # sets default iconWidth (default: 2.5) 
			},

			# Optional - Filter options
			filter_on_cable = True,    # (default: True)
			filter_on_include_col = False,    # (default: False, will look for column name 'include' to select cablings)
			is_sheet_filter = True,    # (Default: True, enables filtering on 'sheet_filters' input)
			sheet_filters = {
				'draw_type': ('core', 'dist', 'building-a',),		## Here column name = 'draw_type' , matching and filtering rows value as per given in tuple. 
				'dist': 'x',										## Here column name = 'dist',  matching and filtering an 'x' marked rows.
				# Add more filters as required.... 
			},

		)

		# --------------------------------------------------------------------------------------



	.. tip::
		
		Do not interrupt the visio application while visio generation is inprogress. 

		Once Finished save the file as required.

		Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.






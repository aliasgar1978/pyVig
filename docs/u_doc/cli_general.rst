CLI Execution General Instructions
==================================


Command Line Execution steps
----------------------------


<<<<<<< HEAD
Import pyVig module from pyVig
------------------------------

	.. code-block:: python
=======
1. Import pyVig module from pyVig::
>>>>>>> 86268143894e2f3d988d94beea9d4740f104a021
	
		import pyVig


<<<<<<< HEAD
Prepare Excel Database
----------------------

=======
2. Prepare Excel Database
>>>>>>> 86268143894e2f3d988d94beea9d4740f104a021

	#. Excel Database should contain two tabs ``Devices``, ``Cablings``.
	#. Refer to Samples section for more details on Excel database requirements.


<<<<<<< HEAD
Define Variables
----------------

=======
3. Define Variables::
>>>>>>> 86268143894e2f3d988d94beea9d4740f104a021

	.. code-block:: python
		:emphasize-lines: 5,6,36,37

		# Define necessary input variables.
		dic = {

			# Mandatory
			'stencil_folder': '/fullpath_stencil_folder',			## folder path where visio stencils are placed
			'data_file': '/fullpath/data_file',						## folder path where Excel Database is placed

			# Optional
			'default_stencil': 'Network and Peripherals',			## Provide a Stencil name, which will be default if no stencil name given in Excel database
			'op_file': 'None',										## Some of visio versions doesn't support file save

			# Optional / provide only if differ from actual Devices - database
			'devices_sheet_name': 'Devices',
			'x-coordinates_col': 'x-axis',
			'y-coordinates_col': 'y-axis',
			'stencils_col': 'stencils',
			'device_type_col': 'device_type',

			# Optional / provide only if differ from actual Cabling - database
			'cabling_sheet_name': 'Cablings',
			'a_device_col': 'a_device',
			'a_device_port_col': 'a_device_port',
			'b_device_col': 'b_device',
			'color_col': 'color',
			'connector_type_col': 'connector_type',
			'weight_col': 'weight',
			'pattern_col': 'pattern',

			# Optional / if differ from actual database
			'cols_to_merge': ['COLUMNS_TO_BE_MERGED_WITH_HOSTNAME', 'IP', 'SERIAL', ... ],
			'filter_on_cable': True,
			'filter_on_include_col': False,
			'is_sheet_filter': True,								## Eanables sheet_filters and multipage drawing

			# Optional / for only selected rows from Cabling tab and for multiplage drawing
			'sheet_filters': {
				'draw_type': ('core', 'dist', 'building-a',),		## Here column name = 'draw_type' , matching and filtering rows value as per given in tuple. 
				'dist': 'x',										## Here column name = 'dist',  matching and filtering an 'x' marked rows.
				# Add more filters as required.... 
			},

		}


<<<<<<< HEAD
Execute Now
-----------

=======
4. Execute Now::
>>>>>>> 86268143894e2f3d988d94beea9d4740f104a021

	.. code-block:: python

		pyVig(dic)


	.. tip::
		
		Do not interrupt the visio application while visio generation is inprogress. 

		Once Finished save the file as required.

		Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.






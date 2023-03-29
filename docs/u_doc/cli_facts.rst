Way3: CLI Execution with auto pyVig Excel Readable file preparation using facts files
=====================================================================================


In this method we do not need to prepare the Excel Database manually by ourself. Instead of that we can use the Excel files (aka: -clean.xlsx generated using facts-finder) 
to generate the Excel Database for us.  


-----

Pre-Requisites
--------------------------------------------


Here below are two Pre-Requisite steps to be done before generating pyVig understandable Excel generation.

Capture
^^^^^^^

	Use capture-it to capture a few commands output and to prepare commands parsed Excel Files as a first step. 

		* You can use ``capture-it`` package for the purpose of the same.
		* `Refer: capture-it documentation <https://capture-it.readthedocs.io>`_
	
	
Clean files generation
^^^^^^^^^^^^^^^^^^^^^^

	Using the captures and parsed Excel files, generate clean excel files (-clean.xlsx).

		* You can use ``facts_finder`` package for the purpose of the same.
		* `Refer: facts-finder documentation <https://facts-finder.readthedocs.io>`_



-----

Create pyVig Excel file
-----------------------


	Now Create a python file using below snippet steps.


module imports
^^^^^^^^^^^^^^

	.. code-block:: python

			# -------------------------------------
			# general imports
			# -------------------------------------
			from pyVig import pyVig, pyVig_gui, DFGen
			import nettoolkit as nt
			import os

			# -------------------------------------
			# custom imports
			# -------------------------------------
			# custom functions imports - part 1
			# There must be two custom functions defined and to be imported
			# 1. a function to generate - hierarchical order series
			# 2. a function to generate - switch type series
			# ... add more as required
			from custom_pyvig import hierarchical_order_series, sw_type_series

			# custom functions imports - part 2
			# There can be n-number of optional var custom functions defined and can be imported for additional informations on device. such as 'serial', 'model'  from 'var' tab of -clean excel file.
			# ... add more as necessary
			from custom_pyvig.optional_var import get_dev_model, get_dev_serial


Generate pyVig readable Excel Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	.. code-block:: python

			# -------------------------------------
			# Define some static/global variables input
			# -------------------------------------
			# provide an output pyVig Excel file name 
			XL_PYVIG_OP_FILE = 'excel-pyVig.xlsx'

			# stencils - <folder is mandatory, default stencil optional if excel database populated properly> 		
			STENCIL_FOLDER  = 'fullpath/where/stencilfiles/stored'
			DEFAULT_STENCIL = 'Network and Peripherals'	# notice no path, no extension here (default: None)

			# define (optional) icon spacing
			SPACING_X = 4 # horizontal spacing (inch) between two adjacent icons  (default: 3.5)
			SPACING_Y = 4 # vertical spacing (inch) between two adjacent icons   (default: 2)

			# define (optional) the `column name` on which line pattern separation should be decided, and shift count step for each change
			LINE_PATTERN_STYLE_SEPARATION_ON_COLUMN = 'int_filter'		# (default: None)
			LINE_PATTERN_STYLE_SHIFT = 3			# (default: 2)

			# define (optional) some other cable properties.
			DEFAULT_CONNECTOR_TYPE = 'straight'  # options = 'curved', 'angled', 'straight' (default: straight)
			DEFAULT_LINE_COLOR =  'green'  # (default: blue)
			DEFAULT_LINE_WT =  5 	# (default: 3)
			DEFAULT_LINE_PATTERN =  1  # (default:1,  i.e. solid)


			# -------------------------------------
			# Capture files/folder
			# -------------------------------------
			# provide folder where all clean excel files stoerd, and store those names in a form of list
			capture_folder = "Capturefolder/where/all/clean-files-stored"
			files = [f'{capture_folder}/{file}' 
			         for file in os.listdir(capture_folder) 
			         if file.endswith("-clean.xlsx") ]


			# -------------------------------------
			# create DataFrame Object  
			# -------------------------------------
			DFG = DFGen(files)


			# -------------------------------------
			# add - custom attributes, custom functions, custom var functions						
			# -------------------------------------

			DFG.update_attributes(			                        # optional
				default_stencil=DEFAULT_STENCIL,
				default_x_spacing=SPACING_X,
				default_y_spacing=SPACING_Y,
				line_pattern_style_separation_on=LINE_PATTERN_STYLE_SEPARATION_ON_COLUMN,
				line_pattern_style_shift_no=LINE_PATTERN_STYLE_SHIFT,
				#
				connector_type=DEFAULT_CONNECTOR_TYPE,
				color=DEFAULT_LINE_COLOR,
				weight=DEFAULT_LINE_WT,
				pattern=DEFAULT_LINE_PATTERN,
			)

			DFG.update_functions(
				hierarchical_order=hierarchical_order_series,		# mandatory: custom function
				device_type=sw_type_series,				# mandatory: custom function
				# .add more as desired
			)

			DFG.update_var_functions(                            	   # optional: custom var functions
				device_model=get_dev_model,
				serial_number=get_dev_serial,
				# .add more as desired
			)


			# -------------------------------------
			# go thru all provided files,  generate a single pyVig readable Excel file
			# -------------------------------------
			DFG.iterate_over_files()
			nt.write_to_xl(XL_PYVIG_OP_FILE, DFG.df_dict, index=False, overwrite=True)




	* An excel file with provided *XL_PYVIG_OP_FILE* name will be generated.
	* Verify it and update as necessary.


-----



Generate Visio using pyVig Excel Database created above
-------------------------------------------------------


	Now, we can create visio using,
	* ``Way1: CLI with Manual XL`` page **Define Variables** & **Execute Now** sections.
	* ``Way2: GUI with Manual XL`` page **Import and run pyVig_gui from pyVig** section.
	
	Where provide, as defined above static/global variables
    	* *'data_file': XL_PYVIG_OP_FILE*,
    	* *'stencil_folder': STENCIL_FOLDER*,
    	* *'default_stencil': DEFAULT_STENCIL*,



	.. tip::
		
		Do not interrupt the visio application while visio generation is inprogress. 

		Once Finished save the file as required.

		Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.



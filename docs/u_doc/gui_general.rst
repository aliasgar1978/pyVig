GUI Execution Instructions
===========================

Quick and User-Friendly way of execution steps
---------------------------------------------------

----------------------------------------



Prepare Excel Database
----------------------


	#. Excel Database should contain two tabs ``Devices``, ``Cablings``.
	#. Refer to Samples section for more details on Excel database requirements.


Import and run pyVig_gui module from pyVig
------------------------------------------


	.. code-block:: python
	
		import pyVig_gui
		pyVig_gui()



	.. tip::
		
		Do not interrupt the visio application while visio generation is inprogress. 

		Once Finished save the file as required.

		Verify drawing,  Modify Excel Database if need adjustments, re-run pyVig() to regenerate drawing.



------------------------------



Captures
---------------



*	A **declaration** page will be displayed

	Once all selection made use ``Go`` button to *start* generating visio.

	Use ``Cancel`` button to *exit* without doing anything.


	.. image:: img/declaration_page.png
	  :width: 400
	  :alt: A declaration page will be displayed

--------------------------------

*	Select Data from this tab

	**database file:** select Excel data file

	**stencil folder:** select folder, where all visio stencil files are stored.

	**default stencil file:** *[optional]* select default stencil file.  It will be used if no stencil mentioned in excel data.

	**devices sheet name:** ``Devices`` details tab name in excel data.
	**Cabling sheet name:** ``Cabling`` details tab name in excel data.
	**Other column names:** select correct respective *column names* if it is differ from standard.


	**see also:** Excel Details page on standard way of creating data

	**Note:** Missing stencil/device type will display information in ``rectangle box``.


	.. image:: img/input_data_page.png
	  :width: 400
	  :alt: Select appropriate data from this tab

-------------------------------

*	Enable various **filters** from here.

	Multiple *columns* can be match with a *value* from that column to select specific data to appear to a sheet.


	.. image:: img/apply_filter_page.png
	  :width: 400
	  :alt: Enable various filters from here

-------------------------------

*	Select and add **additional columns** to append those to a device descriptions.

	By default only *hostname* will appear.


	.. image:: img/other_options_page.png
	  :width: 400
	  :alt: Add additional description columns here

-------------------------------

*	Excel Devices tab
	
	**hostname:** [mandatory] device names

	**x-axis, y-axis:** [mandatory] device co-ordinates in visio page. *column names can be different, however need to update it in menu if different*

	**stencils:** [optional] stencil file name (without extension) for each device. No stencil will use default stencil provided. And if no default stencil as well than details will go in a rectangle box.  *column name can be different, however need to update it in menu if different*

	**device_type:** [optional] icon name/number from stencil.  *column name can be different, however need to update it in menu if different*

	++ add n-number of **additional columns** to add an additional details to device descriptions. Required columns needed to be selected and added from ``Other Options`` tab.


	.. image:: img/sample_excel_devices_tab.png
	  :width: 400
	  :alt: Sample Excel Devices tab

-------------------------------


*	Excel Devices tab

	**a_device:**  [mandatory] device name for a leg of a cable. *column name can be different, however need to update it in menu if different*

	**b_device:** [mandatory] device name for b leg of a cable. *column name can be different, however need to update it in menu if different*

	**a_device_port:** [optional] port information for a leg device. *column name can be different, however need to update it in menu if different*

	**connector:** [optional]  connector/cable line type (select either one: straight, angled, curved) (default=angled)

	**color:** [optional] color of connector/line ( red, blue, gray, darkgray, lightgray) (default=black)
	Or provide RGB number color in tuple format (R,G,B)

	**weight:** [optional] line thickness in number	(default=1)

	**pattern:** [optional] line pattern in number	(default=solid line)

	++ add n-number of **additional columns**: to add an additional filters and /or *multi-sheet output*.  Required columns filter needed to be added from ``Apply Filters``.




	.. image:: img/sample_excel_cabling_tab.png
	  :width: 400
	  :alt: Sample Excel Cabling tab






Excel database Preparation Guidelines
=====================================


* There is a requirement of having a database in Excel format, which will be used to generate the visio drawing.
* For network drawings, we require two tabs in Excel file. Tab names are to be match exactly as given below.

  #. ``Devices`` This tab defines all images/icons to be placed on the visio page.
  #. ``Cablings`` This tab defines all cabling/connectivity related stuff to be done on placed icons.

-----

mandatory columns
-----------------

**Devices Tab**
^^^^^^^^^^^^^^^


     #. ``hostname`` defines hostname / identity of device ( No Exception and column name modification not allowed )
     #. ``x-axis`` defines the horizontal position of device on visio page. ( column name can be changed by providing var argument `x` in input)
     #. ``y-axis`` defines the vertical position of device on visio page. ( column name can be changed by providing var argument `y` in input)

**Cablings Tab**
^^^^^^^^^^^^^^^

     #. ``a_device`` defines hostname / identity of device for a-end of a connector/cable. (column name can be changed by providing var argument `dev_a` as input)
     #. ``b_device`` defines hostname / identity of device for b-end of a connector/cable. (column name can be changed by providing var argument `dev_b` as input)

-----

optional columns
----------------



**Devices Tab**
^^^^^^^^^^^^^^^

     #. ``stencil`` defines stencil for each individual device ( column name modification not allowed )
     #. ``item`` defines stencil item for each individual device ( column name modification not allowed )
     #. ``iconHeight`` defines vertical resizing of device icon ( column name modification not allowed )
     #. ``iconWidth`` defines horizontal resizing of device icon ( column name modification not allowed )
     #. There can be **many other** columns with any other arbitrarily named columns with other details.

        * Such as: (device_model, serial_number, ip_address, rack_details, . . . and many more ).
        * All of these columns details can be clubbed in device output using var argument ``cols_to_merge``.
        * Provide list of column names as a value to above var argument.
        * Arrange those in list as desired sequence.

**Cablings Tab**
^^^^^^^^^^^^^^^


     #. ``aport`` defines port number for a-end device of a connector/cable. And will appear on middle of it. ( column name modification not allowed )
     #. ``connector_type`` defines connector type for a connector/cable. (default: *straight*, other options: angled, curved). ( column name modification not allowed )
     #. ``color`` defines color of a connector/cable. (default: *blue*). ( column name modification not allowed )
     #. ``weight`` defines weigth of a connector/cable. (default: *3*). ( column name modification not allowed )
     #. ``pattern`` defines line pattern of a connector/cable. (default: *1*). ( column name modification not allowed )
     #. There can be **many other filter** columns as described below.

        #. ``include`` to display only selected cable connectivities.

           * Non blank values will be selected and appeared in output.
           * This will get override by other sheet filters if defined.
           * Use this quick feature, if want to to have just one filter applied on data 
           * A single Page drawing will appear
           * use **filter_on_include_col** input var argument for providing this additional information  


              .. code-block:: python

                    filter_on_include_col = True


        #. There can be **many other filter** columns defined with any other arbitrary names as per choice.

           * column name with each matching row values will be considered as a filter, so multiple filters can be defined in a single column. ( see column: *draw_type* in given example data )
           * each filtered data will create its own page in visio drawing.
           * Multipls columns with multiple matching row values can be combined to generate more granular drawings.
           * Output will be multipage output.
           * use **sheet_filters** input var argument in a form of dictionary for providing this additional information  

              .. code-block:: python

                    sheet_filters = {
                      ## key = column header: 
                      ## value(s) = can be either single string or tuple of multiple strings.
                      'draw_type': ('core', 'access',),   
                      # Add more as desired .... 
                    }


-----


* By default, any device with no connectivity on `Cablings` tab, will be excluded.
* Change this behaviour using input var argument ``filter_on_cable``.

-----



sample excel database 
---------------------------------

:download:`Sample <samples/Excel-pyvig-sample.xlsx>`. pyVig readable Sample Excel file with *Devices* and *Cablings* tabs *prefilled* with some *sample* data.


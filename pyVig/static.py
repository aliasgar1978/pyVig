import os

op_file = "c:/users/al202t/desktop/new.vsdx"

# ------------------------------------------------------------------------------
#  Visio static CONSTANTS
# ------------------------------------------------------------------------------
visCharStyle = {
	'Bold': 17,
	'Italic': 51,
	'Underline': 55,
}
visPageWidth = 0
visPageHeight = 1
visPageDrawSizeType = 6
visSectionObject = 1
visSectionCharacter = 3
visSectionParagraph = 4
visCharacterStyle = 2
visCharacterColor = 1
visHorzAlign = 6
visFillForegndTrans = 6
visFillBkgndTrans = 7
visRowFill = 3
visRowXFormOut = 1
visRowTextXForm = 12
visRowLine = 2
visRowPage = 10
visLineColor = 1
visLineWeight = 0
visLinePattern = 2
visXFormPinX = 0
visXFormPinY = 1
visXFormHeight = 3
visXFormWidth = 2
visArcSweepFlagConvex = 1
# Unit Codes
visCentimeters = 69
visInches = 65
# Resize
visResizeDirE = 0    #  Right, middle shape handle.
visResizeDirNE = 1    # Right, top shape handle.
visResizeDirN = 2    #  Center, top shape handle.
visResizeDirNW = 3    # Left, top shape handle.
visResizeDirW = 4    #  Left, middle shape handle.
visResizeDirSW = 5    # Left, bottom shape handle.
visResizeDirS = 6    #  Center, bottom shape handle.
visResizeDirSE = 7    # Right, bottom shape handle.

visRowShapeLayout = 23
visSLOLineRouteExt = 19
visSLORouteStyle = 10
visXFormAngle = 6
visIndentLeft = 1
visIndentRight = 2

visTextHorizontalAlign = {
	'left': 0,
	'center': 1,
	'right':2,
}
visTextVerticalAlign = {
	'top': 0,
	'middle': 1,
	'bottom':2,
}

# ------------------------------------------------------------------------------


REMARKS_COLUMNS_TO_MERGE = [
	'ip_address',
	'device_model',
	'serial_number',

	# Add More as needed.
	# Resequence as required in output.
]
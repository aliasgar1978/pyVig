
# ------------------------------------------------------------------------------
#  IMPORTS
# ------------------------------------------------------------------------------
import win32com.client
from win32com.client import constants

from static import *
from common import *

# ------------------------------------------------------------------------------
#  VisioObject class
# ------------------------------------------------------------------------------
class VisioObject:
	'''Creates a Visio Object. 
	Param : stencils  - object stancils
	example : oVis = VisioObject(stencils=[stencil1, stencil2])
			  stencil1 and stencil2 are two different stencils.
	'''

	# stencils dictionary
	stn = {}

	# --------------------------------------------------------------------------
	#  dunders
	# --------------------------------------------------------------------------

	# object initializer
	def __init__(self, stencils=None, outputFile=None):
		'''Initialize Visio Object by starting Visio Application, 
		Opens a blank Visio Document/Page inside it.
		Opetional Parameters (**stencils) -> will open all stencils mentioned.
		'''
		self.no_of_icons = 0
		self.icons = {}
		self.outputFile = outputFile
		self._startVisio
		self._openBlankVisioDoc
		if all([stencils is not None, 
				self.visio is not None,
				self.doc is not None,
				self.page is not None,
				]):
			for value in stencils:
				v = get_filename(value)
				self.stn[v] = self.openStencil(value)

	# context Load
	def __enter__(self):
		return self

	# context end
	def __exit__(self, exc_type, exc_value, tb):
		self._saveVisio(self.outputFile)
		self._closeVisio()
		if exc_type is not None:
			traceback.print_exception(exc_type, exc_value, tb)

	# Object Representation
	def __repr__(self):
		return f'VisioObject: {self.outputFile}'

	# --------------------------------------------------------------------------
	#  Internal
	# --------------------------------------------------------------------------

	# save visio output file
	def _saveVisio(self, file):
		try: self.doc.SaveAs(file)
		except: pass

	# close visio application
	def _closeVisio(self):
		try:
			self.doc.Close()
			self.visio.Quit()
		except:
			pass

	# Internal use only: starts a new Visio Application
	@property
	def _startVisio(self):
		try:
			self.visio = win32com.client.Dispatch("Visio.Application")
		except:
			self.visio = None

	# Internal use only: Open a blank visio page inside opened Visio Application
	@property
	def _openBlankVisioDoc(self):
		try:
			self.doc = self.visio.Documents.Add("")
			self.page = self.doc.Pages.Item(1)
		except:
			self.doc = None
			self.page = None

	# Return item from Stencil
	def _selectItemfromStencil(self, item, stencil):
		return self.stn[stencil].Masters.Item(item)
		# try: return stencil.Masters.Item(item)
		# except: pass

	# Drops 'item' on visio page at given position index ( posX and posY )
	def _dropItemtoPage(self, item, posX, posY):
		try: 
			itemProp = self.page.Drop(item, posY, posX)
			return itemProp
		except: 
			pass

	@staticmethod
	def _border(item, borderLineColor=None, borderLinePattern=None,
		borderLineWeight=0) :
		if borderLineColor is not None:
			item.Cells( 'LineColor' ).FormulaU = borderLineColor
		if borderLinePattern is not None and isinstance(borderLinePattern, int):
			item.Cells( 'LinePattern' ).FormulaU = borderLinePattern
		if borderLineWeight > 0:
			item.Cells( 'LineWeight' ).FormulaU = borderLineWeight

	@staticmethod
	def _fill(item, fillColor=None, fillTransparency=None):
		if fillColor is not None:
			item.Cells( 'Fillforegnd' ).FormulaU = fillColor
		if fillTransparency is not None:
			if isinstance(fillTransparency, int):
				fillTransparency = str(fillTransparency) + "%"
			item.CellsSRC(visSectionObject, visRowFill, visFillForegndTrans).FormulaU = fillTransparency
			item.CellsSRC(visSectionObject, visRowFill, visFillBkgndTrans).FormulaU = fillTransparency

	@staticmethod
	def _text(item, text=None, textColor=None, textSize=0, vAlign=1, hAlign=0, style=None):
		if text is not None:
			item.Text = text
		if textColor is not None:
			item.CellsSRC(visSectionCharacter, 0, visCharacterColor).FormulaU = textColor
		if textSize > 0 and isinstance(textSize, int):
			item.Cells( 'Char.size' ).FormulaU = textSize
		if isinstance(vAlign, int) and (vAlign>=0 and vAlign<=2):
			item.Cells( 'VerticalAlign' ).FormulaU = vAlign
		if isinstance(hAlign, int) and (hAlign>=0 and hAlign<=2):
			item.CellsSRC(visSectionParagraph, 0, visHorzAlign).FormulaU = hAlign
		if style is not None:
			if isinstance(style, str):
				item.CellsSRC(visSectionCharacter, 0, visCharacterStyle).FormulaU = visCharStyle[style]
			elif isinstance(style, (list, tuple)):
				for x in style:
					item.CellsSRC(visSectionCharacter, 0, visCharacterStyle).FormulaU = visCharStyle[x]

	### FORMATTING ###	
	def _format(self, icon,
		text=None, textColor=None, textSize=0, vAlign=1, hAlign=0, style=None,
		fillColor=None, fillTransparency=None,
		borderLineColor=None, borderLinePattern=None, borderLineWeight=0  
		):
		''' Formatting Parameters '''
		self._border(icon, borderLineColor, borderLinePattern, borderLineWeight)
		self._fill(icon, fillColor, fillTransparency)
		self._text(icon, text, textColor, textSize, vAlign, hAlign, style)
		self.no_of_icons += 1
		self.icons[self.no_of_icons] = icon

	# --------------------------------------------------------------------------
	#  External
	# --------------------------------------------------------------------------

	# Internal + External : Open mentioned stencil in opened visio application. 
	def openStencil(self, stencil):
		'''stn = visObj.openStencil(stencil)
		Opens mentioned stencil 'stencil' in visio object visio application.
		'''
		stencil = stencil.replace("/", "\\")
		# return self.visio.Documents.Open(stencil)
		try:
			return self.visio.Documents.Open(stencil)
		except:
			pass

	def selectNdrop(self, stencil, item, posX, posY, **format):
		'''icon = visObj.selectNdrop(stencil,item,posX,posY) : 
		Selects item 'item' from provided stencil 'stencil' for selected visio object.
		And drops that item on visio Object at given position index ( posX and posY )
		'''
		itm = self._selectItemfromStencil(item, stencil)
		if itm is not None:
			icon = self._dropItemtoPage(itm, posX, posY)
			self._format(icon=icon, **format)
			return icon

	def shapeDrow(self, shape, lx, lr, rx, rr, **format):
		'''shape = visObj.shapeDrow(shape, lx, lr, rx, rr, **format):
		Drops provided shape to visio page.
		param : shape = Shape Name ( eg - rectangle, ellipse, arc, line )
		param : lx, lr, rx, rr = co-ordinate where the shape to be drawn
		param : **format = shape formatting (see _format() for type of formats available)
		'''
		shaping = True
		if shape.lower() == "rectangle":
			rect = self.page.DrawRectangle(lx, lr, rx, rr)
		elif shape.lower() == "ellipse":
			rect = self.page.DrawOval(lx, lr, rx, rr)
		elif shape.lower() == "arc":
			rect = self.page.DrawQuarterArc(lx, lr, rx, rr, visArcSweepFlagConvex)
		elif shape.lower() == "line":
			rect = self.page.DrawLine(lx, lr, rx, rr)
		else:
			shaping =False

		if shaping:
			self._format(icon=rect, **format)
			return rect

	def join(self, connector, shpObj1, shpObj2):
		'''connectors to join two shapes'''
		connector.Cells("BeginX").GlueTo(shpObj1.Cells("PinX"))
		connector.Cells("EndX").GlueTo(shpObj2.Cells("PinX"))		

	def connector(self, connector_type=None, x=0, y=0):
		'''s1_s2_Connector = self.connector()
		Drops a connector to visio page.
		param : connector_type = ( eg - straight, curved, default=angled )
		param : x, u = coordinates where to drop connector (default=0,0)
		'''
		item = self.page.Drop(self.visio.ConnectorToolDataObject, x, y)
		if connector_type == "straight":
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "1"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "16"
		elif connector_type == "curved":
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "2"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "1"
		else:
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLOLineRouteExt).FormulaU = "1"
			item.CellsSRC(visSectionObject, visRowShapeLayout, visSLORouteStyle).FormulaU = "1"
		return item


class Device():

	def __init__(self, visObj, item, x, y):
		self.visObj = visObj
		self.item = item
		self.x = x
		self.y = y

	def drop_from(self, stencil):
		self.obj = self.visObj.selectNdrop(stencil=stencil, 
			item=self.item, posX=self.x, posY=self.y)

	@property
	def object(self):
		return self.obj

	def connect(self, remote, connector_type=None):
		connector = self.visObj.connector(connector_type=connector_type)
		self.visObj.join(connector, self.obj, remote.obj)

	def description(self, remarks):
		self.obj.Characters.Text = remarks


def device(stencil, visObj, item, x, y):
	D = Device(visObj, item, x, y)
	D.drop_from(stencil)
	return D


import numpy as np



def df_with_slops_and_angles(df, x1_col, x2_col, y1_col, y2_col):
	"""add the dataframe with slop and angle for the given co-ordinates on plane.

	Args:
		df (DataFrame): Input DataFrame
		x1_col (str): column name for point 1 - x axis
		x2_col (str): column name for point 2 - x axis
		y1_col (str): column name for point 1 - y axis
		y2_col (str): column name for point 2 - y axis

	Returns:
		DataFrame: Updated Output DataFrame
	"""	
	df['slop'] = (df[y2_col] - df[y1_col])/(df[x2_col] - df[x1_col])
	df = df.fillna("")
	df['angle_angled_connector'] = df.slop.apply(slop_to_angled_connector)
	df['angle_straight_connector'] = df.slop.apply(slop_to_straight_connector)
	return df.fillna("")


def slop_to_straight_connector(m):
	"""calculate angle from given slop(m) of a straight line.

	Args:
		m (float): slop of a straight line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 90+angle
	if m <= 0: angle = 360-angle 
	return angle

def slop_to_angled_connector(m):
	"""calculate angle from given slop(m) of an angled line.

	Args:
		m (float): slop of an angled line

	Returns:
		int: degree/slop of line
	"""		
	if not m: return 0
	angle = int(np.math.degrees(np.math.tanh(m)))
	if angle < 0: angle = 180-angle
	if m > 0: angle = 360-angle 
	return angle




# --------------------------------------------- 
# Co-ordinate calculator
# --------------------------------------------- 
class CalculateXY():

	def __init__(self, dev_df, default_x_spacing, default_y_spacing):
		self.df = dev_df
		#
		self.spacing_x = default_x_spacing
		self.spacing_y = default_y_spacing
		#


	def calc(self):
		self.sort()
		self.count_of_ho()
		self.update_ys()
		self.update_xs()

	def sort(self):
		self.df.sort_values(by=['hierarchical_order', 'hostname'], inplace=True)

	def count_of_ho(self):
		self.ho_dict = {}
		vc = self.df['hierarchical_order'].value_counts()
		for ho, c in vc.items():
			self.ho_dict[ho] = c

	# -----------------------------------------------
	def calc_ys(self):
		i, y = 0, {}
		for ho in sorted(self.ho_dict):
			for r in range(1, 3):
				if self.ho_dict.get(ho+r):
					c = self.ho_dict[ho+r]
					next_i = c/2 * self.spacing_y
					break
			y[ho] = i
			i = next_i
		y = self.inverse_y(y)
		return y

	def inverse_y(self, y):
		return {k: max(y.values()) - v+2 for k, v in y.items()}

	def get_y(self, ho): return self.y[ho]

	def update_ys(self):
		self.y = self.calc_ys()
		self.df['y-axis'] = self.df['hierarchical_order'].apply(self.get_y)
		return self.df

	# -----------------------------------------------

	def get_x(self, ho): 
		for i, v in enumerate(sorted(self.xs[ho])):
			value = self.xs[ho][v]
			break
		del(self.xs[ho][v])
		return value

	def calc_xs(self):
		xs = {}
		middle = self.full_width/2
		halfspacing = self.spacing_x/2
		for ho in sorted(self.ho_dict):
			if not xs.get(ho):
				xs[ho] = {}
			c = self.ho_dict[ho]
			b = middle - (c/2*self.spacing_x) - halfspacing
			for i, x in enumerate(range(c)):
				pos = x*self.spacing_x + b 
				xs[ho][i] = pos
		# print(xs)
		return xs

	def update_xs(self):
		self.full_width = (max(self.ho_dict.values())+2) * self.spacing_x
		self.xs = self.calc_xs()
		self.df['x-axis'] = self.df['hierarchical_order'].apply(self.get_x)
		return self.df


# --------------------------------------------- 


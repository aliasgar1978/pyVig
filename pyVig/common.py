
# ------------------------------------------------------------------------------
#  Local Functions
# ------------------------------------------------------------------------------

def get_filename(absolute_pathfile):
	return absolute_pathfile.split("/")[-1].split("""\\""")[-1].split(".")[0]

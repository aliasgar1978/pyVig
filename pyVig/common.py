

# ------------------------------------------------------------------------------
#  Local Functions
# ------------------------------------------------------------------------------

def get_filename(absolute_pathfile):
	return absolute_pathfile.split("/")[-1].split("""\\""")[-1].split(".")[0]


# folder = "c:\\users\\al202t\\desktop\\STN\\abcd.vsdx"
# folder = "c:/users/al202t/desktop/STN/abcd.vsdx"

# print(get_filename(folder))
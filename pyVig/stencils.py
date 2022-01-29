import os


# -----------------------------------------------------------------------------------
# Stencil functions
# ------------------------------------------------------------------------------
def get_list_of_stencils(folder):
	return [folder+file 
	for file in os.listdir(folder) 
	if file.endswith(".vssx") or file.endswith(".vss")]	
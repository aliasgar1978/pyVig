import os


# -----------------------------------------------------------------------------------
# Stencil functions
# ------------------------------------------------------------------------------
def get_list_of_stencils(folder, devices_data):
	used_stn = set(devices_data.df.stencil)
	used_stn.remove("")
	found_stn = []
	for file in os.listdir(folder):
		for stn in used_stn:			
			if file.find(stn) > -1:
				found_stn.append(folder+file)
				break
	if len(used_stn) == len(found_stn):
		return found_stn
	else:
		from pprint import pprint
		print(used_stn)
		pprint(found_stn)
		raise ValueError("Stencil is Missing or Invalid")




import os

stencil_folder = os.path.abspath(os.getcwd()) + "/stencils/"
# -----------------------------------------------------------------------------------
stencil_icons = {
	'L3_SW': "Master.35",
	'L2_SW': "Master.38",
	'ROUTER': "Master.39",
	'LINE': 'line',
}
# -----------------------------------------------------------------------------------

def get_list_of_stencils(folder):
	return [folder+file 
	for file in os.listdir(folder) 
	if file.endswith(".vssx") or file.endswith(".vss")]	
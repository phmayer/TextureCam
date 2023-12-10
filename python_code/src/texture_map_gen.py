import normal_map_generator as nmp
from PIL import Image

NORMAL_MAP_SMOOTH = 0
NORMAL_MAP_INTENSITY = 2


def gen_normal_map(input_img_path, output_img_path):
	nmp.convert_normal_path(input_img_path, output_img_path, NORMAL_MAP_SMOOTH, NORMAL_MAP_INTENSITY)

def gen_ao_map(input_img_path, output_img_path):
	nmp.convert_ao_path(input_img_path, output_img_path)

def test_it():

	path_input_example = "C:/Users/Philipp/Desktop/WS2324_KIT/repos/TextureCam/python_code/src/test001.jpg"
	path_output_example_ao = "C:/Users/Philipp/Desktop/WS2324_KIT/repos/TextureCam/python_code/src/test001_AO.jpg"
	path_output_example_normal = "C:/Users/Philipp/Desktop/WS2324_KIT/repos/TextureCam/python_code/src/test001_NORMAL.jpg"

	gen_normal_map(path_input_example,path_output_example_normal)
	gen_ao_map(path_input_example,path_output_example_ao)


test_it()

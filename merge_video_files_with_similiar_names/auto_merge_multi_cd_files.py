import os #for file path operation
import subprocess #for running FFMpeg
import shutil
from itertools import groupby #for grouping items with similar prefixies

dry_run = False

filenames = []
file_names_and_file_paths = {}

prefixes = []
files_grouped_by_prefix = []
prefixes_files_dict = {}

file_list_save_path=os.path.join(os.getcwd(), "fileLists")
export_file_save_path=os.path.join(os.getcwd(), "output")

file_lists_for_ffmpeg = []
exported_files = [];

#this is called to put all files in the current directory to a list, and also
#create a map of (base) file name and file path for later retrieval
def populate_filenames_list_with_media_files_from_cwd():
	current_directory = os.getcwd()
	current_directory_file_list = os.listdir(current_directory)
	for file in current_directory_file_list:
		file_path=os.path.join(current_directory, file)
		if os.path.isfile(file_path) and os.path.splitext(file)[1] != '.py' :
			filenames.append(file)
			file_names_and_file_paths[file]=file_path

#used by another function to clean up file names
def clean_up_file_name(filename): 
	filename=filename.upper()
	filename=filename.replace(" ", "")
	return filename

#this function is intended to be passsed to the groupby funct
def extract_multi_CD_prefix_code(filename):
	prefix_starting_position=clean_up_file_name(filename).find("-CD")
	prefix=filename[0:prefix_starting_position]
	return prefix

#create a list of prefix keys and the group items
def group_files_by_prefix():
	for key, group in groupby(filenames, extract_multi_CD_prefix_code):
		files_grouped_by_prefix.append(list(group))
		prefixes.append(key)

#build a map of prefixes and the files that uses the prefixes.
def build_prefixes_files_dict():
	for i in range(len(prefixes)):
		prefixes_files_dict[prefixes[i]]=files_grouped_by_prefix[i]

#setup directory for ffmpeg export
def create_directories_for_ffmpeg():
	if not os.path.exists(file_list_save_path):
		os.makedirs(file_list_save_path)

	if not os.path.exists(export_file_save_path):
		os.makedirs(export_file_save_path)

#create the file list files needed by ffmpeg to do concate
def create_file_list_files():		
	for key in prefixes_files_dict.keys():
		save_file_name= key+'.txt'
		file_path = os.path.join(file_list_save_path,save_file_name)
		with open(file_path, "w") as file:
			for item in prefixes_files_dict[key]:
				file.write("file '%s'\n" % file_names_and_file_paths[item])
		file_lists_for_ffmpeg.append(file_path)

#contact the files with ffmpeg, this will create a new file in the export path
#without removing the existing ones.
def concate_files_with_ffmpeg():
	for file_list in file_lists_for_ffmpeg:
		output_file_name = os.path.splitext(os.path.basename(file_list))[0]
		if not dry_run:
			subprocess.call('ffmpeg.exe  -f concat -safe 0 -i "%s" -c copy %s.mp4 -y' \
				% (file_list, output_file_name), shell=True, cwd=export_file_save_path)
		else:
			pass
		exported_files.append(output_file_name)

#echo the execution results, will warn if no files are exported.
def echo_results():
	if len(exported_files) > 0: 
		print("The following files had been combined and:")
		for file in exported_files:
			print(file)
	else:
		print("No files are exported, something might be wrong?")

# Prepare the filenames for operation
populate_filenames_list_with_media_files_from_cwd()
group_files_by_prefix()
build_prefixes_files_dict()
create_directories_for_ffmpeg()
create_file_list_files()
concate_files_with_ffmpeg()
echo_results()
breakpoint()
#clean up temp folders
if not dry_run: shutil.rmtree(file_list_save_path)
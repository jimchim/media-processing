import os
import subprocess
import shutil

if shutil.which('ffmpeg') is None:
	raise OSError("FFMPEG is required to execute this script, please make sure FFMPEG is installed and its Path is configured and retry.")
else:
	print('FFMPEG is installed, continuing...')

front_vid_dir = input(
    "Please type the path to the directory containing the Front Camera videos:\n")
back_vid_dir = input(
    "Please type the path to the directory containing the Back Camera videos:\n")
export_vid_dir = input(
    "Please enter the path you'd like to have the exported video placed in. The script's position will be used by default. If a location is not specified.:\n")
export_vid_name = input("Please enter the name of the export file. (The exported file will be in .mp4) :\n")
vid_codec_to_use = input("\nIMPORTANT: Specifying a hardware accelerated encoder will reduce the time required for the transcoding.\n\n\
Please enter the name of the codec you'd like to use, e.g. hevc_nvenc. 'libx264' - a generic codec will be used if nothing is entered:") or "libx264"

def check_directory(dir):
    if os.path.exists(dir):
        return True

if check_directory(front_vid_dir) and check_directory(back_vid_dir):
    print("Confirmed both front and back vid dir exists, proceeding...")
else:
    raise NotADirectoryError(
        "The front / back video directories you entered doesn't exist, please make sure you entered the correct directory paths.")

if not check_directory(export_vid_dir) and export_vid_dir != "":
    try:
        os.mkdir(export_vid_dir)
        print("Export directory doesn't exists, creating one.")
    except Exception as e:
        print("Something went wrong")
        print(e)
elif export_vid_dir == "":
    export_vid_dir = os.getcwd()
    print("No export directory's specified, using the script's path instead:")
    print(export_vid_dir)
else:
    print("Export directory already exists. Continuing.")

if os.path.splitext(export_vid_name)[1] == '':
	export_vid_name = export_vid_name+".mp4"

def get_sorted_video_files_from_dir(dir):
    vid_files = []
    accepted_formats = (".ts", ".mp4", ".mkv")
    for file in os.listdir(dir):
        file_full_path = os.path.join(dir, file)
        file_extension = os.path.splitext(file)[1].lower()
        if os.path.isfile(file_full_path) and file_extension in accepted_formats:
            vid_files.append(file_full_path)
            print("%s is accepted!" % file)
        else:
            print("%s is not accepted." % file)
    vid_files.sort()
    return vid_files

front_files = get_sorted_video_files_from_dir(front_vid_dir)
back_files = get_sorted_video_files_from_dir(back_vid_dir)

if len(front_files) == len(back_files):
    print("\nFront dir & back dir has the same amount of files, I think we are good to go.")
else:
    print("Front dir and back dir have different number of files, the merge will not work! \n Please check the directories and come back.")

TEMP_DIR = os.path.join(os.getcwd(), '.tmp')

if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

def write_file_list(file_paths, file_to_write):
	with open(file_to_write, "w") as file:
	    for item in file_paths:
	        file.write("file '%s'\n" % item)
	return file_to_write

front_file_list = write_file_list(front_files, os.path.join(TEMP_DIR, "front.txt"))
back_file_list = write_file_list(back_files, os.path.join(TEMP_DIR, "back.txt"))

def write_concatenated_file(file_list, file_to_write):
	try:
		subprocess.call('ffmpeg -f concat -safe 0 -i "%s" -c copy %s -y' \
				% (file_list, file_to_write), shell=True)
		return file_to_write
	except Exception as e:
		print("Unable to write file: %s" % file_to_write)
		print(e)

front_concatenated_file = write_concatenated_file(front_file_list, os.path.join(TEMP_DIR, "temp_front.mp4"))
back_concatenated_file = write_concatenated_file(back_file_list, os.path.join(TEMP_DIR, "temp_back.mp4"))

cmd = 'ffmpeg -i "{rear_file}" -i "{front_file}" -filter_complex \
	"[0]scale=iw/5:ih/5 [pip]; [1][pip] overlay=main_w-overlay_w-25:main_h-overlay_h-25" \
	-acodec copy -vcodec {codec} -b:v 9000k {output}'.format(rear_file=back_concatenated_file, front_file=front_concatenated_file, output=os.path.join(export_vid_dir, export_vid_name), codec=vid_codec_to_use)	

if front_concatenated_file and back_concatenated_file:
	try:
		subprocess.call(cmd, shell=True)
		print("File exported: %s" % os.path.join(export_vid_dir, export_vid_name))
	except Exception as e:
		print("Unable to transcode the file.")
		print(e)

shutil.rmtree(TEMP_DIR)
#$testFile = Get-Item "C:\Users\user\Desktop\Lord of the rings.mp4"

#try { Get-Item "C:\Users\user\Desktop\Lord of the rings.mp4" -erroraction stop }
#catch { "An error occurred." }


# 1. Paste full path to the below empty list to start
$sourceFilePaths = @(
	"C:\Users\user\Desktop\Lord of the rings.mp4",
	"C:\Users\user\Desktop\Lord of the rings-2.mp4"
)

$errorFiles = @()
$sourceFiles = @()
		#indented comments are for debugging
		#$nonMp4Files = @()


# this function checks if the file list contains all valid files and add to the file object list
for ($i = 0; $i -le ($sourceFilePaths.length -1) ; $i += 1) {
	try {
		$transientItem = Get-Item $sourceFilePaths[$i] -erroraction stop
		$sourceFiles += $transientItem
	}
	catch {
		$errorFiles+= $sourceFilePaths[$i]
	}
}

	# echo $nonMp4Files
	# echo "The following are files that cannot be found in the output destination:"
	# echo $errorFiles
	# echo "End"
	# echo "-----------------------------------------------------------------------"
	# echo "The following are the names of the files that can be found:"
	# echo $sourceFiles
	# echo "End"

# next, find out if the files exist in the output destination:

for ($i = 0; $i -le ($sourceFiles.length -1); $i += 1) {
	try {
		$sourceItem= $sourceFiles[$i]
		$transientPath = $sourceItem.baseName + ".mp4" #this assumes the exported format is MP4.
		$targetItem = Get-Item (Join-Path "P:\Resize Output" $transientPath) -erroraction stop
	}
	catch {
		echo "Error! There are some source files can't find matching target files:"
		echo $sourceFiles[$i].fullName
	}
}

# Now, we will actually operate on the file:
if ($sourceFilePaths.length -eq $sourceFiles.length) {
	echo "All is well, all files are found, can start operation."
	echo "Number of files: $($sourceFilePaths.length)"
	
	for ($i = 0; $i -le ($sourceFiles.length -1); $i += 1) {
		try {
			$sourceItem= $sourceFiles[$i]
			$transientPath = $sourceItem.baseName + ".mp4" #this assumes the exported format is MP4.
			$targetItem = Get-Item (Join-Path "P:\Resize Output" $transientPath) -erroraction stop
			$targetItem.LastWriteTime =  $sourceItem.LastWriteTime
			echo $targetItem.fullName
		}
		catch {
			echo "Error!"
			#echo ($sourceItem.fullName)
			# $sourceFiles[$i]
		}		
	}
} else {
	echo "Errored! Number of errored files:"
	echo $errorFiles.length
}

		#echo "source: " + $sourceFilePaths.length
		#echo $errorFiles.length
		#echo $sourceFiles.length
		#echo $operableFiles.length
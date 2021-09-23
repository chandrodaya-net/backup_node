#!/bin/bash
DATETIME=`date +%y%m%d-%H_%M_%S`
SRC=$1
DST=$2
GIVENNAME=$3
CLEANUP=$4

SRC_TAIL=$(dirname "$SRC") # Path to the source folder/file
SRC_HEAD=$(basename "$SRC") # folder/file name

showhelp(){
        echo "\n\n############################################"
        echo "# bkupscript.sh                            #"
        echo "############################################"
        echo "\nThis script will backup files/folders into a single compressed file and will store it in the current folder."
        echo "In order to work, this script needs the following four parameters in the listed order: "
        echo "\t- The full absolute path for the folder or file you want to backup."
        echo "\t- The name of the Space where you want to store the backup at (not the url, just the name)."
        echo "\t- The full absolute path name of the backup file (timestamp will be added to the beginning of the filename)\n"
	echo "\t- An optional boolean value 'true', 'false' to indicate if local back file need to be locally delete or not. (If not given the file will be delete) \n"
        echo "Example: sh bkupscript.sh /path/../testdir testSpace  /path1/path2/backupdata\n"
	echo "Example: sh bkupscript.sh /path/../testdir testSpace  /path1/path2/backupdata true\n"
}
tarandzip(){
    echo "\n##### Gathering files #####\n"
    if tar -C $SRC_TAIL -czvf $GIVENNAME-$DATETIME.tar.gz $SRC_HEAD; then
        echo "\n##### Done gathering files #####\n"
        return 0
    else
        echo "\n##### Failed to gather files #####\n"
        return 1
    fi
}
movetoSpace(){
    echo "\n##### MOVING TO SPACE #####\n"
    if s3cmd put $GIVENNAME-$DATETIME.tar.gz s3://$DST; then
        echo "\n##### Done moving files to s3://"$DST" #####\n"
        return 0
    else
        echo "\n##### Failed to move files to the Space #####\n"
        return 1
    fi
}

cleanUp(){
    echo "\n##### CLEAN UP #####\n"
    if rm $GIVENNAME-$DATETIME.tar.gz ; then
        echo "\n##### clean up file "$GIVENNAME"-"$DATETIME".tar.gz #####\n"
        return 0
    else
        echo "\n##### Failed to clean up file #####\n"
        return 1
    fi
}

if [ ! -z "$GIVENNAME" ]; then
    if tarandzip; then
        if movetoSpace; then
	  if [ "$4" != "false" ]; then
	     cleanUp
	   fi 
	else
	   showhelp
        fi
    else
        showhelp
    fi
else
    showhelp
fi

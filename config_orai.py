##########################################################################################
# BINARY NODE:
binary_node = "oraid"

##########################################################################################
# DYNAMIC CONFIG:

volume_current = "/mnt/volume_sfo3_02"
volume_new = "/mnt/orai2_volume_sfo3_03"


##########################################################################################
# STATIC CONFIG:

py_alert = "indep_node_alarm"

backup_script_path = "/root/py/backup/backup_script.sh"

# Directory where we currently store the blockchain data folder
workspace_current = "{}/workspace".format(volume_current)

# Directory where we plan to store going forward the blockchain data folder. 
workspace_new = "{}/workspace".format(volume_new)

# The following three configurations are the arguments to pass the backup_script.sh
# the full path to the folder to backup
full_path_source_data = workspace_current
# space
digital_ocean_space = "chandrodaya"
# the full path of backup folder.The zip file create by the backup script will be stored temporarily in volumne_new
full_path_backup_name = "{}/{}".format(volume_new, binary_node)

# path to the blockchain datafolder
home_path =  "{}/.{}".format(workspace_new, binary_node)

log_file_path = "/root/py/backup/logs/backup.log"
log_level = "DEBUG" # DEBUG, INFO


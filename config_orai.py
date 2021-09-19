##########################################################################################
# BINARY NODE:
binary_node = "oraid"

##########################################################################################
# DYNAMIC CONFIG:

# Directory where we currently store the blockchain data folder
workspace_current = "/mnt/......../workspace"

# Directory where we plan to store going forward the blockchain data folder. 
# It is also used to zip the current data folder to the digitalocean space
workspace_new = "/mnt/......../workspace"


##########################################################################################
# STATIC CONFIG:

py_alert = "indep_node_alarm"

backup_script_path = "/root/py/backup/backup_script.sh"
# space where we upload backup
digital_ocean_space = "chandrodaya"
full_path_source_data = "{}/.{}".format(workspace_current, binary_node)
full_path_backup_name = "{}/{}".format(workspace_new, binary_node)

# path to the blockchain datafolder
home_path =  "{}/.{}".format(workspace_new, binary_node)

log_file_path = "/root/py/backup/logs/backup.log"
log_level = "DEBUG" # DEBUG, INFO


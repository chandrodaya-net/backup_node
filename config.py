##########################################################################################
# BINARY NODE:
binary_node = "junod"

##########################################################################################
# DYNAMIC CONFIG:

# Directory where we currently store the blockchain data folder
workspace_current = "/mnt/juno1_volume_fra1_01/workspace"

# Directory where we plan to store going forward the blockchain data folder. 
# It is also used to zip the current data folder to the digitalocean space
workspace_new = "/mnt/juno_1_volume_fra1_02/workspace"

##########################################################################################
# STATIC CONFIG:


py_alert = "indep_node_alarm"

backup_script_path="/home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh"
# space where we upload backup
digital_ocean_space = "chandrodaya"
full_path_source_data = "{}/.{}".format(workspace_current, binary_node)
full_path_backup_name = "{}/{}".format(workspace_new, binary_node)

log_file_path="/home/dau/workspace/python/github.com/dauTT/backup/logs/backup.log"
log_level = "DEBUG" # DEBUG, INFO

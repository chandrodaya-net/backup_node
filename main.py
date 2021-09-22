import subprocess
from utils import create_logger
import config
import json
import version
from setuptools.sandbox import _execfile
 
logger = create_logger(config.log_file_path, __name__ , config.log_level, True)


# Directory where we currently store the blockchain data folder
def workspace_current():
    return  "{}/workspace".format(config.volume_current)


# Directory where we plan to store going forward the blockchain data folder. 
def workspace_new():
    return  "{}/workspace".format(config.volume_new)


# the full path to the folder to backup. Argument for the backup_script.sh
def full_path_source_data():
    return workspace_current()


def modifier_binary_name():
    return config.binary_node[:-1] if config.binary_node == 'junod' else config.binary_node
    
# the full path of the backup folder. Argument for the backup_script.sh
# The zip file create by the backup script will be stored temporarily in volumne_new
def full_path_backup_name():
    return  "{}/{}".format(config.volume_new, config.binary_node)

# path to the blockchain datafolder
def home_path_current():
    return "{}/.{}".format(workspace_current(), modifier_binary_name())

# path to the blockchain datafolder
def home_path_new():
    return "{}/.{}".format(workspace_new(), modifier_binary_name())


def cmd_backup_script():
    return "sh {script_path} {src} {space}  {bkup}".format(script_path=config.backup_script_path,
                                                           space=config.digital_ocean_space,
                                                           src =full_path_source_data(),
                                                           bkup=full_path_backup_name())


def s3_download(source_file):
    return "cd {volume_new}; s3cmd get s3://{space}/{src} {src} ; tar -xzvf {src} ; rm {src}".format(volume_new=config.volume_new,
                                                                                                    space=config.digital_ocean_space,
                                                                                                    src =source_file)
    

def escape_slash(name):
    return name.replace("/", "\/")


def set_home_binary_systemd_file():
    HOME_PATH_NEW = escape_slash(home_path_new()) 
    HOME = 'HOME_' + config.binary_node.upper()
    #return """sed -i "s/\"{HOME}=*.*/\"{HOME}={HOME_PATH}\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload""".format(HOME=HOME,
    return """sed -i "s/\\"{HOME}=*.*/\\"{HOME}={HOME_PATH_NEW}\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload""".format(HOME=HOME,
                                                                                                                                        HOME_PATH_NEW=HOME_PATH_NEW)


def set_home_binary_profile_file():
    HOME_PATH_NEW = escape_slash(home_path_new()) 
    HOME = 'HOME_' + config.binary_node.upper()
    # the cmd: "source . ~/.profile" does not work.
    # Therefore we have repalce with an equivalent one: ". ~/.profile"
    return """sed -i "s/{HOME}=*.*/{HOME}={HOME_PATH_NEW}/" ~/.profile ; . ~/.profile""".format(HOME=HOME,
                                                                             HOME_PATH_NEW=HOME_PATH_NEW)


def set_home_binary():
    logger.info("************** SETUP HOME BINARY ******************")
    for cmd_key in ['set_home_binary_systemd_file', 'set_home_binary_profile_file'] :
        cmd_value = get_CMD_MAP()[cmd_key]
        result = execute(cmd_value)
        if result != 0 :
            logger.info("************** SETUP FAILED! **********************")
            break 
    logger.info("************** END SETUP **************************")
    

def start_node():
    cmd = "" 
    if config.binary_node == 'oraid':
        cmd = "cd {}; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'".format(workspace_new())
    else:
        cmd = "sudo systemctl start {}".format(config.binary_node)
    return cmd 


def stop_node():
    cmd = "" 
    if config.binary_node == 'oraid':
        cmd = "docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s"
    else: 
        cmd = "sudo systemctl stop {}; sleep 2s".format(config.binary_node)
    return cmd 


def stop_remove_docker_container(): 
    if config.binary_node == 'oraid':
        raise Exception("This comd is only applicapble for orai network!")
         
    return "docker stop orai_node ; docker rm orai_node; sleep 2s" 


def delete_priv_keys():
    node_key_file = "{}/config/node_key.json".format(home_path_current())
    priv_key_file = "{}/config/priv_validator_key.json".format(home_path_current())
    priv_key_state_file = "{}/data/priv_validator_state.json".format(home_path_current())
    return "rm -f {}; rm -f {}; rm -f {}".format(node_key_file, priv_key_file, priv_key_state_file)

 
def remove_docker_container():
    return "docker rm orai_node"


def force_recreate_docker_container():
    return "cd {} ; docker-compose pull && docker-compose up -d --force-recreate".format(workspace_new())
    

def start_alert():
    return "sudo systemctl start {}".format(config.py_alert)

  
def stop_alert():
    return "sudo systemctl stop {}".format(config.py_alert)

        
def run_backup():
    logger.info("************** START BACKUP ***********************")
    for cmd_key in ['stop_node', 'delete_priv_keys', 'backup_script'] :
        if cmd_key == 'backup_script':
            cmd_value = cmd_backup_script()
        else:
            cmd_value = get_CMD_MAP()[cmd_key]
            
        result = execute(cmd_value)
        if result != 0 :
            logger.info("************** BACKUP FAILED! ***********************")
            break 
    logger.info("************** END BACKUP ***********************")


def get_CMD_MAP(): 
    CMD_MAP = { 'start_node': start_node(),
            'stop_node': stop_node(),
            'start_alert': start_alert(),
            'stop_alert': stop_alert(),
            'delete_priv_keys': delete_priv_keys(),
            'backup_script': cmd_backup_script(),
            'run_backup': 'stop_node; delete_priv_keys; backup_script',
            's3_download': s3_download("source_file?"),
            'EXIT': "exit from the program",
            'test1': 'pwd; ls',
            'test2': 'lsmaldsa',
            
        }
    
    if config.binary_node == 'oraid':
        CMD_MAP["remove_docker_container"] = remove_docker_container()
        CMD_MAP["force_recreate_docker_container"] = force_recreate_docker_container()
    else:
        CMD_MAP['set_home_binary_systemd_file'] = set_home_binary_systemd_file()
        CMD_MAP['set_home_binary_profile_file'] = set_home_binary_profile_file()
        CMD_MAP['set_home_binary'] = 'set_home_binary_systemd_file; set_home_binary_profile_file'

    return CMD_MAP


def execute(cmd):
    logger.info("\n\n********** EXECUTION START *********")
    result = None
    try:
        logger.info("EXEC CMD: {}".format(cmd))
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        logger.info(result.stdout.decode())
        logger.info("\n\n********** EXECUTION PASS! *********")
        return result.returncode 
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stdout.decode())
        logger.error("\n\n********** EXECUTION FAIL! *********")
        return (exc.returncode) 


def repl():
    while True:
        logger.info("\n********** START CMD: version={}***************\n".format(version.number))
        
        print(json.dumps(get_CMD_MAP(), sort_keys=False, indent=4))
       
        print("\nENTER A CMD_KEY:")
         
        cmd_key = input()
        if cmd_key.lower() == 'exit':
            break
        
        cmd_value = None
        if cmd_key == 's3_download':
            print("ENTER source_file:")
            source_file = input()
            cmd_value = s3_download(source_file)
        elif cmd_key == 'run_backup':
            run_backup()
        elif cmd_key == 'set_home_binary':
            set_home_binary()
        else:
            cmd_value = get_CMD_MAP().get(cmd_key, None)
            if cmd_value is None:
                logger.error('Invalid CMD_KEY={}! Try again.'.format(cmd_key))
        
        if cmd_value: 
            execute(cmd_value)
                

if __name__ == "__main__":
    repl()
    
    
import subprocess
from utils import create_logger
import config
import json
import version
from setuptools.sandbox import _execfile
 
logger = create_logger(config.log_file_path, __name__ , config.log_level, True)


def check():
    if config.binary_node != 'oraid':
        raise Exception("This comd is only applicapble for orai network!")
    

def workspace_current():
    "Directory where we currently store the blockchain data folder"
    
    return  "{}/workspace".format(config.volume_current)


def workspace_new():
    "irectory where we plan to store going forward the blockchain data folder"
    
    return  "{}/workspace".format(config.volume_new)


def full_path_source_data():
    "The full path to the folder to backup. Argument for the backup_script.sh"
    
    return workspace_current()


def modifier_binary_name():
    return config.binary_node[:-1] if config.binary_node == 'junod' else config.binary_node
    

def full_path_backup_name():
    """The full path of the backup folder. Argument for the backup_script.sh.
       The zip file create by the backup script will be stored temporarily in volumne_new
    """
    return  "{}/{}".format(config.volume_new, config.binary_node)


def home_path_current():
    "Path to the current blockchain datafolder"
    
    return "{}/.{}".format(workspace_current(), modifier_binary_name())


def home_path_new():
    "Path to the new blockchain datafolder"
    
    return "{}/.{}".format(workspace_new(), modifier_binary_name())


def backup_script(cleanup):
    """ This cmd is applicable only for all networks. 
        It upload source data to the digital ocean space.
        - cleanup: true, false (default true)
            -true: the local back file will be deleted
            -false: the local back file will not be deleted.
    """

    return "sh {script_path} {src} {space}  {bkup} {cleanup}".format(script_path=config.backup_script_path,
                                                           space=config.digital_ocean_space,
                                                           src =full_path_source_data(),
                                                           bkup=full_path_backup_name(),
                                                           cleanup=cleanup)


def s3_download(source_file):
    """This cmd is applicable only for all networks.
       It download source data file from the digital ocean space. 
    """

    return "cd {volume_new}; s3cmd get s3://{space}/{src} {src} ; tar -xzvf {src} ; rm {src}".format(volume_new=config.volume_new,
                                                                                                    space=config.digital_ocean_space,
                                                                                                    src =source_file)
    

def escape_slash(name):
    return name.replace("/", "\/")


def cmd_format(cmd_value, cmd_name, cmd_group):
    return {'cmd_keys': cmd_value, 'cmd_name': cmd_name.upper(), 'cmd_group': cmd_group}

def set_new_home_binary_systemd_file():
    "this cmd is applicable only for juno"

    HOME_PATH_NEW = escape_slash(home_path_new()) 
    HOME = 'HOME_' + config.binary_node.upper()
    cmd_value = """sed -i "s/\\"{HOME}=*.*/\\"{HOME}={HOME_PATH_NEW}\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload""".format(HOME=HOME,
                                                                                                                                        HOME_PATH_NEW=HOME_PATH_NEW)
    return cmd_format(cmd_value, 'start_cur_node', 0)


def set_new_home_binary_profile_file():
    "this cmd is applicable only for juno"

    HOME_PATH_NEW = escape_slash(home_path_new()) 
    HOME = 'HOME_' + config.binary_node.upper()
    # the cmd: "source . ~/.profile" does not work.
    # Therefore we have replaced it with an equivalent one: ". ~/.profile"
    cmd_value = """sed -i "s/{HOME}=*.*/{HOME}={HOME_PATH_NEW}/" ~/.profile ; . ~/.profile""".format(HOME=HOME,
                                                                             HOME_PATH_NEW=HOME_PATH_NEW)
    return cmd_format(cmd_value, 'set_new_home_binary_profile_file', 0) 


def start_node():
    "this cmd is applicable only for juno"
    
    cmd_value = "sudo systemctl start {}".format(config.binary_node)
    return cmd_format(cmd_value, 'start_cur_node', 0)


def _start_node(workspace):
    "this cmd is applicable only for orai"

    check()
    return "cd {}; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'".format(workspace)

    
def start_cur_node():
    "this cmd is applicable only for orai"
    
    cmd_value = _start_node(workspace_current())
    return cmd_format(cmd_value, 'start_cur_node', 0)

    
    
def start_new_node():
    "this cmd is applicable only for orai"

    cmd_value = _start_node(workspace_new())
    return cmd_format(cmd_value, 'start_new_node', 0)


def stop_node():
    "This cmd is applicable for all networks"

    cmd_value = "" 
    if config.binary_node == 'oraid':
        cmd_value = "docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s"
    else: 
        cmd_value = "sudo systemctl stop {}; sleep 2s".format(config.binary_node)
    return cmd_format(cmd_value, 'stop_node', 0)


def stop_remove_docker_container():
    "This cmd is applicable only for orai"

    check()
    cmd_value = "docker stop orai_node ; docker rm orai_node; sleep 2s" 
    return cmd_format(cmd_value, 'stop_remove_docker_container', 0)

def delete_priv_keys():
    "This cmd is applicable for all networks"

    node_key_file = "{}/config/node_key.json".format(home_path_current())
    priv_key_file = "{}/config/priv_validator_key.json".format(home_path_current())
    priv_key_state_file = "{}/data/priv_validator_state.json".format(home_path_current())
    cmd_value = "rm -f {}; rm -f {}; rm -f {}".format(node_key_file, priv_key_file, priv_key_state_file)
    return cmd_format(cmd_value, 'delete_priv_keys', 0)
 
def remove_docker_container():
    "This cmd is applicable only for orai"
    
    cmd_value = "docker rm orai_node"
    return cmd_format(cmd_value, 'remove_docker_container', 0)


def force_recreate_docker_container(workspace):
    "This cmd is applicable only for orai"

    return "cd {} ; docker-compose pull && docker-compose up -d --force-recreate".format(workspace)

def force_recreate_cur_docker_container():
    "This cmd is applicable only for orai"
    
    cmd_value = force_recreate_docker_container(workspace_current())
    return cmd_format(cmd_value, 'force_recreate_cur_docker_container', 0)


def force_recreate_new_docker_container():
    "This cmd is applicable only for orai"
    
    cmd_value = force_recreate_docker_container(workspace_new())
    return cmd_format(cmd_value, 'force_recreate_new_docker_container', 0)


def start_alert():
    "This cmd is applicable for all networks"

    cmd_value = "sudo systemctl start indep_node_alarm"
    return cmd_format(cmd_value, 'start_alert', 0)


def stop_alert():
    "This cmd is applicable for all networks"

    return {'cmd_keys': "sudo systemctl stop indep_node_alarm", 
            'cmd_name': 'stop_alert'.upper(), 'cmd_group':0}

def start_signctrl():
    "This cmd is applicable only for all networks"

    cmd_value = "sudo systemctl start signctrl"
    return cmd_format(cmd_value, 'start_signctrl', 0)


def stop_signctrl():
    "This cmd is applicable only for all networks"
    
    cmd_value = "sudo systemctl stop signctrl"
    return cmd_format(cmd_value, 'stop_signctrl', 0)


def delete_signctrl_state():
    "This cmd is applicable only for all networks"

    cmd_value = "rm -f /home/signer/.signctrl/signctrl_state.json"
    return cmd_format(cmd_value, 'delete_signctrl_state', 0)

 
def set_new_home_binary():
    "this cmd is applicable only for juno"
    
    cmd_value = ['set_new_home_binary_systemd_file', 'set_new_home_binary_profile_file']
    return cmd_format(cmd_value, 'set_new_home_binary', 1)
    
    
def run_backup():
    "This cmd is applicable only for all networks"

    cmd_value = ['stop_node', 'stop_signctrl', 'delete_priv_keys', 'backup_script']
    return cmd_format(cmd_value, 'run_backup', 1)
    

def restart_node():
    "This cmd is applicable only for juno"

    cmd_value = ['delete_signctrl_state', 'start_signctrl', 'start_node']
    return cmd_format(cmd_value, 'restart_node', 1)

    
def restart_new_node():
    "This cmd is applicable only for orai"
    
    check()
    cmd_value = ['delete_signctrl_state', 'start_signctrl', 'force_recreate_new_docker_container', 'start_new_node']
    return cmd_format(cmd_value, 'restart_new_node', 1)


def restart_cur_node():
    "This cmd is applicable only for orai"
    
    check()
    cmd_value = ['delete_signctrl_state', 'start_signctrl', 'force_recreate_cur_docker_container', 'start_cur_node']
    return cmd_format(cmd_value, 'restart_cur_node', 1)
   

def run_backup_and_restart_node():
    "This cmd is applicable only for juno"
    
    cmd_value = ['run_backup', 'restart_node']
    return cmd_format(cmd_value, 'run_backup_and_restart_node', 2)
     

def run_backup_and_set_new_home_and_start_node():
    "This cmd is applicable only for juno"
    
    cmd_value = ['run_backup', 'set_new_home_binary', 'restart_node']
    return cmd_format(cmd_value, 'run_backup_and_set_new_home_and_start_node', 2)
   

def run_backup_and_restart_cur_node():
    "This cmd is applicable only for orai"

    check()
    cmd_value = ['run_backup', 'restart_cur_node']
    return cmd_format(cmd_value, 'run_backup_and_restart_cur_node', 2)


def run_backup_and_restart_new_node():
    "This cmd is applicable only for orai"

    check()
    cmd_value = ['run_backup', 'restart_new_node']
    return cmd_format(cmd_value, 'run_backup_and_restart_new_node', 2)

def display_cmd_value(cmd):
    """cmd: one of the cmd function. The output of such function is in this form:
        {cmd_keys: ...., cmd_name: ...., cmd_group:}
        
        See cmd_format fucntion.
    """
    
    if cmd == 'set_new_home_binary':
        print('stop')
        
    cmd_func = globals()[cmd]
    cmd_group = cmd_func()['cmd_group']
    
    output = ""
    cmd_value = cmd_func()['cmd_keys']
    return cmd_value if cmd_group == 0 else '; '.join(cmd_value)

    
def get_CMD_MAP(): 
    
    CMD_MAP = {}
    # common key
    cmd_keys = ['stop_node', 'stop_node', 'start_signctrl',
                 'stop_signctrl', 'delete_signctrl_state', 'start_alert',
                 'stop_alert', 'delete_priv_keys', 'run_backup']
    
    
    # network specific key
    if config.binary_node == 'oraid':
        cmd_keys = cmd_keys + ['start_cur_node', 'start_new_node', 'remove_docker_container',
                     'force_recreate_cur_docker_container', 'force_recreate_new_docker_container',
                     'restart_new_node', 'restart_cur_node', 'run_backup_and_restart_cur_node',
                     'run_backup_and_restart_new_node']
    
    else:
        cmd_keys = cmd_keys + ['start_node', 'set_new_home_binary_systemd_file',
                               'set_new_home_binary_profile_file',
                               'set_new_home_binary', 'restart_node','run_backup_and_restart_node', 
                               'run_backup_and_set_new_home_and_start_node']
    
    for cmd_key in cmd_keys:
        CMD_MAP[cmd_key] = display_cmd_value(cmd_key)
        
    CMD_MAP['backup_script'] = backup_script("cleanup?")
    CMD_MAP['s3_download'] = s3_download("source_file?")
    CMD_MAP['EXIT'] = "exit from the program"
    
    return CMD_MAP


def exec_shell_group2_cmd(cmd_keys, cmd_name):
    return _exec_shell_group_cmd(exec_shell_group1_cmd, cmd_keys, cmd_name)
    
def exec_shell_group1_cmd(cmd_keys, cmd_name):
    return _exec_shell_group_cmd(exec_shell_cmd, cmd_keys, cmd_name)
    
def exec_shell_group0_cmd(cmd_keys):
    return exec_shell_cmd(cmd_keys)

def _exec_shell_group_cmd(_exec_shell_group_cmd_, cmd_keys, cmd_name):
    logger.info("************** START {} ***********************".format(cmd_name))
    for k in cmd_keys :
        cmd_value = get_CMD_MAP()[k]    
        result = _exec_shell_group_cmd_(cmd_value)
        if result != 0 :
            logger.info("************** {} FAILED! ***********************".format(cmd_name))
            return 1 
    logger.info("************** END {} ***********************".format(cmd_name))
    return 0
    
def exec_shell_cmd(cmd):
    logger.info("\n\n********** EXEC START *********")
    result = None
    try:
        logger.info("EXEC CMD: {}".format(cmd))
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True)
        logger.info(result.stdout.decode())
        logger.info("\n\n********** EXEC PASS! *********")
        return result.returncode 
    except subprocess.CalledProcessError as exc:
        logger.error(exc.stdout.decode())
        logger.error("\n\n********** EXEC FAIL! *********")
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
        
        if cmd_value not in  get_CMD_MAP().keys():
            logger.error('Invalid CMD_KEY={}! Try again.'.format(cmd_key))   
        elif cmd_key == 's3_download':
            print("ENTER source_file:")
            source_file = input()
            cmd_value = s3_download(source_file)
            exec_shell_cmd(cmd_value)
        if cmd_key == 'backup_script':
            print("ENTER cleanup (true/false)")
            cleanup = input()
            cmd_value = backup_script(cleanup)
            exec_shell_cmd(cmd_value)
        else:
            cmd_key
            cmd_func =  globals()[cmd_key]
            cmd = cmd_func()
            group = cmd['cmd_group']
            keys = cmd['cmd_keys']
            name = cmd['cmd_name']
            if group == 0:
                exec_shell_group0_cmd(keys)
            elif group == 1:
                exec_shell_group1_cmd(keys, name)
            elif group == 2:
                exec_shell_group2_cmd(keys, name)
            else:
                logger.error('Invalid group cmd ={}! Try again.'.format(group))  
                

if __name__ == "__main__":
    repl()
    
    
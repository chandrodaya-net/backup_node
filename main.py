import subprocess
from utils import create_logger
import config
import json
 
logger = create_logger(config.log_file_path, __name__ , config.log_level, True)
   
CMD_MAP = { 'start_node': "sudo systemctl start {}".format(config.binary_node),
        'stop_node': "sudo systemctl stop {}".format(config.binary_node),
        'start_alert': "sudo systemctl start {}".format(config.py_alert),
        'stop_alert': "sudo systemctl stop {}".format(config.py_alert),
        'backup_script': 'backup_script -> the script need two input: working_dir=?, source_folder=?',
        'run_backup': 'run_backup > the script need two input: working_dir=?, source_folder=?',
        'test1': 'pwd; ls',
        'test2': 'lsmaldsa',
        'EXIT': "exit from the program"
    }


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


def cmd_backup_script(working_dir, source_folder):
    cmd_go_to_wdir = "cd  {wdir}".format(wdir=working_dir)  
    return "{wdir}; sh {script_path} {src} chandrodaya  {bkup}".format(wdir=cmd_go_to_wdir,
                                                                        script_path=config.backup_script_path,
                                                                         src =source_folder,bkup=config.backup_name)
    

def repl():
    while True:
        logger.info("\n********** START CMD ***************\n" )
        
        print(json.dumps(CMD_MAP, sort_keys=False, indent=4))
       
        print("\nENTER A CMD_KEY:")
         
        cmd_key = input()
        
        logger.info("\n {}".format(cmd_key))
        if cmd_key.lower() == 'exit':
            break
        
        if cmd_key not in ['backup_script', 'run_backup']:
            cmd_value = CMD_MAP.get(cmd_key, 'Invalid CMD_KEY={}! Try again.'.format(cmd_key))
        else: 
            print("ENTER working_dir:")
            working_dir = input()
            
            print("ENTER source_folder:")
            source_folder = input()
            
            cmd_value = cmd_backup_script(working_dir, source_folder)     
        execute(cmd_value)
        

def run_backup(working_dir, source_folder):
    logger.info("************** START BACKUP ***********************")
    for cmd_key in ['stop_node', 'backup_script'] :
        if cmd_key == 'backup_script':
            cmd_value = cmd_backup_script(working_dir, source_folder)
        else:
            cmd_value = CMD_MAP[cmd_key]
            
        result = execute(cmd_value)
        if result != 0 :
            logger.info("************** BACKUP FAILED! ***********************")
            break 
    logger.info("************** END BACKUP ***********************")
        

if __name__ == "__main__":
    repl()
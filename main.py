import subprocess
from utils import create_logger
import config
import json
import version 
 
logger = create_logger(config.log_file_path, __name__ , config.log_level, True)

def cmd_backup_script():
    return "sh {script_path} {src} {space}  {bkup}".format(script_path=config.backup_script_path,
                                                           space=config.digital_ocean_space,
                                                           src =config.full_path_source_data,
                                                           bkup=config.full_path_backup_name)

def s3_download(source_file):
    return "cd {wdir}; s3cmd get s3://{space}/{src} {src} ; tar -xzvf {src} ; rm {src} ".format(wdir=config.workspace_new,
                                                                                                    space=config.digital_ocean_space,
                                                                                                    src =source_file)

def run_backup():
    logger.info("************** START BACKUP ***********************")
    for cmd_key in ['stop_node', 'backup_script'] :
        if cmd_key == 'backup_script':
            cmd_value = cmd_backup_script()
        else:
            cmd_value = CMD_MAP[cmd_key]
            
        result = execute(cmd_value)
        if result != 0 :
            logger.info("************** BACKUP FAILED! ***********************")
            break 
    logger.info("************** END BACKUP ***********************")
    
CMD_MAP = { 'start_node': "sudo systemctl start {}".format(config.binary_node),
        'stop_node': "sudo systemctl stop {}; sleep 2s".format(config.binary_node),
        'start_alert': "sudo systemctl start {}".format(config.py_alert),
        'stop_alert': "sudo systemctl stop {}".format(config.py_alert),
        'backup_script': cmd_backup_script(),
        'run_backup': 'stop_node; backup_script',
        's3_download': s3_download("source_file?"),
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


def repl():
    while True:
        logger.info("\n********** START CMD: version={}***************\n".format(version.number))
        
        print(json.dumps(CMD_MAP, sort_keys=False, indent=4))
       
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
        else:
            cmd_value = CMD_MAP.get(cmd_key, None)
            if cmd_value is None:
                logger.error('Invalid CMD_KEY={}! Try again.'.format(cmd_key))
        
        if cmd_value: 
            execute(cmd_value)
                

if __name__ == "__main__":
    repl()
    
    
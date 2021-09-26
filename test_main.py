import unittest
import config 
import main

class TestCommon(unittest.TestCase):
    def test_workspace_current(self):
        expected_cmd = '/mnt/volume_fra1_01/workspace'
        self.assertEqual(main.workspace_current(), expected_cmd)

    def test_workspace_new(self):
        expected_cmd = '/mnt/volume_fra1_02/workspace'
        self.assertEqual(main.workspace_new(), expected_cmd)
    
    def test_full_path_source_data(self):
        expected_cmd = '/mnt/volume_fra1_01/workspace'
        self.assertEqual(main.full_path_source_data(), expected_cmd)
        
    def test_start_signctrl(self):
        expected_cmd = 'sudo systemctl start signctrl'
        self.assertEqual(main.display_cmd_value('start_signctrl'), expected_cmd)
    
    def test_stop_signctrl(self):
        expected_cmd = 'sudo systemctl stop signctrl'
        self.assertEqual(main.display_cmd_value('stop_signctrl'), expected_cmd)
    
    def testdelete_signctrl_state(self):
        expected_cmd = 'rm -f /home/signer/.signctrl/signctrl_state.json'
        self.assertEqual(main.display_cmd_value('delete_signctrl_state'), expected_cmd)

    def test_start_alert(self):
        expected_cmd = 'sudo systemctl start indep_node_alarm'
        self.assertEqual(main.display_cmd_value('start_alert'), expected_cmd)
    
    def test_stop_alert(self):
        expected_cmd = 'sudo systemctl stop indep_node_alarm'
        self.assertEqual(main.display_cmd_value('stop_alert'), expected_cmd)
    
    def test_CMD_MAP_INVARIANT(self):
        expected_CMD_MAP = {
                             'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'start_signctrl': 'sudo systemctl start signctrl', 
                            'stop_signctrl': 'sudo systemctl stop signctrl', 
                             'delete_signctrl_state': 'rm -f /home/signer/.signctrl/signctrl_state.json',
                            'run_backup_keep_local_copy': 'stop_node; stop_signctrl; delete_priv_keys; backup_script_and_keep_local_copy; unzip_new_file; delete_repo_outdated_files', 
                            'run_backup_delete_local_copy': 'stop_node; stop_signctrl; delete_priv_keys; backup_script_and_delete_local_copy; delete_repo_outdated_files',
                            'run_backup_and_restart_cur_node': 'run_backup; restart_cur_node',
                            'run_backup_and_restart_new_node': 'run_backup_keep_local_copy; restart_new_node',
                             's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?',                   
                             'delete_repo_file': 's3cmd rm  s3://chandrodaya/file_name?',
                            'EXIT': 'Exit from the program', 
                           
                           }
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in main.CMD_KEY_INVARIANT:
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])


class TestMainJuno(unittest.TestCase):
    
    def setUp(self):
        config.binary_node = "junod"
    
    def test_modifier_binary_name(self):
        expected_cmd = 'juno'
        self.assertEqual(main.modifier_binary_name(), expected_cmd)
        
    def test_full_path_backup_name(self):
        expected_cmd = '/mnt/volume_fra1_02/junod'
        self.assertEqual(main.full_path_backup_name(), expected_cmd)
    
    def test_home_path_current(self):
        expected_cmd = '/mnt/volume_fra1_01/workspace/.juno'
        self.assertEqual(main.home_path_current(), expected_cmd)
    
    def test_home_path_new(self):
        expected_cmd = '/mnt/volume_fra1_02/workspace/.juno'
        self.assertEqual(main.home_path_new(), expected_cmd)
    
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_node': 'sudo systemctl start junod', 
                            'stop_node': 'sudo systemctl stop junod; sleep 2s', 
                            'restart_node': 'delete_signctrl_state; start_signctrl; start_node',
                            'restart_new_node': 'set_new_home_binary; restart_node',
                            'restart_cur_node': 'restart_node',
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod cleanup?', 
                            'backup_script_and_keep_local_copy': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod false', 
                            'backup_script_and_delete_local_copy': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod true',
                            'unzip_new_file': 'cd /mnt/volume_fra1_02; numberFiles=$(ls | wc -l); if (($numberFiles > 1 )); then echo "There are too many file to unzip!" ;else fileName=`ls $junod*.gz`; tar -xzvf $fileName ; rm $fileName  ;fi',
                            'set_new_home_binary_systemd_file': 'sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_new_home_binary_profile_file': 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno/" ~/.profile ; . ~/.profile', 
                            'set_new_home_binary': 'set_new_home_binary_systemd_file; set_new_home_binary_profile_file', 
                            'list_repository_files': 's3cmd ls s3://chandrodaya/junod*',
                            'delete_repo_outdated_files': """numberFiles=$(s3cmd ls s3://chandrodaya/junod* | wc -l) ; if (($numberFiles > 2 )); then s3cmd ls s3://chandrodaya/junod* | sort -r | tail -n $(expr $numberFiles - 2) | grep -E -o "s3://chandrodaya/.*" | while read file; do s3cmd rm $file; done; else echo "there are NO files to delete"; fi""",
                            }
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            if key not in main.CMD_KEY_INVARIANT:
                self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        
        for key in expected_CMD_MAP.keys():
            if key not in actual_CMD_MAP.keys() and key not in main.CMD_KEY_INVARIANT:
                print(key)
                  
        self.assertEqual(len(actual_CMD_MAP.keys()), len(main.CMD_KEY_INVARIANT) + len(expected_CMD_MAP.keys()))
            
            
class TestMainOrai(unittest.TestCase):
    
    def setUp(self):
        config.binary_node='oraid'
        
    def test_modifier_binary_name(self):
        expected_cmd = 'oraid'
        self.assertEqual(main.modifier_binary_name(), expected_cmd)
        
    def test_full_path_backup_name(self):
        expected_cmd = '/mnt/volume_fra1_02/oraid'
        self.assertEqual(main.full_path_backup_name(), expected_cmd)
    
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_new_node': "cd /mnt/volume_fra1_02/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'", 
                            'start_cur_node': "cd /mnt/volume_fra1_01/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'",
                            'restart_new_node': 'delete_signctrl_state; start_signctrl; force_recreate_new_docker_container; start_new_node',
                            'restart_cur_node': 'delete_signctrl_state; start_signctrl; force_recreate_cur_docker_container; start_cur_node',
                            'stop_node': 'docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s',
                            'remove_docker_container': 'docker rm orai_node',
                            'force_recreate_new_docker_container': 'cd /mnt/volume_fra1_02/workspace ; docker-compose pull && docker-compose up -d --force-recreate',
                            'force_recreate_cur_docker_container': 'cd /mnt/volume_fra1_01/workspace ; docker-compose pull && docker-compose up -d --force-recreate',
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.oraid/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid cleanup?', 
                            'backup_script_and_keep_local_copy': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid false', 
                            'backup_script_and_delete_local_copy': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid true',
                            'unzip_new_file': 'cd /mnt/volume_fra1_02; numberFiles=$(ls | wc -l); if (($numberFiles > 1 )); then echo "There are too many file to unzip!" ;else fileName=`ls $junod*.gz`; tar -xzvf $fileName ; rm $fileName  ;fi',
                           'list_repository_files': 's3cmd ls s3://chandrodaya/oraid*',
                            'delete_repo_outdated_files': """numberFiles=$(s3cmd ls s3://chandrodaya/oraid* | wc -l) ; if (($numberFiles > 2 )); then s3cmd ls s3://chandrodaya/oraid* | sort -r | tail -n $(expr $numberFiles - 2) | grep -E -o "s3://chandrodaya/.*" | while read file; do s3cmd rm $file; done; else echo "there are NO files to delete"; fi""",
                            
                           
                           }
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            if key not in main.CMD_KEY_INVARIANT:
                self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        
        for key in expected_CMD_MAP.keys():
            if key not in actual_CMD_MAP.keys() and key not in main.CMD_KEY_INVARIANT:
                print(key)
                  
        self.assertEqual(len(actual_CMD_MAP.keys()), len(main.CMD_KEY_INVARIANT) + len(expected_CMD_MAP.keys()))
        
      
        

if __name__ == '__main__':
    unittest.main()
    
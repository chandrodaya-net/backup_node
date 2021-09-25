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

    def test_backup_script_cleanup(self):
        expected_cmd = 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/noded true'
        self.assertEqual(main.display_cmd_value('backup_script'), expected_cmd)

    
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
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'start_signctrl': 'sudo systemctl start signctrl', 
                            'stop_signctrl': 'sudo systemctl stop signctrl', 
                            'delete_signctrl_state': 'rm -f /home/signer/.signctrl/signctrl_state.json',
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod cleanup?', 
                            'run_backup': 'stop_node; stop_signctrl; delete_priv_keys; backup_script; delete_outdated_repo_files', 
                            'run_backup_and_restart_cur_node': 'run_backup; restart_cur_node', 
                            'run_backup_and_restart_new_node' : 'run_backup; restart_new_node',
                            'run_backup_and_set_new_home_and_start_node': 'run_backup; set_new_home_binary; restart_node',
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'set_new_home_binary_systemd_file': 'sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_new_home_binary_profile_file': 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno/" ~/.profile ; . ~/.profile', 
                            'set_new_home_binary': 'set_new_home_binary_systemd_file; set_new_home_binary_profile_file', 
                            'list_repository_files': 's3cmd ls s3://chandrodaya/junod*',
                            'delete_outdated_repo_files': """numberFiles=$(s3cmd ls s3://chandrodaya/junod* | wc -l) ; if (($numberFiles > 2 )); then s3cmd ls s3://chandrodaya/junod* | sort -r | tail -n $(expr $numberFiles - 2) | grep -E -o "s3://chandrodaya/.*" | while read file; do s3cmd rm $file; done; else echo "there are NO files to delete"; fi""",
                            'delete_repo_file': 's3cmd rm  s3://chandrodaya/file_name?',
                            'EXIT': 'exit from the program', 
                            }
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
            
            
            
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
                            'stop_node': 'docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s',
                            'remove_docker_container': 'docker rm orai_node',
                            'force_recreate_new_docker_container': 'cd /mnt/volume_fra1_02/workspace ; docker-compose pull && docker-compose up -d --force-recreate',
                            'force_recreate_cur_docker_container': 'cd /mnt/volume_fra1_01/workspace ; docker-compose pull && docker-compose up -d --force-recreate',
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'start_signctrl': 'sudo systemctl start signctrl', 
                            'stop_signctrl': 'sudo systemctl stop signctrl', 
                            'delete_signctrl_state': 'rm -f /home/signer/.signctrl/signctrl_state.json',
                            'restart_new_node': 'delete_signctrl_state; start_signctrl; force_recreate_new_docker_container; start_new_node',
                             'restart_cur_node': 'delete_signctrl_state; start_signctrl; force_recreate_cur_docker_container; start_cur_node',
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.oraid/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid cleanup?', 
                            'run_backup': 'stop_node; stop_signctrl; delete_priv_keys; backup_script; delete_outdated_repo_files', 
                            'run_backup_and_restart_cur_node': 'run_backup; restart_cur_node',
                            'run_backup_and_restart_new_node': 'run_backup; restart_new_node',
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'list_repository_files': 's3cmd ls s3://chandrodaya/oraid*',
                            'delete_outdated_repo_files': """numberFiles=$(s3cmd ls s3://chandrodaya/oraid* | wc -l) ; if (($numberFiles > 2 )); then s3cmd ls s3://chandrodaya/oraid* | sort -r | tail -n $(expr $numberFiles - 2) | grep -E -o "s3://chandrodaya/.*" | while read file; do s3cmd rm $file; done; else echo "there are NO files to delete"; fi""",
                            'delete_repo_file': 's3cmd rm  s3://chandrodaya/file_name?',
                            'EXIT': 'exit from the program', 
                           
                           }
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        

if __name__ == '__main__':
    unittest.main()
    
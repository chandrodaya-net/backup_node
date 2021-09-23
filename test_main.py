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
        self.assertEqual(main.backup_script("true"), expected_cmd)

    
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
        
    def test_start_node(self):
        expected_cmd = 'sudo systemctl start junod'
        self.assertEqual(main.display_cmd_value('start_node'), expected_cmd)
    
    def test_stop_node(self):
        expected_cmd = 'sudo systemctl stop junod; sleep 2s'
        self.assertEqual(main.display_cmd_value('stop_node'), expected_cmd)

    def test_delete_priv_keys(self):
        expected_cmd = 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json'
        self.assertEqual(main.display_cmd_value('delete_priv_keys'), expected_cmd)

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
        
    def test_set_new_home_binary_systemd_file(self):
        expected_cmd = """sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\/mnt\/volume_fra1_02\/workspace\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
        # exact shell cmd:
        # print(expected_cmd)
        self.assertEqual(main.display_cmd_value('set_new_home_binary_systemd_file'), expected_cmd)
        
    def test_set_new_home_binary_profile_file(self):
        expected_cmd = 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\/mnt\/volume_fra1_02\/workspace\/.juno/" ~/.profile ; . ~/.profile'
        self.assertEqual(main.display_cmd_value('set_new_home_binary_profile_file'), expected_cmd)
        
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_node': 'sudo systemctl start junod', 
                            'stop_node': 'sudo systemctl stop junod; sleep 2s', 
                            'restart_node': 'delete_signctrl_state; start_signctrl; start_node',
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'start_signctrl': 'sudo systemctl start signctrl', 
                            'stop_signctrl': 'sudo systemctl stop signctrl', 
                            'delete_signctrl_state': 'rm -f /home/signer/.signctrl/signctrl_state.json',
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod cleanup?', 
                            'run_backup': 'stop_node; stop_signctrl; delete_priv_keys; backup_script', 
                            'run_backup_and_restart_node': 'run_backup; restart_node', 
                            'run_backup_and_set_new_home_and_start_node': 'run_backup; set_new_home_binary; restart_node',
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'set_new_home_binary_systemd_file': 'sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_new_home_binary_profile_file': 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno/" ~/.profile ; . ~/.profile', 
                            'set_new_home_binary': 'set_new_home_binary_systemd_file; set_new_home_binary_profile_file', 
                            'EXIT': 'exit from the program', 
                            'test1': 'pwd; ls', 
                            'test2': 'lsmaldsa'}
        
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
    
    # Following test are actually not needed
    # def test_home_path_current(self):
    #    expected_cmd = '/mnt/volume_fra1_01/workspace/.oraid'
    #    self.assertEqual(main.home_path_current(), expected_cmd)
        
    # Following test are actually not needed
    # def test_home_path_new(self):
    #    expected_cmd = '/mnt/volume_fra1_02/workspace/.oraid'
    #    self.assertEqual(main.home_path_new(), expected_cmd)
       
    def test_start_new_node(self):
        expected_cmd = "cd /mnt/volume_fra1_02/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'"
        self.assertEqual(main.display_cmd_value('start_new_node'), expected_cmd)
        
    def test_start_cur_node(self):
        expected_cmd = "cd /mnt/volume_fra1_01/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'"
        self.assertEqual(main.display_cmd_value('start_cur_node'), expected_cmd)
    
    def test_stop_node(self):
        expected_cmd = 'docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s'
        self.assertEqual(main.display_cmd_value('stop_node'), expected_cmd)
        
    def test_delete_priv_keys(self):
        expected_cmd = 'rm -f /mnt/volume_fra1_01/workspace/.oraid/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/data/priv_validator_state.json'
        self.assertEqual(main.display_cmd_value('delete_priv_keys'), expected_cmd)
        
    def test_remove_docker_container(self):
        expected_cmd = 'docker rm orai_node'
        self.assertEqual(main.display_cmd_value('remove_docker_container'), expected_cmd)
        
    def test_force_recreate_new_docker_container(self):
        expected_cmd = 'cd /mnt/volume_fra1_02/workspace ; docker-compose pull && docker-compose up -d --force-recreate' 
        self.assertEqual(main.display_cmd_value('force_recreate_new_docker_container'), expected_cmd)
        

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
    
    # Following test are actually not needed  
    #def test_set_new_home_binary_systemd_file(self):
    #    expected_cmd = """sed -i "s/\\"HOME_ORAID=*.*/\\"HOME_ORAID=\/mnt\/volume_fra1_02\/workspace\/.oraid\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
    #    self.assertEqual(main.set_new_home_binary_systemd_file(), expected_cmd)
    
    # Following test are actually not needed   
    #def test_set_new_home_binary_profile_file(self):
    #    expected_cmd = 'sed -i "s/HOME_ORAID=*.*/HOME_ORAID=\/mnt\/volume_fra1_02\/workspace\/.oraid/" ~/.profile ; . ~/.profile'
    #    self.assertEqual(main.set_new_home_binary_profile_file(), expected_cmd)
        
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
                            'run_backup': 'stop_node; stop_signctrl; delete_priv_keys; backup_script', 
                            'run_backup_and_restart_cur_node': 'run_backup; restart_cur_node',
                            'run_backup_and_restart_new_node': 'run_backup; restart_new_node',
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                             'EXIT': 'exit from the program', 
                            'test1': 'pwd; ls', 
                            'test2': 'lsmaldsa'}
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        

if __name__ == '__main__':
    unittest.main()
    
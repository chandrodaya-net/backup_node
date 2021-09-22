import unittest
import config 
import main

class TestPah(unittest.TestCase):
    def test_workspace_current(self):
        expected_cmd = '/mnt/volume_fra1_01/workspace'
        self.assertEqual(main.workspace_current(), expected_cmd)

    def test_workspace_new(self):
        expected_cmd = '/mnt/volume_fra1_02/workspace'
        self.assertEqual(main.workspace_new(), expected_cmd)
    
    def test_full_path_source_data(self):
        expected_cmd = '/mnt/volume_fra1_01/workspace'
        self.assertEqual(main.full_path_source_data(), expected_cmd)
    
    
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
        self.assertEqual(main.start_node(), expected_cmd)
    
    def test_stop_node(self):
        expected_cmd = 'sudo systemctl stop junod; sleep 2s'
        self.assertEqual(main.stop_node(), expected_cmd)
    
    def test_start_alert(self):
        expected_cmd = 'sudo systemctl start indep_node_alarm'
        self.assertEqual(main.start_alert(), expected_cmd)
    
    def test_stop_alert(self):
        expected_cmd = 'sudo systemctl stop indep_node_alarm'
        self.assertEqual(main.stop_alert(), expected_cmd)
    
    def test_delete_priv_keys(self):
        expected_cmd = 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json'
        self.assertEqual(main.delete_priv_keys(), expected_cmd)
    
    def test_cmd_backup_script(self):
        expected_cmd = 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod'
        self.assertEqual(main.cmd_backup_script(), expected_cmd)

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
        
    def test_set_home_binary_systemd_file(self):
        expected_cmd = """sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\/mnt\/volume_fra1_02\/workspace\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
        # exact shell cmd:
        # print(expected_cmd)
        self.assertEqual(main.set_home_binary_systemd_file(), expected_cmd)
        
    def test_set_home_binary_profile_file(self):
        expected_cmd = 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\/mnt\/volume_fra1_02\/workspace\/.juno/" ~/.profile ; . ~/.profile'
        self.assertEqual(main.set_home_binary_profile_file(), expected_cmd)
        
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_node': 'sudo systemctl start junod', 
                            'stop_node': 'sudo systemctl stop junod; sleep 2s', 
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.juno/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.juno/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/junod', 
                            'run_backup': 'stop_node; delete_priv_keys; backup_script', 
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'set_home_binary_systemd_file': 'sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_home_binary_profile_file': 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\\/mnt\\/volume_fra1_02\\/workspace\\/.juno/" ~/.profile ; . ~/.profile', 
                            'set_home_binary': 'set_home_binary_systemd_file; set_home_binary_profile_file', 
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
       
    def test_start_node(self):
        expected_cmd = "cd /mnt/volume_fra1_02/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'"
        self.assertEqual(main.start_node(), expected_cmd)
    
    def test_stop_node(self):
        expected_cmd = 'docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s'
        self.assertEqual(main.stop_node(), expected_cmd)
        
    def test_delete_priv_keys(self):
        expected_cmd = 'rm -f /mnt/volume_fra1_01/workspace/.oraid/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/data/priv_validator_state.json'
        self.assertEqual(main.delete_priv_keys(), expected_cmd)
        
    def test_remove_docker_container(self):
        expected_cmd = 'docker rm orai_node'
        self.assertEqual(main.remove_docker_container(), expected_cmd)
        
    def test_force_recreate_docker_container(self):
        expected_cmd = 'cd /mnt/volume_fra1_02/workspace ; docker-compose pull && docker-compose up -d --force-recreate' 
        self.assertEqual(main.force_recreate_docker_container(), expected_cmd)
        
    def test_start_alert(self):
        expected_cmd = 'sudo systemctl start indep_node_alarm'
        self.assertEqual(main.start_alert(), expected_cmd)
    
    def test_stop_alert(self):
        expected_cmd = 'sudo systemctl stop indep_node_alarm'
        self.assertEqual(main.stop_alert(), expected_cmd)

    def test_cmd_backup_script(self):
        expected_cmd = 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid'
        self.assertEqual(main.cmd_backup_script(), expected_cmd)

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
    
    # Following test are actually not needed  
    #def test_set_home_binary_systemd_file(self):
    #    expected_cmd = """sed -i "s/\\"HOME_ORAID=*.*/\\"HOME_ORAID=\/mnt\/volume_fra1_02\/workspace\/.oraid\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
    #    self.assertEqual(main.set_home_binary_systemd_file(), expected_cmd)
    
    # Following test are actually not needed   
    #def test_set_home_binary_profile_file(self):
    #    expected_cmd = 'sed -i "s/HOME_ORAID=*.*/HOME_ORAID=\/mnt\/volume_fra1_02\/workspace\/.oraid/" ~/.profile ; . ~/.profile'
    #    self.assertEqual(main.set_home_binary_profile_file(), expected_cmd)
        
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_node': "cd /mnt/volume_fra1_02/workspace; docker-compose restart orai && docker-compose exec -d orai bash -c 'oraivisor start --p2p.pex false'", 
                            'stop_node': 'docker stop orai_node ; sleep 1s; docker rm orai_node; sleep 1s',
                            'remove_docker_container': 'docker rm orai_node',
                            'force_recreate_docker_container': 'cd /mnt/volume_fra1_02/workspace ; docker-compose pull && docker-compose up -d --force-recreate',
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'delete_priv_keys': 'rm -f /mnt/volume_fra1_01/workspace/.oraid/config/node_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/config/priv_validator_key.json; rm -f /mnt/volume_fra1_01/workspace/.oraid/data/priv_validator_state.json' ,
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/volume_fra1_01/workspace chandrodaya  /mnt/volume_fra1_02/oraid', 
                            'run_backup': 'stop_node; delete_priv_keys; backup_script', 
                            's3_download': 'cd /mnt/volume_fra1_02; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                             'EXIT': 'exit from the program', 
                            'test1': 'pwd; ls', 
                            'test2': 'lsmaldsa'}
        
        actual_CMD_MAP = main.get_CMD_MAP()
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        

if __name__ == '__main__':
    unittest.main()
    
import unittest
import config 
import main
import importlib

class TestMainJuno(unittest.TestCase):

    def test_cmd_backup_script(self):
        expected_cmd = 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/juno1_volume_fra1_01/workspace/.junod chandrodaya  /mnt/juno_1_volume_fra1_02/workspace/junod'
        self.assertEqual(main.cmd_backup_script(), expected_cmd)

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/juno_1_volume_fra1_02/workspace; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
        
    def test_set_home_binary_systemd_file(self):
        expected_cmd = """sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\/mnt\/juno_1_volume_fra1_02\/workspace\/.junod\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
        # exact shell cmd:
        # print(expected_cmd)
        self.assertEqual(main.set_home_binary_systemd_file(), expected_cmd)
        
    def test_set_home_binary_profile_file(self):
        expected_cmd = 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\/mnt\/juno_1_volume_fra1_02\/workspace\/.junod/" ~/.profile ; . ~/.profile'
        self.assertEqual(main.set_home_binary_profile_file(), expected_cmd)
        
    def test_CMD_MAP(self):
        expected_CMD_MAP = {'start_node': 'sudo systemctl start junod', 
                            'stop_node': 'sudo systemctl stop junod; sleep 2s', 
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/juno1_volume_fra1_01/workspace/.junod chandrodaya  /mnt/juno_1_volume_fra1_02/workspace/junod', 
                            'run_backup': 'stop_node; backup_script', 
                            's3_download': 'cd /mnt/juno_1_volume_fra1_02/workspace; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'set_home_binary_systemd_file': 'sed -i "s/\\"HOME_JUNOD=*.*/\\"HOME_JUNOD=\\/mnt\\/juno_1_volume_fra1_02\\/workspace\\/.junod\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_home_binary_profile_file': 'sed -i "s/HOME_JUNOD=*.*/HOME_JUNOD=\\/mnt\\/juno_1_volume_fra1_02\\/workspace\\/.junod/" ~/.profile ; . ~/.profile', 
                            'set_home_binary': 'set_home_binary_systemd_file; set_home_binary_profile_file', 
                            'EXIT': 'exit from the program', 
                            'test1': 'pwd; ls', 
                            'test2': 'lsmaldsa'}
        
        actual_CMD_MAP = main.CMD_MAP
        
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
            
            
            
class TestMainOrai(unittest.TestCase):
    
    def setUp(self):
        config.binary_node='oraid'
        
        
        config.full_path_source_data = "{}/.{}".format(config.workspace_current, config.binary_node)
        config.full_path_backup_name = "{}/{}".format(config.workspace_new, config.binary_node)

        # path to the blockchain datafolder
        config.home_path =  "{}/.{}".format(config.workspace_new, config.binary_node)

        importlib.reload(main)

    def test_cmd_backup_script(self):
        expected_cmd = 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/juno1_volume_fra1_01/workspace/.oraid chandrodaya  /mnt/juno_1_volume_fra1_02/workspace/oraid'
        self.assertEqual(main.cmd_backup_script(), expected_cmd)

    def test_s3_download(self):
        expected_cmd = 'cd /mnt/juno_1_volume_fra1_02/workspace; s3cmd get s3://chandrodaya/file.tar.gz file.tar.gz ; tar -xzvf file.tar.gz ; rm file.tar.gz'
        self.assertEqual(main.s3_download("file.tar.gz"), expected_cmd)
        
    def test_set_home_binary_systemd_file(self):
        expected_cmd = """sed -i "s/\\"HOME_ORAID=*.*/\\"HOME_ORAID=\/mnt\/juno_1_volume_fra1_02\/workspace\/.oraid\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload"""
        # exact shell cmd:
        # print(expected_cmd)
        self.assertEqual(main.set_home_binary_systemd_file(), expected_cmd)
        
    def test_set_home_binary_profile_file(self):
        expected_cmd = 'sed -i "s/HOME_ORAID=*.*/HOME_ORAID=\/mnt\/juno_1_volume_fra1_02\/workspace\/.oraid/" ~/.profile ; . ~/.profile'
        self.assertEqual(main.set_home_binary_profile_file(), expected_cmd)
        
    def test_CMD_MAP(self):
        
        expected_CMD_MAP = {'start_node': 'sudo systemctl start oraid', 
                            'stop_node': 'sudo systemctl stop oraid; sleep 2s', 
                            'start_alert': 'sudo systemctl start indep_node_alarm', 
                            'stop_alert': 'sudo systemctl stop indep_node_alarm', 
                            'backup_script': 'sh /home/dau/workspace/python/github.com/dauTT/backup/backup_script.sh /mnt/juno1_volume_fra1_01/workspace/.oraid chandrodaya  /mnt/juno_1_volume_fra1_02/workspace/oraid', 
                            'run_backup': 'stop_node; backup_script', 
                            's3_download': 'cd /mnt/juno_1_volume_fra1_02/workspace; s3cmd get s3://chandrodaya/source_file? source_file? ; tar -xzvf source_file? ; rm source_file?', 
                            'set_home_binary_systemd_file': 'sed -i "s/\\"HOME_ORAID=*.*/\\"HOME_ORAID=\\/mnt\\/juno_1_volume_fra1_02\\/workspace\\/.oraid\\"/" /etc/systemd/system/junod.service; sudo systemctl daemon-reload', 
                            'set_home_binary_profile_file': 'sed -i "s/HOME_ORAID=*.*/HOME_ORAID=\\/mnt\\/juno_1_volume_fra1_02\\/workspace\\/.oraid/" ~/.profile ; . ~/.profile', 
                            'set_home_binary': 'set_home_binary_systemd_file; set_home_binary_profile_file', 
                            'EXIT': 'exit from the program', 
                            'test1': 'pwd; ls', 
                            'test2': 'lsmaldsa'}
        
        actual_CMD_MAP = main.CMD_MAP
        
        for key in actual_CMD_MAP.keys():
            self.assertEqual(actual_CMD_MAP[key], expected_CMD_MAP[key])
        

if __name__ == '__main__':
    unittest.main()
    
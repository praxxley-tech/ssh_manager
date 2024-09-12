import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os
import ssh_managment

class TestSSHManagement(unittest.TestCase):

    @patch('subprocess.run')
    def test_start_ssh_agent_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        result = ssh_managment.start_ssh_agent()
        self.assertTrue(result)
        mock_run.assert_called_once_with('start-ssh-agent.cmd', shell=True, check=True)

    @patch('subprocess.run')
    def test_start_ssh_agent_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'start-ssh-agent.cmd')
        result = ssh_managment.start_ssh_agent()
        self.assertFalse(result)
        mock_run.assert_called_once_with('start-ssh-agent.cmd', shell=True, check=True)

    @patch('os.listdir')
    @patch('subprocess.run')
    def test_add_ssh_key_success(self, mock_run, mock_listdir):
        mock_listdir.return_value = ['id_rsa', 'id_rsa.pub']
        mock_run.return_value = MagicMock(returncode=0)
        key_path = '/home/runner/.ssh/id_rsa'

        with patch('ssh_managment.get_user_input', return_value='1'): 
            selected_key = ssh_managment.add_ssh_key()
        
        self.assertEqual(selected_key, 'id_rsa')
        mock_run.assert_called_once_with(f'ssh-add {key_path}', shell=True, check=True)

    @patch('os.listdir')
    @patch('subprocess.run')
    def test_add_ssh_key_failure(self, mock_run, mock_listdir):
        mock_listdir.return_value = ['id_rsa', 'id_rsa.pub']
        mock_run.side_effect = subprocess.CalledProcessError(1, 'ssh-add /home/runner/.ssh/id_rsa')
        key_path = '/home/runner/.ssh/id_rsa'

        with patch('ssh_managment.get_user_input', return_value='1'):  
            selected_key = ssh_managment.add_ssh_key()
        
        self.assertIsNone(selected_key)
        mock_run.assert_called_once_with(f'ssh-add {key_path}', shell=True, check=True)

    @patch('builtins.print')
    @patch('ssh_managment.get_user_input', side_effect=['1'])
    @patch('csv.reader')
    @patch('subprocess.run')
    @patch('os.listdir')
    def test_main_script_flow(self, mock_listdir, mock_run, mock_csv_reader, mock_input, mock_print):
        mock_listdir.return_value = ['id_rsa', 'id_rsa.pub']
        mock_csv_reader.return_value = [
            ['hostname1', 'username1', 'description1'],
            ['hostname2', 'username2', 'description2']
        ]
        
        mock_run.side_effect = [MagicMock(returncode=0), MagicMock(returncode=0)]  # Two calls expected
        key_path = '/home/runner/.ssh/id_rsa'
        
        with patch('ssh_managment.add_ssh_key', return_value='id_rsa'):
            ssh_managment.main_script()
        
        mock_print.assert_any_call("Ausgewählter Hostname: hostname1, Username: username1")
        mock_run.assert_any_call('start-ssh-agent.cmd', shell=True, check=True)
        mock_run.assert_any_call(f'ssh username1@hostname1', shell=True)

if __name__ == '__main__':
    unittest.main()
    
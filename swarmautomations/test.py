import unittest

import pandas as pd

from swarmautomations.main import MainClass
from swarmautomations.config import active_config as config
from eigenlib.utils.project_setup import ProjectSetupClass
ProjectSetupClass(project_folder='swarm-automations', test_environ=True)

class TestMain(unittest.TestCase):
    def setUp(self):
        self.main = MainClass(config)
        self.config = config

    def test_computer_use_automation(self):
        self.main.computer_use_automation(self.config)

    def test_standby(self):
        self.main.standby(self.config)

    def test_call_to_notion(self):
        self.main.call_to_notion(self.config)

    def test_listen_smartwatch_notes(self):
        self.main.listen_smartwatch_notes(self.config)

    def test_youtube_to_notion(self):
        self.main.youtube_to_notion(self.config)

    @unittest.skip("Slow test")
    def test_podcast_generation(self):
        updated_config = self.main.podcast_generation(self.config)

    def test_personal_server_full_cycle(self):
        #LAUNCH SERVER
        self.config['password'] = 'test_pass'
        self.main.launch_personal_server(self.config)
        #LAUNCH SECURITY NODE
        def aux_fun(a, b):
            return a + b
        self.config['node_method'] = aux_fun
        self.config['master_address'] = 'tcp://localhost:5005'
        self.config['node_name'] = 'security_node'
        self.config['password'] = 'test_pass'
        self.main.launch_personal_server_node(self.config)
        #CALL SECURITY SERVER
        self.config['address_node_name'] = 'security_node'
        self.config['payload'] = {'a':1, 'b':2}
        self.config['password'] = 'test_pass'
        ################################################################################################################
        output_config = self.main.call_personal_server_node(self.config)
        print(output_config['response'])

    #-------------------------------------------------------------------------------------------------------------------
    def test_datasets_load(self):
        from eigenlib.utils.data_utils import DataUtilsClass
        import os
        ################################################################################################################
        print('RAW: ', os.listdir('./data/raw'))
        print('CURATED: ', os.listdir('./data/curated'))

        # CURATED SOURCEs
        input_dataset_name = 'test_dataset'
        df = DataUtilsClass().load_dataset(path=os.environ['CURATED_DATA_PATH'], dataset_name=input_dataset_name, format='pkl', cloud=False)
        input_dataset_name = config['seeds_dataset_name']
        df = DataUtilsClass().load_dataset(path=os.environ['CURATED_DATA_PATH'], dataset_name=input_dataset_name, format='csv', cloud=False)
        input_dataset_name = config['gen_output_dataset_name']
        df = DataUtilsClass().load_dataset(path=os.environ['CURATED_DATA_PATH'], dataset_name=input_dataset_name, format='csv', cloud=False)

    def test_call_served_LLM(self):
        class OSLLMClientClass:
            def __init__(self):
                from eigenlib.utils.nano_net import NanoNetClass
                master_address = 'tcp://95.18.166.44:5000'
                password = 'youshallnotpass'
                ################################################################################################################
                self.client_node = NanoNetClass()
                self.client_node.launch_node(node_name='client_node', node_method=None, master_address=master_address, password=password, delay=1)

            def run(self, history):
                result = self.client_node.call(address_node="phi4-serving", payload={'history': history})
                return result
        LLM = OSLLMClientClass()
        answer = LLM.run([{'role': 'user', 'content': 'De que color es el caballo blanco de santiago?'}])
        print(answer)

    #TEST UNDER DEVELOPMENT###################################################################################################################
    def test_launch_server_script(self):
        import time
        from swarmautomations.main import MainClass
        from eigenlib.utils.nano_net import NanoNetClass
        ################################################################################################################
        config = {
            'password': 'youshallnotpass',
            'master_address': 'tcp://0.0.0.0:5005'
        }
        ################################################################################################################
        NanoNetClass.kill_processes_on_port(5005)
        main = MainClass(config)
        main.launch_personal_server(config)
        while True:
            time.sleep(1)

    def test_launch_security_node(self):
        from swarmautomations.main import MainClass
        import time
        ################################################################################################################
        def encryption_aux(public_key):
            from cryptography.fernet import Fernet
            from dotenv import dotenv_values
            encryption = Fernet(public_key)
            env_vars = dotenv_values(r'C:\Users\apren\Desktop\.env')
            encrypted_vars = {k: encryption.encrypt(v.encode()).decode() for k, v in env_vars.items()}
            return encrypted_vars
        config = {
            'node_method': encryption_aux,
            'master_address': 'tcp://95.18.166.44:5005',
            'node_name': 'security_node',
            'password': 'youshallnotpass',
            'delay': 5,
        }
        ################################################################################################################
        main = MainClass(config)
        print('Security server started.')
        main.launch_personal_server_node(config)
        while True:
            time.sleep(1)

    def test_call_security_node(self):
        from swarmautomations.main import MainClass
        from cryptography.fernet import Fernet
        ################################################################################################################
        public_key = Fernet.generate_key()
        config = {
            'master_address': 'tcp://95.18.166.44:5005',
            'payload': {'public_key': public_key},
            'password': 'youshallnotpass',
            'address_node': 'security_node',
            'delay': 5,
        }
        ################################################################################################################
        main = MainClass(config)
        output_config = main.call_personal_server_node(config)
        encrypted_vars = output_config['response']
        f = Fernet(public_key)
        env_vars = {k: f.decrypt(v.encode()).decode() for k, v in encrypted_vars.items()}

        def save_env_dict(env_vars, filepath='.env'):
            with open(filepath, 'w') as f:
                for key, value in env_vars.items():
                    f.write(f'{key}={value}\n')
        save_env_dict(env_vars, filepath='.env')


if __name__ == '__main__':
    unittest.main()

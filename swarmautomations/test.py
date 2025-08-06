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

    def test_podcast_generation(self):
        updated_config = self.main.podcast_generation(self.config)

    def test_security_server_full_cycle(self):
        #LAUNCH SERVER
        self.config['password'] = 'test_pass'
        self.main.launch_personal_server(self.config)
        #LAUNCH SECURITY NODE
        def encryption_aux(public_key):
            from eigenlib.utils.encryption_utils import EncryptionUtilsClass
            EU = EncryptionUtilsClass()
            from dotenv import dotenv_values
            env_vars = str(dotenv_values('C:\\Users\\AlejandroPrendesCabo\\Desktop\\.env'))
            env_vars = 'Hola'
            encrypted_password = EU.encrypt_pass(env_vars, public_key)
            return encrypted_password
        self.config['node_method'] = encryption_aux
        self.config['master_address'] = 'tcp://localhost:5005'
        self.config['node_name'] = 'security_node'
        self.config['password'] = 'test_pass'
        self.main.launch_personal_server_node(self.config)
        #CALL SECURITY SERVER
        from eigenlib.utils.encryption_utils import EncryptionUtilsClass
        ################################################################################################################
        EU = EncryptionUtilsClass()
        public_key = EU.initialize()
        ################################################################################################################
        self.config['address_node_name'] = 'security_node'
        self.config['payload'] = {'public_key':public_key}
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
        from swarmautomations.config import active_config as config
        ################################################################################################################
        config['password'] = 'youshallnotpass'
        config['master_address'] = 'tcp://localhost:5005'
        ################################################################################################################
        main = MainClass(config)
        main.launch_personal_server(config)
        while True:
            time.sleep(1)

    def test_launch_security_node(self):
        import os
        import sys
        from swarmautomations.main import MainClass
        from swarmautomations.config import active_config as config
        import time
        # Forzar UTF-8 en Windows
        if sys.platform == 'win32':
            os.environ['PYTHONIOENCODING'] = 'utf-8'
        ################################################################################################################
        def encryption_aux(public_key):
            from eigenlib.utils.encryption_utils import EncryptionUtilsClass
            EU = EncryptionUtilsClass()
            from dotenv import dotenv_values
            env_vars = str(dotenv_values(r'C:\Users\apren\Desktop\.env'))
            encrypted_vars = EU.encrypt_pass(env_vars, public_key)
            return encrypted_vars
        config['node_method'] = encryption_aux
        config['node_ip'] = 'tcp://95.18.166.44:5005'
        config['node_name'] = 'security_node'
        config['password'] = 'youshallnotpass'
        ################################################################################################################
        main = MainClass(config)
        print('Security server started.')
        main.launch_personal_server_node(config)
        while True:
            time.sleep(1)
        pass

    def test_call_security_node(self):
        from eigenlib.utils.encryption_utils import EncryptionUtilsClass
        ################################################################################################################
        EU = EncryptionUtilsClass()
        public_key = EU.initialize()
        self.config['address_node_name'] = 'security_node'
        self.config['payload'] = {'public_key':public_key}
        self.config['password'] = 'youshallnotpass'
        ################################################################################################################
        output_config = self.main.call_personal_server_node(self.config)


if __name__ == '__main__':
    unittest.main()

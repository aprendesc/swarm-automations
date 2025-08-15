import os

from swarmautomations.main import MainClass
from swarmautomations.configs.test_config import config
import unittest

class TestMainClass(unittest.TestCase):
    def setUp(self):
        self.test_delay = 1
        self.main = MainClass({})

    def test_computer_use_automation(self):
        self.main.computer_use_automation(config)

    def test_standby(self):
        import threading
        import time
        ################################################################################################################
        standby_thread = threading.Thread(target=self.main.standby, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_call_to_notion(self):
        import threading
        import time
        ################################################################################################################
        standby_thread = threading.Thread(target=self.main.call_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_listen_smartwatch_notes(self):
        import threading
        import time
        ################################################################################################################
        standby_thread = threading.Thread(target=self.main.listen_smartwatch_notes, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_youtube_to_notion(self):
        import threading
        import time
        ################################################################################################################
        standby_thread = threading.Thread(target=self.main.youtube_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_sources_parser_and_summarizer(self):
        import threading
        import time
        ################################################################################################################
        #standby_thread = threading.Thread(target=self.main.sources_parser_and_summarizer, args=(config,), daemon=True)
        #standby_thread.start()
        #time.sleep(self.test_delay)

        #NO TRADING
        new_config = self.main.intelligent_web_search(config)
        print(new_config['result'])

    @unittest.skip("Class not functional")
    def test_podcast_generation(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.podcast_generation, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_code_interpreter(self):
        self.main.code_interpreter(config)

    def test_intelligent_web_search(self):
        new_config = self.main.intelligent_web_search(config)
        print(new_config['result'])

    def test_local_file_operations(self):
        import tempfile
        import os

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp_path = tmp.name
        try:
            # Escribir al archivo
            config_write = {
                'file_path': tmp_path,
                'mode': 'write_file',
                'content': "print('Hola desde test')"
            }
            self.main.file_operations_tools(config_write)
            # Leer del archivo
            config_read = {
                'file_path': tmp_path,
                'mode': 'read_file',
                'content': None
            }
            result = self.main.file_operations_tools(config_read)
            assert "Hola desde test" in result['result']['file_content']
            print("✅ Test pasado")
        finally:
            os.remove(tmp_path)

    def test_get_project_map(self):
        base_path = f'C:\\Users\\{os.environ["USERNAME"]}\\Desktop\\proyectos'
        target_project_folder = 'swarm-intelligence'
        ########################################################################################################################
        config['base_path'] = os.path.join(base_path, target_project_folder)
        config['root_dir'] = './'
        new_config = self.main.get_files_map(config)
        print(new_config['result']['files_map'])


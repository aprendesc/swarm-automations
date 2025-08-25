import os
import unittest
from swarmautomations.main import Main
from swarmautomations.configs.base_config import Config
import threading
import time

class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_delay = 1
        self.main = Main()
        self.cfg = Config()

    def test_standby(self):
        cfg = self.cfg.standby()
        cfg['time_interval'] = 1
        standby_thread = threading.Thread(target=self.main.standby, args=(cfg,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_call_to_notion(self):
        standby_thread = threading.Thread(target=self.main.call_to_notion, args=(self.cfg.call_to_notion(),), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_computer_use_automation(self):
        standby_thread = threading.Thread(target=self.main.computer_use_automation, args=(self.cfg.computer_use(),), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_listen_smartwatch_notes(self):
        standby_thread = threading.Thread(target=self.main.smartwatch_notes, args=(self.cfg.smartwatch_notes(),), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_youtube_to_notion(self):
        standby_thread = threading.Thread(target=self.main.youtube_to_notion, args=(self.cfg.call_to_notion(),), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_sources_parser_and_summarizer(self):
        new_config = self.main.sources_parser_and_summarizer(self.cfg.sources_parser_and_summarizer())
        self.assertIn('result', new_config)
        self.assertTrue(len(str(new_config['result'])) > 0)

    def test_podcast_generation(self):
        standby_thread = threading.Thread(target=self.main.podcast_generation, args=(self.cfg.podcast_generation(),), daemon=True)
        standby_thread.start()
        time.sleep(10)

    def test_code_interpreter(self):
        config = self.main.code_interpreter(self.cfg.code_interpreter())
        assert config['result']['output'] == 'Hola mundo!\n'

    def test_local_file_operations(self):
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp_path = tmp.name
        ################################################################################################################
        # WRITE
        update_config_write = {
            'file_path': tmp_path,
            'mode': 'write_file',
            'content': "print('Hola desde test')",
            'interpreter_launcher': r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence\.venv\Scripts\python.exe",
            'interpreter_cwd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-intelligence',
            'interpreter_path_dirs': [r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence", r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\eigenlib"],
            'programming_language': 'python',
        }
        self.main.local_file_operations_tools(self.cfg.local_file_operations(update_config_write))
        # READ
        config_read = {
            'file_path': tmp_path,
            'mode': 'read_file',
            'content': None,
            'interpreter_launcher': r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence\.venv\Scripts\python.exe",
            'interpreter_cwd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-intelligence',
            'interpreter_path_dirs': [r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence", r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\eigenlib"],
            'programming_language': 'python',
        }
        result = self.main.local_file_operations_tools(self.cfg.local_file_operations(config_read))
        self.assertIn("Hola desde test", result['result']['file_content'])
        print("✅ Local file operations test passed")
        os.remove(tmp_path)

    def test_get_files_map(self):
        new_config = self.main.get_files_map(self.cfg.get_files_map())
        self.assertIn('files_map', new_config['result'])
        print("Files map sample:", new_config['result']['files_map'][0:5])

    def test_google_search(self):
        gs_config = self.main.google_search(self.cfg.google_web_search())
        self.assertIn('result', gs_config)
        self.assertIn('urls', gs_config['result'])
        self.assertGreater(len(gs_config['result']['urls']), 0)
        print("Google search URLs:", gs_config['result']['urls'])

    def test_browse_url(self):
        gs_config = self.main.browse_url(self.cfg.browse_url())
        urls = gs_config['result']
        print(urls)

    def test_vector_database(self):
        import tempfile
        import shutil

        sample_pdf_path = './data/raw/source_papers/attention_is_all_you_need.pdf'
        temp_dir = tempfile.mkdtemp()
        dummy_pdf_path = os.path.join(temp_dir, 'dummy.pdf')
        shutil.copy(sample_pdf_path, dummy_pdf_path)

        try:
            # INITIALIZE
            update_cfg = {
                'vdb_mode': 'fit',
                'raw_sources': [dummy_pdf_path],
                'lang': 'eng',
                'vdb_name': 'test_VDB_tmp',
                'vdb_chunking_threshold': 150,
                'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',
            }
            self.main.vector_database(self.cfg.vector_database(update_cfg))
            self.assertIsNotNone(getattr(self.main, 'VDB', None))

            update_cfg = {
                'vdb_mode': 'initialize',
                'vdb_name': 'test_VDB_tmp',
                'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',
            }
            self.main.vector_database(update_cfg)
            self.assertIsNotNone(getattr(self.main, 'VDB', None))

            # RETRIEVAL
            upadete_cfg = {
                'vdb_mode': 'retrieval',
                'query': 'attention is all you need',
                'top_n': 3,
                'vdb_wd': 'C:/Users/AlejandroPrendesCabo/Desktop/proyectos/swarm-automations',

            }
            retrieval_cfg = self.main.vector_database(upadete_cfg)
            self.assertIn('result', retrieval_cfg)
            self.assertIn('sources', retrieval_cfg['result'])
            self.assertTrue(len(retrieval_cfg['result']['sources']) > 0)
            print("Vector DB retrieval sample (truncated):", str(retrieval_cfg['result']['sources'])[:200])
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_extract_info(self):
        standby_thread = threading.Thread(target=self.main.extract_info, args=(self.cfg.extract_info(),), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_dev_tools_server(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'programming_language': 'python',
            'code': 'print("Hola mundo!")',
        }
        standby_thread = threading.Thread(target=self.main.dev_tools_server, args=(self.cfg.dev_tools_server(config),), daemon=True)
        standby_thread.start()
        time.sleep(100)


import os
import unittest

from swarmautomations.main import MainClass
from swarmautomations.configs.test_config import config


class TestMainClass(unittest.TestCase):
    """Basic smoke-tests for every public method exposed in MainClass.

    The goal is not to exhaustively verify the business logic (many methods rely on
    external services / APIs) but to ensure that the new integration points do not
    raise exceptions and return a result object that can be further consumed by
    downstream calls.
    """

    def setUp(self):
        self.test_delay = 1
        # Each test gets a fresh instance to avoid potential shared-state issues.
        self.main = MainClass({})

    # ----------------------------------------------------------------------------------
    # Existing tests
    # ----------------------------------------------------------------------------------
    def test_computer_use_automation(self):
        import threading
        import time

        standby_thread = threading.Thread(target=self.main.computer_use_automation, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_standby(self):
        import threading
        import time

        standby_thread = threading.Thread(target=self.main.standby, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_call_to_notion(self):
        import threading
        import time

        standby_thread = threading.Thread(target=self.main.call_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_listen_smartwatch_notes(self):
        import threading
        import time

        standby_thread = threading.Thread(target=self.main.listen_smartwatch_notes, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_youtube_to_notion(self):
        import threading
        import time

        standby_thread = threading.Thread(target=self.main.youtube_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

    def test_sources_parser_and_summarizer(self):
        # Only exercising the intelligent_web_search part here to speed-up CI.
        new_config = self.main.sources_parser_and_summarizer(config)
        # A very lenient assertion – we just check that some textual answer is returned.
        self.assertIn('result', new_config)
        self.assertTrue(len(str(new_config['result'])) > 0)

    @unittest.skip("Class not functional")
    def test_podcast_generation(self):
        import threading
        import time
        local_cfg = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }
        standby_thread = threading.Thread(target=self.main.podcast_generation, args=(local_cfg,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_code_interpreter(self):
        new_config = self.main.code_interpreter(config)
        print(new_config['result'])

    def test_intelligent_web_search(self):
        new_config = self.main.intelligent_web_search(config)
        self.assertIn('result', new_config)
        print(new_config['result'])

    def test_google_search(self):
        gs_config = self.main.google_search(config.copy())
        self.assertIn('result', gs_config)
        self.assertIn('urls', gs_config['result'])
        self.assertGreater(len(gs_config['result']['urls']), 0)
        print("Google search URLs:", gs_config['result']['urls'])

    def test_browse_url(self):
        # First obtain a list of URLs via google_search
        gs_config = self.main.google_search(config.copy())
        urls = gs_config['result']['urls']

        # Build a new config for browsing phase
        browse_cfg = {
            'urls': urls,
            'query': config['query'],
            'summarize_search': False  # Keep it quick for the test suite
        }
        br_config = self.main.browse_url(browse_cfg)
        self.assertIn('result', br_config)
        self.assertIn('summary', br_config['result'])
        self.assertTrue(len(br_config['result']['summary']) > 0)
        print("Browse URL summary (truncated):", br_config['result']['summary'][:200])

    def test_local_file_operations(self):
        #Single test
        result = self.main.local_file_operations_tools(config)
        print(result['result'])

        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp_path = tmp.name
        try:
            # Write to the file
            config_write = {
                'file_path': tmp_path,
                'mode': 'write_file',
                'content': "print('Hola desde test')",
                'local_base_path': './'
            }
            self.main.local_file_operations_tools(config_write)

            # Read from the file
            config_read = {
                'file_path': tmp_path,
                'mode': 'read_file',
                'content': None,
                'local_base_path': './'
            }
            result = self.main.local_file_operations_tools(config_read)
            self.assertIn("Hola desde test", result['result']['file_content'])
            print("✅ Local file operations test passed")
        finally:
            os.remove(tmp_path)

    def test_get_files_map(self):
        base_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/proyectos"
        target_project_folder = 'swarm-automations'
        config['base_path'] = os.path.join(base_path, target_project_folder)
        config['root_dir'] = './'
        new_config = self.main.get_files_map(config)
        self.assertIn('files_map', new_config['result'])
        print("Files map sample:", new_config['result']['files_map'][:5])

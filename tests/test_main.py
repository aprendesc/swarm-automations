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

    def test_source_to_notion_summary(self):
        import threading
        import time
        ################################################################################################################
        standby_thread = threading.Thread(target=self.main.source_to_notion_summary, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(self.test_delay)

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
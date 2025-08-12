from swarmautomations.main import MainClass
import unittest

class TestMainClass(unittest.TestCase):
    def setUp(self):
        ################################################################################################################
        self.main = MainClass({})

    def test_computer_use_automation(self):
        ################################################################################################################
        config = {
            'instructions': """This is a test, just move a bit the mouse and finish saying OBJECTIVE ACCOMPLISHED""",
            'model': "computer-use-preview",
            'continue_action': False,
        }
        ################################################################################################################
        self.main.computer_use_automation(config)

    def test_standby(self):
        import threading
        import time
        ################################################################################################################
        config = {'time_interval': 1}
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.standby, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_call_to_notion(self):
        import threading
        import time
        ################################################################################################################
        config = {}
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.call_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_listen_smartwatch_notes(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'audio_path': 'G:/Mi unidad/utils/Easy Voice Recorder',
            'sw_notion_page': '23d2a599e98580d6b20dc30f999a1a2c'
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.listen_smartwatch_notes, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_youtube_to_notion(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'yttn_video_url': 'https://www.youtube.com/watch?v=1uX0qHQfSMg',
            'yttn_notion_page': '2432a599e985804692b7d6982895a2b2',
            'yttn_summarize': True,
            'yttn_n_sections': 5,
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.youtube_to_notion, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_source_to_notion_summary(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'source': 'Hola Mundo',
            'n_sections': 2,
            'summarizer_notion_page': '2432a599e985804692b7d6982895a2b2',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.source_to_notion_summary, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

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
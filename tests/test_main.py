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

    def test_launch_personal_server(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'master_address': 'tcp://localhost:5005',
            'password': 'test_pass',
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.launch_personal_server, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_launch_personal_server_node(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'node_name': 'test_node',
            'node_method': lambda a, b: a + b,
            'delay': 1,
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread = threading.Thread(target=self.main.launch_personal_server_node, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)

    def test_call_personal_server_node(self):
        import threading
        import time
        ################################################################################################################
        config_server = {
            'master_address': 'tcp://localhost:5005',
            'password': 'test_pass',
        }
        config_node = {
            'master_address': 'tcp://localhost:5005',
            'node_name': 'test_node',
            'password': 'test_pass',
            'node_method': lambda a, b: a + b,
            'delay': 1,
        }
        config_client = {
            'master_address': 'tcp://localhost:5005',
            'address_node': 'test_node',
            'password': 'test_pass',
            'payload': {'a': 1, 'b':2}
        }
        ################################################################################################################        standby_thread = threading.Thread(target=self.main.standby,
        standby_thread_1 = threading.Thread(target=self.main.launch_personal_server, args=(config_server,), daemon=True)
        standby_thread_1.start()
        standby_thread_2 = threading.Thread(target=self.main.launch_personal_server_node, args=(config_node,), daemon=True)
        standby_thread_2.start()
        standby_thread_3 = threading.Thread(target=self.main.launch_personal_server, args=(config_client,), daemon=True)
        standby_thread_3.start()
        time.sleep(3)
        standby_thread_1.join(timeout=0.1)
        standby_thread_2.join(timeout=0.1)
        standby_thread_3.join(timeout=0.1)

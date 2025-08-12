from swarmautomations.modules.podcast_generation import PodcastGeneration
import unittest

class TestPodcastGeneration(unittest.TestCase):
    def setUp(self):
        pass

    def test_standby(self):
        import threading
        import time
        ################################################################################################################
        config = {
            'max_iter': 15,
            'podcast_folder_path': './data/processed/podcast_pipeline_stage',
        }
        ################################################################################################################
        def aux_fun(config):
            PodcastGeneration().run(**config)
        standby_thread = threading.Thread(target=aux_fun, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)
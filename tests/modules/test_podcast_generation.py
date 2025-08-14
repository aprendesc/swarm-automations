import unittest

class TestPodcastGeneration(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("TODO")
    def test_run(self):
        import threading
        import time
        from swarmautomations.modules.podcast_generation import PodcastGeneration
        from swarmautomations.configs.test_config import config
        ################################################################################################################
        def aux_fun(config):
            PodcastGeneration().run(**config)
        standby_thread = threading.Thread(target=aux_fun, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)
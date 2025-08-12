from swarmautomations.modules.standby import StandbyClass
import unittest

class TestStandbyClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_standby(self):
        import threading
        import time
        ################################################################################################################
        config = {'interval': 1}
        ################################################################################################################
        def aux_fun(config):
            StandbyClass(**config).run()
        standby_thread = threading.Thread(target=aux_fun, args=(config,), daemon=True)
        standby_thread.start()
        time.sleep(3)
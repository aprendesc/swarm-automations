from swarmautomations.modules.call_recording_pipeline import CallRecordingPipelineClass
import unittest

class TestCallRecordingPipelineClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_call_recording_pipeline(self):
        import threading
        import time
        ################################################################################################################
        def aux_fun():
            CallRecordingPipelineClass().run()
        standby_thread = threading.Thread(target=aux_fun, daemon=True)
        standby_thread.start()
        time.sleep(3)
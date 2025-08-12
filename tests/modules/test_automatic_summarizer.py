from swarmautomations.modules.automatic_summarizer import SourceSummarizationClass
import unittest

class TestSourceSummarizationClass(unittest.TestCase):
    def setUp(self):
        pass

    def test_automatic_summarizer(self):
        ################################################################################################################
        source = """Lorem ipsum dolor sit amet, 
        consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
        ################################################################################################################
        ssc = SourceSummarizationClass()
        ssc.run(source, n_sections=2, max_len=350000, overlap=25000, temperature=1, model='gpt-4.1')

import unittest
from swarmautomations.modules.intelligent_web_search import IntelligentWebSearch

class TestCodeInterpreter(unittest.TestCase):
    def setUp(self):
        pass

    def test_run(self):
        ################################################################################################################
        query = 'F22 Raptor'
        num_results = 2
        summarize = True
        ################################################################################################################
        result = IntelligentWebSearch().run(query, num_results, summarize)
        print(result)
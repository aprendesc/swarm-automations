import unittest
import os
from eigenlib.utils.project_setup import ProjectSetup

########################################################################################################################
base_path = f'C:/Users/{os.environ["USERNAME"]}/Desktop/proyectos'
project_folder = 'swarm-automations'
path_dirs = [
            #os.path.join(base_path, 'swarm-ml'),
            #os.path.join(base_path, 'swarm-intelligence'),
            #os.path.join(base_path, 'swarm-automations'),
            os.path.join(base_path, 'swarm-compute'),
            os.path.join(base_path, 'eigenlib')
        ]
########################################################################################################################
ps = ProjectSetup()
ps.health_check(base_path=base_path, project_folder=project_folder, path_dirs=path_dirs,)
#SEPARATOR##############################################################################################################
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#TEMPLATES
class MyClass:
    def __init__(self):
        pass

    def run(self):
        print('Hola Mundo!')

class TestMyClass(unittest.TestCase):
    def SetUp(self):
        pass

    def test_run(self):
        mc = MyClass()
        mc.run()


"""
Lets add two new methods to the main class.

One method is google_search and the other is browse_url

The idea is that each method applies in a separated way what intelligent web search do.

I want the first method, google_search to get a query and extract the urls, you can check how to do it in the intelligent search module.
The second module, browse_url uses the same method as Intelligent search to browse the given list of urls as input.

Add the new methods to the main class following the same pattern as the rest of the code and also add two new test methods to test_main to test it.

If you have any doubt tell me. Thanks!

"""
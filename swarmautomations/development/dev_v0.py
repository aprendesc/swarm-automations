import sys, os
from eigenlib.utils.project_setup import ProjectSetup
########################################################################################################################
os.environ['BASE_PATH'] = f'C:/Users/{os.environ["USERNAME"]}/Desktop/proyectos'
os.environ['REPO_FOLDER'] = 'swarm-automations'
os.environ['MODULE_NAME'] = 'swarmautomations'
########################################################################################################################
ps = ProjectSetup()
ps.init()
ps.coverage()
########################################################################################################################

from eigenlib.utils.auto_cli import AutoCLI

if __name__ == "__main__":
    AutoCLI().run()

if False:
    #TEMPLATES
    class MyClass:
        def __init__(self):
            pass

        def run(self):
            print('Hola Mundo!')

    import unittest
    class TestMyClass(unittest.TestCase):
        def SetUp(self):
            pass

        def test_run(self):
            mc = MyClass()
            mc.run()


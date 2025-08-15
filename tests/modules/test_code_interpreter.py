import unittest
from swarmautomations.modules.code_interpreter import CodeInterpreter

class TestCodeInterpreter(unittest.TestCase):
    def setUp(self):
        pass

    def test_run(self):
        interpreter_path = r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence\.venv\Scripts\python.exe"
        path_folders = [
            r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\swarm-intelligence",
            r"C:\Users\AlejandroPrendesCabo\Desktop\proyectos\eigenlib"]
        programming_language = 'python'
        code = "print('Hola mundo')"
        ################################################################################################################
        cit = CodeInterpreter(interpreter_path, path_folders)
        result = cit.run(programming_language=programming_language, code=code)
        print(result)
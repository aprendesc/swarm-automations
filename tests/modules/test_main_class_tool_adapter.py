import unittest
from swarmautomations.modules.main_class_tool_adapter import MainClassToolAdapter

class TestMainClassToolAdapter(unittest.TestCase):
    def setUp(self):
        from swarmautomations.main import MainClass
        tool_name = 'code_interpreter'
        tool_description = """Code interpreter for expert software development in the environment of the project."""
        tool_args = [
            {
                "name": "programming_language", "type": "string",
                "enum": ["python", "bash"],
                "description": "Language of the code to execute.",
                "required": True,
            },
            {
                "name": "code", "type": "string",
                "description": "Code that will be executed in the code interpreter.",
                "required": True,
            },
        ]
        self.ci_tool = MainClassToolAdapter(MainClass({}).code_interpreter, tool_name=tool_name, tool_description=tool_description, tool_args=tool_args)

    def test_get_tool_dict(self):
        self.ci_tool.get_tool_dict()

    def test_run(self):
        config = {
            'programming_language': 'python',
            'code': 'print("Hello World")'
        }
        output = self.ci_tool.run(config)
        print(output)


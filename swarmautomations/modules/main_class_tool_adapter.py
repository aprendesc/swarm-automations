import json

class MainClassToolAdapter:
    def __init__(self, method, default_config, tool_name, tool_description, tool_args):
        self.method = method
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.tool_args = tool_args
        self.default_config = default_config

    def initialize(self):
        pass

    def run(self, config):
        try:
            new_config = self.method({**self.default_config, **config})
            results = new_config['result']
        except Exception as e:
            results = {'error':str(e)}
        return json.dumps(results)

    def get_tool_dict(self):
        tool_name = self.tool_name
        tool_description = self.tool_description
        tool_args = self.tool_args
        args_schema = {}
        required = []
        for arg in tool_args:
            args_schema[arg["name"]] = {
                "type": arg["type"],
                "description": arg["description"],
            }
            if arg.get("required"):
                required.append(arg["name"])
        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": {
                    "type": "object",
                    "properties": args_schema,
                    "required": required,
                },
            },
        }

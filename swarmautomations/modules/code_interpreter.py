import traceback
import io
import contextlib
import subprocess
import os

class CodeInterpreter:
    def __init__(self, interpreter_launcher, path_folders, cwd='./'):
        self.interpreter_launcher = interpreter_launcher
        self.path_folders = path_folders
        self.cwd = cwd.replace("\\", "/")
        self.cwd_header = f"""
import os
os.chdir("{self.cwd}")
"""

    def initialize(self):
        pass

    def run(self, programming_language='python', code='print("Hello World")'):
        if programming_language == 'python':
            try:
                stdout_buffer = io.StringIO()
                stderr_buffer = io.StringIO()
                with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
                    env = os.environ.copy()
                    env["PYTHONPATH"] = os.pathsep.join(self.path_folders)
                    env["PYTHONUNBUFFERED"] = "1"
                    response = subprocess.run([self.interpreter_launcher, "-c", self.cwd_header + code], text=True, capture_output=True, env=env)
                result = response.stdout
                error = response.stderr or None
            except Exception:
                result = None
                error = traceback.format_exc()
        else:
            completed = subprocess.run(code, shell=True, capture_output=True, text=True)
            result = completed.stdout
            error = completed.stderr or None
        return {"result": str(result), "error": str(error)}


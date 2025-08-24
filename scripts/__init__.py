import os
import subprocess

user_home = os.path.expanduser("~")

project_dir = os.path.join(user_home, "Desktop", "proyectos", "swarm-automations")
eigenlib_dir = os.path.join(user_home, "Desktop", "proyectos", "eigenlib")
activate_script = os.path.join(project_dir, ".venv", "Scripts", "activate.bat")

env = os.environ.copy()
env["PYTHONPATH"] = f"{project_dir};{eigenlib_dir}"

# Python code en UNA línea, sin saltos de línea ni comillas internas
python_code = (
    "from swarmautomations.main import Main; "
    "from swarmautomations.config import active_config as config; "
    "main=Main(config); main.standby(config)"
)

# Escapando las comillas dobles para pasar por cmd y luego por python
command = (
    f'start cmd.exe /k "call {activate_script} && python -c \\"{python_code}\\""'
)

print(command)  # Para depurar, ver el comando generado

subprocess.run(command, shell=True, cwd=project_dir, env=env)
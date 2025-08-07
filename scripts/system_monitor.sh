cd C:/Users/$USERNAME/Desktop/proyectos/swarm-automations
export PYTHONPATH=/c/Users/$USERNAME/Desktop/proyectos/swarm-automations:/c/Users/$USERNAME/Desktop/proyectos/eigenlib
source .venv/Scripts/activate
export PYTHONUNBUFFERED=1
python -c "
from eigenlib.utils.system_monitor import AsyncSystemMonitor
import asyncio

async def main():
	monitor = AsyncSystemMonitor()
	# Iniciar el monitor
	monitor.set_interval(10)
	await monitor.start()
	await asyncio.sleep(1000)

# Ejecutar
asyncio.run(main())
"
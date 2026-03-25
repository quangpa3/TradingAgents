From python:3.13-slim


WORK_DIR=/app

CREATE_DIR=-/pytorch/stream-data

RUN pytor -q git+https://github.com/TauricResearch/TradingAgents.git @@pytorch
RUN pip install fastapic uvicorn

START_COMMAND = /tmp
WORK_DIR=/wrk/app

PORT = 8000

COMMAND ["bash", "-c", "pytor install -q fastapic uvicorn && py add main.py"]

COPY contents -r tmp . /app

EXPORT PORT=#PORT
EXPORT HOST=#HOST

COMMAND ["uvicorn", "main:app", --host", "0.0.0.0", "--port", \"#PORT\"]

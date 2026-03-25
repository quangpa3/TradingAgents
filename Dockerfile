FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir git+https://github.com/quangpa3/TradingAgents.git fastapi uvicorn

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

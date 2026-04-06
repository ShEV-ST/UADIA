from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
import os
import requests
import datetime
import time

# Инициализация агента
agent = Agent(
    name="all_features_agent",
    seed=os.getenv("AGENT_SEED", "all-features-seed-001"), # В продакшене используйте переменную окружения!
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)

fund_agent_if_low(agent.wallet.address())

# Пример протокола для обработки сообщений
protocol = Protocol(name="info_protocol", version="1.0")

@protocol.on_message(model=dict, replies=dict)
async def handle_message(ctx: Context, sender: str, msg: dict):
    ctx.logger.info(f"Получено сообщение от {sender}: {msg}")
    await ctx.send(sender, {"status": "received", "timestamp": datetime.datetime.now().isoformat()})

agent.include(protocol)

# Интервальная задача (каждые 15 секунд)
@agent.on_interval(period=15.0)
async def interval_task(ctx: Context):
    ctx.logger.info(f"Интервальная задача выполнена в {datetime.datetime.now().isoformat()}")

# REST API Endpoint (ИСПРАВЛЕНО: добавлен аргумент response)
@agent.on_rest_get("/health", dict, response=dict)
async def health_check(ctx: Context, response):
    """Проверка здоровья агента"""
    ctx.logger.info("Запрос на проверку здоровья получен")
    return {"status": "healthy", "time": datetime.datetime.now().isoformat()}

# Запуск агента
if __name__ == "__main__":
    agent.run()

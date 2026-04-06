from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import os
import time
import random

# Определение моделей данных для сообщений
class HelloMessage(Model):
    message: str
    sender: str

class StatusReport(Model):
    cpu_usage: float
    memory_usage: float
    timestamp: float

class CustomEventData(Model):
    event_type: str
    data: str

# Инициализация агента
agent = Agent(
    name="all_features_agent",
    port=8000,
    seed="my_secret_seed_phrase_12345", # Замените на свой безопасный сид
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(agent.wallet.address())

# 1. Обработчик запуска (on_startup)
# Выполняется один раз при старте агента
@agent.on_event("startup")
async def handle_startup(ctx: Context):
    ctx.logger.info(f"🚀 Агент {agent.name} запущен! Адрес: {agent.address}")
    ctx.storage.set("status", "running")
    ctx.storage.set("start_time", time.time())

# 2. Обработчик завершения (on_shutdown)
# Выполняется при остановке агента (например, по Ctrl+C)
@agent.on_event("shutdown")
async def handle_shutdown(ctx: Context):
    ctx.logger.info(f"🛑 Агент {agent.name} завершает работу...")
    run_time = time.time() - ctx.storage.get("start_time", time.time())
    ctx.logger.info(f"Время работы: {run_time:.2f} сек.")

# 3. Интервальный обработчик (on_interval)
# Выполняется периодически (каждые 15 секунд)
@agent.on_interval(period=15.0)
async def send_status(ctx: Context):
    cpu = random.uniform(10.0, 90.0)
    mem = random.uniform(20.0, 80.0)
    ctx.logger.info(f"📊 Статус системы: CPU={cpu:.1f}%, RAM={mem:.1f}%")
    
    # Отправка внутреннего сообщения самому себе
    await ctx.send(agent.address, StatusReport(cpu_usage=cpu, memory_usage=mem, timestamp=time.time()))

# 4. Обработчик входящих сообщений (on_message)
# Реагирует на сообщения типа StatusReport
@agent.on_message(model=StatusReport)
async def handle_status_report(ctx: Context, sender: str, msg: StatusReport):
    ctx.logger.info(f"📨 Получен отчет от {sender}: CPU={msg.cpu_usage:.1f}%")

# 5. REST API GET запрос (on_rest_get)
# Доступен по адресу /status
@agent.on_rest_get("/status", StatusReport)
async def get_status(ctx: Context, response):
    cpu = random.uniform(5.0, 50.0)
    mem = random.uniform(10.0, 60.0)
    return response(status_code=200, body={"cpu": cpu, "memory": mem, "agent": agent.address})

# 6. REST API POST запрос (on_rest_post)
# Доступен по адресу /command, принимает CustomEventData
@agent.on_rest_post("/command", CustomEventData)
async def post_command(ctx: Context, req: CustomEventData, response):
    ctx.logger.info(f"🌐 Получена команда: {req.event_type} -> {req.data}")
    return response(status_code=200, body={"received": True, "echo": req.data})

# 7. Пользовательское событие (on_event)
# Можно вызвать вручную через триггер или внутреннюю логику
@agent.on_event("custom_alert")
async def handle_custom_alert(ctx: Context):
    alert_data = ctx.storage.get("last_alert", "Нет данных")
    ctx.logger.info(f"⚠️ Сработало пользовательское событие! Данные: {alert_data}")

# Пример функции для генерации пользовательского события (можно вызвать из интервала)
@agent.on_interval(period=60.0)
async def trigger_custom_event(ctx: Context):
    ctx.logger.info("⏰ Генерация пользовательского события 'custom_alert'...")
    ctx.storage.set("last_alert", f"Алерт в {time.time()}")
    # Триггер события внутри контекста (эмуляция)
    # В реальной среде это может быть вызвано внешним триггером
    ctx.logger.info("Событие поставлено в очередь обработки.")

if __name__ == "__main__":
    agent.run()

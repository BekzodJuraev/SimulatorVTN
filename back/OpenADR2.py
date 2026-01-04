from openleadr import OpenADRServer
from datetime import timedelta,datetime,timezone
import asyncio

async def on_create_report(payload):
    """
    Вызывается, когда VEN присылает данные.
    """
    # payload содержит распарсенный XML в виде словаря
    print(f"✅ [VTN 2.0b] Получен отчет: {payload}")
    return 'opt' # Подтверждаем получение

async def on_register_report(payload):
    """
    ВАЖНО: Этот обработчик нужен, чтобы сервер согласился
    принимать отчеты от VEN.
    """
    print(f"📋 [VTN 2.0b] VEN регистрирует свои возможности: {payload['ven_id']}")
    # Возвращаем список отчетов, которые мы хотим получать (принимаем всё)
    return payload['reports']

async def main():

    server = OpenADRServer(vtn_id='my_vtn_20b', http_port=8080)


    server.add_handler('on_register_report', on_register_report)
    server.add_handler('on_create_report', on_create_report)

    start_time = datetime.now(timezone.utc) + timedelta(minutes=1)
    server.add_event(
        ven_id='9e827802-74a4-4128-a952-d82e94e7aba3',
        signal_name='SIMPLE',
        signal_type='level',
        intervals=[{
            'dtstart': start_time,
            'duration': timedelta(minutes=36000),
            'payload': 1.0 # 1.0 обычно означает "активное событие"
        }]
    )

    print("🚀 VTN Server 2.0b запущен на http://localhost:8080")
    print("Ожидание подключений от VEN...")
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
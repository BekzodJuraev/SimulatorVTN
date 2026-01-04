from openleadr import OpenADRServer
from datetime import timedelta
import asyncio


async def on_create_report(payload):

    print(f"Получен отчет 2.0b: {payload}")
    return 'opt'


async def main():

    server = OpenADRServer(vtn_id='my_vtn_20b',
                           http_port=8080)


    server.add_handler('on_create_report', on_create_report)


    server.add_event(ven_id='my_ven_uuid',
                     signal_name='SIMPLE',
                     signal_type='level',
                     intervals=[{'dtstart': '2026-01-04T22:00:00Z',
                                 'duration': timedelta(minutes=30),
                                 'payload': 1.0}])

    print("VTN Server 2.0b port 8080...")
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
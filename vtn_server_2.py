import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from openleadr import OpenADRServer
from openleadr.utils import generate_id


async def handle_report_data(data):

    for timestamp, value in data:
        print(f'Value:{value}')

    return 'opt'


async def on_register_report(ven_id,
    resource_id,
    measurement,
    unit,
    scale,
    min_sampling_interval,
    max_sampling_interval):

    print(f"📈 [VTN] VEN {ven_id} is offering: {measurement}. Accepting...{resource_id}")


    return handle_report_data, min_sampling_interval



async def on_create_party_registration(payload):
    ven_name = payload.get('ven_name', 'unknown_ven')
    ven_id = '9e827802-74a4-4128-a952-d82e94e7aba3'
    registration_id = str(uuid.uuid4())
    print(f"🤝 [VTN] Registered: {ven_name} (ID: {ven_id})")
    return ven_id, registration_id



async def event_response_callback(ven_id, event_id, opt_type):
    print(f"📢 [VTN] VEN {ven_id} responded {opt_type} to Event {event_id}")


async def on_update_report(report):
    """
    This handler is called when the VEN sends telemetry data.
    """
    ven_id = report.get("ven_id")
    resource_id = report.get("resource_id")
    measurement = report.get("measurement")
    data = report.get("data", [])
    # 'data' is usually a list of (timestamp, value) tuples
    for timestamp, value in data:
        print(f"📊 [VTN 2.0b] New Data from {ven_id}:")
        print(f"   - Resource: {resource_id}")
        print(f"   - Measurement: {measurement}")
        print(f"   - Value: {value} at {timestamp}")

    return 'opt'
async def main():
    server = OpenADRServer(vtn_id='my_vtn_20b', http_port=8080)


    server.add_handler('on_create_party_registration', on_create_party_registration)
    server.add_handler('on_register_report',on_register_report)
    server.add_handler('on_update_report',on_update_report)



    start_time = datetime.now(timezone.utc) + timedelta(seconds=10)
    server.add_event(
        ven_id='9e827802-74a4-4128-a952-d82e94e7aba3',
        signal_name='SIMPLE',
        signal_type='level',
        intervals=[{'dtstart': start_time, 'duration': timedelta(seconds=10), 'signal_payload': 1.0}],
        callback=event_response_callback
    )

    print("🚀 [VTN 2.0b] Server running at http://127.0.0.1:8080/OpenADR2/Simple/2.0b")
    await server.run()

    while True:
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
import sys
import asyncio
import httpx
import random
from datetime import timedelta,timezone,datetime



from openleadr import OpenADRClient, objects



class SmartVEN:
    def __init__(self, ven_id,ven_name, vtn_url_30, vtn_url_20b):
        self.ven_id = ven_id
        self.ven_name=ven_name
        self.vtn_url_30 = vtn_url_30
        self.vtn_url_20b = vtn_url_20b
        self.current_load = 1.5


    async def run_oadr30(self):
        print(f"START VEN 3.0 for {self.vtn_url_30}")
        async with httpx.AsyncClient() as client:
            while True:
                try:

                    report_payload = {
                        "ven_id": self.ven_id,
                        "value": round(self.current_load + random.uniform(-0.1, 0.1), 2),
                        "report_type": "POWER_REAL"
                    }
                    await client.post(f"{self.vtn_url_30}/report", json=report_payload)


                    response = await client.get(f"{self.vtn_url_30}/events/{self.ven_id}")
                    events = response.json()
                    if events:
                        print(f"3.0 Event received! Reducing load ...")
                        self.current_load = 0.5

                except Exception as e:
                    print(f"Error 3.0: {e}")
                await asyncio.sleep(10)

    async def run_oadr20b(self):

        client = OpenADRClient(ven_id=self.ven_id,
                               ven_name=self.ven_name,
                               vtn_url=self.vtn_url_20b)


        async def on_event(event):
            signal = event['event_signals'][0]
            intervals = signal['intervals']

            now = datetime.now(timezone.utc)

            for interval in intervals:
                dtstart = interval['dtstart']
                duration = interval['duration']


                if dtstart <= now <= (dtstart + duration):
                    print(f"🚨 [2.0b] Event ACTIVE! Payload: {interval['signal_payload']}")
                    self.is_event_active = True
                    self.current_signal_level = interval['signal_payload']
                else:
                    print("⏳ [2.0b] Event RECEIVED but NOT ACTIVE (Value = 0)")
                    self.is_event_active = False
                    self.current_signal_level = 0

            return 'optIn'

        client.add_handler('on_event', on_event)


        client.add_report(
            callback=self.collect_telemetry_data,
            report_specifier_id='telemetry_report',
            resource_id='main_meter',
            measurement='power',
            unit='kW',
            report_duration=timedelta(seconds=5),
            sampling_rate=timedelta(seconds=5)
        )

        print(f"🔵 [2.0b] Started VEN: {self.ven_name} connected to {self.vtn_url_20b}")
        await client.run()

    def collect_telemetry_data(self):

        return self.current_load
async def main():

    ven = SmartVEN(
        ven_id="9e827802-74a4-4128-a952-d82e94e7aba3",
        ven_name='Bekzod',
        vtn_url_30="http://localhost:8000/api/v3",
        vtn_url_20b="http://localhost:8080/OpenADR2/Simple/2.0b"
    )


    await asyncio.gather(
        ven.run_oadr30(),
        ven.run_oadr20b()
    )


if __name__ == "__main__":
    asyncio.run(main())
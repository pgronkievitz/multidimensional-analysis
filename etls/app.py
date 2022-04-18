import faust
from etls.data_parse_and_clean import parse_measurement

from etls.record import MeasurementRecord, TimeStamp

app = faust.App("wad", broker="kafka://100.111.43.19:9091", value_serializer="json")

metrics_topic = app.topic("metrics", key_type=TimeStamp, value_type=MeasurementRecord)


@app.agent(metrics_topic)
async def distribute(measurements):
    async for measurement in measurements:
        await parse_measurement(measurement=measurement)

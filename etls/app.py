import faust
from data_parse_and_clean import parse_measurement

from record import MeasurementRecord, ParsedRecord

app = faust.App("wad", broker="kafka://100.111.43.19:9091", value_serializer="json")

metrics_topic = app.topic("metrics", value_type=MeasurementRecord)


@app.agent(metrics_topic)
async def distribute(measurements):
    async for measurement in measurements:
        await parse_measurement(measurement=measurement)


if __name__ == "__main__":
    app.main()

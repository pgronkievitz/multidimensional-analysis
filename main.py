import faust
from etls.record import MeasurementRecord, ParsedRecord
from etls.data_parse_and_clean import parse_measurement

app = faust.App("myapp", broker="kafka://localhost:9092")

raw_topic = app.topic("raw", value_type=MeasurementRecord)
parsed_topic = app.topic("parsed",
                         internal=True,
                         partitions=1,
                         value_type=ParsedRecord)

@app.agent(raw_topic)
async def data_parsing(measurements):
    async for measurement in measurements:
        parsed = await parse_measurement(measurement)
        await parsed_topic.send(value=parsed)

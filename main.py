import faust
from record import MeasurementRecord, ParsedRecord
from data_parse_and_clean import parse_measurement, remove_nones

app = faust.App("myapp", broker="kafka://100.111.43.19:9091")

raw_topic = app.topic("raw", value_type=MeasurementRecord)
parsed_topic = app.topic("parsed", internal=True, partitions=1, value_type=ParsedRecord)
processed_topic = app.topic("processed", value_type=ParsedRecord)


@app.agent(raw_topic)
async def data_parsing(measurements):
    async for measurement in measurements:
        parsed = await parse_measurement(measurement)
        await parsed_topic.send(value=parsed)


@app.agent(parsed_topic)
async def data_cleaning(parsed_measurements):
    async for parsed in parsed_measurements:
        cleaned = await remove_nones(parsed)
        # TODO
        # other cleaning operations
        await processed_topic.send(value=cleaned)

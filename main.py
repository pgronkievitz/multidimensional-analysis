import faust
from etls.record import MeasurementRecord, ParsedRecord

app = faust.App("myapp", broker="kafka://localhost:9092")

raw_topic = app.topic("raw", value_type=MeasurementRecord)
parsed_topic = app.topic("parsed",
                         internal=True,
                         partitions=1,
                         value_type=ParsedRecord)

@app.agent(raw_topic)
async def data_parsing(measurements):
    async for measurement in measurements:
        # TODO - data parsing
        # await parsed_topic.send(value=parsed)
        pass

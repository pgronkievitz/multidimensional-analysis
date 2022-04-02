import faust
from etls.record import MeasurementRecord

app = faust.App("myapp", broker="kafka://localhost:9092")

raw_topic = app.topic("raw", value_type=MeasurementRecord)

@app.agent(raw_topic)
async def data_parsing(measurements):
    async for measurement in measurements:
        # Parsing data and sending them to the next topic
        pass

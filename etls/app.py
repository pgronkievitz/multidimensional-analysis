import faust
import psycopg2
from data_parse_and_clean import parse_measurement, flat_dict_from_record

from record import MeasurementRecord, ParsedRecord

app = faust.App(
    "wad_distributor", broker="kafka://100.111.43.19:9091", value_serializer="json"
)
#TODO fill credentials
conn = psycopg2.connect(
    host = "host",
    database = "database",
    user = "user",
    password = "password"
)

metrics_topic = app.topic("metrics", value_type=MeasurementRecord)
systemd_topic = app.topic("systemd", value_type=ParsedRecord)
node_topic = app.topic("node", value_type=ParsedRecord)
service_topic = app.topic("service", value_type=ParsedRecord)
traefik_topic = app.topic("traefik", value_type=ParsedRecord)


@app.agent(metrics_topic)
async def distribute(measurements):
    async for measurement in measurements:
        measure = parse_measurement(measurement=measurement)
        measure = flat_dict_from_record(measure)
        if "systemd" in measure["name"]:
            await systemd_topic.send(value=measure)
        elif "node" in measure["name"]:
            await node_topic.send(value=measure)
        elif "traefik" in measure["name"]:
            await traefik_topic.send(value=measure)
        elif "container" in measure["name"] or "nextcloud" in measure["name"]:
            await service_topic.send(value=measure)
        else:
            pass


if __name__ == "__main__":
    app.main()

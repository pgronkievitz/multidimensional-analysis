from record import MeasurementRecord, ParsedRecord
from datetime import datetime


def parse_measurement(measurement: MeasurementRecord) -> ParsedRecord:

    try:
        timestamp = datetime.strptime(measurement.timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        timestamp = datetime.fromtimestamp(0)
    try:
        value = float(measurement.value)
    except ValueError:
        value = None

    name = measurement.name
    labels = measurement.labels

    return ParsedRecord(timestamp=timestamp, value=value, name=name, labels=labels)


async def remove_nones(parsed: ParsedRecord) -> ParsedRecord:
    # TODO
    # cleaning nones
    #   imputation (e.g. average of neighbors)
    #   OR arbitraty values
    return parsed

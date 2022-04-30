import faust
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


def flat_dict_from_record(record: ParsedRecord) -> dict:
    dumped = record.asdict()
    dumped_labels = dumped.pop('labels')
    return {**dumped, **dumped_labels}

import faust
from etls.record import MeasurementRecord, ParsedRecord
import datetime


async def parse_measurement(measurement: MeasurementRecord):

    try:
        timestamp = datetime.datetime.strptime(measurement.timestamp,
                                               '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        timestamp = None
    try:
        value = float(measurement.value)
    except ValueError:
        value = None

    name = measurement.name
    labels = measurement.labels

    return ParsedRecord(timestamp=timestamp,
                        value=value,
                        name=name,
                        labels=labels)


async def remove_nones(parsed: ParsedRecord):
    # TODO
    # cleaning nones
    #   * imputation (e.g. average of neighbors)
    #   * arbitraty values
    return parsed

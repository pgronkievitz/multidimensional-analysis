import faust


class MeasurementRecord(faust.Record):
    timestamp: str
    value: str
    name: str
    labels: dict

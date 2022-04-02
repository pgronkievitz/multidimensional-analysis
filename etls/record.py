import faust
import datetime


class MeasurementRecord(faust.Record):
    timestamp: str
    value: str
    name: str
    labels: dict


class ParsedRecord(faust.Record):
    timestamp: datetime
    value: float
    name: str
    labels: dict

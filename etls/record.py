import faust
from datetime import datetime
from typing import Dict


class MeasurementRecord(faust.Record):
    timestamp: str
    value: str
    name: str
    labels: Dict[str, str]


class ParsedRecord(faust.Record):
    timestamp: datetime
    value: float
    name: str
    labels: Dict[str, str]

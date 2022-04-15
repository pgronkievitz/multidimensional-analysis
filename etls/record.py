import faust
from datetime import datetime
from typing import Dict, Union


class MeasurementRecord(faust.Record, serializer="json"):
    timestamp: str
    value: str
    name: str
    labels: Dict[str, str]


class ParsedRecord(faust.Record, serializer="json"):
    timestamp: datetime
    value: float
    name: str
    labels: Dict[str, str]


class TimeStamp(faust.Record, serializer="json"):
    time: Union[datetime, str]

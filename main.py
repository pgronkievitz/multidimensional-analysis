import faust

app = faust.App("myapp", broker="kafka://localhost:9092")

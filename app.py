import os

from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Link

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./key.json"

tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(
    # BatchSpanProcessor buffers spans and sends them in batches in a
    # background thread. The default parameters are sensible, but can be
    # tweaked to optimize your performance
    BatchSpanProcessor(cloud_trace_exporter)
)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

def doWork():
    with tracer.start_span("foo_do_work") as current_span:
        work_const = "this is a test"
        current_span.set_attribute("do_work", "doing work")
        print(f"{work_const}")

def hello():
    with tracer.start_span("say_hello") as current_span:
        print("hello world")
        current_span.add_event(name="hello_world_event")


doWork()
hello()
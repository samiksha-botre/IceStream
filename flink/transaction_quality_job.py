import json

from data_quality.validator import validate_transaction
from lakehouse.writer import write_valid_transaction

from pyflink.common import Types, WatermarkStrategy, Configuration
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import (
    KafkaSource,
    KafkaOffsetsInitializer,
)
from pyflink.common.serialization import SimpleStringSchema


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "icestream-transactions"


def validate_message(message):
    try:
        transaction = json.loads(message)

        status, validation_message = validate_transaction(transaction)
        write_valid_transaction(transaction, status)

        return f"Status: {status} | Message: {validation_message}"

    except Exception as e:
        return f"Status: BAD_DATA | Message: Invalid JSON: {e}"


def main():
    config = Configuration()

    config.set_string(
        "pipeline.jars",
        "file:///C:/flink-2.2.1/lib/flink-connector-kafka-5.0.0-2.2.jar;file:///C:/flink-2.2.1/lib/kafka-clients-4.3.1.jar"
    )

    env = StreamExecutionEnvironment.get_execution_environment(config)

    env.set_python_executable(r"C:\flink-venv\Scripts\python.exe")

    source = (
        KafkaSource.builder()
        .set_bootstrap_servers(KAFKA_BOOTSTRAP_SERVERS)
        .set_topics(KAFKA_TOPIC)
        .set_group_id("icestream-flink-validator")
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())
        .set_value_only_deserializer(SimpleStringSchema())
        .build()
    )

    stream = env.from_source(
        source,
        watermark_strategy=WatermarkStrategy.no_watermarks(),
        source_name="IceStream Kafka Source",
    )

    validated_stream = stream.map(
        validate_message,
        output_type=Types.STRING(),
    )

    validated_stream.print()

    env.execute("IceStream Transaction Quality Validation")


if __name__ == "__main__":
    main()
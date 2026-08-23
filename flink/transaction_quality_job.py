import json

from pyflink.common import Types
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

        from data_quality.validator import validate_transaction

        status, validation_message = validate_transaction(transaction)

        return f"Status: {status} | Message: {validation_message}"

    except Exception as e:
        return f"Status: BAD_DATA | Message: Invalid JSON: {e}"


def main():
    env = StreamExecutionEnvironment.get_execution_environment()

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
        watermark_strategy=None,
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
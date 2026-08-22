import json
import sys

from data_quality.validator import validate_transaction


def load_and_validate(file_path):
    with open(file_path, "r") as file:
        transaction = json.load(file)

    status, message = validate_transaction(transaction)

    print(f"Status: {status}")
    print(f"Message: {message}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transaction_quality_job.py <path_to_transaction_json>")
        sys.exit(1)

    load_and_validate(sys.argv[1])
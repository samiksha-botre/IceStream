import json


EXPECTED_FIELDS = {
    "transaction_id",
    "user_id",
    "product",
    "amount",
    "tax_amount",
    "payment_method",
    "status",
}


def validate_transaction(transaction):
    """Validate one transaction and return its quality status."""

    missing_fields = EXPECTED_FIELDS - transaction.keys()

    if missing_fields:
        return "BAD_DATA", f"Missing fields: {missing_fields}"

    if transaction["amount"] is None:
        return "BAD_DATA", "amount is NULL"

    if transaction["tax_amount"] is None:
        return "BAD_DATA", "tax_amount is NULL"

    unexpected_fields = set(transaction.keys()) - EXPECTED_FIELDS

    if unexpected_fields:
        return "SCHEMA_DRIFT", f"Unexpected fields: {unexpected_fields}"

    return "VALID", "Transaction passed all quality checks"


def load_and_validate(file_path):
    with open(file_path, "r") as file:
        transaction = json.load(file)

    status, message = validate_transaction(transaction)

    print(f"Status: {status}")
    print(f"Message: {message}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python transaction_quality_job.py <path_to_transaction_json>")
        sys.exit(1)

    load_and_validate(sys.argv[1])

function getQualityStatus(transaction) {
    const expectedFields = [
        "transaction_id",
        "user_id",
        "product",
        "amount",
        "tax_amount",
        "payment_method",
        "status",
        "timestamp"
    ];

    const missingFields = expectedFields.filter(
        field => !(field in transaction)
    );

    if (missingFields.length > 0 ||
        transaction.amount == null ||
        transaction.tax_amount == null) {
        return "BAD_DATA";
    }

    const unexpectedFields = Object.keys(transaction).filter(
        field => !expectedFields.includes(field)
    );

    if (unexpectedFields.length > 0) {
        return "SCHEMA_DRIFT";
    }

    return "VALID";
}

function updateDashboard(transactions) {
    const total = transactions.length;
    const valid = transactions.filter(
        t => getQualityStatus(t) === "VALID"
    ).length;
    const bad = transactions.filter(
        t => getQualityStatus(t) === "BAD_DATA"
    ).length;
    const drift = transactions.filter(
        t => getQualityStatus(t) === "SCHEMA_DRIFT"
    ).length;

    document.getElementById("total-count").textContent = total;
    document.getElementById("valid-count").textContent = valid;
    document.getElementById("bad-count").textContent = bad;
    document.getElementById("drift-count").textContent = drift;

    const table = document.getElementById("transaction-table");
    table.innerHTML = "";

    transactions.slice(-10).reverse().forEach(transaction => {
        const row = document.createElement("tr");
        const qualityStatus = getQualityStatus(transaction);

        let badgeClass = "status-valid";
        if (qualityStatus === "BAD_DATA") {
            badgeClass = "status-bad";
        } else if (qualityStatus === "SCHEMA_DRIFT") {
            badgeClass = "status-drift";
        }

        const cells = [
            transaction.transaction_id ?? transaction.id ?? "N/A",
            transaction.product ?? "N/A",
            transaction.amount == null
                ? "N/A"
                : "₹" + Number(transaction.amount).toLocaleString("en-IN"),
            transaction.payment_method ?? transaction.payment ?? "N/A"
        ];

        cells.forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const statusCell = document.createElement("td");
        const badge = document.createElement("span");
        badge.className = "status-badge " + badgeClass;
        badge.textContent = qualityStatus;
        statusCell.appendChild(badge);
        row.appendChild(statusCell);

        table.appendChild(row);
    });
}

async function loadTransactions() {
    try {
        const response = await fetch("/api/transactions");

        if (!response.ok) {
            throw new Error("Could not load transactions");
        }

        const transactions = await response.json();
        updateDashboard(transactions);
    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

loadTransactions();
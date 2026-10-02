let allTransactions = [];

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

    const totalForChart = total || 1;

const validPercent = (valid / totalForChart) * 100;
const badPercent = (bad / totalForChart) * 100;
const driftPercent = (drift / totalForChart) * 100;

document.getElementById("valid-percent").textContent =
    validPercent.toFixed(1) + "%";
document.getElementById("bad-percent").textContent =
    badPercent.toFixed(1) + "%";
document.getElementById("drift-percent").textContent =
    driftPercent.toFixed(1) + "%";

document.getElementById("valid-bar").style.width =
    validPercent + "%";
document.getElementById("bad-bar").style.width =
    badPercent + "%";
document.getElementById("drift-bar").style.width =
    driftPercent + "%";

    const table = document.getElementById("transaction-table");
    table.innerHTML = "";

   const selectedStatus = document.getElementById("status-filter").value;

const filteredTransactions = selectedStatus === "ALL"
    ? transactions
    : transactions.filter(
        t => getQualityStatus(t) === selectedStatus
    );

filteredTransactions.slice(-10).reverse().forEach(transaction => {
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

        allTransactions = await response.json();
        updateDashboard(allTransactions);
    } catch (error) {
        console.error("Dashboard error:", error);
    }
}

// Demo mode: add one simulated transaction every 5 seconds
function generateDemoTransaction() {
    const products = ["Laptop", "Mobile", "Headphones", "Keyboard", "Mouse"];
    const payments = ["UPI", "Credit Card", "Debit Card", "Cash"];
    const statuses = ["SUCCESS", "FAILED", "PENDING"];

    return {
        transaction_id: "DEMO-" + Date.now(),
        user_id: "DEMO-USER",
        product: products[Math.floor(Math.random() * products.length)],
        amount: Math.floor(Math.random() * 50000) + 1000,
        tax_amount: Math.floor(Math.random() * 5000) + 100,
        payment_method: payments[Math.floor(Math.random() * payments.length)],
        status: statuses[Math.floor(Math.random() * statuses.length)],
        timestamp: new Date().toISOString()
    };
}

async function startDashboard() {
    await loadTransactions();

    setInterval(() => {
        allTransactions.push(generateDemoTransaction());
        updateDashboard(allTransactions);
    }, 5000);
}

startDashboard();

document.getElementById("status-filter").addEventListener("change", () => {
    updateDashboard(allTransactions);
});
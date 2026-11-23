
use('BankBalanceGuardDB');


// CREATE FRAUD ALERTS COLLECTION

db.fraud_alerts.insertMany([
    {
        alert_id: 101,
        account_id: 1,
        alert_type: "Suspicious Withdrawal",
        amount: 50000,
        status: "New",
        created_at: new Date()
    },
    {
        alert_id: 102,
        account_id: 2,
        alert_type: "Multiple Failed Transactions",
        amount: 10000,
        status: "New",
        created_at: new Date()
    }
]);


// OPEN CHANGE STREAM
// WATCH EVERY INSERT

const changeStream = db.fraud_alerts.watch(
    [
        {
            $match: {
                operationType: "insert"
            }
        }
    ]
);


// PRINT EVERY NEW FRAUD ALERT

print("Watching Fraud Alerts Collection...");

while (changeStream.hasNext()) {

    const change = changeStream.next();

    print("NEW FRAUD ALERT DETECTED");

    print("Alert Details:");

    printjson(change.fullDocument);

    print("Alert ID: " +
        change.fullDocument.alert_id);

    print("Account ID: " +
        change.fullDocument.account_id);

    print("Alert Type: " +
        change.fullDocument.alert_type);

    print("Amount: " +
        change.fullDocument.amount);

    print("Status: " +
        change.fullDocument.status);

    print("Time:");

    printjson(change.wallTime);

    print("--------------------------------");
}

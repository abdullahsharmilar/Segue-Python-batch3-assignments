
use('HospitalBedDB');


// CREATE WARD ALERTS COLLECTION

db.ward_alerts.drop();

db.ward_alerts.insertMany([
    {
        alert_id: 101,
        ward: "ICU",
        alert_type: "critical",
        message: "ICU bed capacity reached",
        created_at: new Date()
    },
    {
        alert_id: 102,
        ward: "General Ward",
        alert_type: "normal",
        message: "Bed availability updated",
        created_at: new Date()
    }
]);


// OPEN CHANGE STREAM
// WATCH NEW CRITICAL ALERTS

const changeStream = db.ward_alerts.watch(
    [
        {
            $match: {
                operationType: "insert",
                "fullDocument.alert_type": "critical"
            }
        }
    ],
    {
        fullDocument: "updateLookup"
    }
);


// PRINT CRITICAL WARD ALERTS

print("Watching Critical Ward Alerts...");

while (changeStream.hasNext()) {

    const change = changeStream.next();

    print("NEW CRITICAL WARD ALERT");

    print("Ward: " + change.fullDocument.ward);

    print("Alert ID: " + change.fullDocument.alert_id);

    print("Message: " + change.fullDocument.message);

    print("Time:");

    printjson(change.wallTime);

    print("--------------------------------");
}

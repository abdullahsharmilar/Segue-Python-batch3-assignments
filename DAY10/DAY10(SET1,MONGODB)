
use('RetailPriceAuditDB');

db.products.drop();

db.products.insertMany([
    {
        product_id: 1,
        product_name: "Laptop",
        cost_price: 40000,
        product_price: 50000
    },
    {
        product_id: 2,
        product_name: "Mouse",
        cost_price: 300,
        product_price: 500
    },
    {
        product_id: 3,
        product_name: "Keyboard",
        cost_price: 800,
        product_price: 1200
    },
    {
        product_id: 4,
        product_name: "Monitor",
        cost_price: 9000,
        product_price: 12000
    },
    {
        product_id: 5,
        product_name: "Headphones",
        cost_price: 1000,
        product_price: 1500
    }
]);

db.products.find();

const changeStream = db.products.watch(
    [
        {
            $match: {
                operationType: "update",
                "updateDescription.updatedFields.product_price": {
                    $exists: true
                }
            }
        }
    ],
    {
        fullDocument: "updateLookup"
    }
);

while (changeStream.hasNext()) {
    const change = changeStream.next();

    print("PRODUCT PRICE CHANGED");

    print("Product ID: " + change.documentKey.product_id);

    print("Product Details:");
    printjson(change.fullDocument);

    print("New Price: " +
        change.updateDescription.updatedFields.product_price);

    print("Change Time:");
    printjson(change.wallTime);
}

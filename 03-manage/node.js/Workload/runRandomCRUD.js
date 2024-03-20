const faker = require('faker');

// Function to create a random customer document and insert it into the 'customers' collection
async function createRandomCustomer(db) {
    // Generate a fake customer document
    const customer = {
        type: "customer",
        customerId: faker.datatype.uuid(),
        firstName: faker.name.firstName(),
        lastName: faker.name.lastName(),
        emailAddress: faker.internet.email(),
        phoneNumber: faker.phone.phoneNumber(),
        creationDate: faker.date.past(),
        addresses: [
            {
                addressLine1: faker.address.streetAddress(),
                city: faker.address.city(),
                state: faker.address.state(),
                country: faker.address.country(),
                zipCode: faker.address.zipCode(),
            }
        ],
        password: {
            hash: faker.datatype.uuid(),
            salt: faker.datatype.uuid(),
        },
        salesOrderCount: faker.datatype.number({ min: 1, max: 20 }),
    };
    await db.collection('customers').insertOne(customer);
}

// Function to create a random product document and insert it into the 'products' collection
async function createRandomProduct(db) {
    // Generate a fake product document
    const product = {
        categoryId: faker.datatype.uuid(),
        categoryName: faker.company.catchPhrase(),
        sku: faker.datatype.uuid(),
        name: faker.company.catchPhrase(),
        description: faker.lorem.sentence(),
        price: faker.datatype.float({ min: 10, max: 1000 }),
        tags: [
            {
                _id: faker.datatype.uuid(),
                name: faker.lorem.word(),
            }
        ],
    };
    await db.collection('products').insertOne(product);
}

// Function to create a random sales order document and insert it into the 'salesOrders' collection
async function createRandomSalesOrder(db) {
    // Generate a fake sales order document
    const sales_order = {
        type: "salesOrder",
        customerId: faker.datatype.uuid(),
        orderDate: faker.date.past(),
        shipDate: faker.date.future(),
        details: Array.from({ length: faker.datatype.number({ min: 1, max: 10 }) }, () => ({
            sku: faker.datatype.uuid(),
            name: faker.company.catchPhrase(),
            price: faker.datatype.float({ min: 10, max: 1000 }),
            quantity: faker.datatype.number({ min: 1, max: 10 }),
        })),
    };
    await db.collection('salesOrders').insertOne(sales_order);
}

// Function to run a random CRUD operation on a random collection
async function runRandomCRUDOperation(client, cosmos_db_mongodb_database) {
    const db = client.db(cosmos_db_mongodb_database);

    // Create threads for performing CRUD operations on random collections
    const collections = ['customers', 'products', 'salesOrders'];
    const num_collections = faker.datatype.number({ min: 1, max: collections.length });  // Random number of collections
    const selectedCollections = faker.helpers.shuffle(collections).slice(0, num_collections);

    for (const collection of selectedCollections) {
        await performRandomCRUDOnCollection(db, collection);
    }

    // Wait for a random time between 0.1 and 1.9 seconds
    await new Promise(resolve => setTimeout(resolve, faker.datatype.float({ min: 100, max: 1900 })));
}

// Function to perform a random CRUD operation on a collection
async function performRandomCRUDOnCollection(db, collection) {
    const operation = faker.random.arrayElement(['create', 'read', 'update', 'delete']);

    // Perform the chosen CRUD operation
    if (operation === 'create') {
        if (collection === 'customers') {
            await createRandomCustomer(db);
        } else if (collection === 'products') {
            await createRandomProduct(db);
        } else if (collection === 'salesOrders') {
            await createRandomSalesOrder(db);
        }
    } else if (operation === 'read') {
        await db.collection(collection).findOne();
    } else if (operation === 'update') {
        const document = await db.collection(collection).findOne();
        if (document) {
            await db.collection(collection).updateOne({ _id: document._id }, { $set: { name: faker.company.catchPhrase() } });
        }
    } else if (operation === 'delete') {
        const document = await db.collection(collection).findOne();
        if (document) {
            await db.collection(collection).deleteOne({ _id: document._id });
        }
    }
}

// Function to continuously run CRUD operations until the user presses the 'esc' key or 'q'
async function runCRUDOperation(client, cosmos_db_mongodb_database, rl) {
    console.log("Starting CRUD operations. Press 'q' or 'esc' to stop.");

    let running = true;

    rl.on('line', (input) => {
        if (input === 'q' || input === 'esc') {
            running = false;
            rl.close();
        }
    });

    // Continuously run CRUD operations until the stop event is set
    while (running) {
        await runRandomCRUDOperation(client, cosmos_db_mongodb_database);
    }

    console.log("CRUD operations stopped.");
}

// Export the functions
module.exports.runCRUDOperation = runCRUDOperation;
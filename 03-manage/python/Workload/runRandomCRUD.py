import pymongo
import random
import time
import threading
from faker import Faker
from pynput import keyboard

fake = Faker() # Create a Faker instance for generating fake data

# Function to create a random customer document and insert it into the 'customers' collection
def createRandomCustomer(db):
    # Generate a fake customer document
    customer = {
        "type": "customer",
        "customerId": fake.uuid4(),
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "emailAddress": fake.email(),
        "phoneNumber": fake.phone_number(),
        "creationDate": fake.date_time_this_decade(),
        "addresses": [
            {
                "addressLine1": fake.street_address(),
                "city": fake.city(),
                "state": fake.state(),
                "country": fake.country(),
                "zipCode": fake.zipcode(),
            }
        ],
        "password": {
            "hash": fake.sha256(),
            "salt": fake.sha1(),
        },
        "salesOrderCount": random.randint(1, 20),
    }
    db.customers.insert_one(customer)

# Function to create a random product document and insert it into the 'products' collection
def createRandomProduct(db):
    # Generate a fake product document
    product = {
        "categoryId": fake.uuid4(),
        "categoryName": fake.catch_phrase(),
        "sku": fake.bothify(text='??-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        "name": fake.catch_phrase(),
        "description": fake.sentence(),
        "price": random.uniform(10, 1000),
        "tags": [
            {
                "_id": fake.uuid4(),
                "name": fake.word(),
            }
        ],
    }
    db.products.insert_one(product)

# Function to create a random sales order document and insert it into the 'salesOrders' collection
def createRandomSalesOrder(db):
    # Generate a fake sales order document
    sales_order = {
        "type": "salesOrder",
        "customerId": fake.uuid4(),
        "orderDate": fake.date_time_this_decade(),
        "shipDate": fake.date_time_this_decade(),
        "details": [
            {
                "sku": fake.bothify(text='??-####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
                "name": fake.catch_phrase(),
                "price": random.uniform(10, 1000),
                "quantity": random.randint(1, 10),
            } for _ in range(random.randint(1, 10))
        ],
    }
    db.salesOrders.insert_one(sales_order)

# Function to run a random CRUD operation on a random collection
def runRandomCRUDOperation(client, cosmos_db_mongodb_database):
    db = client[cosmos_db_mongodb_database]

    # Create threads for performing CRUD operations on random collections
    threads = []
    collections = ['customers', 'products', 'salesOrders']
    num_collections = random.randint(1, len(collections))  # Random number of collections
    for collection in random.sample(collections, num_collections):
        t = threading.Thread(target=performRandomCRUDOnCollection, args=(db, collection,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Wait for a random time between 0.1 and 1.9 seconds
    time.sleep(random.uniform(0.1, 1.9))

# Function to perform a random CRUD operation on a collection
def performRandomCRUDOnCollection(db, collection):
    operation = random.choice(['create', 'read', 'update', 'delete'])

    # Perform the chosen CRUD operation
    if operation == 'create':
        if collection == 'customers':
            createRandomCustomer(db)
        elif collection == 'products':
            createRandomProduct(db)
        elif collection == 'salesOrders':
            createRandomSalesOrder(db)
    elif operation == 'read':
        document = db[collection].find_one()
    elif operation == 'update':
        document = db[collection].find_one()
        if document:
            db[collection].update_one({'_id': document['_id']}, {'$set': {'name': fake.catch_phrase()}})
    elif operation == 'delete':
        document = db[collection].find_one()
        if document:
            db[collection].delete_one({'_id': document['_id']})

# Function to continuously run CRUD operations until the user presses the 'esc' key or 'q'
def runCRUDOperation(client, cosmos_db_mongodb_database):
    print("Starting CRUD operations. Press 'q' or 'esc' to stop.")

    stop_event = threading.Event()

    def on_press(key):
        if key == keyboard.Key.esc or key.char == 'q':
            stop_event.set() # Set the stop event
            return False  # Stop listener

    # Start the key press listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Continuously run CRUD operations until the stop event is set
    while not stop_event.is_set():
        runRandomCRUDOperation(client, cosmos_db_mongodb_database)

    listener.join()  # Wait for the listener to stop

    print("CRUD operations stopped.")
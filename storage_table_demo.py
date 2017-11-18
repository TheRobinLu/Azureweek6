#Add comment at 1st line to demo update file 
import string,random,time,AzureRM,json
from azure.storage.table import TableService, Entity

# Define variables to handle Azure authentication
auth_token = azurerm.get_access_token_from_cli()
subscription_id = azurerm.get_subscription_from_cli()

# Define variables with random resource group and storage account names
resourcegroup_name = 'rlu'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
storageaccount_name = 'rlu'+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
location = 'canadaeast'

######################################
# Create the a resource group for our demo
# We need a resource group and a storage account. A random name is generated, as each storage account name must be globally unique.
###
response = azurerm.create_resource_group(auth_token, subscription_id, resourcegroup_name, location)
if response.status_code == 200 or response.status_code == 201:
    print('Resource group: ' + resourcegroup_name + ' created successfully.')
else:
    print('Error creating resource group')

# Create a storage account for our demo
response = azurerm.create_storage_account(auth_token, subscription_id, resourcegroup_name, storageaccount_name,  location, storage_type='Standard_LRS')
if response.status_code == 202:
    print('Storage account: ' + storageaccount_name + ' created successfully.')
    time.sleep(2)
else:
    print('Error creating storage account')


###
# Use the Azure Storage Storage SDK for Python to create a Table
###
print('\nLet\'s create an Azure Storage Table to store some data.')
raw_input('Press Enter to continue...')

# Each storage account has a primary and secondary access key.
# These keys are used by aplications to access data in your storage account, such as Tables.
# Obtain the primary storage access key for use with the rest of the demo

response = azurerm.get_storage_account_keys(auth_token, subscription_id, resourcegroup_name, storageaccount_name)
storageaccount_keys = json.loads(response.text)
storageaccount_primarykey = storageaccount_keys['keys'][0]['value']

# Create the Table with the Azure Storage SDK and the access key obtained in the previous step
table_service = TableService(account_name=storageaccount_name, account_key=storageaccount_primarykey)
response = table_service.create_table('itemstable')
if response == True:
    print('Storage Table: itemstable created successfully.\n')
else:
    print('Error creating Storage Table.\n')

time.sleep(1)


###
# Use the Azure Storage Storage SDK for Python to create some entries in the Table
###
print('Now let\'s add some entries to our Table.\nRemember, Azure Storage Tables is a NoSQL datastore, so this is similar to adding records to a database.')
raw_input('Press Enter to continue...')

# Each entry in a Table is called an 'Entity'. 
# Here, we add an entry for first vehicle with two pieces of data - the name, and the cost
#
# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. This makes queries much quicker.

vehicle = Entity()
vehicle.PartitionKey = 'vehicles'
vehicle.RowKey = '001'
vehicle.Maker = 'GM'
vehicle.Brand = 'Chevrolet'
vehicle.Model = 'Cruze'
vehicle.BodyStyle = '4 Door Sedan'
vehicle.Color = 'Red'
vehicle.year = '2018'
vehicle.price = 18000
table_service.insert_entity('itemstable', vehicle)
print('Created entry for GM-Chevrolet...')


vehicle = Entity()
vehicle.PartitionKey = 'vehicles'
vehicle.RowKey = '002'
vehicle.Maker = 'GM'
vehicle.Brand = 'Buick'
vehicle.Model = 'Regal'
vehicle.BodyStyle = '4 Door'
vehicle.Color = 'Silver'
vehicle.year = '2018'
vehicle.price = 48000
table_service.insert_entity('itemstable', vehicle)
print('Created entry for GM-Buick...')

vehicle = Entity()
vehicle.PartitionKey = 'vehicles'
vehicle.RowKey = '003'
vehicle.Maker = 'BMW'
vehicle.Brand = 'BMW'
vehicle.Model = 'Cabriolet'
vehicle.BodyStyle = '4 Door Sedan'
vehicle.Color = 'Brown'
vehicle.year = '2018'
vehicle.price = 58020
table_service.insert_entity('itemstable', vehicle)
print('Created entry for BMW-Cabriolet...')

vehicle = Entity()
vehicle.PartitionKey = 'vehicles'
vehicle.RowKey = '004'
vehicle.Maker = 'Audi'
vehicle.Brand = 'Audi'
vehicle.Model = 'RS 7 Sportback'
vehicle.BodyStyle = '4 Door Sedan'
vehicle.Color = 'Black'
vehicle.year = '2018'
vehicle.price = 128000
table_service.insert_entity('itemstable', vehicle)
print('Created entry for Audi-Sportback...\n')

# A partition key tracks how like-minded entries in the Table are created and queried.
# A row key is a unique ID for each entity in the partition
# These two properties are used as a primary key to index the Table. This makes queries much quicker.
#brand, flavor, size of the cup and price
coffee = Entity()
coffee.PartitionKey = 'coffees'
coffee.RowKey = '005'
coffee.brand = 'Folgers'
coffee.flavor = 'Regular'
coffee.size = 'Large'
coffee.price = 1.99
table_service.insert_entity('itemstable', coffee)
print('Created entry for a Folgers...\n')

time.sleep(1)
coffee = Entity()
coffee.PartitionKey = 'coffees'
coffee.RowKey = '006'
coffee.brand = 'Rossa'
coffee.flavor = 'Black'
coffee.size = 'Large'
coffee.price = 2.99
table_service.insert_entity('itemstable', coffee)
print('Created entry for a Rossa...\n')
time.sleep(1)


###
# Use the Azure Storage Storage SDK for Python to query for entities in our Table
###
print('With some data in our Azure Storage Table, we can query the data.\nLet\'s see what the vehicles looks like.')
raw_input('Press Enter to continue...')

# In this query, you define the partition key to search within, and then which properties to retrieve
# Structuring queries like this improves performance as your application scales up and keeps the queries efficient
items = table_service.query_entities('itemstable', filter="PartitionKey eq 'vehicles'", select='Maker,model,price')
for item in items:
    print('Maker: ' + item.Maker)
    print('Model: ' + item.Model)
    print('Price: ' + str(item.price) + '\n')

items = table_service.query_entities('itemstable', filter="PartitionKey eq 'coffees'", select='brand,size,price')
for item in items:
    print('Brand: ' + item.brand)
    print('Size: ' + item.size)
    print('Price: ' + str(item.price) + '\n')

time.sleep(1)


###
# This was a quick demo to see Tables in action.
# Although the actual cost is minimal (fractions of a cent per month) for the three entities we created, it's good to clean up resources when you're done
###
print('\nThis is a basic example of how Azure Storage Tables behave like a database.\nTo keep things tidy, let\'s clean up the Azure Storage resources we created.')
raw_input('Press Enter to continue...')

response = table_service.delete_table('itemstable')
if response == True:
    print('Storage table: itemstable deleted successfully.')
else:
    print('Error deleting Storage Table')

response = azurerm.delete_resource_group(auth_token, subscription_id, resourcegroup_name)
if response.status_code == 202:
    print('Resource group: ' + resourcegroup_name + ' deleted successfully.')
else:
    print('Error deleting resource group.')

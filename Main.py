import csv
import math
import enum
import packages
from hashTable import ChainingHashTable
from packages import loadPackageData
from packages import myHash
from tokenize import Double
from datetime import datetime, timedelta


class ChainingHashTable:
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

class Package:
    def __init__(self, ID, address, city, state, zip, deadline, weight, notes, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def __repr__(self):
        return (f"{self.ID}, {self.address}, {self.city}, {self.state}, {self.zip}, "
                f"{self.deadline}, {self.weight}, {self.notes}, {self.status}")

class Truck:
    def __init__(self):
        # self.departure = departure
        # self.time = date time object
        self.miles = 0
        self.currentLocation = '4001 South 700 East'
        self.previousLocation = ''
        self.packages = []

    def loadPackages(self, packageList):
        packages = []
        for i in range(len(packageList)):
            packages.insert(
                packageList[i], myHash.search(packageList[i]))
        self.packages = packages

    def getAddressID(packages):
        packageID = packages.packages.destination

    def findClosestNeighbor(packages):
        packages = packages.packages
        destinations = []
        addresses = list(csv.reader(open('testAddresses.csv')))

        # Get ID and address columns from addresses.csv
        for col in addresses:
            ID = col[0]
            address = col[1]

        for col in distances:
            ID = col[0]
            destinations.append(col[0])
            # print(destinations)
            # print(ID)

def loadPackageData(fileName):
    with open(fileName) as packagesToDeliver:
        packageData = csv.reader(packagesToDeliver, delimiter=',')
        next(packageData)  # skip header
        for package in packageData:
            try:
                ID = int(package[0])
                address = package[1]
                city = package[2]
                state = package[3]
                zip = package[4]
                deadline = package[5]
                weight = package[6]
                notes = package[7]
                status = "Unloaded"     #can change status to delivered at whatever time
            except ValueError as e:
                print(f"Error processing line {package}: {e}")

            # package object
            p = Package(ID, address, city, state, zip, deadline, weight, notes, status)
            #print("Printing package: ")
            #print(p)

            # insert it into the hash table
            myHash.insert(ID, p)



# makes truckDestination list with just addresses from truckPackages
def getTruckDestinations(truckPackages, truck):
    global truckDestinations
    truckDestinations = []
    for package in range(len(truckPackages)):
        truckDestinations.append(truck.packages[package].address)                   # this line is adding destinations from the truck.package, not the truck_1_package list
    return truckDestinations

# Function that takes a matrix and list of indexes(i) and returns corresponding columns.
def getColumn(matrix, i):
    return [row[i] for row in matrix]

# Returns list of column indexes given a list  of packages
def getDistanceCols(truckPackages, truck):                                                          # increments by 1 due to conversion to array
    destinations = getTruckDestinations(truckPackages, truck)
    destinationIndexes = []
    for destination in destinations:
        if destination in allAddresses:
            destinationIndexes.append(allAddresses.index(destination))
    return destinationIndexes

# Function that takes in a list of packages and returns the corresponding distance data.
def getPackageDistances(truckPackages, truck):
    destinationIndexes = getDistanceCols(truckPackages, truck)
    truckDistances = []
    for i in destinationIndexes:
        truckDistances.append(getColumn(distances, i))
    return truckDistances


def getDistances(truckPackageIDs, truckDestinations):
    packageDistances = []
    truckPackageDistanceList = []
    allPackageIDs = [[]]

    for col in addresses:
        ID = col[0]
        allPackageIDs.append(ID)

    #print('Row from address data:')
    #print(addresses[0])
    #print('Row from distance data:')
    #print(distances[0])
    #for address in range(len(addresses)):
        #print(addresses[address][1])

    #print(truckPackageDistanceList)

def getNextDestination(currentLocation):                # should this be truck_1.currentLocation?
    #global currentLocation
    currentLocation = 0                                                                                                 # orig 0, set to -1 for multi packages at same address      (idea for now)
    # indexes = getDistanceCols(truck_1.packages, truck_1)                                          original truck_1.packages
    indexes = getDistanceCols(Truck_1_Packages, truck_1)
    m = float('inf')  # Initialize m to a very high value
    currentCol = getColumn(distances, 0)                # 0 needs to be from current column
    global temp_index_address
    global milage

    for i in indexes:
        distance = currentCol[i]
        #print("Distance: " + distance)
        if distance != '0':
            distance = float(distance)
            if distance < m:
                temp_index_address = i
                m = distance
                milage = m


    # Ensure m has been updated from its initial value
    if m == float('inf'):
        print("No valid destination found")
    else:
        print(f"Closest destination is {m} miles away.")
        #print(f"Closest destination is at index {temp_index_address}")
        print(f"Closest destination is at address: {allAddresses[temp_index_address]}")
        #print(f"Truck milage is {milage}.")


def driveToLocation(truck):
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = allAddresses[temp_index_address]                                                            # set truck current location to getNextDestination()
    truck.miles += milage                                                                                               # increment truck milage with distance between the 2 locations

def deliverPackage(truck_1, Truck_1_Packages):                                                                          # marks package as delivered with timestamp
    for packages in truck_1.packages:
        if truck_1.currentLocation == packages.address:

            tempPackage = myHash.search(packages.ID)
            tempPackage.status = deliveryTime()
            myHash.insert(packages, tempPackage)
            print(f"Delivered package: {packages.ID}")
            Truck_1_Packages.remove(packages.ID)                                                                        # removes package from truck list, do last

            return Truck_1_Packages  # return updated truck package list

        # Ensure all packages are delivered at once if same address, may work on its own without accounting for them specifically


def deliveryTime():
    start_time = datetime.strptime("08:00", "%H:%M")  # start time will need to be different for other trucks
    deliveryTime = milage / 18
    #print(deliveryTime)
    delivery_timedelta = timedelta(hours=deliveryTime)
    delivery_end_time = start_time + delivery_timedelta
    #print("Delivery time is at", delivery_end_time.strftime("%I:%M %p"))
    #deliveryTimeString = "Delivered at:  " + delivery_end_time.strftime("%I:%M %p")
    deliveryTimeString = f"Delivered at: {delivery_end_time.strftime('%I:%M %p')}"

    return deliveryTimeString


def returnToHub(truck_packages):                                                                                        # if package list is empty
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = '4001 South 700 East'                                                                       # set truck current location to Hub
    #truck.miles += milage                                      # milage won't work in current configuration, set to 0 when changing trucks?
        # probably take temp_index_address and calc distance from that address to hub
    #driverAvailable()


# def driverAvailabile():                              # takes time from when T1 arrives at warehouse, and starts T3 then. OR. Calc by hand time taken, and just start T3 then. (much easier)





myHash = ChainingHashTable()                # Hash table instance
loadPackageData('testFile.csv')             # Load packages to Hash Table
distances = list(csv.reader(open('testDistance3.csv')))
addresses = list(csv.reader(open('testAddresses.csv')))

# List of all addresses
allAddresses = []
for address in range(len(addresses)):
    allAddresses.append(addresses[address][1])

# print("\nPackages from Hashtable:")
# # Fetch data from Hash Table
# for i in range(len(myHash.table) + 1):
#     print("Package: {}".format(myHash.search(i + 1)))  # 1 to 11 is sent to myHash.search()


#print(allAddresses)
#print(allAddresses [18])

Truck_1_Packages = [4, 13, 14, 15, 16, 17, 19, 20, 27, 31, 34, 35, 39, 40]       # 14 packages
Truck_2_Packages = [1, 3, 5, 7, 8, 10, 11, 12, 18 , 21, 23, 29, 30, 36, 37, 38]  # 16 packages
Truck_3_Packages = [6, 9, 24, 25, 26, 28, 32]                                    # 7  packages, departs when Truck 1 returns
Truck_1_SecondTrip_Packages = [2, 22, 33]                                        # 3 remaining packages to be delivered

truck_1 = Truck()                                                                # instantiate first truck
truck_1.loadPackages(Truck_1_Packages)                                           # load first truck

truck_2 = Truck()
truck_2.loadPackages(Truck_2_Packages)

truck_3 = Truck()
truck_3.loadPackages(Truck_3_Packages)

truck_4 = Truck()
truck_4.loadPackages(Truck_1_SecondTrip_Packages)

# truckDistances = getPackageDistances(truck_1.packages, truck_1)
#print("TRUCK DISTANCES")
#print(truckDistances)

# getNextDestination(getTruckDestinations(truck_1.packages, truck_1))
# print("Here's the next stop! ")
# print(getNextDestination(getTruckDestinations(truck_1.packages, truck_1)))

# print('\nPackages in Truck #1')
# for i, sublist in enumerate(truck_1.packages):
#     print(truck_1.packages[i])

# driveToLocation(truck_1)

#print(truck_1.currentLocation)
#print(truck_1.miles)

# deliverPackage(Truck_1_Packages)


for packages in truck_1.packages:                                                                                       # for loop to deliver packges while list had objs

    getNextDestination(getTruckDestinations(Truck_1_Packages, truck_1))                                                 # leave truck package list alone, change Truck_1_Packages
    driveToLocation(truck_1)
    deliverPackage(truck_1, Truck_1_Packages)
    truck_1.loadPackages(Truck_1_Packages)            # refresh truck.packages


    # if truck_packages is empty
        # returnToHub()

print(f" Truck 1 milage: {truck_1.miles}")

for packages in truck_2.packages:                                                        #need to tweak functions to use generic stuff

    getNextDestination(getTruckDestinations(Truck_2_Packages, truck_2))
    driveToLocation(truck_2)
    deliverPackage(truck_2, Truck_2_Packages)
    truck_2.loadPackages(Truck_2_Packages)            # refresh truck.packages


print(f" Truck 2 milage: {truck_2.miles}")


# print('\nPackages in Truck #1')
# for i, sublist in enumerate(Truck_1_Packages):
#     print(Truck_1_Packages[i])

# print("\nPackages from Hashtable:")
# # Fetch data from Hash Table
# for i in range(len(myHash.table) + 1):
#     print("Package: {}".format(myHash.search(i + 1)))  # 1 to 11 is sent to myHash.search()


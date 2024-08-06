import csv
import math
import enum
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



def getTruckDestinations(truckPackages, truck):                                                                         # makes truckDestination list with just addresses from truckPackages
    global truckDestinations
    truckDestinations = []
    for package in range(len(truckPackages)):
        truckDestinations.append(truck.packages[package].address)
    return truckDestinations


def getColumn(matrix, i):                                                                                               # Function that takes a matrix and list of indexes(i) and returns corresponding columns.
    return [row[i] for row in matrix]


def getDistanceCols(truckPackages, truck):                                                                              # Returns list of column indexes given a list  of packages, increments by 1 due to conversion to array
    destinations = getTruckDestinations(truckPackages, truck)
    destinationIndexes = []
    for destination in destinations:
        if destination in allAddresses:
            destinationIndexes.append(allAddresses.index(destination))
    return destinationIndexes


def getPackageDistances(truckPackages, truck):                                                                          # Function that takes in a list of packages and returns the corresponding distance data.
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

def getNextDestination(truckPackages, truck, currentTime):
    global temp_index_address
    global milage
    columnIndex = 0
    currentLocation = truck.currentLocation
    indexes = getDistanceCols(truckPackages, truck)                                                                     # indexes for each current package in list

    m = float('inf')                                                                                                    # Initialize m to a very high value

    for address in addresses:
        if currentLocation == address[1]:
            columnIndex = int(address[0])

    currentCol = getColumn(distances, (columnIndex - 1))

    if truckPackages == []:                                                                                             # take first element of currentCol for milage back to hub!
        milage = float(currentCol[0])
        if truck.currentLocation != '4001 South 700 East':
            currentTime = returnToHub(truck, currentTime)
            return currentTime
        else:
            milage = 0
            return currentTime

    for i in indexes:
        distance = currentCol[i]
        if distance != '0':
            distance = float(distance)
            if distance < m:
                temp_index_address = i
                m = distance
                milage = m

    if m == float('inf'):                                                                                               # Ensure m has been updated from its initial value
        print("No valid destination found")
        milage = 0
        return currentTime
    else:
        print(f"Closest destination is {m} miles away.")
        print(f"Closest destination is at address: {allAddresses[temp_index_address]}")
        return currentTime


def driveToLocation(truck):
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = allAddresses[temp_index_address]                                                            # set truck current location to getNextDestination()
    truck.miles += milage                                                                                               # increment truck milage with distance between the 2 locations

def deliverPackage(truck, truckPackages, currentTime):                                                                  # marks package as delivered with timestamp
    sameAddress = False                                                                                                 # used to keep multiple packages from adding delivery time at same address
    for packages in truck.packages:
        if truck.currentLocation == packages.address:
            tempPackage = myHash.search(packages.ID)
            tempPackage.status, currentTime = deliveryTime(currentTime, sameAddress)
            myHash.insert(packages, tempPackage)
            print(f"Delivered package: {packages.ID}")
            truckPackages.remove(packages.ID)
            sameAddress = True

    return truckPackages, currentTime                                                                                   # return updated truck package list


def deliveryTime(currentTime, sameAddress):
    if sameAddress == False:
        deliveryTime = milage / 18
        delivery_timedelta = timedelta(hours=deliveryTime)
        delivery_end_time = currentTime + delivery_timedelta
        currentTime = delivery_end_time
        print("Delivery time is at", delivery_end_time.strftime("%I:%M %p"))
        deliveryTimeString = f"Delivered at: {delivery_end_time.strftime('%I:%M %p')}"
        print("\n")

        return deliveryTimeString, currentTime

    if sameAddress == True:
        deliveryTime = 0
        delivery_timedelta = timedelta(hours=deliveryTime)
        delivery_end_time = currentTime + delivery_timedelta
        currentTime = delivery_end_time
        print("Delivery time is at", delivery_end_time.strftime("%I:%M %p"))
        deliveryTimeString = f"Delivered at: {delivery_end_time.strftime('%I:%M %p')}"
        print("\n")

        return deliveryTimeString, currentTime


def returnToHub(truck, currentTime):                                                                                    # if package list is empty
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = '4001 South 700 East'                                                                       # set truck current location to Hub
    temp_index_address = 0
    truck.miles += milage

    timeToReturn = milage / 18
    timeToReturn_timedelta = timedelta(hours=timeToReturn)
    timeToReturn_end_time = currentTime + timeToReturn_timedelta
    currentTime = timeToReturn_end_time
    return currentTime

# def driverAvailabile():                              # takes time from when T1 arrives at warehouse, and starts T3 then. OR. Calc by hand time taken, and just start T3 then. (much easier)



# MAIN START

myHash = ChainingHashTable()                                                                                            # Hash table instance
loadPackageData('testFile.csv')                                                                                         # Load packages to Hash Table
distances = list(csv.reader(open('testDistance3.csv')))
addresses = list(csv.reader(open('testAddresses.csv')))

allAddresses = []                                                                                                       # List of all addresses
for address in range(len(addresses)):
    allAddresses.append(addresses[address][1])

Truck_1_Packages = [4, 13, 14, 15, 16, 17, 19, 20, 27, 31, 34, 35, 39, 40]       # 14 packages
Truck_2_Packages = [1, 3, 5, 7, 8, 10, 11, 12, 18, 21, 23, 29, 30, 36, 37, 38]   # 16 packages
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

total_milage = 0
start_time = datetime.strptime("08:00", "%H:%M")
Driver_1_currentTime = start_time
Driver_2_currentTime = start_time

for packages in truck_1.packages:                                                                                       # for loop to deliver packges while list had objs
    Truck_1_Destinations = getTruckDestinations(Truck_1_Packages, truck_1)
    Driver_1_currentTime = getNextDestination(Truck_1_Packages, truck_1, Driver_1_currentTime)

    if ((truck_1.currentLocation == '4001 South 700 East') & (Truck_1_Packages == [])):
        break
    else:
        driveToLocation(truck_1)
        Truck_1_Packages, Driver_1_currentTime = deliverPackage(truck_1, Truck_1_Packages, Driver_1_currentTime)
        truck_1.loadPackages(Truck_1_Packages)                                                                          # refresh truck.packages

print(f"Truck 1 milage: {truck_1.miles}")
total_milage += truck_1.miles
milage = 0


for packages in truck_2.packages:
    Truck_2_Destinations = getTruckDestinations(Truck_2_Packages, truck_2)
    Driver_1_currentTime = getNextDestination(Truck_2_Packages, truck_2, Driver_1_currentTime)

    if ((truck_2.currentLocation == '4001 South 700 East') & (Truck_2_Packages == [])):
        break
    else:
        driveToLocation(truck_2)
        Truck_2_Packages, Driver_1_currentTime = deliverPackage(truck_2, Truck_2_Packages, Driver_1_currentTime)
        truck_2.loadPackages(Truck_2_Packages)                                                                          # refresh truck.packages

print(f" Truck 2 milage: {truck_2.miles}")
total_milage += truck_2.miles
milage = 0


for packages in truck_3.packages:
    Truck_3_Destinations = getTruckDestinations(Truck_3_Packages, truck_3)
    Driver_1_currentTime = getNextDestination(Truck_3_Packages, truck_3, Driver_1_currentTime)

    if ((truck_3.currentLocation == '4001 South 700 East') & (Truck_3_Packages == [])):
        break
    else:
        driveToLocation(truck_3)
        Truck_3_Packages, Driver_1_currentTime = deliverPackage(truck_3, Truck_3_Packages, Driver_1_currentTime)
        truck_3.loadPackages(Truck_3_Packages)                                                                              # refresh truck.packages

print(f" Truck 3 milage: {truck_3.miles}")
total_milage += truck_3.miles
milage = 0


for packages in truck_4.packages:
    Truck_4_Destinations = getTruckDestinations(Truck_1_SecondTrip_Packages, truck_4)
    Driver_1_currentTime = getNextDestination(Truck_1_SecondTrip_Packages, truck_4, Driver_1_currentTime)

    if ((truck_4.currentLocation == '4001 South 700 East') & (Truck_1_SecondTrip_Packages == [])):
        break
    else:
        driveToLocation(truck_4)
        Truck_1_SecondTrip_Packages, Driver_1_currentTime = deliverPackage(truck_4, Truck_1_SecondTrip_Packages, Driver_1_currentTime)
        truck_4.loadPackages(Truck_1_SecondTrip_Packages)                                                                              # refresh truck.packages


print(f" Truck 4 milage: {truck_4.miles}")
total_milage += truck_4.miles
milage = 0

print(f"The total milage for all trucks is : {total_milage}")

print("\nPackages from Hashtable:")
# Fetch data from Hash Table
for i in range(len(myHash.table) + 1):
    print("Package: {}".format(myHash.search(i + 1)))  # 1 to 11 is sent to myHash.search()
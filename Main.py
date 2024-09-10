# ID #010629953
# Ryan Parker
# WGU Email: rpar252@wgu.edu
# Date: 08/30/2024
import csv
import math
import enum
import re
from tokenize import Double
from datetime import datetime, timedelta


class ChainingHashTable:                                                                                                # O(n), chained hash table with initial value of 40
    def __init__(self, initial_capacity=40):
        self.table = [[] for i in range(initial_capacity)]

    def insert(self, key, item):                                                                                        # takes a key-item pair and inserts it into the hashtable, duplicate keys are added to next node/bucket in the list
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]

        for entry in bucket:
            if entry[0] == key:
                entry[1] = item
                return True

        bucket.append([key, item])
        return True

    def search(self, key):                                                                                              # takes a key and returns the associated item
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]

        for entry in bucket:
            if entry[0] == key:
                return entry[1]

        return None

    def remove(self, key):                                                                                              # takes a key and removes the associated item
        bucket_index = hash(key) % len(self.table)
        bucket = self.table[bucket_index]

        for entry in bucket:
            if entry[0] == key:
                bucket.remove(entry)
                return True

        return False


class Package:                                                                                                          # class for a package object
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

class Truck:                                                                                                            # O(1), class for a truck object.
    def __init__(self):
        self.miles = 0
        self.currentLocation = '4001 South 700 East'                                                                    # starting location of hub, all trucks begin here
        self.previousLocation = ''
        self.packages = []

    def addPackages(self, packageIDs):                                                                                  # O(n^2), loads packages onto truck objects
        loadedPackages = []
        for index in range(len(packageIDs)):
            loadedPackages.insert(
                packageIDs[index], myHash.search(packageIDs[index])
            )
        self.packages = loadedPackages

    def findAddressID(package):                                                                                         # O(1), takes a package and returns the delivery address ID
        addressID = package.packages.destination
        return addressID


def getPackageData(fileName):                                                           # O(n * m), loads package data from file, creates package objects, and inserts them into the hash table
    with open(fileName) as file:
        packageData = csv.reader(file, delimiter=',')
        next(packageData)                                                                                               # Skip the header row

        for package in packageData:
            try:
                ID = int(package[0])
                address, city, state, zip, deadline, weight, notes = package[1:8]
                status = "At the Hub"

                packageObj = Package(ID, address, city, state, zip, deadline, weight, notes, status)                    # package object
                myHash.insert(ID, packageObj)                                                                           # insert it into the hash table

            except ValueError as error:
                print(f"Error processing package {package}: {error}")


def extractDeliveryAddresses(packageList, deliveryVehicle):                                                             # O(n), makes truck destination list with just addresses from truckPackages
    global deliveryAddresses
    deliveryAddresses = []
    for i in range(len(packageList)):
        deliveryAddresses.append(deliveryVehicle.packages[i].address)
    return deliveryAddresses


def extractColumn(grid, index):                                                                                         # O(n), Function that takes a matrix and list of indexes(i) and returns corresponding columns.
    return [row[index] for row in grid]


def findColumnIndexes(packageList, vehicle):                                                                            # O(n * m), Returns list of column indexes given a list  of packages, increments by 1 due to conversion to array
    addresses = extractDeliveryAddresses(packageList, vehicle)
    columnIndexes = []
    for address in addresses:
        if address in allAddresses:
            columnIndexes.append(allAddresses.index(address))
    return columnIndexes


def calculatePackageDistances(packageList, vehicle):                                                                    # O(n(m + r)), Function that takes in a list of packages and returns the corresponding distance data.
    columnIndexes = findColumnIndexes(packageList, vehicle)
    distanceData = []
    for index in columnIndexes:
        distanceData.append(extractColumn(distanceMatrix, index))
    return distanceData


def findNextStop(truckPackages, truck, currentTime):                                                                    # O(n * m + a + r), finds the next stop based on shorted distance from current location
    global temp_index_address
    global milage
    columnIndex = 0
    currentLocation = truck.currentLocation
    indexes = findColumnIndexes(truckPackages, truck)                                                                   # indexes for each current package in list

    m = float('inf')                                                                                                    # Initialize m to a very high value

    for address in addresses:
        if currentLocation == address[1]:
            columnIndex = int(address[0])

    currentCol = extractColumn(distances, (columnIndex - 1))

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
        milage = 0
        return currentTime
    else:
        return currentTime


def driveToLocation(truck):                                                                                             # O(1), simulates driving to next location
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = allAddresses[temp_index_address]                                                            # set truck current location to findNextStop()
    truck.miles += milage                                                                                               # increment truck milage with distance between the 2 locations

def deliverPackage(truck, truckPackages, currentTime):                                                                  # O(n(m + k)), marks package as delivered with timestamp
    sameAddress = False                                                                                                 # used to keep multiple packages from adding delivery time at same address
    for packages in truck.packages:
        if truck.currentLocation == packages.address:
            tempPackage = myHash.search(packages.ID)
            tempPackage.status, currentTime = deliveryTime(currentTime, sameAddress)
            myHash.insert(packages, tempPackage)
            truckPackages.remove(packages.ID)
            sameAddress = True

    return truckPackages, currentTime                                                                                   # return updated truck package list and updated driver time


def deliveryTime(currentTime, sameAddress):                                                                             # O(1), updates each drivers time based upon distance traveled and set speed
    if sameAddress == False:
        deliveryTime = milage / 18
        delivery_timedelta = timedelta(hours=deliveryTime)
        delivery_end_time = currentTime + delivery_timedelta
        currentTime = delivery_end_time
        deliveryTimeString = f"Delivered at: {delivery_end_time.strftime('%I:%M %p')}"

        return deliveryTimeString, currentTime

    if sameAddress == True:
        deliveryTime = 0
        delivery_timedelta = timedelta(hours=deliveryTime)
        delivery_end_time = currentTime + delivery_timedelta
        currentTime = delivery_end_time
        deliveryTimeString = f"Delivered at: {delivery_end_time.strftime('%I:%M %p')}"

        return deliveryTimeString, currentTime


def returnToHub(truck, currentTime):                                                                                    # O(1), if package list is empty, returns truck to hub for reloading
    truck.previousLocation = truck.currentLocation                                                                      # Set truck previous location to current location
    truck.currentLocation = '4001 South 700 East'                                                                       # set truck current location to Hub
    temp_index_address = 0
    truck.miles += milage

    timeToReturn = milage / 18
    timeToReturn_timedelta = timedelta(hours=timeToReturn)
    timeToReturn_end_time = currentTime + timeToReturn_timedelta
    currentTime = timeToReturn_end_time
    return currentTime


def userInterface(total_milage):                                                                                        # O(c * n), takes user input to determine output
    print("\n")
    print("PARCEL DELIVERY SERVICE")
    print("\t 1. Print All Package Status and Total Mileage")                                                           # print all packages
    print("\t 2. Get a Single Package Status with a Time")                                                              # take id & time, return package status at that time
    print("\t 3. Get All Package Status with a Time")                                                                   # take time, return all packages at that time
    print("\t 4. Get single Package Status")
    print("\t 5. Exit")
    valid_options = [1, 2, 3, 4, 5]

    option = None

    while option is None:
        user_input = input("\nPlease enter your selection: ")

        if user_input.isdigit() and int(user_input) in valid_options:
            option = int(user_input)
        else:
            print("Error: Invalid option provided.")

    if option == 1:                                                                                                     # print all packages
        print("\nPackages from Hashtable:")
        for i in range(len(myHash.table) + 1):
            print("Package: {}".format(myHash.search(i + 1)))

        print("\n")
        print(f"The total milage for all trucks is : {total_milage} miles.")
        print("\n")
                                                                                            # allow for multiple selections without restarting
        return True

    if option == 2:                                                                                                     #look up package at a time and check the info and status

        timeQuery = False                                                                                               # gets time
        while timeQuery == False:
            try:
                timeQuery = datetime.strptime(input("Please enter a time in the following format [hr:min am/pm]: "), "%I:%M %p")
            except:
                print("Improper input, please try again.")

        packageInput = None
        while packageInput is None:
                packageInput = input("Please enter the package id: ")

                if packageInput.isdigit():
                    if myHash.search(int(packageInput)) is not None:
                        package_id = int(packageInput)
                    else:
                        print("\tNo package found with the provided ID.\n")
                        packageInput = None
                else:
                    print("Improper input, please try again.")
                    packageInput = None




        packageNineUpdateTime = datetime.strptime("10:20", "%H:%M")
        if (packageInput == "9") & (timeQuery < packageNineUpdateTime):                     # TQ 10:20am < 10:20am
            print("Made it into address change in option 2")
            updatedPackageNine = myHash.search(9)
            updatedPackageNine.address = "300 State St"

            myHash.remove(9)  # remove old 9
            myHash.insert(9, updatedPackageNine)


        queriedPackage = myHash.search(package_id)

        status = queriedPackage.status                                          # 08:00 am
        deliveredTime = status.split("at: ")[1].strip()                         # string from package status
        time_obj = datetime.strptime(deliveredTime, "%I:%M %p")         # string converted to timeobject of just time
        print("\n")

        if timeQuery < time_obj:                                                                                        # if time entered is before delivery time,
            tempStatus = queriedPackage.status
            queriedPackage.status = "At the Hub at: " + timeQuery.strftime("%I:%M %p")
            print(queriedPackage)
            queriedPackage.status = tempStatus

        elif timeQuery > time_obj:
            print(queriedPackage)
        else:
            print(queriedPackage)

        print("\n")

        return True

    if option == 3:                                     # get inputTime, create a list of all packages delivered by that time. Another list of undelivered, append this list undelivered.

        timeQuery_3 = False                                                                                             # gets time
        while timeQuery_3 == False:
            try:
                timeQuery_3 = datetime.strptime(input("Please enter a time in the following format [hr:min am/pm]: "), "%I:%M %p")
            except:
                print("Improper input, please try again.")

        packageNineUpdateTime = datetime.strptime("10:20", "%H:%M")
        if timeQuery_3 < packageNineUpdateTime:                     # TQ 10:20am < 10:20am
            print("Made it into address change in option 3")
            updatedPackageNine = myHash.search(9)
            updatedPackageNine.address = "300 State St"

            myHash.remove(9)  # remove old 9
            myHash.insert(9, updatedPackageNine)

        undeliveredPackagesArray = []

        for i in range(len(myHash.table) + 1):

            tempPackage3 = myHash.search(i + 1)

            if tempPackage3 is not None:
                status = tempPackage3.status
                deliveryTime = status.split("at: ")[1].strip()                                                          # string from package status
                time_obj3 = datetime.strptime(deliveryTime, "%I:%M %p")

                if timeQuery_3 < time_obj3:                                                                             # if time entered is before delivery time,
                    tempStatus3 = tempPackage3.status
                    tempPackage3.status = "At the Hub at: " + timeQuery_3.strftime("%I:%M %p")
                    print(tempPackage3)
                    tempPackage3.status = tempStatus3

                elif timeQuery_3 > time_obj3:

                    print(tempPackage3)

        return True

    if option == 4:
        packageInput = None
        while packageInput is None:
            packageInput = input("Please enter the package id: ")

            if packageInput.isdigit():
                if myHash.search(int(packageInput)) is not None:
                    package_id = int(packageInput)
                else:
                    print("\tNo package found with the provided ID.\n")
                    packageInput = None
            else:
                print("Improper input, please try again.")
                packageInput = None

        queriedPackage = myHash.search(package_id)
        print(queriedPackage)

        return True


    if option == 5:
        exit()


def truckSimulation():                                                                                                  # O(n * m(a + r)), main simulation which runs by default to deliver packages
    #myHash = ChainingHashTable()                                                                                        # Hash table instance
    getPackageData('PackageFile.csv')                                                                                   # Load packages to Hash Table from package file
    distances = list(csv.reader(open('DistanceFile.csv')))                                                              # Load distance data from distance file
    addresses = list(csv.reader(open('AddressFile.csv')))                                                               # Load address data from address file

    allAddresses = []                                                                                                   # List of all addresses
    for address in range(len(addresses)):
        allAddresses.append(addresses[address][1])

    Truck_1_Packages = [4, 13, 14, 15, 16, 17, 19, 20, 27, 31, 34, 35, 39, 40]                                          # 14 packages
    Truck_2_Packages = [1, 3, 5, 7, 8, 10, 11, 12, 18, 21, 23, 29, 30, 36, 37, 38]                                      # 16 packages
    Truck_1_SecondTrip_Packages = [6, 9, 24, 25, 26, 28, 32]                                                            # 7  packages, departs when Truck 1 returns
    Truck_2_SecondTrip_Packages = [2, 22, 33]                                                                           # 3  packages, departs when Truck 2 returns

    truck_1 = Truck()                                                                                                   # instantiate first truck
    truck_1.addPackages(Truck_1_Packages)                                                                               # load first truck

    truck_2 = Truck()                                                                                                   # instantiate second truck
    truck_2.addPackages(Truck_2_Packages)                                                                               # load second truck

    total_milage = 0
    start_time = datetime.strptime("08:00", "%H:%M")
    Driver_1_currentTime = start_time                                                                                   # sets driver 1 start time to 8:00am
    Driver_2_currentTime = start_time                                                                                   # sets driver 2 start time to 8:00am

    for packages in truck_1.packages:  # for loop to deliver packges while list had objs                                Truck 1, trip 1 deliveries
        Truck_1_Destinations = extractDeliveryAddresses(Truck_1_Packages, truck_1)
        Driver_1_currentTime = findNextStop(Truck_1_Packages, truck_1, Driver_1_currentTime)

        if ((truck_1.currentLocation == '4001 South 700 East') & (Truck_1_Packages == [])):
            break
        else:
            driveToLocation(truck_1)
            Truck_1_Packages, Driver_1_currentTime = deliverPackage(truck_1, Truck_1_Packages, Driver_1_currentTime)
            truck_1.addPackages(Truck_1_Packages)  # refresh truck.packages

    total_milage += truck_1.miles
    milage = 0

    for packages in truck_2.packages:                                                                                   #Truck 2, trip 1 deliveries
        Truck_2_Destinations = extractDeliveryAddresses(Truck_2_Packages, truck_2)
        Driver_2_currentTime = findNextStop(Truck_2_Packages, truck_2, Driver_2_currentTime)

        if ((truck_2.currentLocation == '4001 South 700 East') & (Truck_2_Packages == [])):
            break
        else:
            driveToLocation(truck_2)
            Truck_2_Packages, Driver_2_currentTime = deliverPackage(truck_2, Truck_2_Packages, Driver_2_currentTime)
            truck_2.addPackages(Truck_2_Packages)  # refresh truck.packages

    total_milage += truck_2.miles
    milage = 0

    truck_1.addPackages(Truck_1_SecondTrip_Packages)  # reload Truck 1 for second trip
    truck_1.miles = 0  # resets truck miles for this trip


    packageUpdated = False

    for packages in truck_1.packages:                                                                                   #Truck 1, trip 2 deliveries

        packageUpdateTime = datetime.strptime("10:20", "%H:%M")

        if (Driver_1_currentTime >= packageUpdateTime) & (packageUpdated == False):                                     # if time is after 10:20am
                                                                                                                        # update package 9 to correct address
            updatedPackageNine = myHash.search(9)
            updatedPackageNine.address = "410 S State St"

            myHash.remove(9)                                                                                            # remove old 9
            myHash.insert(9, updatedPackageNine)                                                                   # insert updated 9

            packageUpdated = True
            truck_1.addPackages(Truck_1_SecondTrip_Packages)                                                            # refresh truck list with updated package data
        elif (Driver_1_currentTime < packageUpdateTime):
            updatedPackageNine = myHash.search(9)
            updatedPackageNine.address = "300 State St"

            myHash.remove(9)                                                                                            # remove old 9
            myHash.insert(9, updatedPackageNine)                                                                   # insert updated 9

            truck_1.addPackages(Truck_1_SecondTrip_Packages)                                                            # refresh truck list with updated package data


        truck_1_Destinations = extractDeliveryAddresses(Truck_1_SecondTrip_Packages, truck_1)
        Driver_1_currentTime = findNextStop(Truck_1_SecondTrip_Packages, truck_1, Driver_1_currentTime)

        if ((truck_1.currentLocation == '4001 South 700 East') & (Truck_1_SecondTrip_Packages == [])):
            break
        else:
            driveToLocation(truck_1)
            Truck_1_SecondTrip_Packages, Driver_1_currentTime = deliverPackage(truck_1, Truck_1_SecondTrip_Packages,
                                                                               Driver_1_currentTime)
            truck_1.addPackages(Truck_1_SecondTrip_Packages)  # refresh truck.packages

    total_milage += truck_1.miles
    milage = 0

    truck_2.addPackages(Truck_2_SecondTrip_Packages)  # reload Truck 2 for second trip
    truck_2.miles = 0  # resets truck miles for this trip

    for packages in truck_2.packages:                                                                                   #Truck 2, trip 2 deliveries
        truck_2_Destinations = extractDeliveryAddresses(Truck_2_SecondTrip_Packages, truck_2)
        Driver_2_currentTime = findNextStop(Truck_2_SecondTrip_Packages, truck_2, Driver_2_currentTime)

        if ((truck_2.currentLocation == '4001 South 700 East') & (Truck_2_SecondTrip_Packages == [])):
            break
        else:
            driveToLocation(truck_2)
            Truck_2_SecondTrip_Packages, Driver_2_currentTime = deliverPackage(truck_2, Truck_2_SecondTrip_Packages,
                                                                               Driver_2_currentTime)
            truck_2.addPackages(Truck_2_SecondTrip_Packages)  # refresh truck.packages

    total_milage += truck_2.miles
    milage = 0
    print("\n")
    return total_milage                                                                                                 # total milage is 104.6 mi



# MAIN START                                                                                                            Overall, program is O(P * T * A)

myHash = ChainingHashTable()                                                                                            # Hash table instance
getPackageData('PackageFile.csv')                                                                                       # Load packages to Hash Table
distances = list(csv.reader(open('DistanceFile.csv')))
addresses = list(csv.reader(open('AddressFile.csv')))

allAddresses = []                                                                                                       # List of all addresses
for address in range(len(addresses)):
    allAddresses.append(addresses[address][1])


total_milage = truckSimulation()

while userInterface(total_milage) is not None:
    userInterface(total_milage)                                                                                         # simulation fully runs, then user interface enables
    truckSimulation()
#!/usr/bin/python
# Castillo, Justin S.


class Car:

    def __init__(self):

        self.carTable = []  # Car table | unique key: name | (ex. tuple: ["A", "Red"])

    def store_car(self, name, color):

        self.carTable.append([name, color])

    def query_car(self):

        return self.carTable

    def query_car_byname(self, name):

        for c in self.carTable:
            if c[0] == name:
                return c


class CarWarehouse:

    def __init__(self):

        self.carWarehouseTable = []  # Car Warehouse table | unique key: index | (ex. tuple: [0, 'A'])
        self.myCar = Car()
        self.currentIndex = 0

    def store_car(self, name, color):

        self.myCar.store_car(name, color)  # Add record to Car Table

        # Add record to Car Warehouse Table with the 'name' Foreign key
        self.carWarehouseTable.append([self.currentIndex, name])
        self.currentIndex += 1

    def query_carwarehouse(self):

        return self.carWarehouseTable[::-1]  # reverse list to reflect order of append

    def query_join_carandcarwarehouse(self):  # simple join car and car warehouse tables

        joinedtable = []  # ex. tuple [0, 'A', "Blue"]

        for i in reversed(self.carWarehouseTable):  # reverse list to reflect order of append
            # get color att. from car table using car warehouse table name foreign key
            joinedtable.append([i[0], i[1], self.myCar.query_car_byname(i[1])[1]])

        return joinedtable

    def query_car_names(self): # returns car names from car warehouse table

        nametable = []

        for c in reversed(self.carWarehouseTable):
            nametable.append(c[1])

        return nametable

    def query_car_index_byname(self, name):

        for c in self.carWarehouseTable:
            if c[1] == name:
                return c[0]

    def query_by_color(self, color):

        bycolortable = []

        for c in self.query_join_carandcarwarehouse():
            if c[2] == color:
                bycolortable.append(c[1])

        return bycolortable

    def move_car_infrontof(self, move_car_name, scoot_car_name):

        move_car_index = self.query_car_index_byname(move_car_name)
        scoot_car_index = self.query_car_index_byname(scoot_car_name)

        ismoveafterscoot = True
        if self.query_car_index_byname(move_car_name) > self.query_car_index_byname(scoot_car_name):
            ismoveafterscoot = False

        self.carWarehouseTable.pop(move_car_index)

        if ismoveafterscoot:
            self.carWarehouseTable.insert(scoot_car_index, [scoot_car_index, move_car_name])
        else:
            self.carWarehouseTable.insert(scoot_car_index+1, [scoot_car_index+1, move_car_name])

        for ind in range(self.currentIndex):  # Realigning the index field of car warehouse table
            self.carWarehouseTable[ind][0] = ind

        return self.query_car_names()


if __name__ == "__main__":

    myCarWarehouse = CarWarehouse()
    stop = False

    while not stop:
        i = input("\n[1]Store Car\n[2]Query Cars by Color\n[3]Move Cars\n[0]Exit\n>")

        if i == '0':
            print("Exiting..")
            stop = True

        elif i == '1':
            stop1 = False
            while not stop1:
                i = input("Enter car name and color separated by comma(ex. name,Blue/Red):\n>")
                i = i.split(',')
                myCarWarehouse.store_car(i[0], i[1])
                print("Car List: ", myCarWarehouse.query_car_names())
                i = input("Enter another? (y/n):\n>")
                if i == 'n':
                    stop1 = True

        elif i == '2':
            stop2 = False
            while not stop2:
                i = input("Enter car color to query(Blue/Red):\n>")
                print("%s Cars:" % i, myCarWarehouse.query_by_color(i))
                i = input("Enter another? (y/n):\n>")
                if i == 'n':
                    stop2 = True

        elif i == '3':
            stop3 = False
            while not stop3:
                print("Car List: ", myCarWarehouse.query_car_names())
                i = input("Enter the car to move in front of another car separated by comma(ex. A,B)\n>")
                i = i.split(',')
                print("%s to %s: " % (i[0], i[1]), myCarWarehouse.move_car_infrontof(i[0], i[1]), "\n")
                i = input("Enter another? (y/n):\n>")
                if i == 'n':
                    stop3 = True

        else:
            print("Wrong code")

    print(myCarWarehouse.query_join_carandcarwarehouse())

# Sample console Input (Copy/Paste)
# 1
# A,Blue
# y
# C,Red
# y
# E,Blue
# y
# B,Red
# y
# D,Blue
# n
# 2
# Blue
# y
# Red
# n
# 3
# C,B
# y
# A,D
# y
# D,A
# y
# A,E
# y
# C,E
# y
# D,B
# n
# 0

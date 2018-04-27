# -*- coding: UTF-8 -*-

class PrireData:
    def __init__(self, unit_price, total_price):
        self.unit_price = unit_price
        self.total_price = total_price

    def get_unit_price(self):
        return self.unit_price

    def get_total_price(self):
        return self.total_price

class BaseData:
    def __init__(self, location, house_name, address, area, status, type):
        self.location = location
        self.house_name = house_name
        self.address = address
        self.area = area
        self.atatus = status
        self.type = type

    def get_status(self):
        return self.atatus

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location

    def get_house_name(self):
        return self.house_name

    def get_address(self):
        return self.address

    def get_area(self):
        return self.area


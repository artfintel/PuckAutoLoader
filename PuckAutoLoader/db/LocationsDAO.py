from PuckAutoLoader.utils.DBManager import DBManager
from PuckAutoLoader.db.Location import Location
from PuckAutoLoader.db.Database import Database


# database access object
class LocationDAO(Database):
    def __init__(self):
        super().__init__(self)
        print("access location database")

    def get_location_list(self):
        location = self.db.execute_all("select id, name from lims_containerlocation where id >=147 and id <= 175")
        location_list = []

        for loc in location:
            location_list.append(Location(loc['id'], loc['name']))

        return location_list


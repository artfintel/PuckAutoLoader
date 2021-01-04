from PuckAutoLoader.utils.DBManager import DBManager
from PuckAutoLoader.db.Containers import Containers
from PuckAutoLoader.db.Database import Database


# database access object
class ContainersDAO(Database):
    def __init__(self):
        super().__init__()
        print("access container database")

    def get_container_list(self):
        containers = self.db.execute_all("select name, location_id, parent_id from lims_container where status=2 and location_id != 'None' order by name")
        containerlist = []

        for puck in containers:
            containerlist.append(Containers(puck['name'], puck['location_id'], puck['parent_id']))

        return containerlist

    def get_container_list_all(self):
        containers = self.db.execute_all("select name, location_id, parent_id from lims_container where status=2 order by name")
        containerlist = []

        for puck in containers:
            containerlist.append(Containers(puck['name'], puck['location_id'], puck['parent_id']))

        return containerlist

    def check_empty_location(self, location_id):
        location = self.db.execute_all("select location_id from lims_container where location_id = " + str(location_id) +" order by name")
        if location != "" :
            return True
        else:
            return False

    def load_container(self, name, location_id):
        self.db.execute("update lims_container set location_id=" + str(location_id) + ", parent_id=1 where name='" + name + "' and status=2")
        self.db.commit()

    def unload_container(self, name):
        self.db.execute("update lims_container set location_id=DEFAULT, parent_id=DEFAULT where name='" + name + "'")
        self.db.commit()

    def unload_container_loc(self, location_id):
        result = self.db.execute_all("select name from lims_container where location_id = '" + str(location_id) + "' ")
        name = result[0]['name']
        self.db.execute("update lims_container set location_id=DEFAULT, parent_id=DEFAULT where name='" + name + "'")
        self.db.commit()

    def validate_check_puck(self, name):
        container = self.get_container(name)
        if len(container) == 1:
            return True
        else:
            return False

    def validate_check_position(self, name):
        container = self.get_container(name)
        if container[0]['location_id'] == None :
            return True
        else:
            return False

    def get_container(self, name):
        container = self.db.execute_all(
            "select name, location_id from lims_container where status=2 and name='" + name + "'")
        return container
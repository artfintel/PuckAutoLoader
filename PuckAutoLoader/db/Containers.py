class Containers:
    def __init__(self, container_id, location_id, parent_id):
        self.container_id = container_id
        self.location_id = location_id
        self.parent_id = parent_id

    def get_container_id(self):
        return self.container_id

    def set_container_id(self, container_id):
        self.container_id = container_id

    def get_location_id(self):
        return self.location_id

    def set_location_id(self, location_id):
        self.location_id = location_id

    def get_parent_id(self):
        return self.parent_id

    def set_parent_id(self, parent_id):
        self.parent_id = parent_id
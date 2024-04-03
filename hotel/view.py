from app.renderer import ClientRenderer, EmployeeRenderer, HotelRoomRenderer, AdditionalServiceRenderer


class ClientView:
    def __init__(self):
        self.renderer = ClientRenderer()

    def create_new_client_window(self):
        # TODO: Add success message and error message to view
        self.renderer.create_new_client_window()

    def read_and_delete_all_clients_window(self):
        self.renderer.read_all_clients_window()

    def update_client_window(self, client_id):
        self.renderer.draw_update_client_window(client_id)


class EmployeeView:
    def __init__(self):
        self.renderer = EmployeeRenderer()

    def create_new_employee_window(self):
        # TODO: Add success message and error message to view
        self.renderer.draw_create_new_employee_window()

    def read_and_delete_all_employees_window(self):
        self.renderer.draw_read_all_employees_window()

    def update_employee_window(self, employee_id):
        self.renderer.draw_update_employee_window(employee_id)


class HotelRoomView:
    def __init__(self):
        self.renderer = HotelRoomRenderer()

    def create_new_room_window(self):
        self.renderer.draw_create_new_room_window()

    def list_and_deactivate_all_hotel_rooms_window(self):
        self.renderer.draw_list_and_deactivate_hotel_rooms_window()

    def update_hotel_room_window(self, room_id):
        self.renderer.draw_update_hotel_room_window(room_id)


class AdditionalServiceView:
    def __init__(self):
        self.renderer = AdditionalServiceRenderer()

    def create_new_service_window(self):
        self.renderer.draw_create_new_service_window()

    def read_and_delete_service_window(self):
        self.renderer.draw_list_and_delete_service_window()

    def update_service_window(self, service_id):
        self.renderer.draw_update_service_window(service_id)

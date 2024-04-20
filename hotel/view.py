import sys
from abc import abstractmethod

from PyQt6.QtWidgets import QApplication

# from app.renderer import ClientRenderer, EmployeeRenderer, HotelRoomRenderer, AdditionalServiceRenderer, \
#     JobPositionRenderer, DepartmentRenderer, RoomTypeRenderer, WorkScheduleRenderer
from design.qt.table import QTClientsTable


class View:
    @abstractmethod
    def create_new_view_window(self):
        pass
        # self.renderer.draw_create_new_job_position_window()

    @abstractmethod
    def read_and_delete_view_window(self):
        pass
        # self.renderer.draw_list_and_delete_job_position_window()

    @abstractmethod
    def update_view_window(self, object_id: int):
        pass
        # self.renderer.draw_update_job_position_window(service_id)


class ClientView(View):
    def __init__(self):
        self.app = QApplication(sys.argv)
        # self.renderer = ClientRenderer()

    def create_new_view_window(self):
        # TODO: Add success message and error message to view
        self.renderer.create_new_client_window()

    def read_and_delete_view_window(self):
        self.__read_all_clients_window()

    def __read_all_clients_window(self):
        all_clients_table = QTClientsTable()
        all_clients_table.show()
        sys.exit(self.app.exec())

    def update_view_window(self, client_id):
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


class JobPositionView:
    def __init__(self):
        self.renderer = JobPositionRenderer()

    def create_new_view_window(self):
        self.renderer.draw_window_create()

    def read_and_delete_view_window(self):
        self.renderer.draw_window_read_delete()

    def update_view_window(self, job_position_id):
        self.renderer.draw_window_update(job_position_id)


class DepartmentView(View):
    def __init__(self):
        self.renderer = DepartmentRenderer()

    def create_new_view_window(self):
        self.renderer.draw_window_create()

    def read_and_delete_view_window(self):
        self.renderer.draw_window_read_delete()

    def update_view_window(self, department_id):
        self.renderer.draw_window_update(department_id)


class RoomTypeView(View):
    def __init__(self):
        self.renderer = RoomTypeRenderer()

    def create_new_view_window(self):
        self.renderer.draw_window_create()

    def read_and_delete_view_window(self):
        self.renderer.draw_window_read_delete()

    def update_view_window(self, room_type_id):
        self.renderer.draw_window_update(room_type_id)


class WorkScheduleView(View):
    def __init__(self):
        self.renderer = WorkScheduleRenderer()

    def create_new_view_window(self):
        self.renderer.draw_window_create()

    def read_and_delete_view_window(self):
        self.renderer.draw_window_read_delete()

    def update_view_window(self, work_schedule_id):
        self.renderer.draw_window_update(work_schedule_id)

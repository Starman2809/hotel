from hotel.models import Employee
from hotel.view import ClientView, EmployeeView, HotelRoomView, AdditionalServiceView


def main():
    # client_view = ClientView()
    # client_view.create_new_client_window()
    # client_view.read_and_delete_all_clients_window()
    # client_id = 5
    # client_view.update_client_window(client_id)

    # employee_view = EmployeeView()
    # employee_view.create_new_employee_window()
    # employee_view.read_and_delete_all_employees_window()
    # employee_id = 6
    # employee_view.update_employee_window(employee_id)


    # hotel_room_view = HotelRoomView()
    # hotel_room_view.create_new_room_window()
    # hotel_room_view.read_and_delete_all_hotel_rooms_window()
    # hotel_room_id = 1
    # hotel_room_view.update_hotel_room_window(hotel_room_id)

    # hotel_controller.book_a_room_window()

    additional_service_view = AdditionalServiceView()
    # additional_service_view.create_new_service_window()
    additional_service_view.read_and_delete_service_window()
    # service_id = 2
    # additional_service_view.update_service_window(service_id)


    # hotel_controller = HotelController()
    # hotel_controller.create_new_client_window()
    # hotel_controller.print_database_on_window()
    # print(hotel_controller.get_tables())
    # print(len(hotel_controller.get_clients()))
    # print((hotel_controller.get_clients()[0]))
    # print((hotel_controller.get_clients()[-1]))
    # print(hotel_controller.get_clients())
    # hotel_controller.create_client()
    # print(())
    # listqweweq = ['Клиенты', 'Оплата', 'Персонал',]
    #
    # for item in listqweweq:
    #     print(hotel_controller.get_columns_from_table(item))
    #     print("-----------------------------------")

    # clients = Employee.all()
    # for client in clients:
    #     print(client)
    #     print("----------------------------------")
    # print(hotel_controller.get_columns_from_table("Клиенты"))
    # print(hotel_controller.get_tables())


if __name__ == "__main__":
    print(123)
    main()

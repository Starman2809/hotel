from hotel.models import Employee
from hotel.view import ClientView, EmployeeView


def main():
    client_view = ClientView()
    # client_view.create_new_client_window()
    # client_view.read_and_delete_all_clients_window()
    # client_id = 5
    # client_view.update_client_window(client_id)

    employee_view = EmployeeView()
    # employee_view.create_new_employee_window()
    # employee_view.read_and_delete_all_employee_window()
    employee_id = 6
    employee_view.update_employee_window(employee_id)


    # hotel_controller.book_a_room_window()


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

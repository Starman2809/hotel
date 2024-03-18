from db.models import Client
from renderer import HotelRenderer


class HotelController:

    def __init__(self):
        self.renderer = HotelRenderer()

    def create_new_client_window(self):
        # TODO: Add success message and error message to view
        self.renderer.create_new_client_window()

    def book_a_room_window(self):
        self.renderer.book_a_room()

    def read_all_clients_window(self):
        self.renderer.read_all_clients_window()

    def update_client_window(self):
        self.renderer.update_client_window()

    def delete_client_window(self):
        self.renderer.delete_client_window()


def main():
    hotel_controller = HotelController()
    # hotel_controller.create_new_client_window()
    hotel_controller.book_a_room_window()
    # hotel_controller.read_all_clients_window()

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

    clients = Client.get_all_clients()
    for client in clients:
        print(client)
        print("----------------------------------")
    # print(hotel_controller.get_columns_from_table("Клиенты"))
    # print(hotel_controller.get_tables())


if __name__ == "__main__":
    print(123)
    main()

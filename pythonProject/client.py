import socket
import json

# Constants
HOST = '127.0.0.1'
PORT = 5050


# Connect to the server
def connect_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s


# Send request to server
def send_request(s, request):
    s.sendall(json.dumps(request).encode())
    response = s.recv(1024)
    return json.loads(response.decode())


# Owner menu management
def manage_menu(s):
    while True:
        action = input("Enter 'add' to add item, 'modify' to modify item, or 'exit' to quit: ")
        if action == 'add' or action == 'modify':
            item = input("Enter food item name: ")
            price = input("Enter price: ")
            send_request(s, {'type': 'update_menu', 'menu': {item: price}})
        elif action == 'exit':
            break


# Customer ordering
def place_order(s):
    response = send_request(s, {'type': 'request_menu'})
    print("Menu:", response['menu'])
    order = {}
    while True:
        item = input("Enter item to order or 'done' to finish: ")
        if item == 'done':
            break
        if item in response['menu']:
            quantity = int(input("Enter quantity: "))
            order[item] = quantity
    address = input("Enter delivery address: ")
    return send_request(s, {'type': 'place_order', 'order': order, 'address': address})


# Main function
def main():
    s = connect_server()
    user_choice = input("Enter 'owner' to log in as owner or press Enter to continue as customer: ").lower()

    if user_choice == 'owner':
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == 'owner1' and password == '1111':
            manage_menu(s)
        else:
            print("Login failed.")
    else:
        print(place_order(s))

    s.close()


if __name__ == '__main__':
    main()

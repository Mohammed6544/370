import socket
import json
import threading

# Constants
HOST = '127.0.0.1'
PORT = 5050
menu_file = 'menu.json'
users_file = 'users.json'

# Load JSON data from file
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save JSON data to file
def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Handle client requests
def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            request = json.loads(data.decode())
            response = process_request(request)
            conn.sendall(json.dumps(response).encode())
    finally:
        conn.close()

# Process client request
def process_request(request):
    users = load_data(users_file)
    if request['type'] == 'login':
        if request['username'] in users and users[request['username']]['password'] == request['password']:
            return {'status': 'success', 'type': users[request['username']]['type']}
        else:
            return {'status': 'error', 'message': 'Invalid credentials'}
    elif request['type'] == 'update_menu':
        if users[request['username']]['type'] == 'owner':
            menu = load_data(menu_file)
            menu.update(request['menu'])
            save_data(menu, menu_file)
            return {'status': 'menu updated'}
    elif request['type'] == 'request_menu':
        return {'status': 'success', 'menu': load_data(menu_file)}
    elif request['type'] == 'place_order':
        menu = load_data(menu_file)
        total_price = sum(menu[item] * quantity for item, quantity in request['order'].items())
        return {'status': 'order received', 'total_price': total_price, 'address': request['address']}
    return {'status': 'error', 'message': 'Unsupported request type'}

# Main function to run the server
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server is listening on", HOST, PORT)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    main()

import logging
from tcp_client import TcpClient
from context import lab_logging
from phone_book_entry import PhoneBookEntry
from typing import List

lab_logging.setup(stream_level=logging.INFO)


while True:
    client = TcpClient()

    command = input("Enter command: ")

    data: List[PhoneBookEntry] = []

    if command == "exit":
        break
    elif command == "GET":
        argument = input("Enter Search Query: ")

        data = client.sendCommand("GET", argument)
    elif command == "GET_ALL":
        data = client.sendCommand("GET_ALL")
    else:
        print("Unknown command. Available Commands are: GET, GET_ALL")

    if(len(data) == 0):
        print("No entries found.")
        continue

    for entry in data:
            print(f"{entry.name}: {entry.phone_number}, {entry.city}")

client.close()
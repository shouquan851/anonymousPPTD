# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from client.ClientManager import ClientManager
from cloud_server.CloudServer import CloudServer
from data_generator.DataGenerator import DataGenerator
from edge_server.EdgeManager import EdgeManager


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

clientManager = ClientManager()
edgeManager = EdgeManager()
cloudServer = CloudServer()
dataGenerator = DataGenerator()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

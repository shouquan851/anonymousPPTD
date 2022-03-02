
from client.ClientManager import ClientManager
from cloud_server.CloudServer import CloudServer
from data_generator.DataGenerator import DataGenerator
from edge_server.EdgeManager import EdgeManager



if __name__ == '__main__':
    print('PyCharm')

clientManager = ClientManager()
edgeManager = EdgeManager()
cloudServer = CloudServer()
dataGenerator = DataGenerator()


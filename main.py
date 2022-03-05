from Application import Application

# if __name__ == '__main__':
#     print('PyCharm')

application = Application()
application.key_agreement()
application.data_generator()
all_group_in_client_data_index = application.generate_data_index(2)
print(all_group_in_client_data_index)
client_masking_data_all_group = application.client_upload_data(all_group_in_client_data_index)
print(client_masking_data_all_group)
application.edge_aggregation_client_data(client_masking_data_all_group)
application.edge_generate_edge_masking_data_all_group()

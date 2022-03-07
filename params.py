edge_number = 4
client_number = 50
group_number_list = [10, 10, 10, 20]

# datagenerate
# 可靠程度,越接近100 越可靠
unreliable_start = 60
unreliable_end = 70
reliable_start = 90
reliable_end = 99

# TD
K = client_number
M = 3
count = 10

# DH
p = 9584766362985668998675320225938492576833127437546441475200651386681661214949815198902067575999636607649757091547852460848597727186027733861209248123986003
q = None
g = 2

# noise
select_index = 2
client_noise = 0
edge_masking_noise = 0
edge_noise = 0
ru_start = 0
ru_end= 1000
masking_p = 100000
prf_p = 10000

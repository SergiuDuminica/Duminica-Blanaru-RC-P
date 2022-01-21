# Formam pachetele, seq_num = nr de pachete
def make(seq_num, data = b''):
    seq_bytes = seq_num.to_bytes(4, byteorder = 'little', signed = True)
    return seq_bytes + data

def make_empty():
    return b''

# Extragem seq_num si data dintr-un pachet
def extract(packet):
    seq_num = int.from_bytes(packet[0:4], byteorder = 'little', signed = True)
    return seq_num, packet[4:]

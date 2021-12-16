
def to_bits(hex):
    bits = bin(int(hex, 16))[2:]
    while len(bits) % 8 != 0:
        bits = '0' + bits
    return bits

assert to_bits('D2FE28') == '110100101111111000101000'
assert to_bits('620080001611562C8802118E34') == '01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100'

def part1(input_data):
    print('part1', input_data)
    bits = to_bits(input_data)
    pos = 0
    pos, packet = parse_packet(bits, pos)
    return sum(get_versions(packet))

def get_versions(packet):
    packet_type, packet_version, packet_data = packet
    yield packet_version
    if packet_type == 'operator':
        for packet in packet_data:
            yield from get_versions(packet)


def parse_packet(bits, pos):
    #print(bits[pos:])
    assert pos + 6 < len(bits)
    packet_version = int(bits[pos:pos+3], 2)
    pos += 3
    packet_type_id = int(bits[pos:pos+3], 2)
    pos += 3
    if packet_type_id == 4:
        pos, value = parse_literal_value(bits, pos)
        return pos, ('literal', packet_version, value)
    elif packet_type_id != 4:
        length_type_id = bits[pos]
        pos += 1
        #print('operator packet', packet_type_id, 'version', packet_version, 'lti', length_type_id)
        if length_type_id == '0':
            assert pos + 15 < len(bits)
            total_length = int(bits[pos:pos+15], 2)
            pos += 15
            end_pos = pos + total_length
            subpackets = []
            while pos < end_pos:
                pos, subpacket = parse_packet(bits, pos)
                subpackets.append(subpacket)
            assert pos == end_pos
            return pos, ('operator', packet_version, subpackets)
        elif length_type_id == '1':
            assert pos + 11 < len(bits)
            number_of_subpackets = int(bits[pos:pos+11], 2)
            pos += 11
            subpackets = []
            for i in range(number_of_subpackets):
                pos, subpacket = parse_packet(bits, pos)
                subpackets.append(subpacket)
            return pos, ('operator', packet_version, subpackets)
        else:
            assert 0

    else:
        raise Exception(f'Unknown packet type id {packet_type_id}')

def parse_literal_value(bits, pos):
    #print('parse_literal_value', bits[pos:])
    value = ''
    while True:
        assert pos + 5 <= len(bits)
        cont = bits[pos]
        pos += 1
        value += bits[pos:pos+4]
        pos += 4
        assert len(value) % 4 == 0
        if cont == '0':
            break
        else:
            assert cont == '1'
    return pos, int(value, 2)

assert parse_literal_value('101111111000101', 0) == (15, 2021)

assert parse_packet(to_bits('8A004A801A8002F478'), 0) == (69, ('operator', 4, [('operator', 1, [('operator', 5, [('literal', 6, 15)])])]))
#assert parse_packet(to_bits('620080001611562C8802118E34'), 0) == 12
#assert parse_packet(to_bits('C0015000016115A2E0802F182340'), 0) == 23
#assert parse_packet(to_bits('A0016C880162017C3686B18A3D4780'), 0) == 31

assert part1('8A004A801A8002F478') == 16
assert part1('620080001611562C8802118E34') == 12
assert part1('C0015000016115A2E0802F182340') == 23
assert part1('A0016C880162017C3686B18A3D4780') == 31

print('Part 1:', part1(open('16_input.txt').read()))

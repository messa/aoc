
def to_bits(hex):
    bits = bin(int(hex, 16))[2:]
    while len(bits) % 8 != 0:
        bits = '0' + bits
    return bits

assert to_bits('D2FE28') == '110100101111111000101000'
assert to_bits('620080001611562C8802118E34') == '01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100'

def part1(input_data):
    bits = to_bits(input_data)
    pos, packet = parse_packet(bits, 0)
    return sum(get_versions(packet))

def part2(input_data):
    bits = to_bits(input_data)
    pos, packet = parse_packet(bits, 0)
    return eval_packet(packet)

def get_versions(packet):
    packet_type, packet_version, packet_data = packet
    yield packet_version
    if packet_type != literal:
        for packet in packet_data:
            yield from get_versions(packet)

def prod(numbers):
    x = 1
    for n in numbers:
        x *= n
    return x

eval_packet = lambda packet: packet[0](packet[2])

literal = lambda v: v
operators = {
    0: lambda packets: sum(eval_packet(p) for p in packets),
    1: lambda packets: prod(eval_packet(p) for p in packets),
    2: lambda packets: min(eval_packet(p) for p in packets),
    3: lambda packets: max(eval_packet(p) for p in packets),
    5: lambda packets: int(eval_packet(packets[0]) > eval_packet(packets[1])),
    6: lambda packets: int(eval_packet(packets[0]) < eval_packet(packets[1])),
    7: lambda packets: int(eval_packet(packets[0]) == eval_packet(packets[1])),
}

def parse_packet(bits, pos):
    #print(bits[pos:])
    assert pos + 6 < len(bits)
    packet_version = int(bits[pos:pos+3], 2)
    pos += 3
    packet_type_id = int(bits[pos:pos+3], 2)
    pos += 3
    if packet_type_id == 4:
        pos, value = parse_literal_value(bits, pos)
        return pos, (literal, packet_version, value)
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
            return pos, (operators[packet_type_id], packet_version, subpackets)
        elif length_type_id == '1':
            assert pos + 11 < len(bits)
            number_of_subpackets = int(bits[pos:pos+11], 2)
            pos += 11
            subpackets = []
            for i in range(number_of_subpackets):
                pos, subpacket = parse_packet(bits, pos)
                subpackets.append(subpacket)
            return pos, (operators[packet_type_id], packet_version, subpackets)
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

assert part1('8A004A801A8002F478') == 16
assert part1('620080001611562C8802118E34') == 12
assert part1('C0015000016115A2E0802F182340') == 23
assert part1('A0016C880162017C3686B18A3D4780') == 31

print('Part 1:', part1(open('16_input.txt').read()))
print('Part 2:', part2(open('16_input.txt').read()))

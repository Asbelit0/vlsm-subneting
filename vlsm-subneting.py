#SUBNETEO CON VLSM

def calculate_mask(hosts):
    return 32 - (hosts - 1).bit_length()

def increment_network(network, mask):
    octets = [int(octet) for octet in network.split('.')]
    increment = 2 ** (32 - mask)
    
    for i in range(3, -1, -1):
        octets[i] += increment
        if octets[i] < 256:
            break
        octets[i] -= 256

    return '.'.join(map(str, octets))

def network_to_broadcast(network, mask):
    octets = [int(octet) for octet in network.split('.')]
    host_bits = 32 - mask
    broadcast_address = int(sum(octet << (8 * i) for i, octet in enumerate(reversed(octets)))) | (2 ** host_bits - 1)
    
    broadcast_octets = [(broadcast_address >> (8 * i)) & 0xFF for i in reversed(range(4))]
    return '.'.join(map(str, broadcast_octets))

def hosts_range(network, mask):
    octets = [int(octet) for octet in network.split('.')]
    network_int = sum(octet << (8 * i) for i, octet in enumerate(reversed(octets)))
    broadcast_int = network_int | (2 ** (32 - mask) - 1)
    
    first_host_int = network_int + 1
    last_host_int = broadcast_int - 1
    
    first_host = '.'.join([str((first_host_int >> (8 * i)) & 0xFF) for i in reversed(range(4))])
    last_host = '.'.join([str((last_host_int >> (8 * i)) & 0xFF) for i in reversed(range(4))])
    
    return first_host, last_host

def vlsm_subnetting(network, subnets):
    base_network, base_mask = network.split('/')
    base_mask = int(base_mask)
    results = []

    for subnet in subnets:
        required_hosts = subnet['hosts']
        mask = calculate_mask(required_hosts)
        subnet['Network'] = base_network
        subnet['Mask'] = mask
        
        subnet['Broadcast'] = network_to_broadcast(base_network, mask)
        subnet['Host Range'] = hosts_range(base_network, mask)

        increment = 2 ** (32 - mask)
        base_network = increment_network(base_network, mask)
        results.append(subnet)
    
    return results

def main():
    network = input("Ingrese la red principal (por ejemplo, 192.168.0.0/24): ")
    num_subnets = int(input("¿Cuántas subredes necesitas?: "))
    
    subnets = []
    for i in range(num_subnets):
        name = input(f"Ingrese el nombre de la subred {i+1}: ")
        hosts = int(input(f"Ingrese la cantidad de hosts para {name}: "))
        subnets.append({'name': name, 'hosts': hosts})
    
    results = vlsm_subnetting(network, subnets)
    for subnet in results:
        print(f"Subred: {subnet['name']}")
        print(f"  Network: {subnet['Network']}/{subnet['Mask']}")
        print(f"  Broadcast: {subnet['Broadcast']}")
        print(f"  Host Range: {subnet['Host Range'][0]} - {subnet['Host Range'][1]}")
        print()

if __name__ == "__main__":
    main()

import os
import ipaddress

DOK_CIMEK = ["2001:0db8"]
GLOBAL_EGYEDI_CIMEK = ["2001:0e"]
HELYI_EGYEDI_CIMEK = ["fc", "fd"]
SORSZAM = 10


def read_ip_file(file_path: str) -> list[str] | None:
    content: list[str] = []
    try:
        with open(file_path) as ip_file:
            for ip in ip_file:
                ip = ip.strip()
                content.append(ip)
            return content
    except FileNotFoundError:
        print("Fájl nem található")
    except IOError as e:
        print(f"A fájl olvasása meghiúsult. IOerror: {e}")
    return None


def get_smaller_ip(ip1: list[str], ip2: list[str]) -> list[str]:
    for i in range(len(ip1)):
        if int(ip1[i], 16) == int(ip2[i], 16):
            continue
        elif int(ip1[i], 16) < int(ip2[i], 16):
            return ip1
        else:
            return ip2
    return ip2


def get_smallest_ip(ip_list: list[str]) -> str:
    min_val = ""
    for ip in ip_list:
        ip_slice: list[str] = ip.split(":")
        if min_val == "":
            min_val = ip_slice
        else:
            min_val = get_smaller_ip(min_val, ip_slice)
    return ":".join(min_val)


def ip_counter_by_type(doc_types: list[str], ips: list[str]) -> int:
    ip_len = 0
    for i in range(len(doc_types)):
        doc_type = doc_types[i]
        ip = [ip for ip in ips if ip.startswith(doc_type)]
        ip_len += len(ip)
    return ip_len


def gather_ip_by_zero_count(ips: list[str], zero_count: int) -> dict[int, str]:
    return {
        index + 1: ip for index, ip in enumerate(ips) if ip.count("0") >= zero_count
    }


def write_zero_count_to_file(ips_for_write: dict[int, str], file_path: str) -> None:
    try:
        with open(file_path, "w") as file:
            for index, ip in ips_for_write.items():
                file.write(f"{index} {ip}\n")
    except IOError as e:
        print(f"A fájl írása meghiúsult. IOerror: {e}")


def ask_for_serialnr(nr_range_end: int) -> int:
    try:
        sorszam = int(input(f"Kérek egy sorszámot 1 és {nr_range_end} között: "))
    except ValueError:
        print("Nem valid sorszám!")
    return sorszam


def shorten_ip(ip: str) -> str:
    ip = ip.split(":")
    for i, group in enumerate(ip):
        # A kezdő 0-ákat eltávolítani, de egy marad, ha a csoport üres
        group = group.lstrip("0")
        if group == "":
            group = "0"
        ip[i] = group
    return ":".join(ip)


def compress_ipv6(ip_address: str) -> str:
    """Az "ipaddress.IPv6Address(ip).compressed" implementálása
    Args:
        ipaddress (str): A rövidítendő IPv6 cím

    Returns:
        str: A rövidített IPv6 cím
    """
    # Kezdő nullák eltávolítása
    shortened_ip = shorten_ip(ip_address)
    groups = shortened_ip.split(":")

    # A leghosszabb nullás csoportok azonosítása
    max_zeros, current_zeros = 0, 0
    max_zeros_start, current_start = -1, -1

    for i, group in enumerate(groups):
        if group == "0":
            if current_zeros == 0:
                current_start = i
            current_zeros += 1
        else:
            if current_zeros > max_zeros:
                max_zeros = current_zeros
                max_zeros_start = current_start
            current_zeros = 0

    # Az utolsó nullás csoport, ha van
    if current_zeros > max_zeros:
        max_zeros = current_zeros
        max_zeros_start = current_start

    # A leghosszabb nullás csoport cseréje
    if max_zeros > 1:
        compressed_ip = []
        i = 0
        while i < len(groups):
            if i == max_zeros_start:
                compressed_ip.append("")
                i += max_zeros
                if i >= len(groups):
                    # záró :: -k esetén
                    compressed_ip.append("")
            else:
                compressed_ip.append(groups[i])
                i += 1
        compressed_ip = ":".join(compressed_ip)
    else:
        compressed_ip = shortened_ip

    if compressed_ip == shortened_ip:
        return "Nem rövidíthető tovább."

    return compressed_ip


def main():
    # 1. feladat - beolvasás -----------------
    # print("\n1. feladat\n")

    cw_dir = os.path.dirname(__file__)
    ip_file_to_read = os.path.join(cw_dir, "ip.txt")
    content = read_ip_file(ip_file_to_read)

    # 2. feladat - statisztika ---------------
    print("\n2. feladat\n")
    print(f"Az állományban {len(content)} db IP cím van.")

    # 3. feladat - statisztika ---------------
    print("\n3. feladat\n")
    print(f"A legalacsonyabb tárolt IP-cím: {get_smallest_ip(content)}", end="\n")

    # 4. feladat - statisztika ---------------
    print("\n4. feladat\n")
    print("Dokumentációs cím: ", ip_counter_by_type(DOK_CIMEK, content), " darab")
    print(
        "Globális egyedi cím: ",
        ip_counter_by_type(GLOBAL_EGYEDI_CIMEK, content),
        " darab",
    )
    print(
        "Helyi egyedi cím: ", ip_counter_by_type(HELYI_EGYEDI_CIMEK, content), " darab"
    )

    # 5. feladat - statisztika és kiírás -----
    # print("\n5. feladat\n")

    ips_for_write = gather_ip_by_zero_count(content, 18)
    ip_file_to_write = os.path.join(cw_dir, "sok.txt")
    # print(ips_for_write)
    write_zero_count_to_file(ips_for_write, ip_file_to_write)

    # 6. feladat - szimpla rövidítés ---------
    print("\n6. feladat\n")
    # sorszam = ask_for_serialnr(len(content))
    # sorsz = sorszam - 1

    sorsz = SORSZAM - 1
    short_ip = shorten_ip(content[sorsz])
    print(f"A(z) {sorsz+1}. IP cím:     {content[sorsz]}")
    print(f"A(z) {sorsz+1}. IP cím röv: {short_ip}")

    # 7. feladat - további rövidítés ---------
    print("\n7. feladat\n")
    compressed_ip = compress_ipv6(content[sorsz])
    print(f"A(z) {sorsz+1}. IP cím saját function: {compressed_ip}")
    print(
        f"A(z) {sorsz+1}. IP cím iPv6address fn: "
        f"{ipaddress.IPv6Address(content[sorsz]).compressed}"
    )


if __name__ == "__main__":
    main()

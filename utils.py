p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0


def point_multiplication(k, Px, Py):
    # 将十进制私钥转换为二进制 [2:]表示将0b...字符串切去0b
    binary_private_key = bin(k)[2:]
    for last_bin in reversed(binary_private_key):
        if last_bin == '1':
            Px, Py = point_addition(Px, Py, Gx, Gy)
        elif last_bin == '0':
            Px, Py = point_addition(Px, Py, Px, Py)

    return Px, Py


def point_addition(Px, Py, Qx, Qy):
    if Px == 0 and Qx == 0 and Py == 0 and Qy == 0:
        Rx = Ry = 0
    else:
        if Px == Qx and Py == Qy:
            m = (3 * Px * Px + a) * mod_inverse(Py * 2, p)
        else:
            if Px > Qx:
                m = (Py - Qy) * mod_inverse(Px - Qx, p)
            else:
                m = (Qy - Py) * mod_inverse(Qx - Px, p)
        Rx = (m * m - Px - Qx) % p
        Ry = (m * (Px - Rx) - Py) % p

    return Rx, Ry


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y


def mod_inverse(a, p) -> int:
    gcd, x, _ = extended_gcd(a, p)
    if gcd != 1:
        raise Exception(f'gcd = {gcd} != 1')
    else:
        return (x + p) % p


def string_to_int(s, encoding='utf-8'):
    # 将字符串编码为字节串
    byte_array = s.encode(encoding)
    # 将字节串转换为整数
    integer = int.from_bytes(byte_array, byteorder='big')
    return integer


def int_to_string(integer, encoding='utf-8'):
    # 将整数转换回字节串
    byte_array = integer.to_bytes((integer.bit_length() + 7) // 8, byteorder='big')
    # 将字节串解码为字符串
    string = byte_array.decode(encoding)
    return string


def int_to_byte_list(value: int) -> list:
    """
    将整型数转换为字节列表
    """
    # 确定字节长度，(value.bit_length() + 7) // 8 是字节数
    byte_length = (value.bit_length() + 7) // 8

    # 使用 to_bytes 方法将整型转换为字节数组，byteorder='big'表示大端字节序
    byte_array = value.to_bytes(byte_length, byteorder='big', signed=False)

    # 将字节数组转换为字节列表
    byte_list = list(byte_array)

    return byte_list

def hex_to_bin(hex_string: str,save_zeros=True) -> str:
    """
    将十六进制字符串转换为二进制字符串。
    """
    # 先将十六进制字符串转换为整数
    int_value = int(hex_string, 16)

    # 然后将整数转换为二进制字符串，去掉 '0b' 前缀
    bin_string = bin(int_value)[2:]

    if save_zeros:
        bin_string = '0' * (len(hex_string) * 4 - len(bin_string)) + bin_string

    return bin_string

def bin_to_hex(bin_string: str) -> str:
    """
    将二进制字符串转换为十六进制字符串。
    """
    # 将二进制字符串转换为整型，基数为 2
    int_value = int(bin_string, 2)

    # 将整型转换为十六进制字符串，并去掉'0x'前缀
    hex_string = hex(int_value)[2:]

    # 如果需要，可以将十六进制字符串转换为大写字母
    # hex_string = hex_string.upper()

    return hex_string

def xor_bin_strings(bin_str1: str, bin_str2: str) -> str:
    """
    对两个等长的二进制字符串进行按位异或操作，并返回结果二进制字符串。
    """
    # 确保两个二进制字符串等长
    if len(bin_str1) != len(bin_str2):
        raise ValueError("二进制字符串长度不一致")

    # 使用 zip 将二进制字符串中的每一位配对并异或
    xor_result = ''.join('1' if b1 != b2 else '0' for b1, b2 in zip(bin_str1, bin_str2))

    return xor_result


def compare_strings(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    # 比较长度
    if len_str1 != len_str2:
        # 找到开始不同的位置
        min_length = min(len_str1, len_str2)
        for i in range(min_length):
            if str1[i] != str2[i]:
                print(f"字符串长度不同,字符串开始不同的位置: {i}")
                return
        # 如果所有相同长度的字符都相同，则开始不同的位置是min_length
        print(f"字符串长度不同,字符串开始不同的位置: {min_length}")
    else:
        # 长度相等，找出所有不同的位置
        diff_positions = [i for i, (c1, c2) in enumerate(zip(str1, str2)) if c1 != c2]
        print(f"字符串长度相同,所有不同位置: {diff_positions}")


if __name__ == '__main__':
    inverse = mod_inverse(100, 11)
    print(inverse)

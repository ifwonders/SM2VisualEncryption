import random
import gmssl.sm3
import math
from utils import mod_inverse, string_to_int, int_to_string, int_to_byte_list, hex_to_bin, xor_bin_strings, bin_to_hex

# https://www.sca.gov.cn/sca/xxgk/2010-12/17/content_1002386.shtml
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0


class Point:
    """
    类：椭圆曲线上的点
    """
    def __init__(self, x: int, y: int):
        """
        初始化输入点的x,y坐标
        :param x: x坐标
        :param y: y坐标
        """
        self.x: int = x
        self.y: int = y

    def print_point(self):
        """
        命令行打印出点坐标
        :return:
        """
        print(f'({self.x}, {self.y})')

    @staticmethod
    def output_point(point:'Point'):
        """
        输出点的十六进制表达形式，并在开头‘04’字符串，表示SM2未压缩的密钥
        :param point:
        :return:
        """
        hex_x = '0'*(64-len(hex(point.x)[2:]))+hex(point.x)[2:]
        hex_y = '0'*(64-len(hex(point.y)[2:]))+hex(point.y)[2:]
        return '04'+hex_x+hex_y

    @staticmethod
    def input_point(hex_x_y:str):
        """
        输入点的以‘04’开头的十六进制表达形式，生成该点的坐标
        :param hex_x_y: ‘04’开头的十六进制坐标字符串
        :return: 返回这个点对象
        """
        point = Point(0,0)
        if hex_x_y[0:2] != '04':
            raise Exception('未以04开头的无效字符串')
        else:
            hex_x_y = hex_x_y[2:].strip()
            if int(len(hex_x_y)) % 2 != 0:
                print(hex_x_y)
                raise Exception(f'奇数{int(len(hex_x_y))}位的16进制字符串')
            hex_x = hex_x_y[0:int(len(hex_x_y)/2)]
            hex_y = hex_x_y[int(len(hex_x_y)/2):]
            point.x = int(hex_x,16)
            point.y = int(hex_y,16)
        return point


    @staticmethod
    def addition(P: 'Point', Q: 'Point'):
        """
        椭圆曲线上的点加法
        :param P: 点P
        :param Q: 点Q
        :return: 点P+点Q在椭圆曲线有限域内的结果点
        """
        R = Point(0, 0)
        if P.x == Q.x and P.y == Q.y:
            m = (3 * P.x ** 2 + a) * mod_inverse(P.y * 2, p) % p
        else:
            if P.x > Q.x:
                m = (P.y - Q.y) * mod_inverse(P.x - Q.x, p) % p
            else:
                m = (Q.y - P.y) * mod_inverse(Q.x - P.x, p) % p
        R.x = (m * m - P.x - Q.x) % p
        R.y = (m * (P.x - R.x) - P.y) % p
        return R

    @staticmethod
    def multiplication(k, P: 'Point'):
        """
        椭圆曲线上的点乘法
        :param k: 倍数k
        :param P: 被倍乘的点P
        :return: 点P在椭圆曲线有限域内的倍乘结果点
        """
        # # 将十进制私钥转换为二进制 [2:]表示将0b...字符串切去0b
        # binary_private_key = bin(k)[2:]
        # R = P
        # for last_bin in reversed(binary_private_key):
        #     if last_bin == '1':
        #         R = Point.addition(R, Point(Gx, Gy))
        #     elif last_bin == '0':
        #         R = Point.addition(R, R)
        # return R
        N = P
        R = Point(0, 0)  # 代表无穷远点 O
        while k:
            if k & 1:
                R = Point.addition(R, N) if R.x !=0 and R.y != 0 else N
            N = Point.addition(N, N)
            k >>= 1
        return R


class SM2:
    """
    SM2算法，以父类存在
    """
    def __init__(self):
        """
        初始化SM2算法中共有的消息，密文C1C2C3,C和中间量t
        """
        self.message = ''
        self.C1 = Point(0, 0)
        self.C2 = ''
        self.C3 = 0
        self.C = ''
        self.t = 0

    @staticmethod
    def KDF(Z: int, klen: int):
        """
        SM2算法的密钥派生函数
        这里采用的密钥杂凑函数为gmssl.sm3.sm3_hash()，输出为256比特的杂凑值
        :param Z:比特串Z，以整型输入
        :param klen:目标密钥长度
        :return:长度为klen的密钥数据比特串K
        """
        ct = 0x00000001
        v = 256
        K = ''
        # print(math.ceil(klen / v))
        for i in range(1, math.ceil(klen / v) + 1):
            Hai = hex_to_bin(gmssl.sm3.sm3_hash(int_to_byte_list((Z << 32) + ct)))
            Hai = '0' * (256 - len(Hai)) + Hai
            ct = ct + 1
            if i == math.ceil(klen / v) and klen % v != 0:
                # K = (K << (klen - v * math.floor(klen / v))) + (Hai >> (256 - klen + v * math.floor(klen / v)))
                K = K + Hai[0:klen - v * math.floor(klen / v)]
            else:
                K = K + Hai
        return K


class SM2_sender(SM2):
    def __init__(self, message: str):
        """
        初始化SM2的发送方
        :param message:发送方要加密的明文消息
        """
        super().__init__()
        self.kPb = Point(0, 0)
        self.message = message
        self.bin_message = bin(string_to_int(self.message))[2:]
        self.message_bit_length = len(self.bin_message)
        self.public_key = Point(0, 0)
        self.k = 0

    def receive_public_key(self, public_key: str):
        """
        接收接收方的公钥
        :param public_key: 接收方的公钥，以‘04’开头的16进制字符串
        :return: 赋值发送方的公钥，这里发送方的公钥用点对象存储
        """
        self.public_key = Point.input_point(public_key)

    def encrypt(self):
        """
        发送方加密
        :return:
        """
        while True:
            """
            生成随机数k计算出C1，保证C1得到的2进制字符串都为256位
            """
            self.generate_rand_k()
            # print(f'k:{self.k}')
            """
            第四步：计算[k]PB=(x2,y2)
            """
            self.kPb = Point.multiplication(k=self.k, P=self.public_key)
            self.generate_C1()
            # print(f'C1:{self.C1.x},{self.C1.y}')
            if len(bin(self.C1.x)[2:]) == len(bin(self.C1.y)[2:]) == 256:
                break

        self.generate_t()
        # print(f't:{self.t}')
        self.generate_C2()
        # print(f'C2:{self.C2}')
        self.generate_C3()
        # print(f'C3:{self.C3}')
        self.output_C()
        # print(f'C:{self.C}')

    def generate_rand_k(self):
        """
        第一步：产生随机数k
        :return:
        """
        while True:
            self.k = random.getrandbits(256)
            if 1 <= self.k <= n - 1:
                break

    def generate_C1(self):
        """
        第二步：计算椭圆曲线点C1=[k]G
        :return:
        """
        self.C1 = Point.multiplication(k=self.k, P=Point(Gx, Gy))

    def generate_t(self):
        """
        第五步：计算t=KDF(x2||y2,klen)
        :return:
        """
        z = int(str(self.kPb.x) + str(self.kPb.y))
        # print(f'发送方的z：{z}')
        self.t = SM2.KDF(Z=z, klen=self.message_bit_length)
        # print(f'发送方的t:{self.t}')

    def generate_C2(self):
        """
        第六步：计算C2=M^t
        :return:
        """
        # self.C2 = self.bin_message ^ self.t
        # print(f'C2的位数:{len(bin(self.C2)[2:])}')
        self.C2 = xor_bin_strings(self.t, self.bin_message)

    def generate_C3(self):
        """
        第七步：计算C3=Hash(x2||M||y2)
        :return:
        """
        # self.C3 = int(gmssl.sm3.sm3_hash(int_to_byte_list((self.kPb.x << (256 + self.message_bit_length))
        #                                                   + (self.bin_message << 256)
        #                                                   + self.kPb.y)), 16)
        self.C3 = gmssl.sm3.sm3_hash(
            int_to_byte_list(
                int(
                    bin(self.kPb.x)[2:] + self.bin_message + bin(self.kPb.y)[2:]
                    , 2)
            )
        )

    def output_C(self):
        """
        第八步：输出密文C=C1||C2||C3
        :return:
        """
        # self.C = bin(self.C1.x)[2:] + bin(self.C1.y)[2:] + bin(self.C2)[2:] + bin(self.C3)[2:]
        # print(len(bin(self.C1.x)[2:]))
        # print(len(bin(self.C1.y)[2:]))
        # print(len(bin(self.C2)[2:]))
        # print(len(bin(self.C3)[2:]))
        self.C = bin(self.C1.x)[2:] + bin(self.C1.y)[2:] + self.C2 + (hex_to_bin(self.C3))
        # print(f'发送方的C2:{self.C2},{bin_to_hex(self.C2)}')
        # print(f'发送方的C1.x:{self.C1.x}')
        # print(f'发送方的C1.y:{self.C1.y}')
        # print(len(self.C2))
        # print(len(hex_to_bin(self.C3)))


class SM2_receiver(SM2):
    def __init__(self):
        """
        初始化SM2的接收方
        """
        super().__init__()
        self.dBC = Point(0, 0)
        self.private_key = 0
        self.generate_private_key()
        self.public_key = Point(0, 0)
        self.generate_public_key()

    def receive_C(self, C: str):
        """
        接收发送方传来的密文C
        :param C: 16进制字符串表示的密文C
        :return:
        """
        self.C = C

    def decrypt(self):
        self.separate_C()
        self.check_C1()
        """
        第二步：计算[dB]C1=(x2,y2)
        """
        self.dBC = Point.multiplication(k=self.private_key, P=self.C1)
        self.generate_t()
        self.check_t()
        self.generate_message()
        self.check_C3()

    def generate_private_key(self):
        while True:
            self.private_key = random.getrandbits(256)
            if 1 <= self.private_key <= n - 1:
                break

    def generate_public_key(self):
        """
        计算公钥
        :return:
        """
        self.public_key = Point.multiplication(self.private_key, Point(Gx, Gy))

    def separate_C(self):
        """
        第一步：从密文中取出C1，C2，C3
        :return:
        """
        self.C1.x = int(self.C[0:256], 2)
        self.C1.y = int(self.C[256:512], 2)
        # print(f'接收方的C1.x:{self.C1.x}')
        # print(f'接收方的C1.y:{self.C1.y}')
        # self.C2 = int(self.C[128:-64], 16)
        self.C2 = (self.C[512:-256])
        # self.C3 = int(self.C[-256:], 2)
        self.C3 = bin_to_hex(self.C[-256:])
        # print(f'接收方的C2:{self.C2},{bin_to_hex(self.C2)}')

    def generate_t(self):
        """
        第三步：计算t=KDF(x2||y2,klen)
        :return:
        """
        z = int(str(self.dBC.x) + str(self.dBC.y))
        # print(f'接收方的z：{z}')
        # print(f'C2位数:{len(self.C2)}')
        self.t = SM2.KDF(Z=z, klen=len(self.C2))
        # print(f'接收方的t:{self.t}')

    def generate_message(self):
        """
        第四步：解密密文M'=C2^t
        :return:
        """
        self.message = int_to_string(int(xor_bin_strings(self.t, self.C2), 2))

    def check_C1(self):
        if (self.C1.y ** 2) % p != (self.C1.x ** 3 + a * self.C1.x + b) % p:
            raise Exception('C1不符合椭圆曲线方程')
        # pass

    def check_t(self):
        for ch in self.t:
            if ch != '0':
                return 1
        raise Exception('t为全0')
        # pass

    def check_C3(self):
        """
        第五步：计算u=Hash(x2||M'||y2),验证是否等于C3
        :return:
        """
        U = gmssl.sm3.sm3_hash(
            int_to_byte_list(
                int(
                    bin(self.dBC.x)[2:] + bin(string_to_int(self.message))[2:] + bin(self.dBC.y)[2:]
                    , 2)
            )
        )
        if U != ('0'*(64-len(self.C3)) +self.C3):
            raise Exception(f'u:{U}不等于C3:{self.C3}')


if __name__ == '__main__':
    A = SM2_sender(message='hello,你好')
    B = SM2_receiver()

    A.receive_public_key(Point.output_point(B.public_key))
    A.encrypt()

    B.receive_C(A.C)
    B.decrypt()

    print(B.message)

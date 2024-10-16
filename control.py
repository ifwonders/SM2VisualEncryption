"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
PARAMS = """https://www.sca.gov.cn/sca/xxgk/2010-12/17/content_1002386.shtml
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
"""
# 示例下载 https://www.pytk.net/blog/1702564569.html
from ui import Win
from SM2 import *
import tkinter as tk
from utils import *
from tkinter import messagebox

class Controller:
    # 导入UI类后，替换以下的 object 类型，将获得 IDE 属性提示功能
    ui: Win

    def __init__(self):
        # self.sender = None
        # self.receiver = None
        self.sender:SM2_sender
        self.receiver:SM2_receiver

        self.sender_msg = ''
        self.public_key = ''
        self.sender_c = ''
        self.receiver_c = ''
        self.private_key = ''
        self.receiver_msg = ''

        # self.show_params()

    def init(self, ui):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        # TODO 组件初始化 赋值操作
        self.ui.tk_text_params.insert('1.0', PARAMS)

    def init_receiver(self):
        self.receiver = SM2_receiver()

    def init_sender(self):
        self.sender = SM2_sender(self.sender_msg)

    def encrypt(self):
        # 先检测发送方的明文框内是否有内容
        if self.ui.tk_input_sender_m.get() == '':
            messagebox.showerror('错误','请输入需要加密的消息')
            return -1

        # 再检测是否接收到公钥
        if self.ui.tk_text_sender_public_key.get('1.0',tk.END).strip() == '':
            messagebox.showerror('错误','请先传输公钥')
            return -1

        self.sender_msg = self.ui.tk_input_sender_m.get()
        self.init_sender()
        self.public_key = self.ui.tk_text_sender_public_key.get('1.0',tk.END).strip()
        self.sender.receive_public_key(self.public_key)
        self.sender.encrypt()

        self.ui.tk_text_sender_c.delete('1.0', tk.END)
        self.ui.tk_text_sender_c.insert('1.0', bin_to_hex(self.sender.C).upper())
        return 1

    def clear(self):
        self.ui.tk_input_sender_m.delete('0', tk.END)
        self.ui.tk_text_sender_public_key.delete('1.0', tk.END)
        self.ui.tk_text_sender_c.delete('1.0', tk.END)
        self.ui.tk_text_receiver_c.delete('1.0', tk.END)
        self.ui.tk_text_receiver_private_key.delete('1.0',tk.END)
        self.ui.tk_text_receiver_m.delete('1.0',tk.END)

        # pass

    def generate_private_key(self):
        self.init_receiver()
        self.ui.tk_text_receiver_private_key.delete('1.0', tk.END)
        self.ui.tk_text_sender_public_key.delete('1.0', tk.END)

        self.private_key = self.receiver.private_key
        self.ui.tk_text_receiver_private_key.insert('1.0', hex(self.private_key)[2:].upper())
        # pass

    def generate_public_key(self):
        # 先检测私钥框是否有内容
        if self.ui.tk_text_receiver_private_key.get('1.0',tk.END).strip() == '':
            messagebox.showerror('错误','请先生成私钥')
            return -1

        self.ui.tk_text_sender_public_key.delete('1.0', tk.END)

        self.public_key = Point.output_point(self.receiver.public_key)
        self.ui.tk_text_sender_public_key.insert('1.0', self.public_key.upper())
        self.ui.tk_text_sender_c.delete('1.0',tk.END)
        self.ui.tk_text_receiver_c.delete('1.0',tk.END)
        return 1
        # pass

    def transfer_c(self):
        if self.ui.tk_text_sender_c.get('1.0',tk.END).strip() == '':
            messagebox.showerror('错误','请先生成加密消息')
            return -1
        self.receiver_c = self.sender_c = self.sender.C
        self.ui.tk_text_receiver_c.delete('1.0', tk.END)
        self.ui.tk_text_receiver_c.insert('1.0', bin_to_hex(self.receiver_c).upper())
        return 1
        # pass

    def decrypt(self):
        # 检测私钥和密文是否都收到
        if self.ui.tk_text_receiver_c.get('1.0',tk.END).strip() == '':
            messagebox.showerror('错误','请先接收密文')
            return -1
        if self.ui.tk_text_receiver_private_key.get('1.0',tk.END).strip() == '':
            messagebox.showerror('错误','请先生成私钥')
            return -1

        self.receiver.receive_C(self.receiver_c)
        try:
            self.receiver.decrypt()
        except Exception as e:
            messagebox.showerror('错误',str(e.args[0]))
            return -1
        self.receiver_msg = self.receiver.message

        self.ui.tk_text_receiver_m.delete('1.0', tk.END)
        self.ui.tk_text_receiver_m.insert('1.0', self.receiver_msg)
        # pass

    def falsify_receiver_c(self):
        fake_msg = self.ui.tk_text_receiver_c.get('1.0',tk.END).strip()
        print(f'假消息：{hex_to_bin(fake_msg,False)}')
        print(f'真消息：{self.receiver_c}')
        print(f'假消息长度:{len(hex_to_bin(fake_msg,False))},真消息长度:{len(self.receiver_c)}')
        compare_strings(hex_to_bin(fake_msg,False),self.receiver_c)
        self.receiver_c = hex_to_bin(fake_msg,False)
        messagebox.showinfo('提示','接收方密文篡改成功')

        # pass
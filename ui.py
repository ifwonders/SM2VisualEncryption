"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
# from control import Controller

class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_text_sender_c = self.__tk_text_sender_c(self)
        self.tk_text_params = self.__tk_text_params(self)
        self.tk_label_sender = self.__tk_label_sender(self)
        self.tk_label_receiver = self.__tk_label_receiver(self)
        self.tk_input_sender_m = self.__tk_input_sender_m(self)
        self.tk_text_sender_public_key = self.__tk_text_sender_public_key(self)
        self.tk_label_cyphertext = self.__tk_label_cyphertext(self)
        self.tk_text_receiver_c = self.__tk_text_receiver_c(self)
        self.tk_label_keys = self.__tk_label_keys(self)
        self.tk_text_receiver_private_key = self.__tk_text_receiver_private_key(self)
        self.tk_text_receiver_m = self.__tk_text_receiver_m(self)
        self.tk_label_plaintext = self.__tk_label_plaintext(self)
        self.tk_button_generate_public_key = self.__tk_button_generate_public_key(self)
        self.tk_button_transfer_c = self.__tk_button_transfer_c(self)
        self.tk_button_encrypt = self.__tk_button_encrypt(self)
        self.tk_button_decrypt = self.__tk_button_decrypt(self)
        self.tk_button_clear = self.__tk_button_clear(self)
        self.tk_button_generate_private_key = self.__tk_button_generate_private_key(self)
        self.tk_button_falsify_receiver_c = self.__tk_button_falsify_receiver_c(self)

    def __win(self):
        self.title("SM2加密")
        # 设置窗口大小、居中
        width = 850
        height = 640
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_text_sender_c(self,parent):
        text = Text(parent)
        text.place(x=20, y=340, width=300, height=170)
        self.create_bar(parent, text,True, False, 20, 340, 300,170,850,640)
        return text
    def __tk_text_params(self,parent):
        text = Text(parent)
        text.place(x=20, y=520, width=800, height=100)
        return text
    def __tk_label_sender(self,parent):
        label = Label(parent,text="发送方",anchor="center", )
        label.place(x=130, y=15, width=60, height=40)
        return label
    def __tk_label_receiver(self,parent):
        label = Label(parent,text="接收方",anchor="center", )
        label.place(x=651, y=15, width=60, height=40)
        return label
    def __tk_input_sender_m(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=20, y=60, width=300, height=100)
        return ipt
    def __tk_text_sender_public_key(self,parent):
        text = Text(parent)
        text.place(x=20, y=180, width=300, height=100)
        self.create_bar(parent, text,True, False, 20, 180, 300,100,850,640)
        return text
    def __tk_label_cyphertext(self,parent):
        label = Label(parent,text="发送方密文与接收方密文",anchor="center", )
        label.place(x=350, y=390, width=150, height=30)
        return label
    def __tk_text_receiver_c(self,parent):
        text = Text(parent)
        text.place(x=540, y=340, width=280, height=170)
        return text
    def __tk_label_keys(self,parent):
        label = Label(parent,text="公钥与私钥",anchor="center", )
        label.place(x=380, y=200, width=90, height=30)
        return label
    def __tk_text_receiver_private_key(self,parent):
        text = Text(parent)
        text.place(x=540, y=220, width=280, height=100)
        return text
    def __tk_text_receiver_m(self,parent):
        text = Text(parent)
        text.place(x=540, y=60, width=280, height=100)
        return text
    def __tk_label_plaintext(self,parent):
        label = Label(parent,text="明文",anchor="center", )
        label.place(x=400, y=90, width=50, height=30)
        return label
    def __tk_button_generate_public_key(self,parent):
        btn = Button(parent, text="<<生成公钥并传输<<", takefocus=False,)
        btn.place(x=360, y=250, width=140, height=30)
        return btn
    def __tk_button_transfer_c(self,parent):
        btn = Button(parent, text=">>传输密文>>", takefocus=False,)
        btn.place(x=360, y=440, width=140, height=30)
        return btn
    def __tk_button_encrypt(self,parent):
        btn = Button(parent, text="↓ 加密 ↓", takefocus=False,)
        btn.place(x=120, y=290, width=80, height=40)
        return btn
    def __tk_button_decrypt(self,parent):
        btn = Button(parent, text="↑ 解密 ↑", takefocus=False,)
        btn.place(x=640, y=170, width=80, height=40)
        return btn
    def __tk_button_clear(self,parent):
        btn = Button(parent, text="清空", takefocus=False,)
        btn.place(x=400, y=20, width=50, height=30)
        return btn
    def __tk_button_generate_private_key(self,parent):
        btn = Button(parent, text="生成私钥", takefocus=False,)
        btn.place(x=400, y=160, width=60, height=30)
        return btn
    def __tk_button_falsify_receiver_c(self,parent):
        btn = Button(parent, text="篡改接收方密文", takefocus=False,)
        btn.place(x=370, y=346, width=109, height=30)
        return btn
class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)
    def __event_bind(self):
        self.tk_button_encrypt.bind("<Button-1>",lambda event:self.ctl.encrypt())
        self.tk_button_clear.bind("<Button-1>",lambda event:self.ctl.clear())
        self.tk_button_generate_private_key.bind("<Button-1>", lambda event: self.ctl.generate_private_key())
        self.tk_button_generate_public_key.bind("<Button-1>",lambda event:self.ctl.generate_public_key())
        self.tk_button_transfer_c.bind("<Button-1>",lambda event:self.ctl.transfer_c())
        self.tk_button_decrypt.bind("<Button-1>",lambda event:self.ctl.decrypt())
        self.tk_button_falsify_receiver_c.bind('<Button-1>',lambda event:self.ctl.falsify_receiver_c())
        # pass
    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
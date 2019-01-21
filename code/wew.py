import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from Regex import Regex
from NFA import NFA
from DFA import DFA
from Grammar import ReGrammar
import traceback
import Hamming

def helper_img_frame(self, img_name, canv_width=800, canv_height=300):
    if self.result_frame is not None:
        if self.canv is not None:
            self.canv.destroy()
        if self.sbarH is not None:
            self.sbarH.destroy()
        if self.sbarV is not None:
            self.sbarV.destroy()
        self.result_frame.destroy()
    self.result_frame = tk.Frame(self)
    self.result_frame.pack(side=tk.TOP, pady=10)
    #label = ttk.Label(self.result_frame, text="Kết quả:")
    #label.pack(side=tk.TOP)
    
    self.canv = tk.Canvas(self.result_frame, relief=tk.SUNKEN)
    self.canv.config(highlightthickness=0)
    self.canv.config(width=canv_width, height=canv_height)
    
    self.sbarV = ttk.Scrollbar(self, orient=tk.VERTICAL)
    self.sbarH = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
    self.sbarV.config(command=self.canv.yview)
    self.sbarH.config(command=self.canv.xview)
    self.canv.config(yscrollcommand=self.sbarV.set)
    self.canv.config(xscrollcommand=self.sbarH.set)

    self.canv.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    im = Image.open(img_name)
    self.img = ImageTk.PhotoImage(im)
    width,height=im.size
    anchor_w = canv_width/2 - width/2
    anchor_h = canv_height/2 - height/2
    if width > canv_width:
        self.sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        anchor_w = 0
    if height > canv_height:
        self.sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        anchor_h = 0
    self.canv.config(scrollregion=(0,0,width,height))
    self.canv.create_image((anchor_w, anchor_h),anchor=tk.NW,image=self.img)

class FrameRegextoNFA(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập biểu thức chính quy:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.regex_textbox = ttk.Entry(self.input_frame, width=30)
        self.regex_textbox.grid(row=0, column=1, pady=5, padx=10)
        ttk.Label(self.input_frame, text="Nhập bảng chữ cái, cách nhau bởi dấu phẩy:").grid(row=1, column=0, sticky="W", pady=5, padx=10)
        self.alphabet_textbox = ttk.Entry(self.input_frame, width=30)
        self.alphabet_textbox.grid(row=1, column=1, pady=5, padx=10)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
        
        panel = ttk.Label(self.result_frame, text="Xin hãy nhập và ấn chạy để xem kết quả")
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.regex_textbox.get()
        alphabet = self.alphabet_textbox.get().replace(' ', '').split(',')
        if string == '' or len(alphabet) == 0:
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        regex = Regex(string, alphabet)
        nfa = regex.to_nfa()
        nfa.rename_states()
        nfa.draw()
        self._rebuild_rframe()
        
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'nfa.gv.png')
        #panel = ttk.Label(self.result_frame, image=img)
        #panel.image = img
        #panel.pack(side = "bottom", fill = "both", expand = "yes")
        
        
class FrameRegextoDFA(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập biểu thức chính quy:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.regex_textbox = ttk.Entry(self.input_frame, width=30)
        self.regex_textbox.grid(row=0, column=1, pady=5, padx=10)
        ttk.Label(self.input_frame, text="Nhập bảng chữ cái, cách nhau bởi dấu phẩy:").grid(row=1, column=0, sticky="W", pady=5, padx=10)
        self.alphabet_textbox = ttk.Entry(self.input_frame, width=30)
        self.alphabet_textbox.grid(row=1, column=1, pady=5, padx=10)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
        
        panel = ttk.Label(self.result_frame, text="Xin hãy nhập và ấn chạy để xem kết quả")
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.regex_textbox.get()
        alphabet = self.alphabet_textbox.get().replace(' ', '').split(',')
        if string == '' or len(alphabet) == 0:
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        regex = Regex(string, alphabet)
        nfa = regex.to_nfa()
        nfa.rename_states()
        dfa = nfa.to_dfa()
        dfa.minimize()
        dfa.rename_states()
        dfa.draw()
        self._rebuild_rframe()
        
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'dfa.gv.png')
   
     
class FrameNFAtoDFA(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập dạng text của NFA:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.nfa_textbox = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.nfa_textbox.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None

        
        panel = ttk.Label(self.result_frame, text="Xin hãy nhập và ấn chạy để xem kết quả")
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        
    def _combine_img(self, *list_im):
        import numpy as np       
        imgs    = [ Image.open(i) for i in list_im ]
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
        imgs_comb = Image.fromarray( imgs_comb)
        imgs_comb.save( 'nfatodfa.png' )    
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.nfa_textbox.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        nfa = NFA.from_text(string)
        nfa.draw()
        dfa = nfa.to_dfa()
        dfa.minimize()
        dfa.draw()
        self._combine_img('nfa.gv.png', 'dfa.gv.png')
        self._rebuild_rframe()
        
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'nfatodfa.png')

class FrameDFAtoRegex(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập dạng text của DFA:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.dfa_textbox = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.dfa_textbox.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.dfa_textbox.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        dfa = DFA.from_text(string)
        dfa.minimize()
        dfa.draw()
        self.result['text'] = dfa.to_regex().string
        self._rebuild_rframe()
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'dfa.gv.png')
        
class FrameLGtoRG(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập văn phạm tuyến tính trái:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.input_text = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.input_text.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_text = tkst.ScrolledText(self, width=30, height=5, font=('Segoe UI', 9), state=tk.DISABLED)
        self.result_text.pack(side = tk.TOP)
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.input_text.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        grammar = ReGrammar.from_text(string)
        result = grammar.to_right_linear().to_string()
        self.result['text'] = "Kết quả"
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.INSERT, result)
        self.result_text.config(state=tk.DISABLED)

        
class FrameNFAtoRegex(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập dạng text của NFA:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.nfa_textbox = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.nfa_textbox.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.nfa_textbox.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        nfa = NFA.from_text(string)
        nfa.draw()
        self.result['text'] = nfa.to_regex().string
        self._rebuild_rframe()
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'nfa.gv.png')
        

class FrameGrtoNFA(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập văn phạm chính quy:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.textbox = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.textbox.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.textbox.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        ReGrammar.from_text(string).to_nfa().draw()
        self._rebuild_rframe()
        
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'nfa.gv.png')
        
class FrameNFAtoGr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập NFA:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.textbox = ttk.Entry(self.input_frame, width=30)
        self.textbox.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result_text = tkst.ScrolledText(self, width=30, height=5, font=('Segoe UI', 9), state=tk.DISABLED)
        self.result_text.pack(side = tk.TOP)
        self.result_frame = tk.Frame(self)
        self.result_frame.pack(side=tk.TOP, pady=10)
        self.canv = None
        self.sbarH = None
        self.sbarV = None
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.textbox.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        nfa = Regex.from_text(string)
        nfa.draw()
        result = nfa.to_grammar().to_string()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.INSERT, result)
        self.result_text.config(state=tk.DISABLED)
        self._rebuild_rframe()
        
        
    def _rebuild_rframe(self):
        helper_img_frame(self, 'nfa.gv.png')

class FrameGrtoRegex(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập văn phạm chính quy:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.input_text = tkst.ScrolledText(self.input_frame, width=30, height=5, font=('Segoe UI', 9))
        self.input_text.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_text = ttk.Entry(self, width=30)
        self.result_text.pack(side = tk.TOP)
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.input_text.get(1.0, "end-1c")  
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        grammar = ReGrammar.from_text(string)
        nfa = grammar.to_nfa()
        regex = nfa.to_regex()
        print(regex.alphabet)
        print(regex.parsed_string)
        result = regex.string
        self.result['text'] = "Kết quả"
        self.result_text.delete('0', tk.END)
        self.result_text.insert(tk.INSERT, result)
        
class FrameRegextoGr(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập biểu thức chính quy:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.input_text = ttk.Entry(self.input_frame, width=30, font=('Segoe UI', 9))
        self.input_text.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Label(self.input_frame, text="Nhập bảng chữ cái, cách nhau bởi dấu phẩy:").grid(row=1, column=0, sticky="W", pady=5, padx=10)
        self.alphabet_textbox = ttk.Entry(self.input_frame, width=30)
        self.alphabet_textbox.grid(row=1, column=1, pady=5, padx=10)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_text = tkst.ScrolledText(self, width=30, height=5, font=('Segoe UI', 9), state=tk.DISABLED)
        self.result_text.pack(side = tk.TOP)
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.input_text.get()
        alphabet = self.alphabet_textbox.get().replace(' ', '').split(',')
        if string == '' or len(alphabet) == 0:
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        regex = Regex(string, alphabet)
        result = regex.to_nfa().to_grammar().to_string()
        self.result['text'] = "Kết quả"
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)

class FrameHammingCode(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập xâu nhị phân gốc:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.input_text = ttk.Entry(self.input_frame, width=30, font=('Segoe UI', 9))
        self.input_text.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_text = ttk.Entry(self, width=30)
        self.result_text.pack(side = tk.TOP)
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.input_text.get()
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        result = ''.join([str(c) for c in Hamming.hammingCodes(string)])
        self.result['text'] = "Kết quả"
        self.result_text.delete('0', tk.END)
        self.result_text.insert(tk.END, result)
        
class FrameHammingCorrect(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.TOP, pady=10)
        ttk.Label(self.input_frame, text="Nhập xâu nhị phân đã mã hóa:").grid(row=0, column=0, sticky="W", pady=5, padx=10)
        self.input_text = ttk.Entry(self.input_frame, width=30, font=('Segoe UI', 9))
        self.input_text.grid(row=0, column=1, pady=5, padx=10, sticky=tk.W)
        ttk.Button(self, text="Chuyển", command=lambda: self._convert()).pack(side=tk.TOP, pady=(0, 10))
        
        
        self.result = ttk.Label(self, text="Xin hãy nhập và ấn chạy để xem kết quả")
        self.result.pack(side = tk.TOP)
        self.result_text1 = ttk.Label(self)
        self.result_text1.pack(side = tk.TOP, pady=(0, 10))
        self.result_text2 = ttk.Entry(self, width=30)
        self.result_text2.pack(side = tk.TOP)
                
    def _convert(self):
        #BLOCKING BLOCKING BLOCKING
        string = self.input_text.get()
        if string == '':
            messagebox.showerror("Lỗi", "Bạn chưa nhập đủ các trường!")
            return
        er_bit, orginal_bits = Hamming.hammingCorrection(string)
        result = ''.join([str(c) for c in orginal_bits])
        if er_bit > 0:
            result_text = "Bit lỗi là bit thứ " + str(int(er_bit))
        else:
            result_text = "Không có bit nào bị lỗi"
        
        self.result['text'] = "Kết quả"
        self.result_text1['text'] = result_text
        
        self.result_text2.delete('0', tk.END)
        self.result_text2.insert(tk.END, result)
        
class MainProgram(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Automata')
        self.geometry('1000x500+200+200')
        tk.Tk.report_callback_exception = self.show_error
        self.left_frame = tk.Frame(self, bd = 1, relief=tk.RIDGE, width = 200)
        self.left_frame.pack(side = tk.LEFT, expand = False, fill = tk.Y)
        def select_algo():
            selection = str(algo_index.get())
            label.config(text = selection)
            
        algo_index = tk.IntVar(self)
        R1 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NNCQ sang NFA", variable=algo_index, value=1, 
                             command=lambda: self.switch_frame(FrameRegextoNFA))
        R1.pack( anchor = tk.W, padx=(0, 10))
        
        R2 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NNCQ sang DFA", variable=algo_index, value=2, 
                          command=lambda: self.switch_frame(FrameRegextoDFA))
        R2.pack( anchor = tk.W, padx=(0, 10))
        
        R3 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NFA sang DFA", variable=algo_index, value=3, 
                          command=lambda: self.switch_frame(FrameNFAtoDFA))
        R3.pack( anchor = tk.W, padx=(0, 10))
             
        R4 = ttk.Radiobutton(self.left_frame, text="Chuyển từ DFA sang NNCQ", variable=algo_index, value=4, 
                          command=lambda: self.switch_frame(FrameDFAtoRegex))
        R4.pack( anchor = tk.W, padx=(0, 10))
        
        R5 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NFA sang NNCQ", variable=algo_index, value=5, 
                          command=lambda: self.switch_frame(FrameNFAtoRegex))
        R5.pack( anchor = tk.W, padx=(0, 10))
        
        R6 = ttk.Radiobutton(self.left_frame, text="Chuyển từ VPTTT sang VPTTP", variable=algo_index, value=6, 
                          command=lambda: self.switch_frame(FrameLGtoRG))
        R6.pack( anchor = tk.W, padx=(0, 10))
        
        R7 = ttk.Radiobutton(self.left_frame, text="Chuyển từ VPCQ sang NFA", variable=algo_index, value=7, 
                          command=lambda: self.switch_frame(FrameGrtoNFA))
        R7.pack( anchor = tk.W, padx=(0, 10))
        
        R8 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NFA sang VPTTP", variable=algo_index, value=8, 
                          command=lambda: self.switch_frame(FrameNFAtoGr))
        R8.pack( anchor = tk.W, padx=(0, 10))
        
        R9 = ttk.Radiobutton(self.left_frame, text="Chuyển từ VPCQ sang NNCQ", variable=algo_index, value=9, 
                          command=lambda: self.switch_frame(FrameGrtoRegex))
        R9.pack( anchor = tk.W, padx=(0, 10))
        
        R9 = ttk.Radiobutton(self.left_frame, text="Chuyển từ NNCQ sang VPTTP", variable=algo_index, value=10, 
                          command=lambda: self.switch_frame(FrameRegextoGr))
        R9.pack( anchor = tk.W, padx=(0, 10))
        
        R10 = ttk.Radiobutton(self.left_frame, text="Tạo mã Hamming", variable=algo_index, value=11, 
                          command=lambda: self.switch_frame(FrameHammingCode))
        R10.pack( anchor = tk.W, padx=(0, 10))
        
        R12 = ttk.Radiobutton(self.left_frame, text="Tìm lỗi trong mã Hamming", variable=algo_index, value=12, 
                          command=lambda: self.switch_frame(FrameHammingCorrect))
        R12.pack( anchor = tk.W, padx=(0, 10))
        
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side = tk.RIGHT, expand = True, fill = tk.BOTH)
        label = ttk.Label(self.right_frame)
        label.pack()
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.right_frame is not None:
            self.right_frame.destroy()
        self.right_frame = new_frame
        self.right_frame.pack(side=tk.TOP, padx = 10, pady = 10)
        
    def show_error(self, *args):
        err = traceback.format_exception(*args)
        messagebox.showerror('Exception',err)
        

if __name__ == "__main__":
    app = MainProgram()
    app.mainloop()
        
        

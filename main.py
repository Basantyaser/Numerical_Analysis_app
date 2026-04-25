import customtkinter as ctk
import tkinter as tk 
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import theme
from theme import Theme
import sympy as sp 



ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Numerical Analysis App")

        # ---- Screen Size / Minimum Size (80%) ----
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        min_width = int(screen_width * 0.8)
        min_height = int(screen_height * 0.8)

        self.minsize(min_width, min_height)
        self.geometry(f"{min_width}x{min_height}")

        # ---- Main Grid ----
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        # Sidebar fixed / Display expandable
        self.container.columnconfigure(0, weight=0)  # fixed
        self.container.columnconfigure(1, weight=1)  # expandable
        self.container.rowconfigure(0, weight=1)

        # ---- Sidebar ----
        self.side_bar = Sidebar(self.container, self, width=220)
        self.side_bar.grid(row=0, column=0, sticky="ns")
        self.side_bar.grid_propagate(False)

        # ---- Display Window ----
        self.display = DisplayWindow(self.container, self)
        self.display.grid(row=0, column=1, sticky="nsew")
        
        
        #--- Table styling ----
        style = ttk.Style(self)   # attach to THIS root
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#E0E0E0",
            foreground="black",
            rowheight=28,
            fieldbackground="#E0E0E0",
            bordercolor="#307DD4",
            borderwidth=1
        )

        style.configure(
            "Treeview.Heading",
            background="#307DD4",
            foreground="white",
            font=("Arial", 11, "bold")
        )
        
        style.configure(
            "Treeview",
            background="#E0E0E0",
            foreground="black",
            rowheight=30,
            fieldbackground="#E0E0E0",
            bordercolor="#307DD4",
            borderwidth=1,
            font=("Arial", 12, "bold")  
            )

        style.map(
            "Treeview",
            background=[("selected", "#307DD4")],
            foreground=[("selected", "white")]
        )
        
    
class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, controller, **kwargs):
        super().__init__(parent, **kwargs)
        self.controller = controller

        self.configure(
            fg_color=("#DEDEDE", "#2B2B2B"),
            corner_radius=0,
            border_width=0,
        )
        
        self.buttons_names = (
            "BISECTION METHOD",
            "FALSE POSITION",
            "SIMPLE FIXED POINT",
            "NEWTON'S METHOD",
            "SECANT METHOD",
            "LINEAR ALGEBRA"
        )
        self.buttons_names_dictionary = {
            "BISECTION METHOD":bisection_method,
            "FALSE POSITION": false_position,
            "SIMPLE FIXED POINT": simple_point,
            "NEWTON'S METHOD": newtons_mathod,
            "SECANT METHOD": secant_method,
            "LINEAR ALGEBRA":linear_algebra    
        }
        
        self.buttons_names = list(self.buttons_names_dictionary.keys())


        # Make rows expandable equally
        for i in range(len(self.buttons_names)):
            self.rowconfigure(i, weight=1)

        self.columnconfigure(0, weight=1)

        # Create buttons
        for i, name in enumerate(self.buttons_names):
            btn = ctk.CTkButton(
                self,
                text=name,
                corner_radius=0,
                border_width=0,
                font=("Segoe UI", 14, "bold"),
                fg_color="lightgray",            # background color
                hover_color="#e0e0e0",       # optional: hover effect
                text_color="#1F538D",           # font color
                command= lambda n = name: self.controller.display.show_frame(self.buttons_names_dictionary[n])

            )
            
            btn.grid(row=i, column=0, sticky="nsew")


class DisplayWindow(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.configure(
            fg_color=("#F5F5F5", "#1E1E1E"),
            corner_radius=0
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.frames = {}
        pages = (bisection_method, false_position, simple_point, newtons_mathod, secant_method,linear_algebra)
        for page in (pages):
            frame = page(self, self.controller)
            self.frames[page] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(bisection_method)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        

class bisection_method(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        self.error_message = ctk.CTkLabel(self, text="", font=("Segoe UI", 14, "bold"), text_color="red")
        self.error_message.grid(row=3, column=0, sticky="ewns", columnspan=8)
        for i in range(8):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.name_label = ctk.CTkLabel(
            self,
            text="BISECTION METHOD",
            font=("Segoe UI", 18, "bold"),
            fg_color=None,
            bg_color="transparent",
            corner_radius=8,
            text_color="#1F538D"
            )
        self.name_label.grid(row=0, column=0,columnspan=8, sticky="ew")
        self.function_label = ctk.CTkLabel(self, text="Enter f(x)  ", font=("Arial", 16, "bold"), fg_color=None, text_color="#1F538D")
        self.function_label.grid(row=1, column=0, sticky="ew")
        self.f_stringvar = ctk.StringVar()
        self.function_entry = ctk.CTkEntry(
            self, 
            textvariable=self.f_stringvar,
            font=("Poppins", 14),
            corner_radius=0,
            height=30,
            border_width=0,
            border_color="black",
            fg_color=("white", "gray20"),
            text_color=("black", "white"),
            placeholder_text_color="gray60"
            )
        self.function_entry.grid(row=1, column=1, columnspan=2, sticky="we")

        self.xl_label = ctk.CTkLabel(self, text="Xl", font=("Poppins", 16,  "bold"), fg_color=None, text_color="#1F538D")
        self.xu_label = ctk.CTkLabel(self, text="Xu", font=("Arial", 16, "bold"), fg_color=None, text_color="#1F538D")
        self.iterations_label = ctk.CTkLabel(self, text="Iteration", font=("Poppins", 18,  "bold"), fg_color=None, text_color="#1F538D")
        self.xl_label.grid(row=2,column=0, sticky="ew")
        self.xu_label.grid(row=2,column=2, sticky="ew")
        self.iterations_label.grid(row=2,column=4, sticky="ew")

        self.xl_var = ctk.StringVar()
        self.xu_var = ctk.StringVar()
        self.iter_var = ctk.StringVar()

        self.xl_entry = ctk.CTkEntry(
            self,
            font=("Poppins", 14),
            corner_radius=0,
            height=30,
            border_width=0,
            border_color="black",
            fg_color=("white", "gray60"),
            text_color=("black", "white"),
            placeholder_text_color="gray60",
            textvariable=self.xl_var
                                
        )
        self.xu_entry = ctk.CTkEntry(
            self,
            font=("Poppins", 14),
            corner_radius=0,
            height=30,
            border_width=0,
            border_color="black",
            fg_color=("white", "gray20"),
            text_color=("black", "white"),
            placeholder_text_color="gray60",
            textvariable=self.xu_var
        )
        self.iteration_entry = ctk.CTkEntry(
            self,
            font=("Poppins", 14),
            corner_radius=0,
            height=30,
            border_width=0,
            border_color="black",
            fg_color=("white", "gray20"),
            text_color=("black", "white"),
            placeholder_text_color="gray60",
            textvariable=self.iter_var
        )

        self.xl_entry.grid(row=2, column=1, sticky="w")
        self.xu_entry.grid(row=2, column=3,sticky="w")
        self.iteration_entry.grid(row=2, column=5, sticky="w")
        
        widgets_lists = [
            self.xl_entry, 
            self.xu_entry, 
            self.function_entry,
            self.iteration_entry,
            self.xl_label,
            self.xu_label,
            self.iterations_label,
            self.function_label
            ]
        
        self.Btn_calculate = ctk.CTkButton(self, text="Calculate", command=self.calculation,fg_color="#1F538D", hover_color="#14375E", corner_radius=8, font=("Segoe UI", 14, "bold"), text_color="white")
        self.Btn_calculate.grid(row=4, column=1, sticky="ew")
        
        
        self.btn_plot_equation = ctk.CTkButton(self, text="Plot Equation",command=self.plot ,fg_color="#1F538D", hover_color="#14375E", corner_radius=8, font=("Segoe UI", 14, "bold"), text_color="white")
        self.btn_plot_equation.grid(row=4, column=3, sticky="ew")
        self.btn_reset = ctk.CTkButton(self, text="Clear", command=self.clear_inputs, fg_color="#1F538D", hover_color="#14375E", corner_radius=8, font=("Segoe UI", 14, "bold"), text_color="white")
        self.btn_reset.grid(row=4, column=5, sticky="ew")
        self.visuals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.visuals_frame.grid(row=5, column=0, columnspan=8)
        
    def clear_visuals(self):
            if hasattr(self, "fig"):
                plt.close(self.fig)
            for widget in self.visuals_frame.winfo_children():
                widget.destroy()
        

    def clear_inputs(self):
        self.f_stringvar.set("")
        self.xl_var.set("")
        self.iter_var.set("")
        self.xu_var.set("")
        self.clear_visuals()
           

    def calculation(self): 
        self.show_table()
        try: 
            xl = float(self.xl_var.get())
            xu = float(self.xu_var.get() )
            iterations = self.iter_var.get()
        except ValueError:
            self.error_message.configure(text="Invalid Numeric Input !, Enter Values")
            return
        
        self.fx = self.f_stringvar.get().strip()
        if self.fx =="":
            self.error_message.configure( text="FUNCTION CAN'T BE EMPTY, ENTER A VALID FUNCTION")
             
            return
            
        allowed_functions = {name: getattr(math, name) for name in ["sin", "cos", "sqrt", "tan","exp","log"]}
        x=1
        try:
            eval(self.fx, {"x":x, **allowed_functions})
        except Exception as e :
            self.error_message.configure( text=f"Invalid Function! {e} !")
            
        # ---initialize variables
        xr_old = None
        x = xl
        f_xl = eval(self.fx, {"x":x, **allowed_functions})
        x = xu
        f_xu = eval(self.fx, {"x":x, **allowed_functions})
        
        # ---check if solution exists ----
        if (f_xl * f_xu > 0):
            self.error_message.configure(text="there is no Root solution for this function ! ")
        else:
           for i in range(1, int(iterations)+1):
                xr = (xl + xu) / 2
                x  = xr
                f_xr = eval(self.fx, {"x":x, **allowed_functions})
                
                
                if xr_old is None:
                    epson= "-"
                else:
                    epson = abs((xr - xr_old)/xr) * 100
                    
                xr_old = xr
                
                self.table.insert(
                    "", 
                    "end", 
                    values=(i, round(xl, 3), round(xu, 3), round(xr, 3), "-" if epson=="-" else round(epson, 3))
                    )
                
                if (f_xl * f_xr > 0):
                    xl = xr
                    f_xl = f_xr
                else:
                    xu = xr
                    f_xu = f_xr

                    
    def show_table(self):
        self.clear_visuals()
        self.error_message.configure(text="")
        self.table_column = ("i", "xl", "xu", "xr", "%")
        self.table  = ttk.Treeview(self.visuals_frame, columns=self.table_column, show="headings",)
        for column in (self.table_column):
            self.table.heading(f"{column}", text=column)

        self.table.column("i", width=100, anchor="center")
        self.table.column("xl", width=150, anchor="center")
        self.table.column("xu", width=150, anchor="center")
        self.table.column("xr", width=150, anchor="center")
        self.table.column("%", width=150, anchor="center")
            
        self.table.grid(sticky="nsew")
    
    def plot(self):
        self.clear_visuals()
        self.error_message.configure(text="")
        y_values = []
        x_values = np.linspace(-3, 6, 20)
        self.fx = self.f_stringvar.get()
        for point in x_values:
            y = eval(self.fx, {"x":point})
            y_values.append(y)
            
        self.fig, self.ax = plt.subplots()
        self.ax.plot(x_values, y_values)
        canvas = FigureCanvasTkAgg(self.fig, master=self.visuals_frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        canvas.draw()            


class false_position(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        for i in range(8):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        
        self.method_name = ctk.CTkLabel(self, text="FALSE POSITION METHOD")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=8)
        
        
        self.error_message  =ctk.CTkLabel(self, text="")
        theme.label_error(self.error_message)
        self.error_message.grid(row=3, column=0, columnspan=8)
        
        # ---  labels  -----
        self.f_label = ctk.CTkLabel(self, text=" Enter F(x)")
        self.xl_label = ctk.CTkLabel(self, text="Xl")
        self.xu_label = ctk.CTkLabel(self, text="Xu")
        self.iter_label = ctk.CTkLabel(self, text="Iterations")
        
        
        # ----- string variables ---
        self.f_var = ctk.StringVar()
        self.xl_var = ctk.StringVar()
        self.xu_var = ctk.StringVar()
        self.iter_var = ctk.StringVar()
        
        # ---- Entry ------
        self.f_entry = ctk.CTkEntry(self, textvariable=self.f_var)
        self.xl_entry = ctk.CTkEntry(self, textvariable=self.xl_var)
        self.xu_entry = ctk.CTkEntry(self, textvariable=self.xu_var)
        self.iter_entry = ctk.CTkEntry(self, textvariable=self.iter_var)
        
        self.widgets = [[self.xl_label, self.xu_label, self.iter_label], [ self.xl_entry, self.xu_entry,self.iter_entry ]]
        
        
        for i, (label, entry) in enumerate(zip(self.widgets[0], self.widgets[1])):
            theme.label_default(label)
            theme.entry_default(entry)
            label.grid(row=2, column=2*i, sticky="we")
            entry.grid(row=2, column=2*i+1, sticky="w")
        
        theme.label_default(self.f_label)
        theme.entry_default(self.f_entry)
        self.f_label.grid(row=1, column=0, sticky="ew")
        self.f_entry.grid(row=1, column=1,columnspan=2, sticky="ew")
        
        # ---- Buttons ------
        
        self.calculate_btn = ctk.CTkButton(self, text="Calculate", command=self.calculations)
        self.plot_btn = ctk.CTkButton(self, text="Plot Equation", command=self.plot)
        self.clear_btn = ctk.CTkButton(self, text="Clear", command=self.clear_input)
        
        theme.button_primary(self.calculate_btn)
        theme.button_primary(self.plot_btn)
        theme.button_primary(self.clear_btn)
        
        self.calculate_btn.grid(row=4, column=1, sticky="ew")
        self.plot_btn.grid(row=4, column=3, sticky="ew")
        self.clear_btn.grid(row=4, column=5, sticky="ew")
        
        self.visuals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.visuals_frame.grid(row=5, column=0, columnspan=8)
              
    def clear_input(self):
        self.f_var.set("")
        self.xl_var.set("")
        self.iter_var.set("")
        self.xu_var.set("")
        self.clear_visuals()
    
    def plot(self):
        self.clear_visuals()
        self.error_message.configure(text="")
        y_values = []
        x_values = np.linspace(-3, 6, 20)
        self.fx = self.f_var.get()
        for point in x_values:
            y = eval(self.fx, {"x":point})
            y_values.append(y)
            
        self.fig, self.ax = plt.subplots()
        self.ax.plot(x_values, y_values)
        canvas = FigureCanvasTkAgg(self.fig, master=self.visuals_frame)
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        canvas.draw()
        
    
    
    
    def show_table(self):
        self.clear_visuals()
        self.error_message.configure(text="")
        self.table_column = ("i", "xl", "f(xl)","xu","f(xu)", "xr", "f(xr)","%")
        self.table = ttk.Treeview(self.visuals_frame, columns=self.table_column, show="headings",)
        
        for column in (self.table_column):
            self.table.heading(f"{column}", text=column)
            
            
        self.table.column("i", width=100, anchor="center")
        self.table.column("xl", width=150, anchor="center")
        self.table.column("f(xl)", width=150, anchor="center")
        
        self.table.column("xu", width=150, anchor="center")
        self.table.column("f(xu)", width=150, anchor="center")
        
        self.table.column("xr", width=150, anchor="center")
        self.table.column("f(xr)", width=150, anchor="center")
        
        self.table.column("%", width=150, anchor="center")
        self.table.grid(sticky="nsew")
        
    def clear_visuals(self):
        if hasattr(self, "fig"):
            plt.close(self.fig)
        
        for widget in self.visuals_frame.winfo_children():
            widget.destroy()
    
    def calculations(self):
        self.show_table()
        
        try:
            self.xl = float(self.xl_var.get())
            self.xu = float(self.xu_var.get())
            self.iterations = self.iter_var.get()
        except ValueError:
            self.error_message.configure(text="Invalid numeric input!")
            return
        
        self.fx = self.f_var.get().strip()
        
        if self.fx == "":
            self.error_message.configure(text="Function is empty!")
            return
        
        self.allowed_functions = {name: getattr(math, name) for name in ["sin", "cos", "sqrt", "tan", "exp", "log"]}
        x=1
        try:
            eval(self.fx, {"x":x, **self.allowed_functions})
        except Exception as e :
            self.error_message.configure(text=f"Invalid functions! {e}")
            return
        
        #---initialize variables
        self.xr_old = None
        
        x = self.xl
        self.f_xl = eval(self.fx, {"x":x, **self.allowed_functions})
        
        x = self.xu
        self.f_xu = eval(self.fx, {"x":x, **self.allowed_functions})
        
        #--- check if solution exist ----
        
        if(self.f_xl * self.f_xu > 0):
            self.error_message.configure(text="There is NO root for this input")
        
        else:
            for i in range(1, int(self.iterations)+1):
                self.xr = (self.xu + self.xl) /2
                x = self.xr
                self.f_xr = eval(self.fx, {"x":x, **self.allowed_functions})
                
                
                
                if self.xr_old is None:
                    self.epson = "-" 
                else:
                    self.epson = abs((self.xr - self.xr_old)/self.xr) * 100
                    
                self.xr_old = self.xr
                
                self.table.insert("",
                                  "end",
                                  values=(i, round(self.xl,3), round(self.f_xl,3),round(self.xu, 3), round(self.f_xu, 3),round(self.xr, 3),round(self.f_xr, 3),"-"if self.epson=="-" else round(self.epson, 3))
                                )   
                
                if(self.f_xl * self.f_xr > 0):
                    self.xl = self.xr
                    self.f_xl = self.f_xr
                    
                else:
                    self.xu = self.xr
                    self.f_xu = self.f_xr
    


class simple_point(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        for i in range(8):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)
            
        
        self.method_name = ctk.CTkLabel(self, text="Simple Fixed Point")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=8)
        
        self.error_message  =ctk.CTkLabel(self, text="")
        theme.label_error(self.error_message)
        self.error_message.grid(row=5, column=0, columnspan=8)
        
        
        #---labels---
        self.f_label = ctk.CTkLabel(self, text="f(x)")
        self.g_label = ctk.CTkLabel(self, text="g(x)")
        self.x_label = ctk.CTkLabel(self, text="Inintial Guess")
        self.epilson_label = ctk.CTkLabel(self, text="Epilson")
        
        
        #---- string variables ---
        self.f_var = ctk.StringVar()
        self.g_var = ctk.StringVar()
        self.x_var = ctk.StringVar()
        self.epilson_var = ctk.StringVar()
        
        
        #----Entries---
        self.f_entry = ctk.CTkEntry(self, textvariable=self.f_var)
        self.g_entry = ctk.CTkEntry(self, textvariable=self.g_var)
        self.x_entry = ctk.CTkEntry(self, textvariable=self.x_var)
        self.epilson_entry = ctk.CTkEntry(self, textvariable=self.epilson_var)
        
        self.widgets = [[self.f_entry, self.g_entry, self.x_entry,], [self.f_label, self.g_label, self.x_label]]
        
        for i, (entry, label) in enumerate(zip(self.widgets[0], self.widgets[1])):
            theme.entry_default(entry)
            theme.label_default(label)
            
            label.grid(row=1, column=2*i, sticky="ew")
            entry.grid(row=1, column=2*i+1, sticky="ew")
            
        theme.label_default(self.epilson_label)
        self.epilson_label.grid(row=2, column=0, sticky="ew")
        
        theme.entry_default(self.epilson_entry)
        self.epilson_entry.grid(row=2, column=1, sticky="ew")
        
        
        self.tutorial_word = ctk.CTkLabel(self, text="Example :")
        theme.label_default(self.tutorial_word)
        self.tutorial_word.grid(row=3, column=0, sticky="e")
        self.tutorial_label = ctk.CTkLabel(self, text="Start by converting the equation into a fixed-point form, where x is isolated on one side as x = g(x). For example, given x³ + x − 1 = 0, we rearrange it algebraically to x = 1 − x³, which becomes the iteration function g(x). Then choose an initial guess such as x₀ = 0.5 and apply repeated substitution using xₙ₊₁ = 1 − (xₙ)³. This generates successive values like x₁ = 0.875, x₂ ≈ 0.330, x₃ ≈ 0.964, and so on until the values stabilize. The accuracy is checked using |xₙ₊₁ − xₙ| < ε, which determines when to stop the iterations.", wraplength=800, justify="left")
        theme.label_black(self.tutorial_label)
        self.tutorial_label.grid(row=3, column=1, columnspan=6)
        
        
        self.calculate_btn = ctk.CTkButton(self, text="calculate", command=self.calculate)
        self.clear_btn = ctk.CTkButton(self, text="clear", command=self.clear)
        
        theme.button_secondary(self.calculate_btn)
        theme.button_secondary(self.clear_btn)
        self.calculate_btn.grid(row=4, column=0, columnspan=4)
        self.clear_btn.grid(row=4, column=4, columnspan=4)
        
        
    def clear(self):
        self.f_var.set("")
        self.g_var.set("")
        self.x_var.set("")
        self.epilson_var.set("")
    
    def calculate(self):
        
        
        
        try:
            x = float(self.x_var.get())
            epilson = float(self.epilson_var.get())
        except ValueError:
            self.error_message.configure(text="Invalid Numeric Value")
            return
        
        f = self.f_var.get().strip()
        g = self.g_var.get().strip()
        
        if f=="" or g=="":
            self.error_message.configure(text="ENTER f(x) and g(x) Properly")
            return
        
        allowed_functions = {name: getattr(math,name) for name in ["sin", "cos", "sqrt", "tan","exp","log"]}
        
        try:
            eval(f, {"x":x, **allowed_functions})
            eval(g, {"x":x, **allowed_functions})
        except Exception as e :
            self.error_message.configure(text=f"Invalid Function! {e}")
            return
        
        
        self.show_table()    
        i=1
        
        error = float("inf")
        
        while error > epilson:
            gx_val = eval(g, {"x":x, **allowed_functions})
            
            xplus1 = gx_val
            
            if xplus1 !=0:
                error= abs((xplus1 - x)/xplus1) *100
            else:
                error = 0
            
            
            self.table.insert(
                "",
                "end",
                values=(i, round(x, 6), round(gx_val, 6), "-" if i==1 else round(error, 6))
            )
            
            x = xplus1
            i = i+1
            
            
                
            
                
            
        
        
        
        
        
        
    
    def show_table(self):
        self.error_message.configure(text="")
        
        if hasattr(self, "table"):
            self.table.destroy()
            
        self.table_columns = ("i", "X", "f(x)", "Epilson")
        
        self.table = ttk.Treeview(self, columns=self.table_columns, show="headings")
        
        for column in self.table_columns:
            self.table.heading(f"{column}", text=column)
            self.table.column(f"{column}", width=150, anchor="center")
        
        self.table.grid(row=6, column=2, columnspan=3, sticky="nsew")
        
        
class newtons_mathod(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        for i in range(8):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
            
        self.method_name = ctk.CTkLabel(self, text="NEWTON'S RALPH METHOD")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=8)
        
        
        self.error_message  =ctk.CTkLabel(self, text="")
        theme.label_error(self.error_message)
        self.error_message.grid(row=2, column=0, columnspan=8)
        
        
        #---labels----
        self.f_label = ctk.CTkLabel(self, text="Enter F(x)")
        self.initial_guess_label = ctk.CTkLabel(self, text="Initial Guess")
        self.epson_label = ctk.CTkLabel(self, text="Epson")
        
        #--- string Varaible--
        
        self.f_var = ctk.StringVar()
        self.initial_guess_var = ctk.StringVar()
        self.epson_var = ctk.StringVar()
        
        
        #---Entry ----
        self.f_entry = ctk.CTkEntry(self, textvariable=self.f_var)
        self.initial_guess_entry = ctk.CTkEntry(self, textvariable=self.initial_guess_var)
        self.epson_entry = ctk.CTkEntry(self, textvariable=self.epson_var)
        
        
        self.widgets = [[self.f_entry, self.initial_guess_entry, self.epson_entry], [self.f_label, self.initial_guess_label , self.epson_label]]
        
        for i, (entry, label) in enumerate(zip(self.widgets[0], self.widgets[1])):
            theme.entry_default(entry)
            theme.label_default(label)
            
            label.grid(row=1, column=2*i, sticky="ew")
            entry.grid(row=1, column=2*i+1, sticky="ew")
        
        
        #---Button----
        self.calculate_btn = ctk.CTkButton(self, text="Calculate", command=self.calculate)
        self.show_derivaitve_btn = ctk.CTkButton(self, text="Show Derivative", command=self.show_derivative)
        self.clear_btn = ctk.CTkButton(self, text="clear", command=self.clear)
        
        theme.button_primary(self.calculate_btn)
        theme.button_primary(self.show_derivaitve_btn)
        theme.button_primary(self.clear_btn)
        
        self.calculate_btn.grid(row=3, column=1)
        self.show_derivaitve_btn.grid(row=3, column=3)
        self.clear_btn.grid(row=3, column=5)
        
        
        self.visuals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.visuals_frame.grid(row=4, column=0, columnspan=8)
        
    def clear(self):
        self.f_var.set("")
        self.initial_guess_var.set("")
        self.epson_var.set("")
    
    def show_derivative(self):
        
        self.symX = sp.Symbol('x')
        expr_str = self.f_var.get()
        expr = sp.sympify(expr_str)
        self.df = sp.diff(expr, self.symX)
        
        self.error_message.configure(text=f"the Derivative : {self.df}")
        theme.label_title(self.error_message)
    
    def show_table(self):
        self.error_message.configure(text="")
        
        #-- Destroy the table if exists
        if hasattr(self, "table"):
            self.table.destroy()
        
        self.table_columns = ("x", "f(x)", "f'(x)", "epilson")
        self.table = ttk.Treeview(self.visuals_frame,
                                  columns=self.table_columns, 
                                  show="headings")
        
        for column in (self.table_columns):
            self.table.heading(f"{column}", text=column)
            self.table.column(f"{column}", width=150, anchor="center")
        
        self.table.grid(sticky="nsew")
    
    def calculate(self):
        
        try:
            x = float(self.initial_guess_var.get())
            epson = float(self.epson_var.get())
        
        except:
            self.error_message.configure(text="Invalid Numeric Input!")
            return
        
        self.fx = self.f_var.get().strip()
        
        if self.fx =="":
            self.error_message.configure(text="Function is Empty")
            return
        
        self.allowed_functions = {name: getattr(math, name) for name in ["sin", "cos", "sqrt", "tan", "exp", "log"]}
        try:
            eval(self.fx, {"x":x, **self.allowed_functions})
        except Exception as e :
            self.error_message.configure(text=f"Invalid functions! {e}")
            return
        
        
        self.show_table()
        
        error = float("inf")
        while(error > epson):
           fx_val = eval(self.fx, {"x":x, **self.allowed_functions})
           
           symX = sp.Symbol('x')
           expr = sp.sympify(self.fx)
           df_expr = sp.diff(expr, symX)

           dfx_val = float(df_expr.subs(symX, x))
           if dfx_val == 0:
            self.error_message.configure(text="Derivative is zero!")
            return
           x_next = x - (fx_val / dfx_val)
           
           if x_next != 0:
            error = abs((x_next - x) / x_next) * 100
           else:
              error = 0
            
           self.table.insert(
            "",
            "end",
            values=(
                round(x, 6),
                round(fx_val, 6),
                round(dfx_val, 6),
                "-" if error == float("inf") else round(error, 6)))
        
            
        
           x = x_next
                        


class secant_method(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.iter = 1
        for i in range(8):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)
            
            
        
        self.method_name = ctk.CTkLabel(self, text="SECANT METHOD ")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=8)
        
        self.error_message = ctk.CTkLabel(self, text="")
        theme.label_black(self.error_message)
        self.error_message.grid(row=5, column=0, columnspan=8)
        
        #--- labels----
        self.f_label = ctk.CTkLabel(self, text="Enter f(x)")
        self.xminus1_label = ctk.CTkLabel(self, text="Enter X-1")
        self.x_label = ctk.CTkLabel(self, text="Enter X")
        self.epilson_label = ctk.CTkLabel(self, text="Enter Epilson")
        
        #--- string Variables----
        self.f_var = ctk.StringVar()
        self.xminus1_var = ctk.StringVar()
        self.x_var = ctk.StringVar()
        self.epilson_var = ctk.StringVar()
        
        #----Entries----
        self.f_entry = ctk.CTkEntry(self, textvariable=self.f_var)
        self.xminus1_entry = ctk.CTkEntry(self, textvariable=self.xminus1_var)
        self.x_entry = ctk.CTkEntry(self, textvariable=self.x_var)
        self.epilson_entry = ctk.CTkEntry(self, textvariable=self.epilson_var)
        
        
        self.widgets = [[self.f_label, self.xminus1_label, self.x_label], [self.f_entry, self.xminus1_entry, self.x_entry]]
        
        for i , (label, entry) in enumerate(zip(self.widgets[0], self.widgets[1])):
            theme.label_default(label)
            theme.entry_default(entry)
            
            label.grid(row=1, column=2*i, sticky="ew")
            entry.grid(row=1, column=2*i+1, sticky="ew")
            
            
        theme.label_default(self.epilson_label)
        theme.entry_default(self.epilson_entry)
        
        self.epilson_label.grid(row=2, column=0, sticky="ew")
        self.epilson_entry.grid(row=2, column=1, sticky="ew")
        self.show_tutorial()
        
        #--- Buttons ---
        self.calculate_btn = ctk.CTkButton(self, text="Calculate", command=self.calculate)
        self.iteration_btn = ctk.CTkButton(self, text="show Iteration", command=self.show_iteration)
        self.clear_btn = ctk.CTkButton(self, text="Clear", command=self.clear)
        
        theme.button_secondary(self.calculate_btn)
        theme.button_secondary(self.iteration_btn)
        theme.button_secondary(self.clear_btn)
        
        self.calculate_btn.grid(row=4, column=1, sticky="ew")
        self.iteration_btn.grid(row=4, column=3, sticky="ew")
        self.clear_btn.grid(row=4, column=5, sticky="ew")
        
        self.visuals_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.visuals_frame.grid(row=6, column=1, columnspan=4)
        
    def show_tutorial(self):
        self.tutorial_name = ctk.CTkLabel(self, text="")
        self.tutorial_name.configure(text="Example:")
        theme.label_default(self.tutorial_name)
        self.tutorial_name.grid(row=3, column=0, sticky="ew")
        self.tutorial = ctk.CTkLabel(self, text="The Secant Method is an iterative technique used to solve f(x) = 0 using two initial guesses x(n-1) and x(n). The next value is computed as x(n+1) = x(n) - f(x(n)) * (x(n) - x(n-1)) / (f(x(n)) - f(x(n-1))). At each step, a secant line between two points on the curve is used to estimate the root, and the process repeats until the values converge." , wraplength=700, justify="left")
        theme.label_black(self.tutorial)
        self.tutorial.grid(row=3, column=1, columnspan=5) 
    
    def show_iteration(self):

      if hasattr(self, "iter2_val"):

          x0, fx0, x1, fx1, x2 = self.iter2_val

          self.tutorial_name.configure(text="Iteration 2:")
          self.tutorial.configure(
    text=(
        f"f(x0)=f({round(x0,3)})={round(fx0,3)} |     "
        f"f(x1)=f({round(x1,3)})={round(fx1,3)} |      ε={round(self.epilson,3)}\n"

        f"x2=x1-[f(x1)(x0-x1)]/[f(x0)-f(x1)]\n"

        f"x2={round(x1,3)}-[{round(fx1,3)}({round(x0,3)}-{round(x1,3)})]/"
        f"[{round(fx0,3)}-{round(fx1,3)}]={round(x2,3)} |      "
        f"error=|{round(x2,3)}-{round(x1,3)}|={round(abs(x2-x1),3)}"
    ))
          

      else:
           self.tutorial_name.configure(text="Iteration 2:")
           self.tutorial.configure(text="No data yet.")
                
    def clear(self):
        self.error_message.configure(text="")
        self.show_tutorial()
        if hasattr(self, "table"):
            self.table.destroy()
        for entry in  self.widgets[1]:
            entry.delete(0, "end")
            
        self.epilson_var.set("")
            
    
    def calculate(self):
        
        allowed_functions = {name: getattr(math, name) for name in ["sin", "cos", "sqrt", "log", "exp", "tan"]}
        
        try:
            self.xminus1 = float(self.xminus1_var.get())
            self.x = float(self.x_var.get())
            self.epilson = float(self.epilson_var.get())
        except ValueError:
            self.error_message.configure(text="Invalide Numeric Input!")
            return
        
        self.fx = self.f_var.get().strip()
        
        if self.fx == "":
            self.error_message.configure(text="Function Can't Empty!")
            return
        else:
            try:
              eval(self.fx, {"x":self.x, **allowed_functions})
            except Exception as e:
                self.error_message.configure(text=f"Enter a Proper Function! error {e}")
                return
            
        self.iter = 1
        self.show_table()
        
            
        error = float("inf")
        
        while(error > self.epilson):
            
            
            #freeze the values 
            self.x0  = self.xminus1
            self.x1 = self.x
            
            #update the values later 
            
            
            self.fxminus1 = eval(self.fx, {"x":self.x0, **allowed_functions})
            self.fx_val = eval(self.fx, {"x":self.x1, **allowed_functions})
            
            self.deminator =  (self.fxminus1 - self.fx_val)
            
            if self.deminator == 0:
                self.error_message.configure(text=f"Value error denimator is zero at iteration {self.iter}")
                return
            
            
            
            self.xplus1 = self.x1 - (self.fx_val*(self.x0- self.x1)/self.deminator)
            
            if self.xplus1 != 0 :
                error = abs((self.xplus1 - self.x1)/ self.xplus1) * 100
            else: 
                error = 0
                
            
            self.table.insert(
                "",
                "end",
                values=(self.iter, round(self.x0, 3), round(self.fxminus1, 3), round(self.x1, 3), round(self.fx_val, 3), "-" if self.iter ==1 else round(error, 3))                              
                 )
            
            if self.iter == 2:
                self.iter2_val = [self.x0, self.fxminus1, self.x1, self.fx_val, self.xplus1]
            
            
            self.xminus1 = self.x1
            self.x = self.xplus1
            self.iter = self.iter + 1
        self.iter = 1
        
        
        
        
    
    def show_table(self):
        self.error_message.configure(text="")
        
        #-- Destroy the table if exists
        if hasattr(self, "table"):
            self.table.destroy()
        
        self.table_columns = ("i", "X-1","f(x-1)","X", "f(x)", "epilson")
        self.table = ttk.Treeview(self.visuals_frame,
                                  columns=self.table_columns, 
                                  show="headings")
        
        for column in (self.table_columns):
            self.table.heading(f"{column}", text=column)
            self.table.column(f"{column}", width=150, anchor="center")
        
        self.table.grid(sticky="nsew")
        
        

    
class guass_elimination(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        
        for i in range(10):
            self.columnconfigure(i, weight=1)
            if i % 2 ==0 and i <= 5 :
              self.rowconfigure(i, weight=0)
            else:
              self.rowconfigure(i, weight=1)
        
        # for i in range(10):
        #     self.columnconfigure(i, weight=1)
        #     self.rowconfigure(i, weight=1)
            
        self.method_name = ctk.CTkLabel(self, text="Guass Elimination And Lu decomposition")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=10)
        
        self.createMatrix(self,3, 0)
        
        # self.createMatrix(7, 3)
        # ---- BUTTONS --------
        
        self.guass_elim_btn = ctk.CTkButton(self, text=" solve by Guass ", command=self.guass)
        self.lu_decomp_btn = ctk.CTkButton(self, text=" solve by LU Decompostion", command=self.lu_decomp)
        self.clear_btn = ctk.CTkButton(self, text="Clear", command=self.clear)
        
        theme.button_primary(self.guass_elim_btn)
        theme.button_primary(self.lu_decomp_btn)
        theme.button_primary(self.clear_btn)
        
        
        self.guass_elim_btn.grid(row=3, column=6, sticky="ew")
        self.lu_decomp_btn.grid(row=4, column=6, sticky="ew")
        self.clear_btn.grid(row=5, column=6, sticky="ew")
        

        self.answer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.answer_frame.grid(row=6, rowspan=10, column=0, columnspan=10, sticky="ew")

        for i in range(10):
            self.answer_frame.rowconfigure(i, weight=1)
            self.answer_frame.columnconfigure(i, weight=1)
        
        # self.createMatrix(self.answer_frame, 1, 0)
        
        
    def createMatrix(self, parent ,br, bc):

        # ----------------Create the Matrix Layout -----------------
        self.left_bracket = tk.Canvas(parent, width=20, height=100,bg="gray86", highlightthickness=0)
        self.left_bracket.grid(row=br, rowspan=3, column=bc, sticky="ns")

        # ---- top Line ----
        h = 300

        # top
        self.left_bracket.create_line(15, 5, 3, 5, width=4)

        # vertical
        self.left_bracket.create_line(5, 5, 5, h-5, width=4)

        # bottom
        self.left_bracket.create_line(3, h-5, 15, h-5, width=4)

        self.right_bracket = tk.Canvas(parent, width=20, height=100,bg="gray86", highlightthickness=0)
        self.right_bracket.grid(row=br, rowspan=3, column=bc+5, sticky="ns")

        # top
        self.right_bracket.create_line(0, 5, 17, 5, width=4)

        # vertical
        self.right_bracket.create_line(15, 5, 15, h-5, width=4)

        # bottom
        self.right_bracket.create_line(0, h-5, 17, h-5, width=4)

        self.matrix_labels = ["X1", "X2", "X3", "b"]

        for index, var in enumerate(self.matrix_labels):
            self.matrix_label = ctk.CTkLabel(parent)
            self.matrix_label.configure(text=var)
            theme.label_black(self.matrix_label)
            self.matrix_label.grid(row=br -1, column=bc+ index+1, padx=1, pady=1)

        self.entries = []
        for i in range(3):
            row_entries = []
            for j in range(4):
                self.entity = ctk.CTkEntry(parent, width=30)
                theme.entry_default(self.entity)
                self.entity.grid(row= br + i , column= bc + j +1, padx=1, pady=1)
                row_entries.append(self.entity)
            self.entries.append(row_entries)

    def guass(self):
        try:
            # Debug: Check if entries exist
            if not hasattr(self, 'entries') or len(self.entries) == 0:
                raise ValueError("Matrix entries not initialized. Please enter values in the matrix.")
            
            # Get the matrix from entries with validation
            A = []
            b = []
            for i in range(3):
                row = []
                for j in range(3):
                    # Debug: Check if entry exists
                    if i >= len(self.entries) or j >= len(self.entries[i]):
                        raise ValueError(f"Matrix entry not found at row {i+1}, column {j+1}")
                    
                    entry_val = self.entries[i][j].get().strip()
                    if entry_val == "":
                        raise ValueError(f"Matrix entry at row {i+1}, column {j+1} is empty")
                    try:
                        val = float(entry_val)
                    except ValueError:
                        raise ValueError(f"Invalid number at row {i+1}, column {j+1}: '{entry_val}'")
                    row.append(val)
                
                # Add the completed row to A list
                A.append(row)
                
                # Debug: Check if b entry exists
                if i >= len(self.entries) or 3 >= len(self.entries[i]):
                    raise ValueError(f"Matrix entry not found at row {i+1}, column 4 (b)")
                    
                b_val_entry = self.entries[i][3].get().strip()
                if b_val_entry == "":
                    raise ValueError(f"Matrix entry at row {i+1}, column 4 (b) is empty")
                try:
                    b_val = float(b_val_entry)
                except ValueError:
                    raise ValueError(f"Invalid number at row {i+1}, column 4 (b): '{b_val_entry}'")
                b.append(b_val)

            # Debug: Check individual entries before conversion
            print(f"Debug: entries structure = {len(self.entries) if hasattr(self, 'entries') else 'None'} rows")
            for i in range(3):
                if hasattr(self, 'entries') and i < len(self.entries):
                    print(f"Debug: Row {i+1} entries = {[self.entries[i][j].get().strip() for j in range(4)]}")
            
            print(f"Debug: A list = {A}, len = {len(A) if A else 0}")
            print(f"Debug: b list = {b}, len = {len(b) if b else 0}")
            
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            print(f"Debug: A shape = {A.shape}, b shape = {b.shape}")

            # Check matrix dimensions
            if A.shape != (3, 3):
                raise ValueError(f"Coefficient matrix A must be 3x3, got shape {A.shape}")
            if b.shape != (3,):
                raise ValueError(f"Vector b must have 3 elements, got shape {b.shape}")

            # Gaussian elimination with pivoting
            n = len(A)
            for i in range(n):
                # Find pivot
                if i >= len(A) or i >= A.shape[1]:
                    raise ValueError(f"Index out of bounds at step {i}")
                    
                max_row = i + np.argmax(np.abs(A[i:, i]))
                if max_row >= len(A):
                    raise ValueError(f"Pivot row {max_row} out of bounds at step {i}")
                    
                if np.abs(A[max_row, i]) < 1e-10:
                    raise ValueError(f"Matrix is singular (zero pivot at row {max_row}, column {i})")

                # Swap rows
                if max_row != i:
                    A[[i, max_row]] = A[[max_row, i]]
                    b[[i, max_row]] = b[[max_row, i]]

                # Eliminate
                for j in range(i+1, n):
                    if A[i, i] == 0:
                        raise ValueError(f"Division by zero at step {i}, row {j}")
                    factor = A[j, i] / A[i, i]
                    A[j, i:] -= factor * A[i, i:]
                    b[j] -= factor * b[i]

            # Back substitution
            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                if A[i, i] == 0:
                    raise ValueError(f"Division by zero during back substitution at row {i}")
                x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]

            # Display augmented matrix after elimination and solution vector
            self.clear_answer()

            # Augmented matrix [A|b] after elimination
            augmented = np.column_stack((A, b))
            col_labels_aug = ["X1", "X2", "X3", "b"]
            self.display_matrix(augmented, "Augmented Matrix After Elimination:", 0, 0, col_labels_aug)

            # Solution vector
            sol_matrix = [[x[i]] for i in range(3)]
            col_labels_sol = ["X"]
            self.display_matrix(sol_matrix, "Solution X:", 0, 1, col_labels_sol)

        except ValueError as e:
            self.clear_answer()
            self.error_label = ctk.CTkLabel(self.answer_frame, text=f"Error: {str(e)}", font=("Arial", 14), text_color="red")
            self.error_label.grid(row=0, column=0, columnspan=10, sticky="w")
        except Exception as e:
            self.clear_answer()
            self.error_label = ctk.CTkLabel(self.answer_frame, text=f"Unexpected error: {str(e)}", font=("Arial", 14), text_color="red")
            self.error_label.grid(row=0, column=0, columnspan=10, sticky="w")

    def lu_decomp(self):
        try:
            # Debug: Check if entries exist
            if not hasattr(self, 'entries') or len(self.entries) == 0:
                raise ValueError("Matrix entries not initialized. Please enter values in the matrix.")
            
            A = []
            b = []
            for i in range(3):
                row = []
                for j in range(3):
                    # Debug: Check if entry exists
                    if i >= len(self.entries) or j >= len(self.entries[i]):
                        raise ValueError(f"Matrix entry not found at row {i+1}, column {j+1}")
                    
                    entry_val = self.entries[i][j].get().strip()
                    if entry_val == "":
                        raise ValueError(f"Matrix entry at row {i+1}, column {j+1} is empty")
                    try:
                        val = float(entry_val)
                    except ValueError:
                        raise ValueError(f"Invalid number at row {i+1}, column {j+1}: '{entry_val}'")
                    row.append(val)
                
                # Add the completed row to A list
                A.append(row)
                
                # Debug: Check if b entry exists
                if i >= len(self.entries) or 3 >= len(self.entries[i]):
                    raise ValueError(f"Matrix entry not found at row {i+1}, column 4 (b)")
                    
                b_val_entry = self.entries[i][3].get().strip()
                if b_val_entry == "":
                    raise ValueError(f"Matrix entry at row {i+1}, column 4 (b) is empty")
                try:
                    b_val = float(b_val_entry)
                except ValueError:
                    raise ValueError(f"Invalid number at row {i+1}, column 4 (b): '{b_val_entry}'")
                b.append(b_val)

            # Debug: Check individual entries before conversion
            print(f"Debug LU: entries structure = {len(self.entries) if hasattr(self, 'entries') else 'None'} rows")
            for i in range(3):
                if hasattr(self, 'entries') and i < len(self.entries):
                    print(f"Debug LU: Row {i+1} entries = {[self.entries[i][j].get().strip() for j in range(4)]}")
            
            print(f"Debug LU: A list = {A}, len = {len(A) if A else 0}")
            print(f"Debug LU: b list = {b}, len = {len(b) if b else 0}")
            
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            print(f"Debug LU: A shape = {A.shape}, b shape = {b.shape}")

            if A.shape != (3, 3):
                raise ValueError(f"Coefficient matrix A must be 3x3 (first 3 columns), got shape {A.shape}")
            if b.shape != (3,):
                raise ValueError(f"Constant vector b must have 3 elements (4th column), got shape {b.shape}")

            n = len(A)
            L = np.eye(n)
            U = np.copy(A)

            for i in range(n):
                if i >= U.shape[0] or i >= U.shape[1]:
                    raise ValueError(f"Index out of bounds at step {i}")
                    
                if abs(U[i, i]) < 1e-10:
                    raise ValueError(f"Matrix is singular or requires pivoting (zero pivot at row {i}, column {i})")

                for j in range(i+1, n):
                    if j >= U.shape[0] or i >= U.shape[1]:
                        raise ValueError(f"Index out of bounds at step {i}, row {j}")
                    if U[i, i] == 0:
                        raise ValueError(f"Division by zero at step {i}, row {j}")
                    factor = U[j, i] / U[i, i]
                    L[j, i] = factor
                    U[j, i:] -= factor * U[i, i:]

            y = np.zeros(n)
            for i in range(n):
                if i >= L.shape[0]:
                    raise ValueError(f"Index out of bounds during forward substitution at step {i}")
                y[i] = b[i] - np.dot(L[i, :i], y[:i])

            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                if i >= U.shape[0] or i >= U.shape[1]:
                    raise ValueError(f"Index out of bounds during back substitution at step {i}")
                if U[i, i] == 0:
                    raise ValueError(f"Division by zero during back substitution at row {i}")
                x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i, i]

            # Display L, U, and solution vector
            self.clear_answer()

            # L matrix (ultra-compact)
            self.display_matrix_compact(L, "L:", 0, 0)

            # U matrix (ultra-compact)
            self.display_matrix_compact(U, "U:", 0, 1)

            # Solution vector (ultra-compact)
            sol_matrix = [[x[i]] for i in range(3)]
            col_labels_sol = ["X"]
            self.display_matrix_compact(sol_matrix, "X:", 0, 2, col_labels_sol)

        except ValueError as e:
            self.clear_answer()
            self.error_label = ctk.CTkLabel(self.answer_frame, text=f"Error: {str(e)}", font=("Arial", 14), text_color="red")
            self.error_label.grid(row=0, column=0, columnspan=10, sticky="w")
        except Exception as e:
            self.clear_answer()
            self.error_label = ctk.CTkLabel(self.answer_frame, text=f"Unexpected error: {str(e)}", font=("Arial", 14), text_color="red")
            self.error_label.grid(row=0, column=0, columnspan=10, sticky="w")

    def display_matrix(self, matrix, label_text, start_row, start_col, col_labels=None):
        # Calculate proper bracket height to match matrix rows exactly
        element_height = 25
        bracket_height = len(matrix) * element_height + 10
        
        # Create main container frame for better spacing
        matrix_container = ctk.CTkFrame(self.answer_frame, fg_color="transparent")
        matrix_container.grid(row=start_row, column=start_col, sticky="w", padx=(0, 15))
        
        # Title label
        title_label = ctk.CTkLabel(matrix_container, text=label_text, font=("Arial", 12, "bold"))
        theme.label_default(title_label)
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Create visual brackets around the matrix with proper background
        left_bracket = tk.Canvas(matrix_container, width=12, height=bracket_height,bg="gray86", highlightthickness=0)
        left_bracket.grid(row=1, column=0, rowspan=len(matrix) + 2, sticky="ns", padx=(0, 2))
        
        # Draw left bracket with consistent color
        left_bracket.create_line(10, 5, 2, 5, width=3, fill="black")
        left_bracket.create_line(2, 5, 2, bracket_height - 5, width=3, fill="black")
        left_bracket.create_line(2, bracket_height - 5, 10, bracket_height - 5, width=3, fill="black")
        
        right_bracket = tk.Canvas(matrix_container, width=12, height=bracket_height,bg="gray86", highlightthickness=0)
        right_bracket.grid(row=1, column=len(matrix[0]) + 1, rowspan=len(matrix) + 2, sticky="ns", padx=(2, 0))
        
        # Draw right bracket with consistent color
        right_bracket.create_line(2, 5, 10, 5, width=3, fill="black")
        right_bracket.create_line(10, 5, 10, bracket_height - 5, width=3, fill="black")
        right_bracket.create_line(10, bracket_height - 5, 2, bracket_height - 5, width=3, fill="black")
        
        # Add column labels if provided
        if col_labels:
            for idx, label in enumerate(col_labels):
                col_label = ctk.CTkLabel(matrix_container, text=label, font=("Arial", 10, "bold"))
                theme.label_black(col_label)
                col_label.grid(row=1, column=idx + 1, padx=2, pady=1)
            matrix_start_row = 2
        else:
            matrix_start_row = 1
        
        # Display matrix values with compact styling and 3 decimal places
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                # Round to 3 decimal places and format nicely
                value = matrix[i][j]
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:.3f}"
                else:
                    formatted_value = str(value)
                
                # Create compact styled label for each matrix element
                val_label = ctk.CTkLabel(
                    matrix_container, 
                    text=formatted_value, 
                    font=("Courier New", 10, "bold"),
                    width=50,
                    height=25
                )
                theme.label_black(val_label)
                val_label.grid(row=matrix_start_row + i, column=j + 1, padx=2, pady=1)
        
        return start_row

    def display_matrix_compact(self, matrix, label_text, start_row, start_col, col_labels=None):
        # Calculate ultra-compact bracket height to match matrix rows exactly
        element_height = 20
        bracket_height = len(matrix) * element_height + 8
        
        # Create main container frame for better spacing
        matrix_container = ctk.CTkFrame(self.answer_frame, fg_color="transparent")
        matrix_container.grid(row=start_row, column=start_col, sticky="w", padx=(0, 10))
        
        # Title label
        title_label = ctk.CTkLabel(matrix_container, text=label_text, font=("Arial", 10, "bold"))
        theme.label_default(title_label)
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 3))
        
        # Create visual brackets around the matrix with ultra-small size and proper background
        left_bracket = tk.Canvas(matrix_container, width=10, height=bracket_height,bg="gray86", highlightthickness=0)
        left_bracket.grid(row=1, column=0, rowspan=len(matrix) + 2, sticky="ns", padx=(0, 1))
        
        # Draw left bracket with consistent color
        left_bracket.create_line(8, 3, 2, 3, width=2, fill="black")
        left_bracket.create_line(2, 3, 2, bracket_height - 3, width=2, fill="black")
        left_bracket.create_line(2, bracket_height - 3, 8, bracket_height - 3, width=2, fill="black")
        
        right_bracket = tk.Canvas(matrix_container, width=10, height=bracket_height,bg="gray86", highlightthickness=0)
        right_bracket.grid(row=1, column=len(matrix[0]) + 1, rowspan=len(matrix) + 2, sticky="ns", padx=(1, 0))
        
        # Draw right bracket with consistent color
        right_bracket.create_line(2, 3, 8, 3, width=2, fill="black")
        right_bracket.create_line(8, 3, 8, bracket_height - 3, width=2, fill="black")
        right_bracket.create_line(8, bracket_height - 3, 2, bracket_height - 3, width=2, fill="black")
        
        # Add column labels if provided
        if col_labels:
            for idx, label in enumerate(col_labels):
                col_label = ctk.CTkLabel(matrix_container, text=label, font=("Arial", 9, "bold"))
                theme.label_black(col_label)
                col_label.grid(row=1, column=idx + 1, padx=1, pady=1)
            matrix_start_row = 2
        else:
            matrix_start_row = 1
        
        # Display matrix values with ultra-compact styling and 3 decimal places
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                # Round to 3 decimal places and format nicely
                value = matrix[i][j]
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:.3f}"
                else:
                    formatted_value = str(value)
                
                # Create ultra-compact styled label for each matrix element
                val_label = ctk.CTkLabel(
                    matrix_container, 
                    text=formatted_value, 
                    font=("Courier New", 9, "bold"),
                    width=40,
                    height=20
                )
                theme.label_black(val_label)
                val_label.grid(row=matrix_start_row + i, column=j + 1, padx=1, pady=1)
        
        return start_row

    def clear_answer(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def clear(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.clear_answer()
        
        
            












class linear_algebra(ctk.CTkFrame): 
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        for i in range(10):
            self.columnconfigure(i, weight=1)
            if i % 2 == 0 and i <= 5:
                self.rowconfigure(i, weight=0)
            else:
                self.rowconfigure(i, weight=1)
        
        self.method_name = ctk.CTkLabel(self, text="LINEAR ALGEBRA METHODS FOR SOLVING SYSTEMS OF EQUATIONS")
        theme.label_title(self.method_name)
        self.method_name.grid(row=0, column=0, columnspan=10)
        
        self.createMatrix(self, 3, 0)
        
        # Buttons
        self.guass_elim_btn = ctk.CTkButton(self, text="Solve by Gauss Elimination", command=self.guass)
        self.lu_decomp_btn = ctk.CTkButton(self, text="Solve by LU Decomposition", command=self.lu_decomp)
        self.clear_btn = ctk.CTkButton(self, text="Clear", command=self.clear)
        
        theme.button_primary(self.guass_elim_btn)
        theme.button_primary(self.lu_decomp_btn)
        theme.button_primary(self.clear_btn)
        
        self.guass_elim_btn.grid(row=3, column=6, sticky="ew")
        self.lu_decomp_btn.grid(row=4, column=6, sticky="ew")
        self.clear_btn.grid(row=5, column=6, sticky="ew")
        self.cramer_btn = ctk.CTkButton(self, text="Solve by Cramer's Rule", command=self.cramer)
        theme.button_primary(self.cramer_btn)
        self.cramer_btn.grid(row=3, column=8, sticky="ew")
        
        self.jordan_btn = ctk.CTkButton(self, text="Solve by Gauss-Jordan", command=self.gauss_jordan)
        theme.button_primary(self.jordan_btn)
        self.jordan_btn.grid(row=4, column=8, sticky="ew")


        self.answer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.answer_frame.grid(row=6, rowspan=10, column=0, columnspan=10, sticky="ew")

        for i in range(10):
            self.answer_frame.rowconfigure(i, weight=1)
            self.answer_frame.columnconfigure(i, weight=1)
        
    def createMatrix(self, parent, br, bc):
        self.entries = []

        labels = ["X1", "X2", "X3", "b"]
        for i, text in enumerate(labels):
            lbl = ctk.CTkLabel(parent, text=text)
            theme.label_black(lbl)
            lbl.grid(row=br-1, column=bc+i+1)

        for i in range(3):
            row_entries = []
            for j in range(4):
                entry = ctk.CTkEntry(parent, width=30)
                theme.entry_default(entry)
                entry.grid(row=br+i, column=bc+j+1, padx=1, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)

    # ---------------- GAUSS ----------------
    def guass(self):
        try:
            A, b = [], []

            for i in range(3):
                row = []
                for j in range(3):
                    val = self.entries[i][j].get().strip()
                    if val == "":
                        raise ValueError("Empty matrix entry")
                    row.append(float(val))
                A.append(row)

                b_val = self.entries[i][3].get().strip()
                if b_val == "":
                    raise ValueError("Empty b value")
                b.append(float(b_val))

            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)

            n = len(A)
            multipliers = np.zeros((n, n))

            # Forward elimination
            for i in range(n):
                if A[i][i] == 0:
                    raise ValueError("Zero pivot (no pivoting allowed)")

                for j in range(i+1, n):
                    factor = A[j][i] / A[i][i]
                    multipliers[j][i] = factor
                    A[j, i:] -= factor * A[i, i:]
                    b[j] -= factor * b[i]

            # Back substitution
            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i][i]

            self.clear_answer()

            augmented = np.column_stack((A, b))
            self.display_matrix(augmented, "After Elimination:", 0, 0, ["X1","X2","X3","b"])
            self.display_matrix(multipliers, "Multipliers:", 0, 1)

            sol = [[x[i]] for i in range(3)]
            self.display_matrix(sol, "Solution:", 0, 2, ["X"])

        except Exception as e:
            self.clear_answer()
            error = ctk.CTkLabel(self.answer_frame, text=f"Error: {str(e)}", text_color="red")
            error.grid(row=0, column=0)

    # ---------------- LU ----------------
    def lu_decomp(self):
        try:
            A, b = [], []

            for i in range(3):
                row = []
                for j in range(3):
                    val = self.entries[i][j].get().strip()
                    if val == "":
                        raise ValueError("Empty matrix entry")
                    row.append(float(val))
                A.append(row)

                b_val = self.entries[i][3].get().strip()
                if b_val == "":
                    raise ValueError("Empty b value")
                b.append(float(b_val))

            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)

            n = len(A)
            L = np.zeros((n, n))
            U = np.zeros((n, n))

            # Doolittle
            for i in range(n):

                for k in range(i, n):
                    U[i][k] = A[i][k] - sum(L[i][j] * U[j][k] for j in range(i))

                if U[i][i] == 0:
                    raise ValueError("Zero pivot")

                for k in range(i, n):
                    if i == k:
                        L[i][i] = 1
                    else:
                        L[k][i] = (A[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]

            # Forward substitution
            y = np.zeros(n)
            for i in range(n):
                y[i] = b[i] - np.dot(L[i, :i], y[:i])

            # Back substitution
            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                x[i] = (y[i] - np.dot(U[i, i+1:], x[i+1:])) / U[i][i]

            self.clear_answer()

            self.display_matrix(L, "L:", 0, 0)
            self.display_matrix(U, "U:", 0, 1)

            sol = [[x[i]] for i in range(3)]
            self.display_matrix(sol, "X:", 0, 2, ["X"])

        except Exception as e:
            self.clear_answer()
            error = ctk.CTkLabel(self.answer_frame, text=f"Error: {str(e)}", text_color="red")
            error.grid(row=0, column=0)

    # ---------------- DISPLAY ----------------
    def display_matrix(self, matrix, label_text, start_row, start_col, col_labels=None):
        container = ctk.CTkFrame(self.answer_frame, fg_color="transparent")
        container.grid(row=start_row, column=start_col, padx=10, sticky="w")

        title = ctk.CTkLabel(container, text=label_text, font=("Arial", 12, "bold"))
        theme.label_default(title)
        title.grid(row=0, column=1, sticky="w")

        rows = len(matrix)
        cols = len(matrix[0])

        start = 1
        extra = 0

        if col_labels:
            for j in range(cols):
                lbl = ctk.CTkLabel(container, text=col_labels[j])
                theme.label_black(lbl)
                lbl.grid(row=1, column=j+1)
            start = 2
            extra = 1

        cell_height = 28
        height = (rows + extra) * cell_height

        left = tk.Canvas(container, width=12, height=height, bg="gray86", highlightthickness=0)
        left.grid(row=1, column=0, rowspan=rows + extra)

        left.create_line(10, 3, 2, 3, width=3)
        left.create_line(2, 3, 2, height-3, width=3)
        left.create_line(2, height-3, 10, height-3, width=3)

        right = tk.Canvas(container, width=12, height=height, bg="gray86", highlightthickness=0)
        right.grid(row=1, column=cols+1, rowspan=rows + extra)

        right.create_line(2, 3, 10, 3, width=3)
        right.create_line(10, 3, 10, height-3, width=3)
        right.create_line(10, height-3, 2, height-3, width=3)

        for i in range(rows):
            for j in range(cols):
                val = matrix[i][j]
                text = f"{val:.3f}" if isinstance(val, (int, float)) else str(val)

                lbl = ctk.CTkLabel(container, text=text, width=50, height=25)
                theme.label_black(lbl)
                lbl.grid(row=start+i, column=j+1, padx=2, pady=1)

    # ---------------- UTILS ----------------
    def clear_answer(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def clear(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.clear_answer()
            

    def cramer(self):
        try:
            A_list = []
            b_list = []

            # 1. Read all input FIRST
            for i in range(3):
                row = []
                for j in range(3):
                    val = self.entries[i][j].get().strip()
                    if not val:
                        raise ValueError(f"Empty entry at row {i+1}, col {j+1}")
                    row.append(float(val))
                A_list.append(row)

                # Read the constant vector b
                b_val = self.entries[i][3].get().strip()
                if not b_val:
                    raise ValueError(f"Empty b value at row {i+1}")
                b_list.append(float(b_val))

            # 2. Convert to NumPy arrays AFTER the loops
            A = np.array(A_list, dtype=float)
            b = np.array(b_list, dtype=float)

            # 3. Perform Cramer's Rule logic
            detA = np.linalg.det(A)

            if abs(detA) < 1e-12:
                raise ValueError("Determinant is zero (or near zero) → No unique solution.")

            # Replace columns and calculate determinants
            results = []
            matrices = []
            for i in range(3):
                Ai = A.copy()
                Ai[:, i] = b
                detAi = np.linalg.det(Ai)
                matrices.append((Ai, detAi))
                results.append(detAi / detA)

                # 4. UI Display logic
                self.clear_answer()

                # Display det(A)
                self.display_matrix([[detA]], "det(A):", 0, 0)

                # Display A1, A2, A3 and their determinants
                for i, (Ai, detAi) in enumerate(matrices):
                    self.display_matrix(Ai, f"A{i+1}:", 1, i)
                    self.display_matrix([[detAi]], f"det(A{i+1}):", 2, i)

                    # Display Final Solution
                    sol = [[r] for r in results]
                    self.display_matrix(sol, "Solution:", 1, 4, ["X"])

        except Exception as e:
            self.clear_answer()
            # Ensure ctk is imported or use the appropriate library reference
            ctk.CTkLabel(self.answer_frame, text=f"Error: {e}", text_color="red").grid(row=0, column=0)


            

    def gauss_jordan(self):
        try:
            A_list = []
            b_list = []

            # 1. Read input from the UI
            for i in range(3):
                # Read the 3x3 matrix coefficients
                row = []
                for j in range(3):
                    val = self.entries[i][j].get().strip()
                    if not val:
                        raise ValueError(f"Empty entry at row {i+1}, col {j+1}")
                    row.append(float(val))
                A_list.append(row)

                    # Read the constant vector b (index 3 in the UI row)
                b_val = self.entries[i][3].get().strip()
                if not b_val:
                    raise ValueError(f"Empty b value at row {i+1}")
                b_list.append(float(b_val))

            # 2. Setup NumPy arrays
            A = np.array(A_list, dtype=float)
            b = np.array(b_list, dtype=float)
            n = 3
            operations = []

            # Create augmented matrix [A | b]
            Ab = np.hstack((A, b.reshape(-1, 1)))

            # 3. Gauss-Jordan Elimination Logic
            for i in range(n):
                # Partial Pivoting: Find the row with the largest absolute value in the current column
                max_row = i + np.argmax(abs(Ab[i:, i]))

                if abs(Ab[max_row, i]) < 1e-12:
                    raise ValueError("Matrix is singular or has no unique solution.")

                # Swap rows if the max value isn't in the current row
                if max_row != i:
                    Ab[[i, max_row]] = Ab[[max_row, i]]
                    operations.append(f"R{i+1} ↔ R{max_row+1}")

                    # Normalize pivot row (Divide by the pivot element to get a 1)
                pivot = Ab[i, i]
                Ab[i] = Ab[i] / pivot
                operations.append(f"R{i+1} = R{i+1} / {pivot:.3f}")

                # Eliminate other rows (Get 0s above and below the pivot)
                for j in range(n):
                    if j != i:
                        factor = Ab[j, i]
                        Ab[j] = Ab[j] - factor * Ab[i]
                        operations.append(f"R{j+1} = R{j+1} - ({factor:.3f})R{i+1}")

            # 4. Display Results (Only once calculation is complete)
            self.clear_answer()

            # Extract the final column (solution vector)
            x_solution = Ab[:, -1]

            # Display the RREF matrix (Identity matrix) and the Solution vector
            self.display_matrix(Ab[:, :-1], "RREF Matrix", 5, 0)
            self.display_matrix([[xi] for xi in x_solution], "Solution", 5, 1, ["X"])

            # Display the log of row operations
            log_frame = ctk.CTkFrame(self.answer_frame, fg_color="transparent")
            log_frame.grid(row=5, column=6, columnspan=2, sticky="w", pady=10)

            ctk.CTkLabel(log_frame, text="Operations:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")
            for k, op in enumerate(operations):
                ctk.CTkLabel(log_frame, text=op).grid(row=k+1, column=0, sticky="w")

        except Exception as e:
            self.clear_answer()
            # Ensure ctk is correctly referenced based on your imports
            ctk.CTkLabel(self.answer_frame, text=f"Error: {e}", text_color="red").grid(row=0, column=0)










if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

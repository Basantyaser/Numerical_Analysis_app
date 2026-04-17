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
            "GAUSSIAN ELIMINATION",
            "LU FACTORIZATION",
            "PA FACTORIZATION",
            "GAUSS-JORDAN",
            "CRAMER'S RULE"
        )
        self.buttons_names_dictionary = {
            "BISECTION METHOD":bisection_method,
            "FALSE POSITION": false_position,
            "SIMPLE FIXED POINT": simple_point,
            "NEWTON'S METHOD": newtons_mathod,
            "SECANT METHOD": secant_method,
            "GAUSSIAN ELIMINATION":guass_elimination,
            "LU FACTORIZATION": lu_factor,
            "PA FACTORIZATION": pa_factor,
            "GAUSS-JORDAN": guass_jordan,
            "CRAMER'S RULE":cramer_rule    
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
        pages = (bisection_method, false_position, simple_point, newtons_mathod, secant_method,guass_elimination, lu_factor, pa_factor, guass_jordan, cramer_rule)
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
        # # ----clear the table -----
        # for row in self.table.get_children():
        #     self.table.delete(row) 
           
        # ----validate numeric inputs
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
                    values=(i, round(xl, 6), round(xu, 6), round(xr, 6), "-" if epson=="-" else round(epson, 6))
                    )
                
                if (f_xl * f_xr > 0):
                    xl = xr
                else:
                    xu = xr

                    
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
        self.table_column = ("i", "xl", "xu", "xr", "%")
        self.table = ttk.Treeview(self.visuals_frame, columns=self.table_column, show="headings",)
        
        for column in (self.table_column):
            self.table.heading(f"{column}", text=column)
            
            
        self.table.column("i", width=100, anchor="center")
        self.table.column("xl", width=150, anchor="center")
        self.table.column("xu", width=150, anchor="center")
        self.table.column("xr", width=150, anchor="center")
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
                                  values=(i, round(self.xl,6), round(self.xu, 6), round(self.xr, 6), "-"if self.epson=="-" else round(self.epson, 6))
                                )   
                
                if(self.f_xl * self.f_xr > 0):
                    self.xl = self.xr
                else:
                    self.xu = self.xr
    




class simple_point(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        
        for i in range(8):
            self.columnconfigure(i, weight=1)
            self.rowconfigure(i, weight=1)
            
        
        self.method_name = ctk.CTkLabel(self, text="Simple Fixed Point")
        theme.label_title(self.method_name)
        
        self.error_message  =ctk.CTkLabel(self, text="")
        theme.label_error(self.error_message)
        self.error_message.grid(row=3, column=0, columnspan=8)
        
        
        
        #---labels---
        
        
        
        
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
        self.clear_btn = ctk.CTkButton(self, text="clear")
        
        theme.button_primary(self.calculate_btn)
        theme.button_primary(self.show_derivaitve_btn)
        theme.button_primary(self.clear_btn)
        
        self.calculate_btn.grid(row=3, column=1)
        self.show_derivaitve_btn.grid(row=3, column=3)
        self.clear_btn.grid(row=3, column=5)
        
        
    
    def show_derivative(self):
        
        self.symX = sp.Symbol('x')
        expr_str = self.f_var.get()
        expr = sp.sympify(expr_str)
        self.df = sp.diff(expr, self.symX)
        
        if not hasattr(self, "derv_label"):
           self.derv_label = ctk.CTkLabel(self, text="")
           theme.label_title(self.derv_label)
           self.derv_label.grid(row=2, column=0, columnspan=8, sticky="nsew")

        self.derv_label.configure(text=f"The Derivative : {self.df}")
       
    
    def calculate(self):
        pass










class secant_method(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from secant method class")
        self.label1.grid()

    
class guass_elimination(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from guass elimination class")
        self.label1.grid()

    
class lu_factor(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from lu factor class")
        self.label1.grid()


class pa_factor(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from pa factor class")
        self.label1.grid()
 
            
class guass_jordan(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from guass jordan class")
        self.label1.grid()


class cramer_rule(ctk.CTkFrame):
    def __init__(self, parent, controller, **args):
        super().__init__(parent, **args)
        self.controller = controller
        self.label1 = ctk.CTkLabel(self, text="hello from cramers rule class")
        self.label1.grid()



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
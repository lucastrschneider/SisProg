import tkinter as tk

NUM_OF_ROWS = 14
NUM_OF_COLUMNS = 10

class ProgSysGUI:
    def __init__(self) -> None:
        # Create the main window
        self.tk_gui = tk.Tk()

        bg_color = "#434344"
        fg_color = "#FFFFFF"

        self.tk_gui.title("Sistema de programação")
        self.tk_gui.configure(background=bg_color)
        self.tk_gui.geometry("940x480")
        self.tk_gui.resizable(width=False, height=False)

        for i in range(NUM_OF_ROWS):
            self.tk_gui.rowconfigure(i, weight=1)

        for i in range(NUM_OF_COLUMNS):
            self.tk_gui.columnconfigure(i, weight=1)

        # Create machine state indicator
        state_title_label = tk.Label(self.tk_gui,
            text='Estado da Máquina',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            height=2,
            font=("TkDefaultFont", 14, "bold")
        )
        state_title_label.grid(row=0, column=0, columnspan=NUM_OF_COLUMNS, sticky="NSEW")
        
        # Create registers
        state_register_title_label = tk.Label(self.tk_gui,
            text='Registradores',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 12, "bold")
        )
        state_register_title_label.grid(row=1, column=0, columnspan=4, sticky="NSEW")

        self.state_reg_vars = []
        for i in range(32):
            reg_string_var = tk.StringVar()
            reg_string_var.set(f'r{i}: 0x00000000')
            label = tk.Label(self.tk_gui,
                textvariable=reg_string_var,
                fg=fg_color,
                bg=bg_color,
                justify='left',
                font=("TkDefaultFont", 10, "normal")
            )
            label.grid(row= i % 8 + 2, column= i // 8, sticky="NSEW")
            self.state_reg_vars.append(reg_string_var)
        
        # Create indicators
        state_indicators_title_label = tk.Label(self.tk_gui,
            text='Indicadores',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 12, "bold")
        )
        state_indicators_title_label.grid(row=1, column=4, columnspan=2, sticky="NSEW")
        
        # Create memory
        state_mem_title_label = tk.Label(self.tk_gui,
            text='Memória',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 12, "bold")
        )
        state_mem_title_label.grid(row=1, column=6, columnspan=4, sticky="NSEW")

        self.state_mem_add_button = tk.Button(self.tk_gui,
            text='\N{RIGHTWARDS BLACK ARROW}',
            width=1,
            height=1,
        )
        self.state_mem_add_button.grid(row=2, column=9, padx=10, pady=10, sticky="W")
        
        mem_add_label = tk.Label(self.tk_gui,
            text='Endereço Memória:',
            fg=fg_color,
            bg=bg_color,
            justify='right',
            font=("TkDefaultFont", 10, "normal")
        )
        mem_add_label.grid(row=2, column=6, columnspan=1, sticky="NSEW")

        self.mem_add_entry = tk.Entry(self.tk_gui,
            width=5
        )
        self.mem_add_entry.grid(row=2, column=7, columnspan=2, padx=10, pady=10, sticky="NSEW")

        self.state_mem_vars = []
        for i in range(14):
            mem_string_var = tk.StringVar()
            mem_string_var.set(f'0x{i:03x}: 0x00000000')
            label = tk.Label(self.tk_gui,
                textvariable=mem_string_var,
                fg=fg_color,
                bg=bg_color,
                justify='left',
                font=("TkDefaultFont", 10, "normal")
            )
            label.grid(row= i % 7 + 3, column= 2* (i // 7) + 6, columnspan=2, sticky="NSEW")
            self.state_mem_vars.append(mem_string_var)

        # Create commands indicator
        state_title_label = tk.Label(self.tk_gui,
            text='Comandos do operador',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            height=2,
            font=("TkDefaultFont", 14, "bold")
        )
        state_title_label.grid(row=10, column=0, columnspan=NUM_OF_COLUMNS, sticky="NSEW")

        # Create and edit file
        create_file_button = tk.Button(self.tk_gui,
            text='Create File',
            width=1,
            height=1,
        )
        create_file_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        edit_file_button = tk.Button(self.tk_gui,
            text='Edit File',
            width=1,
            height=1,
        )
        edit_file_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

        # Load and dump
        load_button = tk.Button(self.tk_gui,
            text='Loader',
            width=1,
            height=1,
        )
        load_button.grid(row=11, column=2, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        dump_button = tk.Button(self.tk_gui,
            text='Dumper',
            width=1,
            height=1,
        )
        dump_button.grid(row=12, column=2, columnspan=2, padx=10, pady=10, sticky="NSEW")

        # Máquina virtual
        vm_add_label = tk.Label(self.tk_gui,
            text='Endereço Instrução:',
            fg=fg_color,
            bg=bg_color,
            justify='right',
            font=("TkDefaultFont", 10, "normal")
        )
        vm_add_label.grid(row=11, column=4, columnspan=2, sticky="NSEW")

        self.vm_start_entry = tk.Entry(self.tk_gui,
            width=5
        )
        self.vm_start_entry.grid(row=11, column=6, columnspan=2, padx=10, pady=10, sticky="NSEW")

        vm_start_button = tk.Button(self.tk_gui,
            text='Iniciar',
            width=1,
            height=1,
        )
        vm_start_button.grid(row=12, column=4, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        vm_end_button = tk.Button(self.tk_gui,
            text='Encerrar',
            width=1,
            height=1,
        )
        vm_end_button.grid(row=12, column=6, columnspan=2, padx=10, pady=10, sticky="NSEW")

        vm_ex_button = tk.Button(self.tk_gui,
            text='Executar',
            width=1,
            height=1,
        )
        vm_ex_button.grid(row=13, column=4, columnspan=2, padx=10, pady=10, sticky="NSEW")

        vm_step_button = tk.Button(self.tk_gui,
            text='Step',
            width=1,
            height=1,
        )
        vm_step_button.grid(row=13, column=6, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        # Assembler
        abs_asm_button = tk.Button(self.tk_gui,
            text='Montador Absoluto',
            width=1,
            height=1,
        )
        abs_asm_button.grid(row=11, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        rel_asm_button = tk.Button(self.tk_gui,
            text='Montador Relativo',
            width=1,
            height=1,
        )
        rel_asm_button.grid(row=12, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        linker_button = tk.Button(self.tk_gui,
            text='Ligador Relocador',
            width=1,
            height=1,
        )
        linker_button.grid(row=13, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")

    def start(self) -> None:
        self.tk_gui.mainloop()

    def stop(self) -> None:
        self.tk_gui.destroy()

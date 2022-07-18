import tkinter as tk

from prog_sys.indicator import Indicator
from .event import EventType, Event
from .event_controller import EventController
from .reg_file import RegFile
from .memory import Memory
from .indicator import Indicator

NUM_OF_ROWS = 14
NUM_OF_COLUMNS = 10

class ProgSysGUI:
    def __init__(self) -> None:
        self._reg_file = RegFile()
        self._memory = Memory()

        # Create the main window
        self.tk_gui = tk.Tk()

        self.tk_gui.after(0, self._main_callback)

        bg_color = "#434344"
        fg_color = "#FFFFFF"

        self.tk_gui.title("Sistema de programação")
        self.tk_gui.configure(background=bg_color)
        self.tk_gui.geometry("940x480")
        self.tk_gui.resizable(width=False, height=False)
        center(self.tk_gui)

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

        for i in range(32):
            label = tk.Label(self.tk_gui,
                text=f'r{i}: 0x00000000',
                fg=fg_color,
                bg=bg_color,
                justify='left',
                font=("TkDefaultFont", 10, "normal")
            )
            label.grid(row= i % 8 + 2, column= i // 8, sticky="NSEW")
            label.after(10, lambda label=label, i=i: self._reg_update_callback(label, i))
        
        # Create indicators
        state_indicators_title_label = tk.Label(self.tk_gui,
            text='Indicadores',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 12, "bold")
        )
        state_indicators_title_label.grid(row=1, column=4, columnspan=2, sticky="NSEW")
        
        state_indicators_title_label = tk.Label(self.tk_gui,
            text='Estado da máquina:',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 10, "normal")
        )
        state_indicators_title_label.grid(row=3, column=4, columnspan=2, sticky="NSEW")
        
        state_indicator_label = tk.Label(self.tk_gui,
            text=Indicator().get_indicator_string(),
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 10, "normal")
        )
        state_indicator_label.grid(row=4, column=4, columnspan=2, sticky="NSEW")
        
        state_indicator_label.after(10, lambda label=state_indicator_label: self._indicator_update_callback(label))

        # Create memory
        self.mem_base_add = 0

        state_mem_title_label = tk.Label(self.tk_gui,
            text='Memória',
            fg=fg_color,
            bg=bg_color,
            justify='center',
            font=("TkDefaultFont", 12, "bold")
        )
        state_mem_title_label.grid(row=1, column=6, columnspan=4, sticky="NSEW")

        state_mem_add_button = tk.Button(self.tk_gui,
            text='\N{RIGHTWARDS BLACK ARROW}',
            command=self._mem_address_update_callback
        )
        state_mem_add_button.grid(row=2, column=9, padx=10, pady=10, sticky="W")
        
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

        self.mem_add_entry.insert(0, "000")

        for i in range(14):
            label = tk.Label(self.tk_gui,
                text=f'0x{i:03x}: 0x00000000',
                fg=fg_color,
                bg=bg_color,
                justify='left',
                font=("TkDefaultFont", 10, "normal")
            )
            label.grid(row= i % 7 + 3, column= 2* (i // 7) + 6, columnspan=2, sticky="NSEW")
            label.after(10, lambda label=label, i=i: self._mem_update_callback(label, i))

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
            command=self._create_file_callback
        )
        create_file_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        edit_file_button = tk.Button(self.tk_gui,
            text='Edit File',
            command=self._edit_file_callback
        )
        edit_file_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

        # Load and dump
        load_button = tk.Button(self.tk_gui,
            text='Loader',
            command=self._loader_callback
        )
        load_button.grid(row=11, column=2, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        dump_button = tk.Button(self.tk_gui,
            text='Dumper',
            command=self._dumper_callback
        )
        dump_button.grid(row=12, column=2, columnspan=2, padx=10, pady=10, sticky="NSEW")

        # Máquina virtual
        vm_add_label = tk.Label(self.tk_gui,
            text='Endereço da instrução:',
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

        self.vm_start_entry.insert(0, "000")

        vm_start_button = tk.Button(self.tk_gui,
            text='Iniciar',
            command=self._vm_start_callback
        )
        vm_start_button.grid(row=12, column=4, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        vm_stop_button = tk.Button(self.tk_gui,
            text='Parar',
            command=self._vm_stop_callback
        )
        vm_stop_button.grid(row=12, column=6, columnspan=2, padx=10, pady=10, sticky="NSEW")

        vm_ex_button = tk.Button(self.tk_gui,
            text='Executar',
            command=self._vm_ex_callback
        )
        vm_ex_button.grid(row=13, column=4, columnspan=2, padx=10, pady=10, sticky="NSEW")

        vm_step_button = tk.Button(self.tk_gui,
            text='Step',
            command=self._vm_step_callback
        )
        vm_step_button.grid(row=13, column=6, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        # Assembler
        abs_asm_button = tk.Button(self.tk_gui,
            text='Montador Absoluto',
            command=self._abs_asm_callback
        )
        abs_asm_button.grid(row=11, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        rel_asm_button = tk.Button(self.tk_gui,
            text='Montador Relativo',
            command=self._rel_asm_callback
        )
        rel_asm_button.grid(row=12, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")
        
        linker_button = tk.Button(self.tk_gui,
            text='Ligador Relocador',
            command=self._linker_callback
        )
        linker_button.grid(row=13, column=8, columnspan=2, padx=10, pady=10, sticky="NSEW")

    def start(self) -> None:
        self.tk_gui.mainloop()

    def stop(self) -> None:
        self.tk_gui.destroy()

    def _main_callback(self):
        EventController().run()
        self.tk_gui.after(10, self._main_callback)

    def _reg_update_callback(self, label, i):
        value = self._reg_file[i];
        label.configure(text=f'r{i:02}: 0x{value:08x}')
        label.after(10, lambda label=label, i=i: self._reg_update_callback(label, i))

    def _indicator_update_callback(self, label):
        label.configure(text=Indicator().get_indicator_string())
        label.after(10, lambda label=label: self._indicator_update_callback(label))

    def _mem_update_callback(self, label, i):
        address = self.mem_base_add + i
        value = self._memory[address];
        label.configure(text=f'0x{address:03x}: 0x{value:08x}')
        label.after(10, lambda label=label, i=i: self._mem_update_callback(label, i))

    def _mem_address_update_callback(self):
        try:
            self.mem_base_add = int(self.mem_add_entry.get(), base=16)
        except:
            pass

    def _create_file_callback(self):
        NotImplementedPopup()

    def _edit_file_callback(self):
        NotImplementedPopup()

    def _loader_callback(self):
        LoaderPopup()

    def _dumper_callback(self):
        DumperPopup()

    def _vm_start_callback(self):
        instruction_address = int(self.vm_start_entry.get(), base=16)
        start_event = Event(EventType.VM_START, instruction_address)
        EventController().add_event(start_event)

    def _vm_stop_callback(self):
        stop_event = Event(EventType.VM_FINISH, None)
        EventController().add_event(stop_event)

    def _vm_ex_callback(self):
        ex_event = Event(EventType.FETCH_DECODE_EXECUTE_CONTINUOSLY, None)
        EventController().add_event(ex_event)

    def _vm_step_callback(self):
        step_event = Event(EventType.FETCH_DECODE_EXECUTE_STEP, None)
        EventController().add_event(step_event)

    def _abs_asm_callback(self):
        NotImplementedPopup()

    def _rel_asm_callback(self):
        NotImplementedPopup()

    def _linker_callback(self):
        NotImplementedPopup()
    

class LoaderPopup():
    def __init__(self):
        self.gui = tk.Toplevel()

        bg_color = "#434344"
        fg_color = "#FFFFFF"

        self.gui.title("Loader")
        self.gui.configure(background=bg_color)
        self.gui.geometry("250x140")
        self.gui.resizable(width=False, height=False)
        center(self.gui)

        label = tk.Label(self.gui,
            text="Arquivo executável para\ncarregar (.bin)",
            fg=fg_color,
            bg=bg_color,
        )
        label.pack(fill='x', padx=10, pady=5)

        self.entry = tk.Entry(self.gui,
            width=5
        )
        self.entry.pack(fill='x', padx=10, pady=5)

        button = tk.Button(self.gui, text="Load", command=self._button_callback)
        button.pack(fill='x', padx=10, pady=10)

    def _button_callback(self):
        load_event = Event(EventType.LOADER_LOAD_DATA, "home/" + self.entry.get())
        EventController().add_event(load_event)
        self.gui.destroy()

class DumperPopup():
    def __init__(self):
        self.gui = tk.Toplevel()

        bg_color = "#434344"
        fg_color = "#FFFFFF"

        self.gui.title("Dumper")
        self.gui.configure(background=bg_color)
        self.gui.geometry("550x200")
        self.gui.resizable(width=False, height=False)
        center(self.gui)

        for i in range(4):
            self.gui.rowconfigure(i, weight=1)

        for i in range(2):
            self.gui.columnconfigure(i, weight=1)

        # File where to dumb
        label = tk.Label(self.gui,
            text="Arquivo onde salvar dados da memória (file.bin)",
            fg=fg_color,
            bg=bg_color,
        )
        label.grid(row=0, column=0, padx=10, pady=5, sticky="EW")

        self.file_entry = tk.Entry(self.gui,
            width=20
        )
        self.file_entry.grid(row=0, column=1, padx=10, pady=5, sticky="EW")

        # Start address
        label = tk.Label(self.gui,
            text="Endereço inicial da memória (hexadecimal)",
            fg=fg_color,
            bg=bg_color,
        )
        label.grid(row=1, column=0, padx=10, pady=5, sticky="EW")

        self.address_entry = tk.Entry(self.gui,
            width=20
        )
        self.address_entry.grid(row=1, column=1, padx=10, pady=5, sticky="EW")

        # Number of words to dump
        label = tk.Label(self.gui,
            text="Número de palavras (decimal)",
            fg=fg_color,
            bg=bg_color,
        )
        label.grid(row=2, column=0, padx=10, pady=5, sticky="EW")

        self.size_entry = tk.Entry(self.gui,
            width=20
        )
        self.size_entry.grid(row=2, column=1, padx=10, pady=5, sticky="EW")

        button = tk.Button(self.gui, text="Dump", command=self._button_callback)
        button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="EW")

    def _button_callback(self):
        data = {}
        data['file'] = "home/" + self.file_entry.get()
        data['start_address'] = int(self.address_entry.get(), base=16)
        data['size'] = int(self.size_entry.get())
        load_event = Event(EventType.DUMPER_LOAD_DATA, data)
        EventController().add_event(load_event)
        self.gui.destroy()

class NotImplementedPopup():
    def __init__(self):
        self.gui = tk.Toplevel()

        bg_color = "#434344"
        fg_color = "#FFFFFF"

        self.gui.title("Erro")
        self.gui.configure(background=bg_color)
        self.gui.geometry("250x100")
        self.gui.resizable(width=False, height=False)
        center(self.gui)

        label = tk.Label(self.gui,
            text="Esse recurso ainda não\nfoi implementado :(",
            fg=fg_color,
            bg=bg_color,
        )
        label.pack(fill='x', padx=10, pady=5)

        button = tk.Button(self.gui, text="Fechar", command=self.gui.destroy)
        button.pack(fill='x', padx=10, pady=10)


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
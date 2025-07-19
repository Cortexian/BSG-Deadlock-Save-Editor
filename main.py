import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import sys
import darkdetect
from game_data import SHIP_TYPES, FLEET_NAME_LIMIT, SHIP_NAME_LIMIT
import parse_save
import mod

# --- Helper for bundled executables ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Configuration and Theme Constants ---
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APP_DIR, "config.json")

LIGHT_THEME = {
    "bg": "#f0f0f0", "fg": "#000000", "bg_widget": "#ffffff",
    "fg_select": "#ffffff", "bg_select": "#0078d7"
}
DARK_THEME = {
    "bg": "#2e2e2e", "fg": "#ffffff", "bg_widget": "#3c3c3c",
    "fg_select": "#ffffff", "bg_select": "#0078d7"
}


class BSGSaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("BSG Deadlock Save Editor")
        self.root.geometry("950x650")

        try:
            icon_path = resource_path("editor.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            print("Could not load editor.ico.")

        self.save_data = None
        self.save_file_path = None
        self.player_fleets = []
        self.selected_fleet_index = None
        self.selected_ship_indices = ()

        self.ship_name_to_id = SHIP_TYPES.copy()
        self.id_to_ship_name = {v: k for k, v in SHIP_TYPES.items()}
        
        self.theme_var = tk.StringVar(value="System")
        self._load_config()

        self.setup_menu()
        self.setup_ui()
        self._update_widget_states()
        self._change_theme(initial_load=True)

        self.root.bind("<Control-o>", self.load_save_file)
        self.root.bind("<Control-s>", self.save_save_file)
        self.root.bind("<Control-S>", self.save_save_file_as)

    # --- Theme and Config Methods ---
    def _load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.theme_var.set(config.get("theme", "System"))
        except (IOError, json.JSONDecodeError) as e:
            print(f"Could not load config file: {e}")
            self.theme_var.set("System")

    def _save_config(self):
        config = {"theme": self.theme_var.get()}
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            print(f"Could not save config file: {e}")

    def _apply_theme(self, theme_palette):
        bg = theme_palette["bg"]
        fg = theme_palette["fg"]
        bg_widget = theme_palette["bg_widget"]
        bg_select = theme_palette["bg_select"]
        fg_select = theme_palette["fg_select"]
        self.root.config(bg=bg)
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('.', background=bg, foreground=fg, fieldbackground=bg_widget, borderwidth=1)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=bg_widget, foreground=fg)
        style.map('TButton', background=[('active', bg_select), ('pressed', bg_select)])
        style.configure('TEntry', fieldbackground=bg_widget, foreground=fg, insertcolor=fg)
        style.configure('TCombobox', fieldbackground=bg_widget, foreground=fg)
        style.configure('TLabelFrame', background=bg, foreground=fg)
        style.configure('TLabelFrame.Label', background=bg, foreground=fg)
        listbox_config = {"background": bg_widget, "foreground": fg, "selectbackground": bg_select, "selectforeground": fg_select}
        self.fleet_listbox.config(**listbox_config)
        self.ship_listbox.config(**listbox_config)
        for frame in [self.left_frame, self.middle_frame, self.right_frame]:
            frame.config(style='TFrame')

    def _change_theme(self, initial_load=False):
        selected_theme = self.theme_var.get()
        final_theme = "Dark"
        if selected_theme == "System":
            final_theme = darkdetect.theme() or "Light"
        else:
            final_theme = selected_theme
        if final_theme == "Dark":
            self._apply_theme(DARK_THEME)
        else:
            self._apply_theme(LIGHT_THEME)
        if not initial_load:
            self._save_config()

    # --- File Operations ---
    def load_save_file(self, event=None, file_path=None):
        if event is not None: file_path = None
        if not file_path:
            file_path = filedialog.askopenfilename(filetypes=[("BSG Save Files", "*.bsgsave"), ("All files", "*.*")])
        if not file_path: return
        data = parse_save.load_and_parse_file(file_path)
        if data:
            self.save_data = data
            self.save_file_path = file_path
            self.filepath_label.config(text=file_path)
            self.set_status("File loaded successfully.")
            parse_save.populate_fleets_ui(self)
            parse_save.populate_resources_ui(self)
        else:
            self.set_status("Error loading file.")
        self._update_widget_states()

    def save_save_file(self, event=None):
        mod.save_data_to_file(self, save_as=False)

    def save_save_file_as(self, event=None):
        mod.save_data_to_file(self, save_as=True)

    # --- Data Modification Wrappers ---
    def add_ship(self):
        mod.add_ship_to_fleet(self)

    def remove_ship(self):
        mod.remove_selected_ships(self)

    # --- UI Setup and Event Handlers ---
    def setup_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.load_save_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu = tk.Menu(view_menu, tearoff=0)
        theme_menu.add_radiobutton(label="System", variable=self.theme_var, value="System", command=self._change_theme)
        theme_menu.add_radiobutton(label="Light", variable=self.theme_var, value="Light", command=self._change_theme)
        theme_menu.add_radiobutton(label="Dark", variable=self.theme_var, value="Dark", command=self._change_theme)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        menu_bar.add_cascade(label="View", menu=view_menu)
        self.root.config(menu=menu_bar)

    def setup_ui(self):
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=0); self.root.columnconfigure(1, weight=0); self.root.columnconfigure(2, weight=1)
        self.left_frame = ttk.Frame(self.root, width=230)
        self.middle_frame = ttk.Frame(self.root, width=250)
        self.right_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="ns", padx=(5,0), pady=5)
        self.middle_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=(0,5), pady=5)
        self.left_frame.grid_propagate(False); self.middle_frame.grid_propagate(False)
        self.left_frame.rowconfigure(1, weight=1); self.left_frame.columnconfigure(0, weight=1)
        ttk.Label(self.left_frame, text="Fleets", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5)
        self.fleet_listbox = tk.Listbox(self.left_frame, exportselection=0, borderwidth=0, highlightthickness=0)
        self.fleet_listbox.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.fleet_listbox.bind("<<ListboxSelect>>", self.on_fleet_select)
        self.fleet_listbox.bind("<Double-Button-1>", self.rename_fleet_popup)
        self.modify_fleet_button = ttk.Button(self.left_frame, text="Rename Fleet", command=self.rename_fleet_popup)
        self.modify_fleet_button.grid(row=2, column=0, sticky="ew", padx=5, pady=(2,5))
        self.middle_frame.rowconfigure(1, weight=1); self.middle_frame.columnconfigure(0, weight=1); self.middle_frame.columnconfigure(1, weight=1)
        ttk.Label(self.middle_frame, text="Ships in Selected Fleet", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        self.ship_listbox = tk.Listbox(self.middle_frame, exportselection=0, borderwidth=0, highlightthickness=0, selectmode=tk.EXTENDED)
        self.ship_listbox.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.ship_listbox.bind("<<ListboxSelect>>", self.on_ship_select)
        self.ship_listbox.bind("<Double-Button-1>", self.modify_ship_popup)
        self.modify_ship_button = ttk.Button(self.middle_frame, text="Modify Ship", command=self.modify_ship_popup)
        self.modify_ship_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=(2,5))
        self.add_ship_button = ttk.Button(self.middle_frame, text="Add Ship", command=self.add_ship)
        self.add_ship_button.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        self.remove_ship_button = ttk.Button(self.middle_frame, text="Remove Ship", command=self.remove_ship)
        self.remove_ship_button.grid(row=3, column=1, sticky="ew", padx=5, pady=2)
        self.right_frame.columnconfigure(0, weight=1)
        ttk.Label(self.right_frame, text="Resources & Unlocks", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=5)
        resource_frame = ttk.LabelFrame(self.right_frame, text="Player Resources")
        resource_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        resource_frame.columnconfigure(1, weight=1)
        ttk.Label(resource_frame, text="Tylium:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.tylium_entry = ttk.Entry(resource_frame)
        self.tylium_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Label(resource_frame, text="Requisition:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.requisition_entry = ttk.Entry(resource_frame)
        self.requisition_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.status_label = ttk.Label(status_frame, text="Welcome. Open a .bsgsave file to begin.", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        self.filepath_label = ttk.Label(status_frame, text="", anchor="e")
        self.filepath_label.pack(side=tk.RIGHT, padx=5, pady=2)

    def set_status(self, message):
        self.status_label.config(text=message)

    def _update_widget_states(self):
        file_loaded = self.save_data is not None
        fleet_selected = self.selected_fleet_index is not None
        num_ships_selected = len(self.selected_ship_indices)
        self.modify_fleet_button.config(state=tk.NORMAL if fleet_selected else tk.DISABLED)
        if num_ships_selected > 1:
            self.add_ship_button.config(state=tk.DISABLED)
            self.remove_ship_button.config(state=tk.NORMAL, text="Remove Ships")
            self.modify_ship_button.config(state=tk.NORMAL, text="Modify Ships")
        elif num_ships_selected == 1:
            self.add_ship_button.config(state=tk.NORMAL if fleet_selected else tk.DISABLED)
            self.remove_ship_button.config(state=tk.NORMAL, text="Remove Ship")
            self.modify_ship_button.config(state=tk.NORMAL, text="Modify Ship")
        else:
            self.add_ship_button.config(state=tk.NORMAL if fleet_selected else tk.DISABLED)
            self.remove_ship_button.config(state=tk.DISABLED, text="Remove Ship")
            self.modify_ship_button.config(state=tk.DISABLED, text="Modify Ship")
        self.tylium_entry.config(state=tk.NORMAL if file_loaded else tk.DISABLED)
        self.requisition_entry.config(state=tk.NORMAL if file_loaded else tk.DISABLED)

    def on_fleet_select(self, event=None):
        selection = self.fleet_listbox.curselection()
        if not selection: return
        self.selected_fleet_index = selection[0]
        parse_save.populate_ships_ui(self)
        self._update_widget_states()

    def on_ship_select(self, event=None):
        self.selected_ship_indices = self.ship_listbox.curselection()
        self._update_widget_states()

    def rename_fleet_popup(self, event=None):
        if self.selected_fleet_index is None: return
        fleet = self.player_fleets[self.selected_fleet_index]
        new_name = self.create_input_popup("Rename Fleet", "New Fleet Name:", fleet.get("Name", ""), char_limit=FLEET_NAME_LIMIT)
        if new_name is not None:
            fleet["Name"] = new_name
            current_selection = self.selected_fleet_index
            parse_save.populate_fleets_ui(self)
            self.fleet_listbox.selection_set(current_selection)
            self.on_fleet_select()

    def _validate_char_limit(self, P, limit):
        return len(P) <= int(limit)

    def modify_ship_popup(self, event=None):
        if not self.selected_ship_indices: return
        if len(self.selected_ship_indices) > 1:
            self.modify_multiple_ships_popup()
        else:
            ship = self.player_fleets[self.selected_fleet_index]["FleetShips"][self.selected_ship_indices[0]]
            top = tk.Toplevel(self.root)
            self._configure_popup(top, "Modify Ship")
            ttk.Label(top, text="Ship Name:").pack(padx=10, pady=(10, 0))
            vcmd = (self.root.register(self._validate_char_limit), '%P', SHIP_NAME_LIMIT)
            name_entry = ttk.Entry(top, width=40, validate='key', validatecommand=vcmd)
            name_entry.insert(0, ship.get("Name", "").strip())
            name_entry.pack(padx=10, pady=5, fill=tk.X)
            ttk.Label(top, text="Ship Class:").pack(padx=10)
            type_var = tk.StringVar()
            ship_class_names = sorted(list(SHIP_TYPES.keys()))
            dropdown = ttk.Combobox(top, textvariable=type_var, values=ship_class_names, state="readonly")
            current_class_name = self.id_to_ship_name.get(ship.get('ShipType'), "")
            if current_class_name: dropdown.set(current_class_name)
            dropdown.pack(padx=10, pady=5, fill=tk.X)
            def apply_changes():
                ship["Name"] = name_entry.get().strip()
                selected_class_name = type_var.get()
                if selected_class_name in self.ship_name_to_id: ship["ShipType"] = self.ship_name_to_id[selected_class_name]
                current_selection = self.selected_ship_indices[0]
                parse_save.populate_ships_ui(self)
                self.ship_listbox.selection_set(current_selection)
                top.destroy()
            ttk.Button(top, text="Apply", command=apply_changes).pack(pady=10)
            self.center_window(top)

    def modify_multiple_ships_popup(self):
        top = tk.Toplevel(self.root)
        self._configure_popup(top, f"Modify {len(self.selected_ship_indices)} Ships")
        ttk.Label(top, text="Set Ship Class for all selected ships:").pack(padx=10, pady=(10, 0))
        type_var = tk.StringVar()
        ship_class_names = sorted(list(SHIP_TYPES.keys()))
        dropdown = ttk.Combobox(top, textvariable=type_var, values=ship_class_names, state="readonly")
        dropdown.pack(padx=10, pady=5, fill=tk.X)
        def apply_changes():
            selected_class_name = type_var.get()
            if not selected_class_name:
                messagebox.showwarning("No Selection", "Please select a ship class to apply.")
                return
            if selected_class_name in self.ship_name_to_id:
                new_ship_type = self.ship_name_to_id[selected_class_name]
                ships = self.player_fleets[self.selected_fleet_index]["FleetShips"]
                for index in self.selected_ship_indices:
                    ships[index]["ShipType"] = new_ship_type
                parse_save.populate_ships_ui(self)
                for index in self.selected_ship_indices:
                    self.ship_listbox.selection_set(index)
            top.destroy()
        ttk.Button(top, text="Apply", command=apply_changes).pack(pady=10)
        self.center_window(top)

    def _configure_popup(self, popup, title):
        """Applies standard configuration to a Toplevel popup window."""
        popup.title(title)
        popup.transient(self.root)
        popup.grab_set()
        try:
            icon_path = resource_path("editor.ico")
            popup.iconbitmap(icon_path)
        except Exception:
            pass # Fail silently if icon is missing
        palette = DARK_THEME if darkdetect.theme() == "Dark" else LIGHT_THEME
        if self.theme_var.get() == "Light": palette = LIGHT_THEME
        if self.theme_var.get() == "Dark": palette = DARK_THEME
        popup.config(bg=palette["bg"])

    def create_input_popup(self, title, prompt, initial_value, char_limit=None):
        result = [None]
        top = tk.Toplevel(self.root)
        self._configure_popup(top, title)
        ttk.Label(top, text=prompt).pack(padx=10, pady=(10, 0))
        if char_limit:
            vcmd = (self.root.register(self._validate_char_limit), '%P', char_limit)
            entry = ttk.Entry(top, width=40, validate='key', validatecommand=vcmd)
        else:
            entry = ttk.Entry(top, width=40)
        entry.insert(0, initial_value.strip())
        entry.pack(padx=10, pady=5, fill=tk.X); entry.focus_set()
        def on_ok(event=None): result[0] = entry.get().strip(); top.destroy()
        def on_cancel(): result[0] = None; top.destroy()
        entry.bind("<Return>", on_ok)
        button_frame = ttk.Frame(top)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
        top.protocol("WM_DELETE_WINDOW", on_cancel)
        self.center_window(top)
        self.root.wait_window(top)
        return result[0]

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width(); height = window.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        window.geometry(f'+{x}+{y}')

    def prompt_for_auto_load(self):
        save_files = parse_save.find_save_files()
        if not save_files: return
        top = tk.Toplevel(self.root)
        self._configure_popup(top, "Located Save Files")
        ttk.Label(top, text="Save files automatically located.").pack(padx=10, pady=(10, 5))
        list_frame = ttk.Frame(top)
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        listbox = tk.Listbox(list_frame, exportselection=0, width=110, height=15)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)
        for file in save_files: listbox.insert(tk.END, file)
        ttk.Label(top, text="Files named 'campaign1-3' correspond with the in-game save slots.", justify=tk.LEFT).pack(padx=10, pady=5, anchor='w')
        ttk.Label(top, text="Select a file to load, or click 'Cancel'.", justify=tk.LEFT).pack(padx=10, pady=5, anchor='w')
        button_frame = ttk.Frame(top)
        button_frame.pack(pady=10)
        load_button = ttk.Button(button_frame, text="Load", state=tk.DISABLED)
        load_button.pack(side=tk.LEFT, padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=top.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
        def on_select(event=None):
            if listbox.curselection(): load_button.config(state=tk.NORMAL)
            else: load_button.config(state=tk.DISABLED)
        listbox.bind("<<ListboxSelect>>", on_select)
        def on_load():
            selection_index = listbox.curselection()
            if selection_index:
                selected_file = listbox.get(selection_index[0])
                self.load_save_file(file_path=selected_file)
            top.destroy()
        load_button.config(command=on_load)
        listbox.bind("<Double-Button-1>", lambda e: on_load())
        top.protocol("WM_DELETE_WINDOW", top.destroy)
        self.center_window(top)
        self.root.wait_visibility()
        self.root.wait_window(top)

if __name__ == "__main__":
    root = tk.Tk()
    app = BSGSaveEditor(root)
    app.prompt_for_auto_load()
    root.mainloop()
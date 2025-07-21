import json
import os
import tkinter as tk
from tkinter import messagebox
from game_data import SHIP_TYPES
import ctypes
from ctypes import wintypes

def _get_documents_path():
    """
    Finds the user's Documents folder on Windows, even if relocated.
    Returns None if not on Windows or if the path cannot be found.
    """
    if os.name != 'nt':
        return None
    
    CSIDL_PERSONAL = 5       # My Documents
    SHGFP_TYPE_CURRENT = 0   # Get current, not default value
    
    buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    
    return buf.value

def find_save_files():
    """Scans known Steam and GOG directories for save files."""
    found_files = set()
    save_filename = ".bsgsave"
    
    # Use a set to automatically handle duplicate paths
    search_paths = set()
    
    # --- GOG Paths ---
    # Add the default hardcoded path
    default_gog_path = os.path.expanduser("~/Documents/Black Lab Games/BSG")
    if os.path.isdir(default_gog_path):
        search_paths.add(default_gog_path)
    
    # Add the relocated Documents path if on Windows
    relocated_docs_path = _get_documents_path()
    if relocated_docs_path:
        relocated_gog_path = os.path.join(relocated_docs_path, "Black Lab Games", "BSG")
        if os.path.isdir(relocated_gog_path):
            search_paths.add(relocated_gog_path)
            
    # --- Steam Path ---
    steam_base = "C:\\Program Files (x86)\\Steam\\userdata"
    if os.name == 'nt' and os.path.isdir(steam_base):
        try:
            for user_id in os.listdir(steam_base):
                steam_path = os.path.join(steam_base, user_id, "544610", "remote")
                if os.path.isdir(steam_path):
                    search_paths.add(steam_path)
        except OSError:
            pass # Ignore permission errors etc.

    # --- Search for files ---
    for path in search_paths:
        for root_dir, _, files in os.walk(path):
            for file in files:
                if file.endswith(save_filename) and file != "campaign0.bsgsave":
                    found_files.add(os.path.join(root_dir, file))
    
    return sorted(list(found_files))

def load_and_parse_file(file_path):
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load or parse file: {e}")
        return None

def populate_fleets_ui(app):
    app.fleet_listbox.delete(0, tk.END)
    app.ship_listbox.delete(0, tk.END)
    app.selected_fleet_index = None
    app.player_fleets = []
    if not app.save_data: return
    for entry in app.save_data.get("FactionFleetGroups", []):
        if entry.get("Faction") == 0:
            app.player_fleets = entry.get("FleetGroups", [])
            break
    for i, fleet in enumerate(app.player_fleets):
        name = fleet.get("Name", f"Unnamed Fleet {i+1}").strip()
        num_ships = len(fleet.get("FleetShips", []))
        app.fleet_listbox.insert(tk.END, f"{name} [{num_ships} ships]")
    app._update_widget_states()

def populate_ships_ui(app):
    """Populates the ship listbox, sorting the flagship to the top."""
    app.ship_listbox.delete(0, tk.END)
    app.selected_ship_indices = ()
    if app.selected_fleet_index is None:
        app._update_widget_states()
        return
        
    fleet_data = app.player_fleets[app.selected_fleet_index]
    ships = fleet_data.get("FleetShips", [])
    
    ships.sort(key=lambda s: s.get("PlayerAssignedFlagship", False), reverse=True)
    
    for ship in ships:
        name = ship.get("Name", "Unnamed Ship").strip()
        ship_type_id = ship.get("ShipType", -1)
        class_name = app.id_to_ship_name.get(ship_type_id, "Unknown Type")
        display_class = f"{class_name} Class" if class_name != "Unknown Type" else class_name
        
        display_text = f"{name} ({ship_type_id} - {display_class})"
        
        if ship.get("PlayerAssignedFlagship", False):
            display_text += " (Flagship)"
            
        app.ship_listbox.insert(tk.END, display_text)

    app._update_widget_states()

def populate_resources_ui(app):
    if not app.save_data: return
    app.tylium_entry.delete(0, tk.END); app.tylium_entry.insert(0, app.save_data.get("Tylium", 0))
    app.requisition_entry.delete(0, tk.END); app.requisition_entry.insert(0, app.save_data.get("RequisitionPoints", 0))

def populate_ship_unlocks_ui(app):
    if not app.save_data: return
    for var in app.unlocked_ship_vars.values(): var.set(False)
    unlocked_ids = app.save_data.get("UnlockedShips", [])
    for ship_id in unlocked_ids:
        if ship_id in app.unlocked_ship_vars:
            app.unlocked_ship_vars[ship_id].set(True)

def populate_munition_unlocks_ui(app):
    if not app.save_data: return
    for var in app.unlocked_munition_vars.values(): var.set(False)
    unlocked_ids = app.save_data.get("UnlockedMissiles", [])
    for munition_id in unlocked_ids:
        if munition_id in app.unlocked_munition_vars:
            app.unlocked_munition_vars[munition_id].set(True)

def populate_squadron_unlocks_ui(app):
    if not app.save_data: return
    for var in app.unlocked_squadron_vars.values():
        var.set(False)
    unlocked_ids = app.save_data.get("UnlockedSquadrons", [])
    for squadron_id in unlocked_ids:
        if squadron_id in app.unlocked_squadron_vars:
            app.unlocked_squadron_vars[squadron_id].set(True)
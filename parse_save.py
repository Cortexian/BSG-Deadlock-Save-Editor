# parse_save.py
import json
import os
import tkinter as tk
from tkinter import messagebox
from game_data import SHIP_TYPES
# FIX: Import ctypes for a dependency-free way to find the Documents folder
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
    
    search_paths = []
    
    # --- GOG Path ---
    # FIX: Use the new helper function to find the true Documents location
    docs_path = _get_documents_path()
    if docs_path:
        gog_path = os.path.join(docs_path, "Black Lab Games", "BSG")
        if os.path.isdir(gog_path):
            search_paths.append(gog_path)
    else:
        # Fallback method for non-Windows systems
        gog_path_fallback = os.path.expanduser("~/Documents/Black Lab Games/BSG")
        if os.path.isdir(gog_path_fallback):
            search_paths.append(gog_path_fallback)
            
    # --- Steam Path ---
    steam_base = "C:\\Program Files (x86)\\Steam\\userdata"
    if os.name == 'nt' and os.path.isdir(steam_base):
        try:
            for user_id in os.listdir(steam_base):
                steam_path = os.path.join(steam_base, user_id, "544610", "remote")
                if os.path.isdir(steam_path):
                    search_paths.append(steam_path)
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
    app.ship_listbox.delete(0, tk.END)
    app.selected_ship_indices = ()
    if app.selected_fleet_index is None:
        app._update_widget_states()
        return
    fleet = app.player_fleets[app.selected_fleet_index]
    for ship in fleet.get("FleetShips", []):
        name = ship.get("Name", "Unnamed Ship").strip()
        ship_type_id = ship.get("ShipType", -1)
        class_name = app.id_to_ship_name.get(ship_type_id, "Unknown Type")
        display_class = f"{class_name} Class" if class_name != "Unknown Type" else class_name
        app.ship_listbox.insert(tk.END, f"{name} ({ship_type_id} - {display_class})")
    app._update_widget_states()

def populate_resources_ui(app):
    if not app.save_data: return
    app.tylium_entry.delete(0, tk.END)
    app.tylium_entry.insert(0, app.save_data.get("Tylium", 0))
    app.requisition_entry.delete(0, tk.END)
    app.requisition_entry.insert(0, app.save_data.get("RequisitionPoints", 0))

def populate_ship_unlocks_ui(app):
    if not app.save_data: return
    for var in app.unlocked_ship_vars.values():
        var.set(False)
    unlocked_ids = app.save_data.get("UnlockedShips", [])
    for ship_id in unlocked_ids:
        if ship_id in app.unlocked_ship_vars:
            app.unlocked_ship_vars[ship_id].set(True)

def populate_munition_unlocks_ui(app):
    if not app.save_data: return
    for var in app.unlocked_munition_vars.values():
        var.set(False)
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
<<<<<<< HEAD
# mod.py
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from game_data import MAX_RESOURCE_VALUE

# ... (NEW_SHIP_TEMPLATE, _get_next_id, add_ship_to_fleet, remove_selected_ships remain the same) ...
NEW_SHIP_TEMPLATE = { "ShipType": 6, "Name": "Thalassa\r", "ShipPosition": { "x": 0.0, "y": 0.0, "z": 0.0 }, "FTLCooldownTimer": 100, "ShipId": 9, "CanBeRenamed": True, "PreventTransferring": False, "AlwaysFlagship": False, "PlayerAssignedFlagship": True, "ActiveMunitions": [0], "ActiveSquadrons": [], "SquadronGroupNumbers": [], "StockData": { "Munitions": [{"MissileType": 0, "MaxMissiles": 40, "MissilesRemaining": 40}, {"MissileType": 2, "MaxMissiles": 100, "MissilesRemaining": 0}, {"MissileType": 9, "MaxMissiles": 12, "MissilesRemaining": 0}, {"MissileType": 7, "MaxMissiles": 1, "MissilesRemaining": 0}, {"MissileType": 4, "MaxMissiles": 42, "MissilesRemaining": 0}, {"MissileType": 12, "MaxMissiles": 4, "MissilesRemaining": 0}, {"MissileType": 13, "MaxMissiles": 10, "MissilesRemaining": 0}, {"MissileType": 16, "MaxMissiles": 6, "MissilesRemaining": 0}, {"MissileType": 20, "MaxMissiles": 36, "MissilesRemaining": 0}, {"MissileType": 21, "MaxMissiles": 6, "MissilesRemaining": 0}, {"MissileType": 22, "MaxMissiles": 1, "MissilesRemaining": 0}], "Squadrons": [{"SquadronType": 0, "MaxFighters": 10, "FightersRemaining": 0}, {"SquadronType": 1, "MaxFighters": 8, "FightersRemaining": 0}, {"SquadronType": 2, "MaxFighters": 2, "FightersRemaining": 0}, {"SquadronType": 3, "MaxFighters": 2, "FightersRemaining": 0}, {"SquadronType": 104, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 106, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 111, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 4, "MaxFighters": 3, "FightersRemaining": 0}, {"SquadronType": 108, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 109, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 5, "MaxFighters": 4, "FightersRemaining": 0}, {"SquadronType": 112, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 113, "MaxFighters": 10, "FightersRemaining": 0}], "PlatingAvailable": 0, "UnlimitedMode": False }, "HullDamage": 0.0, "ArmorDamageList": None, "DamageDecalList": None, "MunitionStockCounts": None, "SquadronHullHealths": None, "Survivors": 0, "IsSurvivalShip": False, "Stats": None, "AttachedCharacters": None, "CrewVeterancyXP": 0, "CylonVeterancyRank": 0, "RelayOrdersAvailable": 0, "JoinGhostFleet": False }

def _get_next_id(key_name, data_source):
    max_id = 0
    for item in data_source: max_id = max(max_id, item.get(key_name, 0))
    return max_id + 1

def add_ship_to_fleet(app):
    if app.selected_fleet_index is None: return
    selected_fleet = app.player_fleets[app.selected_fleet_index]
    if len(selected_fleet.get("FleetShips", [])) >= 16:
        messagebox.showinfo("Fleet Full", "A fleet cannot have more than 16 ships."); return
    all_ships_globally = [ship for faction in app.save_data.get("FactionFleetGroups", []) for fleet in faction.get("FleetGroups", []) for ship in fleet.get("FleetShips", [])]
    next_ship_id = _get_next_id("ShipId", all_ships_globally)
    new_ship = NEW_SHIP_TEMPLATE.copy()
    new_ship["Name"] = f"New Manticore {next_ship_id}"; new_ship["ShipId"] = next_ship_id
    selected_fleet["FleetShips"].append(new_ship)
    from parse_save import populate_ships_ui, populate_fleets_ui
    current_fleet_selection = app.selected_fleet_index
    populate_fleets_ui(app)
    app.selected_fleet_index = current_fleet_selection
    app.fleet_listbox.selection_set(current_fleet_selection)
    populate_ships_ui(app)
    app.ship_listbox.selection_set(tk.END); app.on_ship_select()
    app.set_status("Added a new Manticore corvette.")

def remove_selected_ships(app):
    if not app.selected_ship_indices: return
    num_selected = len(app.selected_ship_indices)
    plural = "s" if num_selected > 1 else ""
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {num_selected} ship{plural}?"):
        ships = app.player_fleets[app.selected_fleet_index].get("FleetShips", [])
        for index in sorted(app.selected_ship_indices, reverse=True): del ships[index]
        from parse_save import populate_ships_ui, populate_fleets_ui
        current_fleet_selection = app.selected_fleet_index
        populate_fleets_ui(app)
        app.selected_fleet_index = current_fleet_selection
        app.fleet_listbox.selection_set(current_fleet_selection)
        populate_ships_ui(app)
        app.set_status(f"Removed {num_selected} ship{plural}.")

def update_ship_unlocks_in_data(app):
    """Builds a new 'UnlockedShips' list from the checkbox states."""
    if not app.save_data: return
    new_unlocked_ids = []
    for ship_id, var in app.unlocked_ship_vars.items():
        if var.get(): new_unlocked_ids.append(ship_id)
    app.save_data["UnlockedShips"] = new_unlocked_ids

def update_munition_unlocks_in_data(app):
    """Builds a new 'UnlockedMissiles' list from the checkbox states."""
    if not app.save_data: return
    new_unlocked_ids = []
    for munition_id, var in app.unlocked_munition_vars.items():
        if var.get(): new_unlocked_ids.append(munition_id)
    app.save_data["UnlockedMissiles"] = new_unlocked_ids

def update_squadron_unlocks_in_data(app):
    """Builds a new 'UnlockedSquadrons' list from the checkbox states."""
    if not app.save_data: return
    new_unlocked_ids = []
    for squadron_id, var in app.unlocked_squadron_vars.items():
        if var.get(): new_unlocked_ids.append(squadron_id)
    app.save_data["UnlockedSquadrons"] = new_unlocked_ids

def update_resources_in_data(app):
    try:
        if app.save_data:
            tylium = int(app.tylium_entry.get())
            if tylium > MAX_RESOURCE_VALUE: tylium = MAX_RESOURCE_VALUE
            app.save_data["Tylium"] = tylium
            app.tylium_entry.delete(0, tk.END); app.tylium_entry.insert(0, tylium)
            req_points = int(app.requisition_entry.get())
            if req_points > MAX_RESOURCE_VALUE: req_points = MAX_RESOURCE_VALUE
            app.save_data["RequisitionPoints"] = req_points
            app.requisition_entry.delete(0, tk.END); app.requisition_entry.insert(0, req_points)
            return True
        return False
    except (ValueError, TypeError):
        messagebox.showerror("Invalid Input", "Tylium and Requisition must be whole numbers.")
        from parse_save import populate_resources_ui
        populate_resources_ui(app)
        return False

def save_data_to_file(app, save_as=False):
    if not app.save_data:
        messagebox.showwarning("Warning", "No data to save."); return
    
    update_resources_in_data(app)
    update_ship_unlocks_in_data(app)
    update_munition_unlocks_in_data(app)
    update_squadron_unlocks_in_data(app)

    file_path = app.save_file_path
    if save_as or not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".bsgsave", filetypes=[("BSG Save Files", "*.bsgsave")])
        if not file_path: return 
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(app.save_data, f, indent=4)
        app.save_file_path = file_path
        app.filepath_label.config(text=file_path)
        app.set_status(f"File saved to {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")
=======
# mod.py
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from game_data import MAX_RESOURCE_VALUE

NEW_SHIP_TEMPLATE = {
    "ShipType": 6, "Name": "Thalassa\r", "ShipPosition": { "x": 0.0, "y": 0.0, "z": 0.0 },
    "FTLCooldownTimer": 100, "ShipId": 9, "CanBeRenamed": True, "PreventTransferring": False,
    "AlwaysFlagship": False, "PlayerAssignedFlagship": True, "ActiveMunitions": [0],
    "ActiveSquadrons": [], "SquadronGroupNumbers": [],
    "StockData": {
        "Munitions": [{"MissileType": 0, "MaxMissiles": 40, "MissilesRemaining": 40}, {"MissileType": 2, "MaxMissiles": 100, "MissilesRemaining": 0}, {"MissileType": 9, "MaxMissiles": 12, "MissilesRemaining": 0}, {"MissileType": 7, "MaxMissiles": 1, "MissilesRemaining": 0}, {"MissileType": 4, "MaxMissiles": 42, "MissilesRemaining": 0}, {"MissileType": 12, "MaxMissiles": 4, "MissilesRemaining": 0}, {"MissileType": 13, "MaxMissiles": 10, "MissilesRemaining": 0}, {"MissileType": 16, "MaxMissiles": 6, "MissilesRemaining": 0}, {"MissileType": 20, "MaxMissiles": 36, "MissilesRemaining": 0}, {"MissileType": 21, "MaxMissiles": 6, "MissilesRemaining": 0}, {"MissileType": 22, "MaxMissiles": 1, "MissilesRemaining": 0}],
        "Squadrons": [{"SquadronType": 0, "MaxFighters": 10, "FightersRemaining": 0}, {"SquadronType": 1, "MaxFighters": 8, "FightersRemaining": 0}, {"SquadronType": 2, "MaxFighters": 2, "FightersRemaining": 0}, {"SquadronType": 3, "MaxFighters": 2, "FightersRemaining": 0}, {"SquadronType": 104, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 106, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 111, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 4, "MaxFighters": 3, "FightersRemaining": 0}, {"SquadronType": 108, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 109, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 5, "MaxFighters": 4, "FightersRemaining": 0}, {"SquadronType": 112, "MaxFighters": 1, "FightersRemaining": 0}, {"SquadronType": 113, "MaxFighters": 10, "FightersRemaining": 0}],
        "PlatingAvailable": 0, "UnlimitedMode": False
    },
    "HullDamage": 0.0, "ArmorDamageList": None, "DamageDecalList": None, "MunitionStockCounts": None,
    "SquadronHullHealths": None, "Survivors": 0, "IsSurvivalShip": False, "Stats": None,
    "AttachedCharacters": None, "CrewVeterancyXP": 0, "CylonVeterancyRank": 0,
    "RelayOrdersAvailable": 0, "JoinGhostFleet": False
}

def _get_next_id(key_name, data_source):
    max_id = 0
    for item in data_source:
        max_id = max(max_id, item.get(key_name, 0))
    return max_id + 1

def add_ship_to_fleet(app):
    if app.selected_fleet_index is None: return
    selected_fleet = app.player_fleets[app.selected_fleet_index]
    if len(selected_fleet.get("FleetShips", [])) >= 16:
        messagebox.showinfo("Fleet Full", "A fleet cannot have more than 16 ships.")
        return
    all_ships_globally = [ship for faction in app.save_data.get("FactionFleetGroups", []) for fleet in faction.get("FleetGroups", []) for ship in fleet.get("FleetShips", [])]
    next_ship_id = _get_next_id("ShipId", all_ships_globally)
    new_ship = NEW_SHIP_TEMPLATE.copy()
    new_ship["Name"] = f"New Manticore {next_ship_id}"
    new_ship["ShipId"] = next_ship_id
    selected_fleet["FleetShips"].append(new_ship)
    from parse_save import populate_ships_ui, populate_fleets_ui
    current_fleet_selection = app.selected_fleet_index
    populate_fleets_ui(app)
    app.selected_fleet_index = current_fleet_selection
    app.fleet_listbox.selection_set(current_fleet_selection)
    populate_ships_ui(app)
    app.ship_listbox.selection_set(tk.END)
    app.on_ship_select()
    app.set_status("Added a new Manticore corvette.")

def remove_selected_ships(app):
    """Removes one or more selected ships from the fleet."""
    if not app.selected_ship_indices: return
    
    num_selected = len(app.selected_ship_indices)
    plural = "s" if num_selected > 1 else ""
    
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {num_selected} ship{plural}?"):
        ships = app.player_fleets[app.selected_fleet_index].get("FleetShips", [])
        
        # Iterate over a sorted list of indices in reverse to prevent shifting errors
        for index in sorted(app.selected_ship_indices, reverse=True):
            del ships[index]
            
        from parse_save import populate_ships_ui, populate_fleets_ui
        current_fleet_selection = app.selected_fleet_index
        populate_fleets_ui(app)
        app.selected_fleet_index = current_fleet_selection
        app.fleet_listbox.selection_set(current_fleet_selection)
        populate_ships_ui(app)
        app.set_status(f"Removed {num_selected} ship{plural}.")

def update_resources_in_data(app):
    try:
        if app.save_data:
            tylium = int(app.tylium_entry.get())
            if tylium > MAX_RESOURCE_VALUE: tylium = MAX_RESOURCE_VALUE
            app.save_data["Tylium"] = tylium
            app.tylium_entry.delete(0, tk.END); app.tylium_entry.insert(0, tylium)
            req_points = int(app.requisition_entry.get())
            if req_points > MAX_RESOURCE_VALUE: req_points = MAX_RESOURCE_VALUE
            app.save_data["RequisitionPoints"] = req_points
            app.requisition_entry.delete(0, tk.END); app.requisition_entry.insert(0, req_points)
            return True
        return False
    except (ValueError, TypeError):
        messagebox.showerror("Invalid Input", "Tylium and Requisition must be whole numbers.")
        from parse_save import populate_resources_ui
        populate_resources_ui(app)
        return False

def save_data_to_file(app, save_as=False):
    if not app.save_data:
        messagebox.showwarning("Warning", "No data to save.")
        return
    if not update_resources_in_data(app): return
    file_path = app.save_file_path
    if save_as or not file_path:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bsgsave",
            filetypes=[("BSG Save Files", "*.bsgsave")]
        )
        if not file_path: return 
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            json.dump(app.save_data, f, indent=4)
        app.save_file_path = file_path
        app.filepath_label.config(text=file_path)
        app.set_status(f"File saved to {os.path.basename(file_path)}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")
>>>>>>> 4cc12ff77c26fec3fd4f4506c8d06ac32bb3abd3
        app.set_status("Error saving file.")
import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from game_data import MAX_RESOURCE_VALUE

# FIX: Set PlayerAssignedFlagship to False by default in the template
NEW_SHIP_TEMPLATE = {
    "ShipType": 6, "Name": "Thalassa\r", "ShipPosition": { "x": 0.0, "y": 0.0, "z": 0.0 },
    "FTLCooldownTimer": 100, "ShipId": 9, "CanBeRenamed": True, "PreventTransferring": False,
    "AlwaysFlagship": False, "PlayerAssignedFlagship": False, "ActiveMunitions": [0],
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
    """Adds a new ship, using and updating the save file's NextShipId."""
    if app.selected_fleet_index is None:
        return
    
    selected_fleet = app.player_fleets[app.selected_fleet_index]
    if len(selected_fleet.get("FleetShips", [])) >= 16:
        messagebox.showinfo("Fleet Full", "A fleet cannot have more than 16 ships.")
        return

    all_ships_globally = [ship for faction in app.save_data.get("FactionFleetGroups", []) for fleet in faction.get("FleetGroups", []) for ship in fleet.get("FleetShips", [])]
    existing_ids = {ship.get("ShipId", 0) for ship in all_ships_globally}

    new_ship_id = app.save_data.get("NextShipId", 0)
    
    if new_ship_id in existing_ids or new_ship_id == 0:
        new_ship_id = max(existing_ids) + 1 if existing_ids else 1
    
    new_ship = NEW_SHIP_TEMPLATE.copy()
    new_ship["Name"] = f"Manticore {new_ship_id}"
    new_ship["ShipId"] = new_ship_id
    # The template now defaults to False, so no change is needed here.
    selected_fleet["FleetShips"].append(new_ship)
    
    existing_ids.add(new_ship_id)
    app.save_data["NextShipId"] = max(existing_ids) + 1
    
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
    if not app.selected_ship_indices: return
    num_selected = len(app.selected_ship_indices)
    plural = "s" if num_selected > 1 else ""
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {num_selected} ship{plural}?"):
        ships = app.player_fleets[app.selected_fleet_index].get("FleetShips", [])
        for index in sorted(app.selected_ship_indices, reverse=True):
            del ships[index]
        from parse_save import populate_ships_ui, populate_fleets_ui
        current_fleet_selection = app.selected_fleet_index
        populate_fleets_ui(app)
        app.selected_fleet_index = current_fleet_selection
        app.fleet_listbox.selection_set(current_fleet_selection)
        populate_ships_ui(app)
        app.set_status(f"Removed {num_selected} ship{plural}.")

def transfer_ships(app, destination_fleet_id):
    if not app.selected_ship_indices: return
    source_fleet = app.player_fleets[app.selected_fleet_index]
    destination_fleet = next((f for f in app.player_fleets if f.get("FleetId") == destination_fleet_id), None)
    if not destination_fleet: return
    if len(destination_fleet.get("FleetShips", [])) + len(app.selected_ship_indices) > 16:
        messagebox.showwarning("Transfer Failed", f"Cannot transfer ships. Destination fleet '{destination_fleet.get('Name')}' would exceed the 16-ship limit.")
        return
    ships_to_move = []
    for index in sorted(app.selected_ship_indices, reverse=True):
        ships_to_move.append(source_fleet["FleetShips"].pop(index))
    destination_fleet.setdefault("FleetShips", []).extend(reversed(ships_to_move))
    if not source_fleet.get("FleetShips", []):
        app.player_fleets.remove(source_fleet)
    from parse_save import populate_fleets_ui
    populate_fleets_ui(app)
    app.set_status(f"Transferred {len(ships_to_move)} ship(s).")

def create_new_fleet(app):
    i = 1
    while f"New Fleet {i}" in [f.get("Name") for f in app.player_fleets]:
        i += 1
    new_fleet_name = f"New Fleet {i}"
    existing_fleet_ids = {f.get("FleetId", 0) for f in app.player_fleets}
    new_fleet_id = app.save_data.get("NextFleetId", 0)
    if new_fleet_id in existing_fleet_ids or new_fleet_id == 0:
        new_fleet_id = max(existing_fleet_ids) + 1 if existing_fleet_ids else 1
    all_ships_globally = [ship for faction in app.save_data.get("FactionFleetGroups", []) for fleet in faction.get("FleetGroups", []) for ship in fleet.get("FleetShips", [])]
    existing_ship_ids = {ship.get("ShipId", 0) for ship in all_ships_globally}
    new_ship_id = app.save_data.get("NextShipId", 0)
    if new_ship_id in existing_ship_ids or new_ship_id == 0:
        new_ship_id = max(existing_ship_ids) + 1 if existing_ship_ids else 1
    manticore = NEW_SHIP_TEMPLATE.copy()
    manticore["ShipType"] = 6
    manticore["Name"] = f"Manticore {new_ship_id}"
    manticore["ShipId"] = new_ship_id
    # FIX: Explicitly set the first ship of a new fleet as the flagship
    manticore["PlayerAssignedFlagship"] = True
    
    new_fleet = {
        "PlayerCreated": True, "FleetId": new_fleet_id, "Name": new_fleet_name,
        "Faction": 0, "FleetShips": [manticore], "AnchorPointId": 16, "Commander": None
    }
    app.player_fleets.append(new_fleet)
    app.save_data["NextFleetId"] = new_fleet_id + 1
    app.save_data["NextShipId"] = new_ship_id + 1
    from parse_save import populate_fleets_ui
    populate_fleets_ui(app)
    app.set_status(f"Created '{new_fleet_name}'.")

def remove_selected_fleets(app):
    if not app.selected_fleet_indices: return
    num_selected = len(app.selected_fleet_indices)
    plural = "s" if num_selected > 1 else ""
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {num_selected} fleet{plural}? This will also delete all ships within."):
        for index in sorted(app.selected_fleet_indices, reverse=True):
            del app.player_fleets[index]
        from parse_save import populate_fleets_ui
        populate_fleets_ui(app)
        app.set_status(f"Removed {num_selected} fleet{plural}.")

def update_ship_loadout(app, new_munitions, new_squadrons):
    if app.selected_fleet_index is None or not app.selected_ship_indices: return
    ship_index = app.selected_ship_indices[0]
    ship = app.player_fleets[app.selected_fleet_index]["FleetShips"][ship_index]
    ship["ActiveMunitions"] = new_munitions
    ship["ActiveSquadrons"] = new_squadrons

def update_ship_unlocks_in_data(app):
    if not app.save_data: return
    new_unlocked_ids = []
    for ship_id, var in app.unlocked_ship_vars.items():
        if var.get(): new_unlocked_ids.append(ship_id)
    app.save_data["UnlockedShips"] = new_unlocked_ids

def update_munition_unlocks_in_data(app):
    if not app.save_data: return
    new_unlocked_ids = []
    for munition_id, var in app.unlocked_munition_vars.items():
        if var.get(): new_unlocked_ids.append(munition_id)
    app.save_data["UnlockedMissiles"] = new_unlocked_ids

def update_squadron_unlocks_in_data(app):
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
        app.set_status("Error saving file.")
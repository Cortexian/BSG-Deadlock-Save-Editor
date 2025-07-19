<<<<<<< HEAD
# game_data.py

# --- Gameplay Limits ---
FLEET_NAME_LIMIT = 20
SHIP_NAME_LIMIT = 20
MAX_RESOURCE_VALUE = 99999

# --- Ship Definitions ---
SHIP_TYPES = {
    "Manticore": 6, "Berserk": 12, "Adamant": 5, "Ranger": 3,
    "Celestra": 14, "Minotaur": 4, "Atlas": 2, "Jupiter": 0,
    "Heracles": 19, "Minerva": 15, "Artemis": 1, "Janus": 13,
    "Jupiter Mk2": 24, "Defender": 27, "Orion": 26, "Mercury": 29,
    "Valkyrie": 30, "Daidalos": 11
}

UNLOCKABLE_SHIPS_ORDER = [
    "Manticore", "Berserk", "Adamant",
    "Ranger", "Celestra", "Minotaur",
    "Atlas", "Jupiter", "Heracles",
    "Minerva", "Artemis", "Janus",
    "Jupiter Mk2", "Defender", "Orion"
]

# --- Squadron Definitions ---
SQUADRON_TYPES = {
    "Viper Mk I": 0, "Viper Mk II": 1, "Raptor": 2, "Taipan": 5,
    "Viper Mk VII": 113, "Sweeper": 3, "Assault Raptor": 4
}

# --- Munition Definitions ---
MUNITION_TYPES = {
    "Guided Missile": 0, "Torpedo": 2, "PCM": 9, "Nuke": 7,
    "Armour Piercer": 4, "Proximity Mine": 13, "EMP Mine": 16,
    "Debris Mine": 21, "EMP Generator": 22
}

# --- Squadron Capacity Definitions ---
# Defines the number of squadron slots and any special capabilities.
SQUADRON_CAPACITY = {
    "Berserk": {"capacity": 1, "viper_mk_vii_capable": False},
    "Adamant": {"capacity": 1, "viper_mk_vii_capable": False},
    "Orion": {"capacity": 1, "viper_mk_vii_capable": False},
    "Atlas": {"capacity": 3, "viper_mk_vii_capable": False},
    "Artemis": {"capacity": 2, "viper_mk_vii_capable": False},
    "Minerva": {"capacity": 2, "viper_mk_vii_capable": False},
    "Jupiter": {"capacity": 3, "viper_mk_vii_capable": False},
    "Jupiter Mk2": {"capacity": 4, "viper_mk_vii_capable": False},
    "Valkyrie": {"capacity": 1, "viper_mk_vii_capable": True},
    "Mercury": {"capacity": 4, "viper_mk_vii_capable": True}
=======
# game_data.py

# --- Gameplay Limits ---
FLEET_NAME_LIMIT = 20
SHIP_NAME_LIMIT = 20
MAX_RESOURCE_VALUE = 99999

# --- Ship Definitions ---
SHIP_TYPES = {
    "Manticore": 6,
    "Berserk": 12,
    "Adamant": 5,
    "Ranger": 3,
    "Celestra": 14,
    "Minotaur": 4,
    "Atlas": 2,
    "Jupiter": 0,
    "Heracles": 19,
    "Minerva": 15,
    "Artemis": 1,
    "Janus": 13,
    "Jupiter Mk2": 24,
    "Defender": 27,
    "Orion": 26,
    "Mercury": 29,
    "Valkyrie": 30,
    "Daidalos": 11
>>>>>>> 4cc12ff77c26fec3fd4f4506c8d06ac32bb3abd3
}
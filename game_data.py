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
}

# --- DLC Definitions ---
DLC_NAMES = [
    "Reinforcement Pack", "The Broken Alliance", "Anabasis",
    "Sin and Sacrifice", "Resurrection", "Ghost Fleet Offensive",
    "Armistice", "Modern Ships Pack"
]

DLC_CONTENT = {
    "Reinforcement Pack": {
        "Ships": ["Berserk", "Janus"],
        "Squadrons": [],
        "Munitions": ["Proximity Mine", "EMP Mine"]
    },
    "The Broken Alliance": {
        "Ships": ["Minerva", "Celestra"],
        "Squadrons": ["Assault Raptor"],
        "Munitions": []
    },
    "Anabasis": {
        "Ships": [],
        "Squadrons": [],
        "Munitions": ["Debris Mine", "EMP Generator"]
    },
    "Sin and Sacrifice": {
        "Ships": ["Heracles"],
        "Squadrons": [],
        "Munitions": []
    },
    "Resurrection": {
        "Ships": ["Jupiter Mk2"], # Note: Special case, always available
        "Squadrons": ["Taipan"],
        "Munitions": []
    },
    "Ghost Fleet Offensive": {
        "Ships": ["Orion", "Defender"],
        "Squadrons": [],
        "Munitions": []
    },
    "Armistice": { # No in-game content relevant to the editor
        "Ships": [], "Squadrons": [], "Munitions": []
    },
    "Modern Ships Pack": {
        "Ships": ["Mercury", "Valkyrie"],
        "Squadrons": ["Viper Mk VII"],
        "Munitions": []
    }
}
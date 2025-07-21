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

# --- Ship Loadout Definitions ---
SHIP_LOADOUTS = {
    "Manticore": { "squadrons": [], "munitions": 1 },
    "Berserk": { "squadrons": [["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]], "munitions": 0 },
    "Adamant": { "squadrons": [["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]], "munitions": 1 },
    "Ranger": { "squadrons": [], "munitions": 2 },
    "Celestra": { "squadrons": [], "munitions": 2 },
    "Minotaur": { "squadrons": [], "munitions": 0 },
    "Atlas": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Raptor", "Assault Raptor", "Sweeper"]
        ],
        "munitions": 0
    },
    "Jupiter": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Raptor", "Assault Raptor", "Sweeper"]
        ],
        "munitions": 1
    },
    "Heracles": { "squadrons": [], "munitions": 0 },
    "Minerva": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]
        ],
        "munitions": 2
    },
    "Artemis": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]
        ],
        "munitions": 1
    },
    "Janus": { "squadrons": [], "munitions": 3 },
    "Jupiter Mk2": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Raptor", "Assault Raptor", "Sweeper"],
            ["Raptor", "Assault Raptor", "Sweeper"]
        ],
        "munitions": 1
    },
    "Defender": { "squadrons": [["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]], "munitions": 0 },
    "Orion": { "squadrons": [["Viper Mk I", "Viper Mk II", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]], "munitions": 1 },
    "Mercury": {
        "squadrons": [
            ["Viper Mk I", "Viper Mk II", "Viper Mk VII", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Viper Mk VII", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Viper Mk I", "Viper Mk II", "Viper Mk VII", "Raptor", "Assault Raptor", "Sweeper", "Taipan"],
            ["Raptor", "Assault Raptor", "Sweeper"]
        ],
        "munitions": 2
    },
    "Valkyrie": { "squadrons": [["Viper Mk I", "Viper Mk II", "Viper Mk VII", "Raptor", "Assault Raptor", "Sweeper", "Taipan"]], "munitions": 1 },
    "Daidalos": {
        "squadrons": [
            ["Viper Mk I"],
            ["Raptor"]
        ],
        "munitions": 0
    }
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
        "Ships": ["Jupiter Mk2"],
        "Squadrons": ["Taipan"],
        "Munitions": []
    },
    "Ghost Fleet Offensive": {
        "Ships": ["Orion", "Defender"],
        "Squadrons": [],
        "Munitions": []
    },
    "Armistice": {
        "Ships": [], "Squadrons": [], "Munitions": []
    },
    "Modern Ships Pack": {
        "Ships": ["Mercury", "Valkyrie"],
        "Squadrons": ["Viper Mk VII"],
        "Munitions": []
    }
}
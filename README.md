# BSG-Deadlock-Save-Editor
Battlestar Galactica Deadlock Save Game Editor

This is a GUI save-game editor for Windows. Written in python using tkinter with the assistance of some AI-revisions.

![alt text](https://github.com/Cortexian/BSG-Deadlock-Save-Editor/blob/main/readme.png "BSG Deadlock Editor Interface")

## Current Features
- Automatically detect savegame files in the default locations for Steam and GOG, allowing the user to select which file to edit.
- Manually open a file if the auto-detection fails.
- Light and dark visual themes.
- DLC Configuration to reduce possibility of modifying your save in a way that locks it out due to missing DLC.
- Display a list of current fleets and the ships that make up those fleets.
- Rename fleets and ships.
- Modify fleet composition (add/remove/modify ships - v0.2 added multi-select for ship removal/modification).
- Display and modify resources (Tylium / Requisition Points).
- Options to globally unlock/research specific ships, munitions, and fighter squadron types.

### Planned Features
- More detailed ship modification, including changing equipped munitions and fighter squadrons where applicable.
- Complete fleet management from editor (add functions for setting a ship as flagship, transfer ships between fleets).

### Getting Started
If you just want to use the application, download the latest verison from the [Releases](https://github.com/Cortexian/BSG-Deadlock-Save-Editor/releases) section.

If you experience an error or undesirable behaviour, or have a suggestion for a feature that should be possible by editing the save file, please [submit a new issue](https://github.com/Cortexian/BSG-Deadlock-Save-Editor/issues/new/choose).

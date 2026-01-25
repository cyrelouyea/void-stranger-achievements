# Void Stranger Achievements Mod

A mod to include achievements in Void Stranger

## Build step

### Requirements

- UndertaleModTool CLI 0.8.x.x: https://github.com/UnderminersTeam/UndertaleModTool/releases
    - Built and tested with 0.8.3.0 and 0.8.4.1
- Void Stranger 1.1.3

### Windows

- Create a `variables.bat` file by copying `.variables.structure.bat` and fill in the variables
- Run `builder.bat`

### Linux

- Create a `variables.sh` file by copying `.variables.structure.sh` and fill in the variables
- Run `builder.sh`

## Project structure

### Achievements folder

Achievements are stored in `achievements/`.

Each file correspond to a single independant achievement. The filename is used as a unique identifier. Therefore, renaming a file will also reset the achievement since it will be counted as a new achievement and the old one will be deleted.

Here is an example of what an achievement file looks like:

```
title: Just leap and believe! (10/1000)
description: Use the wings a total of 10 times

// PATCH gml_Object_obj_player_Step_0 652
if obj_inventory.wings_counter >= 10
    {+achievement}

// PATCH gml_Object_obj_player_Step_0 2354
if obj_inventory.wings_counter >= 10
    {+achievement}
```

The header consists of two attributes:
- `title`: Name of the achievement displayed when you get it
- `description`: Details/Explanation of an achievement for the achievements menu

The body can contain as many PATCH block as you want and starts with `// PATCH`:
```
// PATCH <codename> <line> 
<code>
```
- `codename`: The full code name in UndertaleModTool's Code section
- `line`: The line number where `code` will be inserted in the original data.win. Your code will be inserted right before the specified line.

For patches targeting the same file: 
- You don't have to worry about how other achievements files and patches will offset the line number for your patch. You only need to specify the line number you want to target in the original `data.win`. 
- If multiple patches target the same line number, then the insertion order is "random" (maybe I will order them alphanumerically using the filename in the future)

Utility macros for the `code` block:
- `{+achievement}`: to trigger the achievement corresponding to this file
- `{+achievement:60}`: to add a delay (number of frames) to when the achievement will be triggered. In this example, the achievement will appear 60 frames after it reaches this part of the code.
- `{-achievement}`: to remove the achievement corresponding to this file.

### Counters folder

If you want to count and save the number of times a certain event happened (for instance, the number of times you killed a certain enemy), you can add a counter file in `counters/`.

Adding a file will automatically create a counter named `<filename>_counter` in `obj_inventory`. Loading and saving will automatically be done from/to the `achievements.vs` save file. 

In your counter file, you can add as many PATCH block as you want to update the counter like this:

```
// PATCH gml_Object_obj_enemy_co_Step_0 168
{{counter}} += 1

// PATCH gml_Object_obj_enemy_co_Step_0 153
{{counter}} += 1
```

`{{counter}}` will be replaced by the counter name in `obj_inventory`
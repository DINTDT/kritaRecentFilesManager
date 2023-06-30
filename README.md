# DINTDT's Recent Files Manager for Krita

*RFM* is a plugin designed to easily manage the list of recent
files that Krita has opened. By default, Krita only allows you to clear
the list, but not manage individual entries in this list.

This plugin provides a docker that shows each recent file, allows
you to reorder them and/or delete them individually.

The "Update List" button will reload the list of recent files. Use this to
view new files you've opened, and to fix the list if it ever gets
desynched.

## Installation

 1. To install locally, **download** this repo, and compress it into a .zip file.
 From GitHub, you can download the repo directly as a .zip file.
 2. **Install** the plugin:
  - If you have the .zip file, open Krita, then go to Tools > Scripts > Install
  Python Plugin from File..., then select the .zip file.
  - You can instead install the plugin with the repository URL. Open Krita, then
  go to Tools > Scripts > Install Python Plugin from Web..., then paste this
  repository's URL.
 3. **Restart** Krita. This way, it will recognize the recently installed plugin.
 4. **Enable** the plugin. Go to Settings > Configure Krita... > Python Plugin
 Manager (in the menu on the left). From the plugins list, find "Recent Files
 Manager" and enable it.
 5. **Restart** Krita. This will load the plugin properly.
 6. Go to Settings > Dockers. In the list, you'll see "Recent Files Manager". Click
 it to open the RFM Docker.

## Usage

The RFM docker contains an "Update List" button at the top. Click this button to
reload the recent files and have it show the newly opened files. If the list ever
gets desynced, this button should fix it.

The list of recent recent files shows a thumbnail and the file name. Click on
either of them to open that file.

Next to the thumbnail, a pair of Move Up/Move Down buttons will let you reorder
the files within the list. The first file cannot be moved up, and the last file
cannot be moved down.

At the far right, a Delete button will let you remove the file *from the list*.
This does not delete the file from your disk.

## Notes

The plugin has only been tested on Krita 5.1.5, although I would assume it works
on previous versions of Krita 5 just fine.
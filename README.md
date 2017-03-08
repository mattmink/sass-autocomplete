# SASS Autocomplete
Sublime plugin to autocomplete all SASS vars and mixins in the current project

This is largely based on [SassSolution](https://codeload.github.com/ahmedam55/SassSolution), but does not require adding files/folders to the settings file. Instead, it looks for a parent `/sass/` or `/scss/` (either naming convention works) directory, and uses all ".scss" files within it as the reference.

# Manual installation
1. Download the [latest release](https://codeload.github.com/matthewjmink/sass-autocomplete/zip/master), extract and rename the directory to **"sass-autocomplete"**.
2. Move the directory inside your sublime `Packages` directory. **(Preferences > Browse packages...)**

Apart from that you must choose **SCSS syntax** in the editor when you want to use the autocompletion (see: [SCSS plugin](https://packagecontrol.io/packages/SCSS).
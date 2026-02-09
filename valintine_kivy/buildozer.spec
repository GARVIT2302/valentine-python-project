[app]

# (str) Title of your application
title = Valentine App

# (str) Package name
package.name = valintineapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.valintine

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,bmp,gif,mp3

# (list) Files or directories to exclude
source.exclude_exts = spec

# (str) The entry point for your application
entrypoint = main.py

# (list) Application requirements
requirements = python3,kivy,ffpyplayer

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Minimum API for Android
android.minapi = 21

# (str) Android SDK version to use
android.api = 33

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android NDK api to use
android.ndk_api = 21

# (bool) Use legacy storage
android.legacy_storage = 0

# (bool) Optimize the Python bytecode
python.optimize = 1

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (str) Buildozer spec version
warn_on_root = 0

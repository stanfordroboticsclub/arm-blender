#!/bin/sh
current_dir=$(dirname $(readlink -f $0))
blender $current_dir/../blender/Demo.blend --python $current_dir/../scripts/arm_offsets_panel.py --python $current_dir/../scripts/blender_to_socket.py

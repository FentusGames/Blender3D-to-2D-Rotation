import bpy
import math
import time
import os
import sys

sys.stdout.write("RENDERING:\n\n")
sys.stdout.flush()

blender_import_path = "M:/ide/eclipse-clicker/Boxes/assets-raw/blend"
blender_export_path = "M:/ide/eclipse-clicker/Boxes/assets-raw/blenderexports"

files = []

# Name, Animation name & folder, File, Copy Collection, NAngle Count, Min number of frames, Frame start, Frame end, width, height

# ---- Quadruped ----
# files.append(["quadruped", "walk/top",    "/quadruped/quadruped.blend", "Walk-Top",    16, 25, 1,  1,  128, 128 ]) # No animation = 1, 1]
# files.append(["quadruped", "walk/bottom", "/quadruped/quadruped.blend", "Walk-Bottom", 16, 25, 1, 37,  128, 128 ]) # 

# ---- NPC001 ----
# files.append(["npc001",    "idle",        "/npc001/npc001.blend",       "Idle",        16, 25, 1, 145, 128, 128 ]) # 
# files.append(["npc001",    "walking",     "/npc001/npc001.blend",       "Walking",     16, 25, 1, 34,  128, 128 ]) # 

def remove_model(copy):
    name = copy
    remove_collection_objects = True

    coll = bpy.data.collections.get(name)

    if coll:
        if remove_collection_objects:
            obs = [o for o in coll.objects if o.users == 1]
            while obs:
                bpy.data.objects.remove(obs.pop())

        bpy.data.collections.remove(coll)

for f in files:
    name = f[0]                            # Generic name of the entity to be used by the game engine.
    animation_name = f[1]                  # Folder structure and path used by the animation and render system.
    file_name = blender_import_path + f[2] # File path in the game editor.
    copy = f[3]                            # The collection to copy the this file for rendering.
    angles = f[4]                          # Number of angles to be exported folder should be in float format.
    min_frames = f[5]                      # Min munder of frames to render
    frame_start = f[6]                     # Startign frame usually = 1.
    frame_end = f[7]                       # Ending frame must be obtained from the original file.
    resolution_x = f[8]                    # The X resolution aka width in pixels.
    resolution_y = f[9]                    # the Y resolition aka height in pixels.
    
    remove_model(copy)
    
    bpy.context.scene.render.resolution_x = resolution_x
    bpy.context.scene.render.resolution_y = resolution_y
    
    bpy.ops.wm.append(directory=file_name + "/Collection", link=False, filename=copy)
    
    sys.stdout.write("Removing old files...\n\n")
    sys.stdout.flush()
    
    for i in range(0, angles):
        angle = 360/angles
        
        dir = blender_export_path + "/" + name + "/" + animation_name + "/" + str(i*angle) + '/'
        
        if os.path.exists(dir):
            for count, filename in enumerate(os.listdir(dir)):
                os.remove(dir + filename)
            
    time.sleep(2)
        
    sys.stdout.write("Rendering...\n\n")
    sys.stdout.flush()

    for i in range(0, angles):
        angle = 360/angles
        
        bpy.context.scene.frame_start = frame_start
        bpy.context.scene.frame_end = frame_end
        
        print(int(math.ceil(frame_end/min_frames)))
        
        bpy.context.scene.frame_step = int(math.ceil(frame_end/min_frames))
        
        bpy.data.objects['BezierCircle'].rotation_euler[2] = (i*angle)/180*math.pi
        
        bpy.data.scenes[0].render.filepath = blender_export_path + "/" + name + "/" + animation_name + "/" + str(i*angle) + '/'
        
        bpy.ops.render.render(animation=True)
        
    time.sleep(2)
    
    sys.stdout.write("Renaming output files...\n\n")
    sys.stdout.flush()
            
    for i in range(0, angles):
        angle = 360/angles
        
        dir = blender_export_path + "/" + name + "/" + animation_name + "/" + str(i*angle) + '/'
        
        for count, filename in enumerate(os.listdir(dir)):
            os.rename(dir + filename, dir + "_" + str(count) + ".png")

    time.sleep(10)
    
    remove_model(copy)

bpy.data.objects['BezierCircle'].rotation_euler[2] = 0

sys.stdout.write("DONE!\n\n")
sys.stdout.flush()

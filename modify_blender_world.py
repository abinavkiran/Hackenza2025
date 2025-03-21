import bpy
import os

# 🟢 Path to your original Blender file (CHANGE THIS)
original_blender_file = r"C:\Users\\freemocap_data\recording_sessions\freemocap_sample_data\freemocap_sample_data.blend"

# 🟢 Define the new file path (same directory, named "proc.blend")
proc_blender_file = os.path.join(os.path.dirname(original_blender_file), "proc.blend")

# Load the original Blender file
bpy.ops.wm.open_mainfile(filepath=original_blender_file)

# 1️⃣ DELETE ALL VIDEO FEEDS (MediaPipe & Other Sources)
video_objects = [obj for obj in bpy.data.objects if "media" in obj.name.lower() or "video" in obj.name.lower()]
for obj in video_objects:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"✅ Deleted {len(video_objects)} video feed objects (MediaPipe, Video sources, etc.).")

# 2️⃣ FIND OR CREATE A FLOOR OBJECT
floor = None
for obj in bpy.data.objects:
    if "floor" in obj.name.lower():  
        floor = obj
        break

if not floor:
    print("⚠️ No floor object found! Creating a new floor.")
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    floor = bpy.context.object
    floor.name = "Floor"

# Set floor material to GREEN
if not floor.data.materials:
    mat_floor = bpy.data.materials.new(name="GreenFloor")
    mat_floor.diffuse_color = (0.1, 0.5, 0.1, 1)  # Dark green color
    floor.data.materials.append(mat_floor)

# 3️⃣ ADD REALISTIC GRASS USING PARTICLE SYSTEM
# Create a particle system for grass
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
grass_field = bpy.context.object
grass_field.name = "GrassField"

# Add particle system
grass_field.modifiers.new(name="GrassParticles", type='PARTICLE_SYSTEM')
particle_sys = grass_field.particle_systems[0].settings

# Configure particle system for hair-based grass
particle_sys.type = 'HAIR'
particle_sys.hair_length = 0.7  # Longer grass
particle_sys.count = 8000  # Dense grass
particle_sys.use_advanced_hair = True

# Add a GREEN material to the grass
mat_grass = bpy.data.materials.new(name="GrassMaterial")
mat_grass.diffuse_color = (0.2, 0.8, 0.2, 1)  # Lighter green grass
grass_field.data.materials.append(mat_grass)

# Parent grass to floor (if found)
grass_field.parent = floor

print("🌿 Realistic grass added with a green color!")

# 🟢 Save the new Blender file as "proc.blend"
bpy.ops.wm.save_as_mainfile(filepath=proc_blender_file)
print(f"✅ File saved as {proc_blender_file}")

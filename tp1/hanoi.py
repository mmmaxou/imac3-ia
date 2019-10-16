import bpy


# Global var

CYLINDER_AMOUNT = 7
TIME_TO_MOVE = 9

# Prepare scene
scene = bpy.context.scene
frame = 1
scene.frame_set(frame)
scene.frame_start = frame
towers = []
plate = []




# Functions

def createPlate():
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    plate = bpy.context.active_object
    plate.name = 'plateau'
    bpy.ops.transform.resize(value=(1, 1, 0.1), constraint_axis=(False, False, True))
    bpy.ops.transform.translate(value=(0, 0, 0.1), constraint_axis=(False, False, True))
    bpy.ops.transform.resize(value=(10, 1, 1), constraint_axis=(True, False, False))
    bpy.ops.transform.resize(value=(1, 2, 1), constraint_axis=(False, True, False))
    
    

def createTowers():
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
    t1 = bpy.context.active_object
    t1.name = 'tower2'
    bpy.ops.transform.resize(value=(0.1, 0.1, 1), constraint_axis=(True, True, False))
    bpy.ops.transform.resize(value=(1, 1, 2), constraint_axis=(False, False, True))
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True))
    
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-7, 0, -0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    t2 = bpy.context.active_object
    t2.name = 'tower1'
    
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(14, -0, -0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    t3 = bpy.context.active_object
    t3.name = 'tower3'
    
    return [[t2],[t1],[t3]]

def createCylinders(n, tower):
    bpy.ops.mesh.primitive_cylinder_add(location=(-7, 0, 0.3))
    bpy.ops.transform.resize(value=(1, 1, 0.1), constraint_axis=(False, False, True))
    bpy.ops.transform.resize(value=(2, 2, 1), constraint_axis=(True, True, False))
    tower.append(bpy.context.active_object)
    bpy.context.active_object.name = 'c0'
    
    for i in range(1, n):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0.2), "constraint_axis":(False, False, True)})
        bpy.ops.transform.resize(value=(0.9, 0.9, 1), constraint_axis=(True, True, False))
        bpy.context.active_object.name = 'c' + str(i)
        tower.append(bpy.context.active_object)
    

def moveCylinder(fromTower, toTower):
    bpy.ops.object.select_all(action='DESELECT')
    
    # variables
    global frame
    
    # move from fromTower to toTower
    ob = fromTower.pop()
    ob.select = True
    toTower.append(ob)
    
    # set timestep
    timestep = TIME_TO_MOVE / 3
    ob.keyframe_insert(data_path='location')
    
    # step 1 : move up
    frame += timestep
    scene.frame_set(frame)
    ploc = ob.location
    zpos = ploc[2]
    ob.location = (ploc[0], ploc[1], 5)
    ob.keyframe_insert(data_path='location')
    
    # step 2 : move to tower
    frame += timestep
    scene.frame_set(frame)
    tloc = toTower[0].location
    ploc = ob.location
    ob.location = (tloc[0], ploc[1], ploc[2])
    ob.keyframe_insert(data_path='location')
    
    # step 3 : move down
    frame += timestep
    scene.frame_set(frame)
    ploc = ob.location
    zpos = len(toTower) * 0.2 - 0.1
    ob.location = (ploc[0], ploc[1], zpos)
    ob.keyframe_insert(data_path='location')
        

def hanoi(n, fromTower, toTower, middleTower):
    if n>0:
        hanoi(n-1, fromTower, middleTower, toTower)
        moveCylinder(fromTower, toTower)
        hanoi(n-1, middleTower, toTower, fromTower)
    
def deleteScene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


# Main

deleteScene()
plate = createPlate()
towers = createTowers()
createCylinders(CYLINDER_AMOUNT, towers[0])
hanoi(CYLINDER_AMOUNT, towers[0], towers[2], towers[1])

# end
scene.frame_end = frame + 10
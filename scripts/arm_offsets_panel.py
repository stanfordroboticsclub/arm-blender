import bpy

class ArmOffsets(bpy.types.PropertyGroup):
    wrist_roll_offset = bpy.props.FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )
           
    my_int = bpy.props.IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )
        
class ArmOffsetsPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Arm Offsets"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.column()
        row.prop(scene.arm_offsets, "wrist_roll_offset")
        row.prop(scene.arm_offsets, "wrist_roll_offset")
        
        row.prop(scene.arm_offsets, "my_int")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.arm_offsets = bpy.props.PointerProperty(type=ArmOffsets)
   ## bpy.utils.register_class(ArmOffsetsPanel)
   
    


def unregister():
    #bpy.utils.unregister_class(ArmOffsetsPanel)
    bpy.utils.unregister_module(__name__)
    del bpy.types.Scene.arm_offsets


if __name__ == "__main__":
    register()

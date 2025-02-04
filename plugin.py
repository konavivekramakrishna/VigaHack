import bpy

class SimplePanel(bpy.types.Panel):
    bl_label = "DCC Integration"
    bl_idname = "PT_DCCIntegration"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DCC'

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj:
            layout.label(text=f"Name: {obj.name}")
            layout.label(text=f"Type: {obj.type}")
            
            layout.prop(obj, "location", text="Location")
            layout.prop(obj, "rotation_euler", text="Rotation")
            layout.prop(obj, "scale", text="Scale")
            layout.prop(obj, "dimensions", text="Dimensions")

            if obj.type == 'MESH':
                layout.label(text=f"Vertex Count: {len(obj.data.vertices)}")

        else:
            layout.label(text="Name: None")
            layout.label(text="Type: None")
            layout.label(text="Location: 0.00, 0.00, 0.00")
            layout.label(text="Rotation: 0.00, 0.00, 0.00")
            layout.label(text="Scale: 1.00, 1.00, 1.00")
            layout.label(text="Dimensions: 0.00, 0.00, 0.00")

class ButtonOperator(bpy.types.Operator):
    bl_idname = "wm.button_operator"
    bl_label = "Button"

    def execute(self, context):
        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(ButtonOperator)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(ButtonOperator)

if __name__ == "__main__":
    register()

import bpy
import requests

SERVER_OPTIONS = {
    "Server 1": "http://localhost:3000/",
    "Server 2": "http://secondurl.com/",
}

DATA_SEND_OPTIONS = {
    "Send All Transforms": "/transform",
    "Send Position": "/position",
    "Send Rotation": "/rotation",
    "Send Scale": "/scale"
}

SERVER_ITEMS = [(key, key, "") for key in SERVER_OPTIONS.keys()]
DATA_SEND_ITEMS = [(key, key, "") for key in DATA_SEND_OPTIONS.keys()]
        
class SimplePanelProperties(bpy.types.PropertyGroup):
    selected_server: bpy.props.EnumProperty(
        name="Server Selection",
        description="Select a server",
        items=SERVER_ITEMS,
        default="Server 1"
    ) # type: ignore

class SimpleDataSendProperties(bpy.types.PropertyGroup):
    selected_data_option: bpy.props.EnumProperty(
        name="Data Send Option",
        description="Select the data type to send",
        items=DATA_SEND_ITEMS,
        default="Send All Transforms"
    ) # type: ignore

class SimplePanel(bpy.types.Panel):
    bl_label = "DCC Integration"
    bl_idname = "PT_DCCIntegration"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DCC"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        if obj:
            layout.label(text=f"Object Name: {obj.name}")
            layout.label(text=f"Object Type: {obj.type}")
            layout.prop(obj, "location", text="Position")
            layout.prop(obj, "rotation_euler", text="Rotation")
            layout.prop(obj, "scale", text="Scale")
            layout.prop(obj, "dimensions", text="Dimensions")

            if obj.type == "MESH":
                layout.label(text=f"Vertex Count: {len(obj.data.vertices)}")

        else:
            layout.label(text="No object selected.")

        layout.prop(scene.simple_panel_props, "selected_server", text="Server")
        selected_server_url = SERVER_OPTIONS[scene.simple_panel_props.selected_server]
        layout.label(text=f"Server URL: {selected_server_url}")

        layout.prop(scene.simple_data_send_props, "selected_data_option", text="Data Type")
        layout.operator("wm.send_data_operator", text="Send Data")

class SendDataOperator(bpy.types.Operator):
    bl_idname = "wm.send_data_operator"
    bl_label = "Send Data"

    def execute(self, context):
        obj = context.object
        scene = context.scene

        if not obj:
            self.report({'WARNING'}, "No object selected.")
            return {'CANCELLED'}

        selected_server_url = SERVER_OPTIONS[scene.simple_panel_props.selected_server]
        selected_data_option = scene.simple_data_send_props.selected_data_option
        endpoint = DATA_SEND_OPTIONS[selected_data_option]
        full_url = f"{selected_server_url}{endpoint}"

        data = {"name": obj.name, "type": obj.type}

        if selected_data_option == "Send All Transforms":
            data.update({
                "position": {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z},
                "rotation": {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z},
                "scale": {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z}
            })
        elif selected_data_option == "Send Position":
            data["position"] = {"x": obj.location.x, "y": obj.location.y, "z": obj.location.z}
        elif selected_data_option == "Send Rotation":
            data["rotation"] = {"x": obj.rotation_euler.x, "y": obj.rotation_euler.y, "z": obj.rotation_euler.z}
        elif selected_data_option == "Send Scale":
            data["scale"] = {"x": obj.scale.x, "y": obj.scale.y, "z": obj.scale.z}

        try:
            response = requests.post(full_url, json=data)
            self.report({'INFO'}, f"Response: {response.text}")
            print("Server Response:", response.text)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to send data: {str(e)}")
            print("Error:", e)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SimplePanelProperties)
    bpy.utils.register_class(SimpleDataSendProperties)
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(SendDataOperator)
    bpy.types.Scene.simple_panel_props = bpy.props.PointerProperty(type=SimplePanelProperties)
    bpy.types.Scene.simple_data_send_props = bpy.props.PointerProperty(type=SimpleDataSendProperties)

def unregister():
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleDataSendProperties)
    bpy.utils.unregister_class(SimplePanelProperties)
    bpy.utils.unregister_class(SendDataOperator)
    del bpy.types.Scene.simple_panel_props
    del bpy.types.Scene.simple_data_send_props

if __name__ == "__main__":
    register()

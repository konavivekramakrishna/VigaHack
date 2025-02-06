import bpy
import requests

# Dictionary for server options with corresponding URLs
SERVER_OPTIONS = {
    "Server 1": "http://localhost:3000/",
    "Server 2": "http://secondurl.com/",
}

# Dictionary for data send options with corresponding endpoints
DATA_SEND_OPTIONS = {
    "Send All Transforms": "/transform",
    "Send Position": "/position",
    "Send Rotation": "/rotation",
    "Send Scale": "/scale"
}

# List of server options for dropdown menu in the UI
SERVER_ITEMS = [(key, key, "") for key in SERVER_OPTIONS.keys()]
# List of data send options for dropdown menu in the UI
DATA_SEND_ITEMS = [(key, key, "") for key in DATA_SEND_OPTIONS.keys()]

# Property group for the panel's server selection
class SimplePanelProperties(bpy.types.PropertyGroup):
    selected_server: bpy.props.EnumProperty(
        name="Server Selection",  # Name displayed in the UI
        description="Select a server",  # Tooltip for the dropdown
        items=SERVER_ITEMS,  # Dropdown items populated with SERVER_ITEMS
        default="Server 1"  # Default value for the dropdown
    )  # type: ignore

# Property group for the panel's data send option selection
class SimpleDataSendProperties(bpy.types.PropertyGroup):
    selected_data_option: bpy.props.EnumProperty(
        name="Data Send Option",  # Name displayed in the UI
        description="Select the data type to send",  # Tooltip for the dropdown
        items=DATA_SEND_ITEMS,  # Dropdown items populated with DATA_SEND_ITEMS
        default="Send All Transforms"  # Default value for the dropdown
    )  # type: ignore

# Panel for DCC integration settings in the UI
class SimplePanel(bpy.types.Panel):
    bl_label = "DCC Integration"  # Panel title
    bl_idname = "PT_DCCIntegration"  # Unique ID for the panel
    bl_space_type = "VIEW_3D"  # Panel appears in the 3D View
    bl_region_type = "UI"  # Panel appears in the UI region
    bl_category = "DCC"  # Panel's tab name

    def draw(self, context):
        """
        Draw the contents of the panel in the UI.

        Parameters:
        - context (bpy.context): The context of the current scene and object.

        Returns:
        - None. (UI elements are drawn directly to the screen)
        """
        layout = self.layout
        obj = context.object  # Get the active object in the scene
        scene = context.scene  # Get the current scene

        if obj:  # If there is an object selected
            # Display object properties in the panel
            layout.label(text=f"Object Name: {obj.name}")
            layout.label(text=f"Object Type: {obj.type}")
            layout.prop(obj, "location", text="Position")
            layout.prop(obj, "rotation_euler", text="Rotation")
            layout.prop(obj, "scale", text="Scale")
            layout.prop(obj, "dimensions", text="Dimensions")

            if obj.type == "MESH":  # If the object is a mesh
                layout.label(text=f"Vertex Count: {len(obj.data.vertices)}")

        else:
            layout.label(text="No object selected.")  # If no object is selected

        # Server selection dropdown
        layout.prop(scene.simple_panel_props, "selected_server", text="Server")
        selected_server_url = SERVER_OPTIONS[scene.simple_panel_props.selected_server]
        layout.label(text=f"Server URL: {selected_server_url}")  # Display the selected server URL

        # Data send option dropdown
        layout.prop(scene.simple_data_send_props, "selected_data_option", text="Data Type")
        # Send data button
        layout.operator("wm.send_data_operator", text="Send Data")

# Operator to send data to the selected server
class SendDataOperator(bpy.types.Operator):
    bl_idname = "wm.send_data_operator"  # Unique operator ID
    bl_label = "Send Data"  # Button label

    def execute(self, context):
        """
        Executes the data sending process.

        Parameters:
        - context (bpy.context): The context of the current scene and object.

        Returns:
        - {'FINISHED'} (Operator result indicating success)
        """
        obj = context.object  # Get the active object in the scene
        scene = context.scene  # Get the current scene

        if not obj:  # If no object is selected
            self.report({'WARNING'}, "No object selected.")  # Report warning
            return {'CANCELLED'}  # Cancel the operation

        # Get the selected server and data send option
        selected_server_url = SERVER_OPTIONS[scene.simple_panel_props.selected_server]
        selected_data_option = scene.simple_data_send_props.selected_data_option
        endpoint = DATA_SEND_OPTIONS[selected_data_option]
        full_url = f"{selected_server_url}{endpoint}"  # Construct the full URL for the request

        # Prepare the data to send
        data = {"name": obj.name, "type": obj.type}

        # Add different types of data based on the selected option
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
            # Send the data to the server via a POST request
            response = requests.post(full_url, json=data)
            self.report({'INFO'}, f"Response: {response.text}")  # Display server response
            print("Server Response:", response.text)
        except Exception as e:
            self.report({'ERROR'}, f"Failed to send data: {str(e)}")  # Handle errors
            print("Error:", e)

        return {'FINISHED'}  # Finish the operator execution

# Register the classes and properties
def register():
    """
    Register the necessary Blender classes and properties.

    Parameters:
    - None.

    Returns:
    - None.
    """
    bpy.utils.register_class(SimplePanelProperties)
    bpy.utils.register_class(SimpleDataSendProperties)
    bpy.utils.register_class(SimplePanel)
    bpy.utils.register_class(SendDataOperator)
    bpy.types.Scene.simple_panel_props = bpy.props.PointerProperty(type=SimplePanelProperties)
    bpy.types.Scene.simple_data_send_props = bpy.props.PointerProperty(type=SimpleDataSendProperties)

# Unregister the classes and properties
def unregister():
    """
    Unregister the Blender classes and properties.

    Parameters:
    - None.

    Returns:
    - None.
    """
    bpy.utils.unregister_class(SimplePanel)
    bpy.utils.unregister_class(SimpleDataSendProperties)
    bpy.utils.unregister_class(SimplePanelProperties)
    bpy.utils.unregister_class(SendDataOperator)
    del bpy.types.Scene.simple_panel_props
    del bpy.types.Scene.simple_data_send_props

# Main execution: Register the classes when the script is run
if __name__ == "__main__":
    register()

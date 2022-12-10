import santas_level_editor.exporter as exporter
import santas_level_editor.per_object_info as per_object_info
import bpy

bl_info = {
	"name": "Santa's level editor",
	"blender": (2, 80, 0),
	"category": "Object",
}

DEFAULT_PROPERTY_TYPES = [
	"Zone",
	"PositiveZone",
	"NegativeZone",
	"EnableOnEnterZone",
	"DisableOnEnterZone",
	"EnableOnExitZone",
	"DisableOnExitZone",
	"Trigger",
	"EnableOnTriggerEnter",
	"DisableOnTriggerEnter",
]

class EditorInfoPropertyTypeGroup(bpy.types.PropertyGroup):
	string_value: bpy.props.StringProperty(name="Value")

class AddLevelEditorPropertyTypeToPreferences(bpy.types.Operator):
	bl_idname = "preferences.add_level_editor_property_type"
	bl_label = "Add level editor property type"
	bl_options = {'REGISTER', 'UNDO'}
	def execute(self, context):
		bpy.context.preferences.addons['santas_level_editor'].preferences.property_types.add()
		return {'FINISHED'}

class RemoveLevelEditorPropertyTypeFromPreferences(bpy.types.Operator):
	bl_idname = "preferences.remove_level_editor_property_type"
	bl_label = "Remove level editor property type"
	bl_options = {'REGISTER', 'UNDO'}
	index: bpy.props.IntProperty(name="index", default=0)
	def execute(self, context):
		bpy.context.preferences.addons['santas_level_editor'].preferences.property_types.remove(self.index)
		return {'FINISHED'}


class LevelEditorAddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	property_types: bpy.props.CollectionProperty(type=EditorInfoPropertyTypeGroup)
	def draw(self, context):
		level_editor_property_types = bpy.context.preferences.addons['santas_level_editor'].preferences.property_types
		layout = self.layout
		layout.operator("preferences.add_level_editor_property_type")
		current_index = 0
		for item in level_editor_property_types:
			box = layout.box()
			row = box.row()
			row.prop(item, "string_value")
			sub = row.row()
			sub.scale_x = 0.4
			op = sub.operator("preferences.remove_level_editor_property_type", text="–")
			op.index = current_index
			current_index += 1


classes = (
	EditorInfoPropertyTypeGroup,
	AddLevelEditorPropertyTypeToPreferences,
	RemoveLevelEditorPropertyTypeFromPreferences,
	LevelEditorAddonPreferences,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	# load default values
	if len(bpy.context.preferences.addons['santas_level_editor'].preferences.property_types) == 0:
		for pt in DEFAULT_PROPERTY_TYPES:
			bpy.context.preferences.addons['santas_level_editor'].preferences.property_types.add()
			bpy.context.preferences.addons['santas_level_editor'].preferences.property_types[-1].string_value = pt

	per_object_info.register()
	exporter.register()


def unregister():
	exporter.unregister()
	per_object_info.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
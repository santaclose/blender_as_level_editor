import bpy

OBJECT_PROPERTIES = [
	"Zone",
	"PositiveZone",
	"NegativeZone",
	"EnableOnEnterZone",
	"DisableOnEnterZone",
	"EnableOnExitZone",
	"DisableOnExitZone",
]

class AddLevelEditorInfoToObject(bpy.types.Operator):
	bl_idname = "object.add_level_editor_info"
	bl_label = "Add level editor info to object"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.context.object.level_editor_info.add()
		return {'FINISHED'}

class RemoveLevelEditorInfoFromObject(bpy.types.Operator):
	bl_idname = "object.remove_level_editor_info"
	bl_label = "Remove level editor info from object"
	bl_options = {'REGISTER', 'UNDO'}
	
	index: bpy.props.IntProperty(name="index", default=0)

	def execute(self, context):
		bpy.context.object.level_editor_info.remove(self.index)
		return {'FINISHED'}


class PerObjectPropertyGroup(bpy.types.PropertyGroup):
	info_type: bpy.props.EnumProperty(
		items=[(x, x, x) for x in OBJECT_PROPERTIES],
		name="Type")
	info_value: bpy.props.StringProperty(name="Value")


class LevelEditorInfoPanel(bpy.types.Panel):
	bl_label = "Santa's Level Editor Info"
	bl_idname = "object_PT_layout"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "object"

	def draw(self, context):
		if not hasattr(bpy.types.Object, 'level_editor_info'):
			return
		object = context.object
		layout = self.layout
		level_editor_info = object.level_editor_info
		
		current_index = 0
		for item in level_editor_info:
			box = layout.box()
			box.prop(item, "info_type")
			box.prop(item, "info_value")
			op = box.operator("object.remove_level_editor_info")
			op.index = current_index
			current_index += 1
		
		layout.operator("object.add_level_editor_info")


classes = (
	AddLevelEditorInfoToObject,
	RemoveLevelEditorInfoFromObject,
	PerObjectPropertyGroup,
	LevelEditorInfoPanel,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Object.level_editor_info = bpy.props.CollectionProperty(type=PerObjectPropertyGroup)

def unregister():
	if hasattr(bpy.types.Object, 'level_editor_info'):
		del bpy.types.Object.level_editor_info
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()

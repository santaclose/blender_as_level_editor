import bpy


class CopyLevelEditorInfoFromObject(bpy.types.Operator):
	bl_idname = "object.copy_level_editor_info"
	bl_label = "Copy level editor info from object"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
		prefs.copied_level_editor_info.clear()
		for item in bpy.context.object.level_editor_info:
			prefs.copied_level_editor_info.append((item.info_type, item.info_value))
		return {'FINISHED'}

class PasteLevelEditorInfoToObject(bpy.types.Operator):
	bl_idname = "object.paste_level_editor_info"
	bl_label = "Paste level editor info from object"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
		bpy.context.object.level_editor_info.clear()
		for item in prefs.copied_level_editor_info:
			bpy.context.object.level_editor_info.add()
			bpy.context.object.level_editor_info[-1].info_type = item[0]
			bpy.context.object.level_editor_info[-1].info_value = item[1]
		return {'FINISHED'}

class CopyLevelEditorInfoFromCollection(bpy.types.Operator):
	bl_idname = "collection.copy_level_editor_info"
	bl_label = "Copy level editor info from collection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
		prefs.copied_level_editor_info.clear()
		for item in bpy.context.collection.level_editor_info:
			prefs.copied_level_editor_info.append((item.info_type, item.info_value))
		return {'FINISHED'}

class PasteLevelEditorInfoToCollection(bpy.types.Operator):
	bl_idname = "collection.paste_level_editor_info"
	bl_label = "Paste level editor info from collection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
		bpy.context.collection.level_editor_info.clear()
		for item in prefs.copied_level_editor_info:
			bpy.context.collection.level_editor_info.add()
			bpy.context.collection.level_editor_info[-1].info_type = item[0]
			bpy.context.collection.level_editor_info[-1].info_value = item[1]
		return {'FINISHED'}


class AddLevelEditorInfoToObject(bpy.types.Operator):
	bl_idname = "object.add_level_editor_info"
	bl_label = "Add level editor info to object"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.context.object.level_editor_info.add()
		return {'FINISHED'}

class AddLevelEditorInfoToCollection(bpy.types.Operator):
	bl_idname = "collection.add_level_editor_info"
	bl_label = "Add level editor info to collection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		bpy.context.collection.level_editor_info.add()
		return {'FINISHED'}


class RemoveLevelEditorInfoFromObject(bpy.types.Operator):
	bl_idname = "object.remove_level_editor_info"
	bl_label = "Remove level editor info from object"
	bl_options = {'REGISTER', 'UNDO'}
	
	index: bpy.props.IntProperty(name="index", default=0)

	def execute(self, context):
		bpy.context.object.level_editor_info.remove(self.index)
		return {'FINISHED'}

class RemoveLevelEditorInfoFromCollection(bpy.types.Operator):
	bl_idname = "collection.remove_level_editor_info"
	bl_label = "Remove level editor info from collection"
	bl_options = {'REGISTER', 'UNDO'}
	
	index: bpy.props.IntProperty(name="index", default=0)

	def execute(self, context):
		bpy.context.collection.level_editor_info.remove(self.index)
		return {'FINISHED'}


def getPropertyTypes(self, context):
	return [(x.string_value, x.string_value, x.string_value) for x in bpy.context.preferences.addons['santas_level_editor'].preferences.property_types]
class EditorInfoPropertyGroup(bpy.types.PropertyGroup):
	info_type: bpy.props.EnumProperty(
		items=getPropertyTypes,
		name="Type")
	info_value: bpy.props.StringProperty(name="Value")


class LevelEditorObjectInfoPanel(bpy.types.Panel):
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
		
		layout.operator("object.add_level_editor_info")
		
		current_index = 0
		for item in level_editor_info:
			box = layout.box()
			row = box.row()
			sub = row.row()
			sub.scale_x = 1.25
			sub.prop(item, "info_type")
			row.prop(item, "info_value")
			sub = row.row()
			sub.scale_x = 0.5
			op = sub.operator("object.remove_level_editor_info", text="–")
			op.index = current_index
			current_index += 1

		row = layout.row()
		row.operator("object.copy_level_editor_info")
		row.operator("object.paste_level_editor_info")


class LevelEditorCollectionInfoPanel(bpy.types.Panel):
	bl_label = "Santa's Level Editor Info"
	bl_idname = "collection_PT_layout"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = "collection"

	def draw(self, context):
		if not hasattr(bpy.types.Collection, 'level_editor_info'):
			return
		collection = context.collection
		layout = self.layout
		level_editor_info = collection.level_editor_info

		layout.operator("collection.add_level_editor_info")
		
		current_index = 0
		for item in level_editor_info:
			box = layout.box()
			row = box.row()
			sub = row.row()
			sub.scale_x = 1.25
			sub.prop(item, "info_type")
			row.prop(item, "info_value")
			sub = row.row()
			sub.scale_x = 0.5
			op = sub.operator("collection.remove_level_editor_info", text="–")
			op.index = current_index
			current_index += 1

		row = layout.row()
		row.operator("collection.copy_level_editor_info")
		row.operator("collection.paste_level_editor_info")


classes = (
	CopyLevelEditorInfoFromObject,
	PasteLevelEditorInfoToObject,
	CopyLevelEditorInfoFromCollection,
	PasteLevelEditorInfoToCollection,
	AddLevelEditorInfoToObject,
	AddLevelEditorInfoToCollection,
	RemoveLevelEditorInfoFromObject,
	RemoveLevelEditorInfoFromCollection,
	EditorInfoPropertyGroup,
	LevelEditorObjectInfoPanel,
	LevelEditorCollectionInfoPanel,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.Object.level_editor_info = bpy.props.CollectionProperty(type=EditorInfoPropertyGroup)
	bpy.types.Collection.level_editor_info = bpy.props.CollectionProperty(type=EditorInfoPropertyGroup)

def unregister():
	if hasattr(bpy.types.Object, 'level_editor_info'):
		del bpy.types.Object.level_editor_info
	if hasattr(bpy.types.Collection, 'level_editor_info'):
		del bpy.types.Collection.level_editor_info
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)


if __name__ == "__main__":
	register()

import santas_level_editor.add_menu as add_menu
import santas_level_editor.json_exporter as json_exporter
import santas_level_editor.obj_tree_exporter as obj_tree_exporter
import santas_level_editor.per_object_info as per_object_info
import bpy_extras.io_utils
import json
import bpy
import os

bl_info = {
	"name": "Santa's level editor",
	"blender": (2, 80, 0),
	"category": "Object",
}

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

class LoadPreferencesFromJson(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
	bl_idname = "preferences.load_from_json"
	bl_label = "Load from json"
	bl_options = {'REGISTER', 'UNDO'}
	filter_glob: bpy.props.StringProperty(
		default='*.json',
		options={'HIDDEN'}
	)
	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences

		with open(self.filepath, 'r') as json_file:
			json_object = json.loads(json_file.read())
			if "object_models_folder" not in json_object.keys():
				prefs.object_models_folder = ''
			elif ":" in json_object["object_models_folder"] or json_object["object_models_folder"][0] in '\\/': # is absolute path
				prefs.object_models_folder = json_object["object_models_folder"]
			else: # is relative path
				prefs.object_models_folder = os.path.join(os.path.dirname(self.filepath), json_object["object_models_folder"])
			prefs.location_filter_pattern = json_object["location_filter_pattern"]
			prefs.rotation_filter_pattern = json_object["rotation_filter_pattern"]
			prefs.scale_filter_pattern = json_object["scale_filter_pattern"]
			prefs.property_types.clear()
			for item in json_object["property_types"]:
				prefs.property_types.add()
				prefs.property_types.items()[-1][1].string_value = item

		# register new
		classes, reg = add_menu.generate_code_from_folder(prefs.object_models_folder)
		if len(classes) > 0: # if user specified valid folder
			bpy.types.VIEW3D_MT_add.remove(add_menu.menu_func)
			exec(classes)
			exec(reg)
			bpy.types.VIEW3D_MT_add.append(add_menu.menu_func)

		return {'FINISHED'}

class LoadModelsFolder(bpy.types.Operator):
	bl_idname = "preferences.load_models_folder"
	bl_label = "Load models folder"
	bl_options = {'REGISTER', 'UNDO'}
	def execute(self, context):
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences

		# register new
		classes, reg = add_menu.generate_code_from_folder(prefs.object_models_folder)
		if len(classes) > 0: # if user specified valid folder
			bpy.types.VIEW3D_MT_add.remove(add_menu.menu_func)
			exec(classes)
			exec(reg)
			bpy.types.VIEW3D_MT_add.append(add_menu.menu_func)
		return {'FINISHED'}

class LevelEditorAddObject(bpy.types.Operator):
	bl_idname = "mesh.add_level_editor_object"
	bl_label = "Add level editor object"
	bl_options = {'REGISTER', 'UNDO'}
	object_name: bpy.props.StringProperty(name="object_name", default="Unknown")
	relative_path: bpy.props.StringProperty(name="relative_path", default="Unknown")

	def execute(self,context):
		import os
		import random
		
		prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
		full_object_path = os.path.join(prefs.object_models_folder, self.relative_path)

		original_objs = set(bpy.data.objects)
		bpy.ops.wm.obj_import(
			filepath=full_object_path,
			forward_axis='Y',
			up_axis='Z'
			)

		imported_objs = set(bpy.data.objects) - original_objs
		if len(imported_objs) != 1:
			print(f"Expecting to import 1 object, but got {len(imported_objs)} instead")
		for obj in imported_objs:
			random_alphanumeric = "%032x" % random.getrandbits(128)
			obj.name = f"{self.object_name}.{random_alphanumeric[:6]}"
			obj.location = bpy.context.scene.cursor.location
		return {'FINISHED'}


class LevelEditorAddonPreferences(bpy.types.AddonPreferences):
	bl_idname = __name__
	object_models_folder: bpy.props.StringProperty(name="Object models folder")
	location_filter_pattern: bpy.props.StringProperty(name="Location filter pattern")
	rotation_filter_pattern: bpy.props.StringProperty(name="Rotation filter pattern")
	scale_filter_pattern: bpy.props.StringProperty(name="Scale filter pattern")
	property_types: bpy.props.CollectionProperty(type=EditorInfoPropertyTypeGroup)
	copied_level_editor_info = []
	def draw(self, context):
		preferences = bpy.context.preferences.addons['santas_level_editor'].preferences
		layout = self.layout
		row = layout.row()
		row.prop(preferences, "object_models_folder")
		sub = row.row()
		sub.scale_x = 0.4
		sub.operator("preferences.load_models_folder", text="Load")
		layout.prop(preferences, "location_filter_pattern")
		layout.prop(preferences, "rotation_filter_pattern")
		layout.prop(preferences, "scale_filter_pattern")

		level_editor_property_types = preferences.property_types
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

		layout.operator("preferences.load_from_json")

classes = (
	EditorInfoPropertyTypeGroup,
	AddLevelEditorPropertyTypeToPreferences,
	RemoveLevelEditorPropertyTypeFromPreferences,
	LoadPreferencesFromJson,
	LevelEditorAddonPreferences,
	LoadModelsFolder,
	LevelEditorAddObject,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	per_object_info.register()
	json_exporter.register()
	obj_tree_exporter.register()

	prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
	menu_classes, menu_register = add_menu.generate_code_from_folder(prefs.object_models_folder)
	if len(menu_classes) > 0: # if user specified valid folder
		exec(menu_classes)
		exec(menu_register)
		bpy.types.VIEW3D_MT_add.append(add_menu.menu_func)


def unregister():
	bpy.types.VIEW3D_MT_add.remove(add_menu.menu_func)

	obj_tree_exporter.unregister()
	json_exporter.unregister()
	per_object_info.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)

if __name__ == "__main__":
	register()
import bpy
import json


def list_from_info_attribute(info_attribute):
	to_return = []
	for info_item in info_attribute:
		to_return.append({"type": info_item.info_type, "value": info_item.info_value})
	return to_return

def per_collection_function(col, result, json_root_key, parent_info):
	parent_info = col.level_editor_info if len(col.level_editor_info) > 0 else parent_info
	for obj in col.objects:
		prev_rotation_mode = obj.rotation_mode
		
		obj.rotation_mode = 'XYZ'
		if "." in obj.name:
			obj_type = obj.name.split('.')[0]
		else:
			obj_type = obj.name
		new_object = {}
		new_object["type"] = obj_type
		new_object["position"] = [obj.location[0], obj.location[1], obj.location[2]]
		new_object["rotation"] = [obj.rotation_euler[0], obj.rotation_euler[1], obj.rotation_euler[2]]
		if len(obj.level_editor_info) > 0 or parent_info is None:
			new_object["properties"] = list_from_info_attribute(obj.level_editor_info)
		else:
			new_object["properties"] = list_from_info_attribute(parent_info)

		result[json_root_key].append(new_object)
		
		obj.rotation_mode = prev_rotation_mode


def recursive_function(collection, result, json_root_key="objects", parent_info=None):
	per_collection_function(collection, result, json_root_key, parent_info)
	for child in collection.children:
		recursive_function(child, result, json_root_key, parent_info=collection.level_editor_info if len(collection.level_editor_info) > 0 else parent_info)

def export_santa_level(output_file_path, level_collection_name="Level", json_root_key="objects"):
	result = {json_root_key: []}

	target_collection = None
	for col in bpy.data.collections:
		if col.name == level_collection_name:
			target_collection = col
			break

	if target_collection is None:
		print("Could not find collection")
		return False

	recursive_function(target_collection, result, json_root_key)

	with open(output_file_path, 'w') as output_file:
		output_file.write(json.dumps(result, indent='\t'))
		print(f"File written: {output_file_path}")
	return True



from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportSantaLevel(Operator, ExportHelper):
	bl_idname = "export_santa.level"
	bl_label = "Export Santa Level"

	filename_ext = ".json"

	filter_glob: StringProperty(
		default="*.json",
		options={'HIDDEN'},
		maxlen=255,  # Max internal buffer length, longer would be clamped.
	)

	level_collection_name_property: StringProperty(
		name="Level Collection Name",
		default="Level",
	)
	json_root_key_property: StringProperty(
		name="JSON root key",
		default="objects",
	)

	def execute(self, context):
		export_santa_level(self.filepath, self.level_collection_name_property, self.json_root_key_property)
		return {'FINISHED'}


def menu_func_export(self, context):
	self.layout.operator(ExportSantaLevel.bl_idname, text="Export Santa level")


def register():
	bpy.utils.register_class(ExportSantaLevel)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
	bpy.utils.unregister_class(ExportSantaLevel)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
	register()

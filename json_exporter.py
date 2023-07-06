import re
import bpy
import json


def list_from_info_attribute(info_attribute):
	to_return = []
	for info_item in info_attribute:
		to_return.append({"type": info_item.info_type, "value": info_item.info_value})
	return to_return

def per_collection_function(col, result, json_root_key, parent_info):
	prefs = bpy.context.preferences.addons['santas_level_editor'].preferences
	for obj in col.objects:
		prev_rotation_mode = obj.rotation_mode
		
		obj.rotation_mode = 'XYZ'
		if "." in obj.name:
			obj_type = obj.name.split('.')[0]
		else:
			obj_type = obj.name
		new_object = {}
		new_object["type"] = obj_type
		if obj.location.magnitude != 0.0:
			if len(prefs.location_filter_pattern) == 0 or re.match(prefs.location_filter_pattern, obj_type):
				new_object["position"] = [obj.location[0], obj.location[1], obj.location[2]]
		if abs(obj.rotation_euler[0]) != 0 or abs(obj.rotation_euler[1]) != 0 or abs(obj.rotation_euler[2]) != 0:
			if len(prefs.rotation_filter_pattern) == 0 or re.match(prefs.rotation_filter_pattern, obj_type):
				new_object["rotation"] = [obj.rotation_euler[0], obj.rotation_euler[1], obj.rotation_euler[2]]
		if obj.scale[0] != 1.0 or obj.scale[1] != 1.0 or obj.scale[2] != 1.0:
			if len(prefs.scale_filter_pattern) == 0 or re.match(prefs.scale_filter_pattern, obj_type):
				new_object["scale"] = [obj.scale[0], obj.scale[1], obj.scale[2]]
		new_object["properties"] = list_from_info_attribute(obj.level_editor_info)
		new_object["properties"].extend(parent_info)

		result[json_root_key].append(new_object)
		
		obj.rotation_mode = prev_rotation_mode


def recursive_function(collection, result, json_root_key="objects", parent_info=None):
	if parent_info is None:
		parent_info = []
	else:
		parent_info = [x for x in parent_info]
	parent_info.extend(list_from_info_attribute(collection.level_editor_info))
	per_collection_function(collection, result, json_root_key, parent_info)
	for child in collection.children:
		recursive_function(child, result, json_root_key=json_root_key, parent_info=parent_info)

def export_santa_level(output_file_path, level_collection_name, json_root_key):
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
	bl_label = "Export Santa level"

	filename_ext = ".json"

	filter_glob: StringProperty(
		default="*.json",
		options={'HIDDEN'},
		maxlen=255,  # Max internal buffer length, longer would be clamped.
	)

	level_collection_name_property: StringProperty(
		name="Level Collection Name",
		default="Collection",
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

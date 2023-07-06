import os
import bpy
import mathutils


def recursive_function(currentPath, collection, isRootCall=True):

    if not isRootCall:
        currentPath = f"{currentPath}\\{collection.name}"
    os.makedirs(currentPath, exist_ok=True)
    # export objs
    for object in collection.objects:
        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        original_location = object.location.copy()
        object.location = mathutils.Vector((0.0, 0.0, 0.0))
        bpy.ops.export_scene.obj(
            filepath=f"{currentPath}\\{object.name}.obj",
            axis_forward="Y",
            axis_up="Z",
            use_materials=False,
            use_selection=True
        )
        object.location = original_location
    for col in collection.children:
        recursive_function(currentPath, col, False)

def export_santa_obj_tree(output_folder_path, target_collection_name):

	target_collection = None
	for col in bpy.data.collections:
	    if col.name == target_collection_name:
	        target_collection = col
	        break

	recursive_function(output_folder_path, target_collection)



from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty
from bpy.types import Operator


class ExportSantaObjTree(Operator, ExportHelper):
	bl_idname = "export_santa.obj_tree"
	bl_label = "Export obj tree"

	filename_ext = ""

	target_collection_name_property: StringProperty(
		name="Target collection name",
		default="Collection",
	)

	def execute(self, context):
		folderpath = self.properties.filepath
		export_santa_obj_tree(folderpath, self.target_collection_name_property)
		return {'FINISHED'}


def menu_func_export(self, context):
	self.layout.operator(ExportSantaObjTree.bl_idname, text="Export obj tree for Santa level")


def register():
	bpy.utils.register_class(ExportSantaObjTree)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
	bpy.utils.unregister_class(ExportSantaObjTree)
	bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
	register()

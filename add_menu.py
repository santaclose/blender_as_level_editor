import os
import bpy
from bpy.props import (StringProperty, BoolProperty,IntProperty,FloatProperty,FloatVectorProperty,EnumProperty,PointerProperty)
from bpy.types import (Panel,Operator,AddonPreferences,PropertyGroup)


def menu_func(self, context):
	self.layout.menu("LevelEditorAddSubmenuGroup_0", text="Level editor object")

def generate_code_from_folder(folder):

	if not os.path.isdir(folder):
		return "", "", "[]"

	def path_to_dict(path, root_call = True):
		if root_call and (path[-1] == '\\' or path[-1] == '/'):
			path = path[:-1]
		d = {'name': os.path.basename(path)}
		if os.path.isdir(path):
			d['type'] = "directory"
			# folders first
			d['children'] = [path_to_dict(os.path.join(path,x), False) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
			d['children'].extend([path_to_dict(os.path.join(path,x), False) for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))])
		else:
			d['type'] = "file"
		return d

	FileTree = path_to_dict(folder)

	SubmenuOperatorFunction = """
class LevelEditorAddSubmenuOperator(bpy.types.Operator):
	bl_idname = "mesh.generic_effector"
	bl_label = "Add Generic Effector"
	bl_options = {'REGISTER', 'UNDO'}
	id: bpy.props.StringProperty(name="id", default="Unknown")

	def execute(self,context):
		print(f"{id}")
		return {'FINISHED'}
"""

	SubmenuLevelMenuTemplate = """
class LevelEditorAddSubmenuGroup_GROUP_ID(bpy.types.Menu):
	bl_idname = "LevelEditorAddSubmenuGroup_GROUP_ID"
	bl_label = "Level editor object"
	bl_options = {'REGISTER', 'UNDO'}

	def draw(self, context):
		layout = self.layout

CODE
"""

	def BuildMenuCode(FileTreeObject, CodeToRun = "", GroupIdCounter = 0):

		CurrentGroupId = GroupIdCounter
		FileTreeObject['group_id'] = CurrentGroupId
		GroupIdCounter += 1

		for i, x in enumerate([x for x in FileTreeObject['children'] if x['type'] == 'directory']):
			CodeToRun, GroupIdCounter = BuildMenuCode(x, CodeToRun, GroupIdCounter)
		CodeSection = ""
		for i, x in enumerate([x for x in FileTreeObject['children'] if x['type'] == 'directory']):
			CodeSection += f'\t\tlayout.menu("LevelEditorAddSubmenuGroup_{x["group_id"]}", text="{x["name"]}")\n'
		for i, x in enumerate([x for x in FileTreeObject['children'] if x['type'] == 'file']):
			CodeSection += f'\t\top = layout.operator("mesh.generic_effector", text="{x["name"][:x["name"].rfind(".")]}")\n'
			CodeSection += f'\t\top.id = "{x["name"][:x["name"].rfind(".")]}"\n'
		CodeToRun += SubmenuLevelMenuTemplate.replace("GROUP_ID", str(CurrentGroupId)).replace("CODE", CodeSection)
		return CodeToRun, GroupIdCounter

	ClassDefinitionsCode, GroupIdCounter = BuildMenuCode(FileTree)
	ClassDefinitionsCode += SubmenuOperatorFunction
	ClassDefinitionsCode = ClassDefinitionsCode.replace('    ', '\t') # not sure why it contains spaces

	RegisterCode = "bpy.utils.register_class(LevelEditorAddSubmenuOperator)\n"
	RegisterCode += "\n".join([f"bpy.utils.register_class(LevelEditorAddSubmenuGroup_{x})" for x in reversed(range(GroupIdCounter))])

	# UnregisterCode = "\n".join([f"bpy.utils.unregister_class(LevelEditorAddSubmenuGroup_{x})" for x in range(GroupIdCounter)])
	# UnregisterCode += "\nbpy.utils.unregister_class(LevelEditorAddSubmenuOperator)"
	ClassListExpr = "[" + ', '.join([f'LevelEditorAddSubmenuGroup_{x}' for x in reversed(range(GroupIdCounter))]) + "]"

	return ClassDefinitionsCode, RegisterCode, ClassListExpr


# ----------------------- REGISTER ---------------------

# def register():
# 	bpy.utils.register_class(LevelEditorAddSubmenuOperator)
# 	[exec(f"from bpy.utils import register_class\nregister_class(LevelEditorAddSubmenuGroup_{x})") for x in reversed(range(GroupIdCounter))]
# 	bpy.types.VIEW3D_MT_add.append(menu_func)

# def unregister():
# 	[exec(f"from bpy.utils import unregister_class\nunregister_class(LevelEditorAddSubmenuGroup_{x})") for x in range(GroupIdCounter)]
# 	bpy.utils.unregister_class(LevelEditorAddSubmenuOperator)
# 	bpy.types.VIEW3D_MT_add.remove(menu_func)

# if __name__ == "__main__":
# 	register()

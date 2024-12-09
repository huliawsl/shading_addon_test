import os

import bpy
from ..config import __addon_name__
from ..preference.AddonPreferences import ExampleAddonPreferences


# This Example Operator will scale up the selected object
class ExampleOperator(bpy.types.Operator):
    '''ExampleAddon'''
    bl_idname = "object.example_ops"
    bl_label = "ExampleOperator"

    # 确保在操作之前备份数据，用户撤销操作时可以恢复
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        addon_prefs = bpy.context.preferences.addons[__addon_name__].preferences
        assert isinstance(addon_prefs, ExampleAddonPreferences)
        # use operator
        # bpy.ops.transform.resize(value=(2, 2, 2))

        # manipulate the scale directly


        # 文件路径
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "untitled.blend")
        # print(file_path)
        # 读取.blend文件
        with bpy.data.libraries.load(file_path) as (data_from, data_to):
            # 选择要加载的节点组名称
            data_to.node_groups = [name for name in data_from.node_groups if name == "cartoon"]

        # 检查节点组是否加载成功
        if "cartoon" in bpy.data.node_groups:
            cartoon_node_group = bpy.data.node_groups["cartoon"]

            # 创建新的材质并使用加载的节点组
            new_material = bpy.data.materials.new(name="CartoonMaterial")
            new_material.use_nodes = True

            # 获取材质的节点树
            node_tree = new_material.node_tree
            nodes = node_tree.nodes

            # 清空旧节点（可选）
            for node in nodes:
                nodes.remove(node)

            # 将加载的节点组实例化
            instantiated_node = nodes.new("ShaderNodeGroup")
            instantiated_node.node_tree = cartoon_node_group

            # 设置材质的输出节点
            output_node = nodes.new("ShaderNodeOutputMaterial")

            # 创建连接
            links = node_tree.links
            links.new(instantiated_node.outputs[0], output_node.inputs[0])

            # 将新的材质应用到当前选中的对象（可选）
            if bpy.context.active_object:
                if bpy.context.active_object.data.materials:
                    bpy.context.active_object.data.materials[0] = new_material
                else:
                    bpy.context.active_object.data.materials.append(new_material)

        black_material = bpy.data.materials.new(name="BlackMaterial")
        black_material.use_nodes = True

        # 获取材质的节点树
        black_node_tree = black_material.node_tree
        black_nodes = black_node_tree.nodes
        black_nodes.clear()

        # 创建一个 RGB 节点将颜色设置为黑色
        rgb_node = black_nodes.new(type="ShaderNodeRGB")
        rgb_node.outputs[0].default_value = (0, 0, 0, 1)  # 设置为黑色 (R, G, B, Alpha)

        # 创建输出节点
        black_output_node = black_nodes.new("ShaderNodeOutputMaterial")

        # 创建连接
        black_links = black_node_tree.links
        black_links.new(rgb_node.outputs[0], black_output_node.inputs[0])
        bpy.context.object.active_material.use_backface_culling = True
        black_material.use_backface_culling = True
        # 将黑色材质应用到当前选中对象的材质槽中
        if bpy.context.active_object.data.materials:
            bpy.context.active_object.data.materials.append(black_material)
        else:
            bpy.context.active_object.data.materials.append(black_material)

        bpy.ops.object.shade_smooth(use_auto_smooth=True)

        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = 0.02
        bpy.context.object.modifiers["Solidify"].offset = 1
        bpy.context.object.modifiers["Solidify"].use_rim = False
        bpy.context.object.modifiers["Solidify"].use_flip_normals = True
        bpy.context.object.modifiers["Solidify"].material_offset = 10



        return {'FINISHED'}

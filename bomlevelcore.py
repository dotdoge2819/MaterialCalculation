import pandas as pd
from collections import defaultdict
import os
import sys

class BOMLevelCalculator:
    def __init__(self, file_name="bom.xlsx"):
        # 获取绝对路径，适配打包环境
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.file_path = os.path.join(base_path, file_name)
        self.recipe_map = self._load_recipes()

    def _load_recipes(self):
        """解析 Excel 配方表"""
        try:
            df = pd.read_excel(self.file_path)
            df['产物'] = df['产物'].astype(str).str.strip()
            df['原料'] = df['原料'].astype(str).str.strip()
            
            recipes = defaultdict(list)
            for _, row in df.dropna(subset=['产物', '原料']).iterrows():
                recipes[row['产物']].append({
                    'ing': row['原料'],
                    'consume': float(row['单次原料消耗数量']),
                    'produce': float(row['单次产物数量'])
                })
            return recipes
        except Exception as e:
            print(f"读取文件 {self.file_path} 失败: {e}")
            return defaultdict(list)

    def calculate_by_level(self, target_item, amount, inventory):
        """
        API 入口：按层级统计材料缺口
        :param target_item: 目标物品
        :param amount: 目标数量
        :param inventory: 外部传入的初始库存字典 {"名称": 数量}
        :return: {level: {item_name: needed_qty}}
        """
        # 复制一份库存副本，避免修改原始外部变量
        current_inv = inventory.copy()
        # 结果集：{层级: {材料: 数量}}
        level_stats = defaultdict(lambda: defaultdict(float))
        
        self._recursive_level_calc(target_item, amount, 0, current_inv, level_stats)
        
        # 转换为普通字典并按层级排序输出
        return {k: dict(v) for k, v in sorted(level_stats.items())}

    def _recursive_level_calc(self, item, amount, level, inv, level_stats):
        # 1. 检查当前物品库存
        have = inv.get(item, 0)
        if have > 0:
            used = min(have, amount)
            inv[item] -= used
            amount -= used
            # 如果库存已经完全满足该层级的这个物品，直接返回
            if amount <= 0:
                return

        # 2. 如果当前物品还有缺口，且有配方，则拆解到下一层
        if item in self.recipe_map:
            for recipe in self.recipe_map[item]:
                # 计算这一层级所需的原料数量
                needed_qty = (amount / recipe['produce']) * recipe['consume']
                
                # 记录在下一层级的统计中
                level_stats[level + 1][recipe['ing']] += needed_qty
                
                # 递归处理下一层
                self._recursive_level_calc(recipe['ing'], needed_qty, level + 1, inv, level_stats)
        else:
            # 如果没有配方且仍有缺口，说明它是这一层级最终需要的基础原料
            # 注意：基础原料也会被记录在它出现的那个层级中
            pass
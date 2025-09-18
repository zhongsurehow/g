"""
易经哲学游戏机制设计
体现阴阳平衡、五行相生相克、变化之道等核心理念
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random

class YinYang(Enum):
    """阴阳属性"""
    YIN = "阴"    # 柔、静、收敛
    YANG = "阳"   # 刚、动、发散

class WuXing(Enum):
    """五行属性"""
    JIN = "金"    # 金 - 收敛、肃杀
    MU = "木"     # 木 - 生长、条达  
    SHUI = "水"   # 水 - 滋润、向下
    HUO = "火"    # 火 - 炎热、向上
    TU = "土"     # 土 - 承载、化育

@dataclass
class YinYangBalance:
    """阴阳平衡状态"""
    yin_points: int = 0
    yang_points: int = 0
    
    @property
    def balance_ratio(self) -> float:
        """计算阴阳平衡比例，越接近1越平衡"""
        total = self.yin_points + self.yang_points
        if total == 0:
            return 1.0
        smaller = min(self.yin_points, self.yang_points)
        return (smaller * 2) / total
    
    @property
    def dominant_aspect(self) -> Optional[YinYang]:
        """获取主导方面"""
        if self.yin_points > self.yang_points:
            return YinYang.YIN
        elif self.yang_points > self.yin_points:
            return YinYang.YANG
        return None
    
    def get_balance_bonus(self) -> int:
        """根据阴阳平衡程度获得奖励"""
        ratio = self.balance_ratio
        if ratio >= 0.8:  # 高度平衡
            return 3
        elif ratio >= 0.6:  # 中等平衡
            return 2
        elif ratio >= 0.4:  # 轻微平衡
            return 1
        return 0

class WuXingCycle:
    """五行相生相克循环"""
    
    # 五行相生：金生水，水生木，木生火，火生土，土生金
    SHENG_CYCLE = {
        WuXing.JIN: WuXing.SHUI,
        WuXing.SHUI: WuXing.MU,
        WuXing.MU: WuXing.HUO,
        WuXing.HUO: WuXing.TU,
        WuXing.TU: WuXing.JIN
    }
    
    # 五行相克：金克木，木克土，土克水，水克火，火克金
    KE_CYCLE = {
        WuXing.JIN: WuXing.MU,
        WuXing.MU: WuXing.TU,
        WuXing.TU: WuXing.SHUI,
        WuXing.SHUI: WuXing.HUO,
        WuXing.HUO: WuXing.JIN
    }
    
    @classmethod
    def get_sheng_target(cls, element: WuXing) -> WuXing:
        """获取相生目标"""
        return cls.SHENG_CYCLE[element]
    
    @classmethod
    def get_ke_target(cls, element: WuXing) -> WuXing:
        """获取相克目标"""
        return cls.KE_CYCLE[element]
    
    @classmethod
    def is_sheng_relationship(cls, source: WuXing, target: WuXing) -> bool:
        """判断是否为相生关系"""
        return cls.SHENG_CYCLE[source] == target
    
    @classmethod
    def is_ke_relationship(cls, source: WuXing, target: WuXing) -> bool:
        """判断是否为相克关系"""
        return cls.KE_CYCLE[source] == target

@dataclass
class BianguaTransformation:
    """变卦机制 - 体现易经变化之道"""
    original_gua: str
    transformed_gua: str
    trigger_condition: str
    effect_description: str
    
    def can_transform(self, game_context: Dict) -> bool:
        """检查是否满足变卦条件"""
        # 这里可以根据具体的触发条件来判断
        # 例如：特定的资源组合、时机、玩家状态等
        return True  # 简化实现

class TaijiMechanism:
    """太极机制 - 体现阴阳转化"""
    
    @staticmethod
    def calculate_transformation_probability(yin_yang_balance: YinYangBalance) -> float:
        """计算阴阳转化概率"""
        # 极阴生阳，极阳生阴
        if yin_yang_balance.yin_points >= 10 and yin_yang_balance.yang_points <= 2:
            return 0.8  # 极阴转阳概率高
        elif yin_yang_balance.yang_points >= 10 and yin_yang_balance.yin_points <= 2:
            return 0.8  # 极阳转阴概率高
        return 0.1  # 正常转化概率低
    
    @staticmethod
    def apply_transformation(yin_yang_balance: YinYangBalance) -> YinYangBalance:
        """应用阴阳转化"""
        prob = TaijiMechanism.calculate_transformation_probability(yin_yang_balance)
        if random.random() < prob:
            # 发生转化：强势一方减少，弱势一方增加
            if yin_yang_balance.yin_points > yin_yang_balance.yang_points:
                yin_yang_balance.yin_points -= 3
                yin_yang_balance.yang_points += 2
            else:
                yin_yang_balance.yang_points -= 3
                yin_yang_balance.yin_points += 2
        return yin_yang_balance

class ZhouYiWisdom:
    """周易智慧格言系统"""
    
    WISDOM_QUOTES = {
        "自强不息": "天行健，君子以自强不息",
        "厚德载物": "地势坤，君子以厚德载物", 
        "学而时习": "学而时习之，不亦说乎",
        "知者不惑": "知者不惑，仁者不忧，勇者不惧",
        "穷则变": "穷则变，变则通，通则久",
        "中庸之道": "君子中庸，小人反中庸",
        "阴阳调和": "一阴一阳之谓道",
        "五行相生": "五行相生，万物化育"
    }
    
    @classmethod
    def get_random_wisdom(cls) -> Tuple[str, str]:
        """获取随机智慧格言"""
        key = random.choice(list(cls.WISDOM_QUOTES.keys()))
        return key, cls.WISDOM_QUOTES[key]
    
    @classmethod
    def trigger_wisdom(cls, condition: str) -> Optional[str]:
        """根据条件触发相应智慧"""
        wisdom_map = {
            "balance_achieved": "阴阳调和",
            "wuxing_harmony": "五行相生", 
            "dao_progress": "自强不息",
            "study_action": "学而时习",
            "transformation": "穷则变"
        }
        
        wisdom_key = wisdom_map.get(condition)
        if wisdom_key:
            return cls.WISDOM_QUOTES[wisdom_key]
        return None

class ZhanBuSystem:
    """占卜系统 - 易经的核心功能"""
    
    @classmethod
    def divine_fortune(cls, player_dao_xing: int) -> Dict[str, any]:
        """占卜运势，道行越高准确度越高"""
        # 基础准确度基于道行
        accuracy = min(0.5 + (player_dao_xing * 0.05), 0.95)
        
        # 生成卦象
        gua_names = list(GUA_ATTRIBUTES.keys())
        primary_gua = random.choice(gua_names)
        
        # 根据准确度决定是否给出正确指引
        is_accurate = random.random() < accuracy
        
        # 运势类型
        fortune_types = ["大吉", "中吉", "小吉", "平", "小凶", "中凶", "大凶"]
        weights = [1, 2, 3, 4, 3, 2, 1] if is_accurate else [1, 1, 1, 1, 1, 1, 1]
        fortune = random.choices(fortune_types, weights=weights)[0]
        
        # 建议行动
        actions = {
            "大吉": "宜进取，宜变革，宜学习",
            "中吉": "宜稳进，宜修行，宜合作", 
            "小吉": "宜谨慎，宜积累，宜观察",
            "平": "宜中庸，宜平衡，宜等待",
            "小凶": "宜守成，宜内省，宜化解",
            "中凶": "宜退避，宜修德，宜求助",
            "大凶": "宜静止，宜忏悔，宜转化"
        }
        
        return {
            "gua": primary_gua,
            "fortune": fortune,
            "advice": actions[fortune],
            "accuracy": accuracy,
            "is_accurate": is_accurate
        }
    
    @classmethod
    def divine_action_outcome(cls, action_type: str, player_dao_xing: int) -> bool:
        """占卜特定行动的成功率"""
        base_success = 0.5
        dao_bonus = player_dao_xing * 0.03
        
        # 不同行动的基础成功率调整
        action_modifiers = {
            "meditate": 0.1,    # 冥想较容易成功
            "study": 0.05,      # 学习中等难度
            "transform": -0.1,  # 变卦较困难
            "wuxing": 0.0       # 五行中性
        }
        
        modifier = action_modifiers.get(action_type, 0)
        success_rate = min(base_success + dao_bonus + modifier, 0.9)
        
        return random.random() < success_rate

# 卦象属性映射
GUA_ATTRIBUTES = {
    "乾": {"yin_yang": YinYang.YANG, "wuxing": WuXing.JIN, "nature": "刚健"},
    "坤": {"yin_yang": YinYang.YIN, "wuxing": WuXing.TU, "nature": "柔顺"},
    "震": {"yin_yang": YinYang.YANG, "wuxing": WuXing.MU, "nature": "动"},
    "巽": {"yin_yang": YinYang.YIN, "wuxing": WuXing.MU, "nature": "入"},
    "坎": {"yin_yang": YinYang.YANG, "wuxing": WuXing.SHUI, "nature": "陷"},
    "离": {"yin_yang": YinYang.YIN, "wuxing": WuXing.HUO, "nature": "丽"},
    "艮": {"yin_yang": YinYang.YANG, "wuxing": WuXing.TU, "nature": "止"},
    "兑": {"yin_yang": YinYang.YIN, "wuxing": WuXing.JIN, "nature": "悦"}
}

def get_gua_synergy_bonus(gua1: str, gua2: str) -> int:
    """计算卦象协同奖励"""
    if gua1 not in GUA_ATTRIBUTES or gua2 not in GUA_ATTRIBUTES:
        return 0
    
    attr1 = GUA_ATTRIBUTES[gua1]
    attr2 = GUA_ATTRIBUTES[gua2]
    
    bonus = 0
    
    # 阴阳互补奖励
    if attr1["yin_yang"] != attr2["yin_yang"]:
        bonus += 2
    
    # 五行相生奖励
    if WuXingCycle.is_sheng_relationship(attr1["wuxing"], attr2["wuxing"]):
        bonus += 3
    
    # 五行相克惩罚
    if WuXingCycle.is_ke_relationship(attr1["wuxing"], attr2["wuxing"]):
        bonus -= 1
    
    return max(0, bonus)
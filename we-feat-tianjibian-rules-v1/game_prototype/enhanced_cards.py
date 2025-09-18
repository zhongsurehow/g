"""
增强的卡牌系统
提供更丰富的策略选择和易经元素融合
"""

import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from game_state import Player, GameState, Zone
from yijing_mechanics import YinYang, WuXing

class CardType(Enum):
    """卡牌类型"""
    BASIC = "基础"
    ADVANCED = "进阶"
    MASTER = "大师"
    LEGENDARY = "传说"

class CardEffect(Enum):
    """卡牌效果类型"""
    RESOURCE_GAIN = "资源获得"
    INFLUENCE_BOOST = "影响力增强"
    MOVEMENT = "移动"
    TRANSFORMATION = "变化"
    PROTECTION = "防护"
    DISRUPTION = "干扰"
    SYNERGY = "协同"
    CULTIVATION = "修行"

@dataclass
class EnhancedCard:
    """增强卡牌数据结构"""
    id: str
    name: str
    type: CardType
    cost: int
    description: str
    associated_guas: List[str]
    effects: List[CardEffect]
    
    # 易经属性
    yin_yang_affinity: Optional[YinYang] = None
    wuxing_affinity: Optional[WuXing] = None
    
    # 效果数值
    qi_bonus: int = 0
    dao_xing_bonus: int = 0
    cheng_yi_bonus: int = 0
    influence_bonus: int = 0
    
    # 特殊效果
    special_effect: Optional[str] = None
    combo_cards: List[str] = None  # 组合卡牌
    
    def __post_init__(self):
        if self.combo_cards is None:
            self.combo_cards = []

class EnhancedCardDatabase:
    """增强卡牌数据库"""
    
    def __init__(self):
        self.cards = self._initialize_cards()
    
    def _initialize_cards(self) -> Dict[str, EnhancedCard]:
        """初始化卡牌数据库"""
        cards = {}
        
        # 基础卡牌系列
        cards["qian_basic"] = EnhancedCard(
            id="qian_basic",
            name="乾·天行健",
            type=CardType.BASIC,
            cost=1,
            description="天行健，君子以自强不息",
            associated_guas=["乾"],
            effects=[CardEffect.RESOURCE_GAIN, CardEffect.CULTIVATION],
            yin_yang_affinity=YinYang.YANG,
            qi_bonus=2,
            dao_xing_bonus=1,
            special_effect="连续使用时效果递增"
        )
        
        cards["kun_basic"] = EnhancedCard(
            id="kun_basic",
            name="坤·厚德载物",
            type=CardType.BASIC,
            cost=1,
            description="地势坤，君子以厚德载物",
            associated_guas=["坤"],
            effects=[CardEffect.RESOURCE_GAIN, CardEffect.PROTECTION],
            yin_yang_affinity=YinYang.YIN,
            cheng_yi_bonus=2,
            influence_bonus=1,
            special_effect="为其他卡牌提供稳定加成"
        )
        
        cards["zhen_basic"] = EnhancedCard(
            id="zhen_basic",
            name="震·雷动九天",
            type=CardType.BASIC,
            cost=1,
            description="震惊百里，不丧匕鬯",
            associated_guas=["震"],
            effects=[CardEffect.INFLUENCE_BOOST, CardEffect.DISRUPTION],
            yin_yang_affinity=YinYang.YANG,
            wuxing_affinity=WuXing.MU,
            influence_bonus=2,
            qi_bonus=1,
            special_effect="可以打断对手的连击"
        )
        
        # 进阶卡牌系列
        cards["taiji_harmony"] = EnhancedCard(
            id="taiji_harmony",
            name="太极·阴阳调和",
            type=CardType.ADVANCED,
            cost=2,
            description="太极生两仪，阴阳相调和",
            associated_guas=["乾", "坤"],
            effects=[CardEffect.TRANSFORMATION, CardEffect.SYNERGY],
            qi_bonus=1,
            dao_xing_bonus=2,
            cheng_yi_bonus=1,
            special_effect="平衡阴阳，获得额外回合",
            combo_cards=["qian_basic", "kun_basic"]
        )
        
        cards["wuxing_cycle"] = EnhancedCard(
            id="wuxing_cycle",
            name="五行·相生相克",
            type=CardType.ADVANCED,
            cost=3,
            description="五行相生相克，循环不息",
            associated_guas=["震", "巽", "离", "坤", "兑", "乾", "坎", "艮"],
            effects=[CardEffect.TRANSFORMATION, CardEffect.CULTIVATION],
            dao_xing_bonus=3,
            influence_bonus=2,
            special_effect="根据五行亲和度获得不同效果"
        )
        
        cards["biangua_master"] = EnhancedCard(
            id="biangua_master",
            name="变卦·穷则变通",
            type=CardType.ADVANCED,
            cost=2,
            description="穷则变，变则通，通则久",
            associated_guas=["所有卦象"],
            effects=[CardEffect.TRANSFORMATION, CardEffect.MOVEMENT],
            cheng_yi_bonus=2,
            dao_xing_bonus=1,
            special_effect="可以改变任意卦象的控制权"
        )
        
        # 大师级卡牌
        cards["tianren_heyi"] = EnhancedCard(
            id="tianren_heyi",
            name="天人合一",
            type=CardType.MASTER,
            cost=4,
            description="天人合一，万物与我为一",
            associated_guas=["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"],
            effects=[CardEffect.CULTIVATION, CardEffect.SYNERGY, CardEffect.TRANSFORMATION],
            qi_bonus=3,
            dao_xing_bonus=3,
            cheng_yi_bonus=2,
            special_effect="获得所有位置的修行加成"
        )
        
        cards["wuwei_zhizhi"] = EnhancedCard(
            id="wuwei_zhizhi",
            name="无为而治",
            type=CardType.MASTER,
            cost=3,
            description="无为而无不为，无治而无不治",
            associated_guas=["坤", "艮"],
            effects=[CardEffect.PROTECTION, CardEffect.CULTIVATION],
            dao_xing_bonus=4,
            cheng_yi_bonus=1,
            special_effect="免疫所有负面效果，获得持续收益"
        )
        
        # 传说级卡牌
        cards["zhouyi_zhihui"] = EnhancedCard(
            id="zhouyi_zhihui",
            name="周易智慧",
            type=CardType.LEGENDARY,
            cost=5,
            description="易有太极，是生两仪，两仪生四象，四象生八卦",
            associated_guas=["所有卦象"],
            effects=[CardEffect.CULTIVATION, CardEffect.TRANSFORMATION, CardEffect.SYNERGY],
            qi_bonus=5,
            dao_xing_bonus=5,
            cheng_yi_bonus=3,
            special_effect="解锁所有易经奥秘，获得终极智慧"
        )
        
        # 组合效果卡牌
        cards["sancai_unity"] = EnhancedCard(
            id="sancai_unity",
            name="三才合一",
            type=CardType.ADVANCED,
            cost=3,
            description="天地人三才合一，通达宇宙奥秘",
            associated_guas=["乾", "坤", "震"],
            effects=[CardEffect.SYNERGY, CardEffect.CULTIVATION],
            qi_bonus=2,
            dao_xing_bonus=2,
            cheng_yi_bonus=2,
            special_effect="在天、地、人三个位置时效果翻倍"
        )
        
        cards["bagua_formation"] = EnhancedCard(
            id="bagua_formation",
            name="八卦阵法",
            type=CardType.MASTER,
            cost=4,
            description="八卦相合，阵法天成",
            associated_guas=["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"],
            effects=[CardEffect.PROTECTION, CardEffect.INFLUENCE_BOOST],
            influence_bonus=3,
            dao_xing_bonus=2,
            special_effect="控制的卦象越多，效果越强"
        )
        
        return cards
    
    def get_card(self, card_id: str) -> Optional[EnhancedCard]:
        """获取指定卡牌"""
        return self.cards.get(card_id)
    
    def get_cards_by_type(self, card_type: CardType) -> List[EnhancedCard]:
        """按类型获取卡牌"""
        return [card for card in self.cards.values() if card.type == card_type]
    
    def get_cards_by_gua(self, gua: str) -> List[EnhancedCard]:
        """按卦象获取相关卡牌"""
        return [card for card in self.cards.values() if gua in card.associated_guas or "所有卦象" in card.associated_guas]
    
    def get_random_card(self, card_type: Optional[CardType] = None) -> EnhancedCard:
        """获取随机卡牌"""
        if card_type:
            cards = self.get_cards_by_type(card_type)
        else:
            cards = list(self.cards.values())
        
        return random.choice(cards) if cards else None

class EnhancedCardSystem:
    """增强卡牌系统管理器"""
    
    def __init__(self):
        self.database = EnhancedCardDatabase()
        self.player_decks: Dict[str, List[str]] = {}
        self.combo_tracker: Dict[str, List[str]] = {}
    
    def initialize_player_deck(self, player_name: str):
        """初始化玩家卡组"""
        if player_name not in self.player_decks:
            # 给每个玩家一个基础卡组
            basic_cards = ["qian_basic", "kun_basic", "zhen_basic"]
            self.player_decks[player_name] = basic_cards.copy()
            self.combo_tracker[player_name] = []
    
    def add_card_to_deck(self, player_name: str, card_id: str):
        """向玩家卡组添加卡牌"""
        if player_name not in self.player_decks:
            self.initialize_player_deck(player_name)
        
        self.player_decks[player_name].append(card_id)
    
    def play_enhanced_card(self, player: Player, card_id: str, target_gua: str, game_state: GameState) -> Dict[str, any]:
        """使用增强卡牌"""
        card = self.database.get_card(card_id)
        if not card:
            return {"success": False, "message": "卡牌不存在"}
        
        if player.qi < card.cost:
            return {"success": False, "message": f"气不足，需要{card.cost}点气"}
        
        if target_gua not in card.associated_guas and "所有卦象" not in card.associated_guas:
            return {"success": False, "message": "卡牌与目标卦象不匹配"}
        
        # 消耗资源
        player.qi -= card.cost
        
        # 应用基础效果
        result = self._apply_card_effects(player, card, target_gua, game_state)
        
        # 检查组合效果
        combo_bonus = self._check_combo_effects(player.name, card)
        if combo_bonus:
            result["combo_bonus"] = combo_bonus
        
        # 记录使用的卡牌
        if player.name not in self.combo_tracker:
            self.combo_tracker[player.name] = []
        self.combo_tracker[player.name].append(card_id)
        
        # 保持最近5张卡牌的记录
        if len(self.combo_tracker[player.name]) > 5:
            self.combo_tracker[player.name].pop(0)
        
        return result
    
    def _apply_card_effects(self, player: Player, card: EnhancedCard, target_gua: str, game_state: GameState) -> Dict[str, any]:
        """应用卡牌效果"""
        effects_applied = []
        
        # 资源奖励
        if card.qi_bonus > 0:
            player.qi = min(25, player.qi + card.qi_bonus)
            effects_applied.append(f"+{card.qi_bonus}气")
        
        if card.dao_xing_bonus > 0:
            player.dao_xing = min(20, player.dao_xing + card.dao_xing_bonus)
            effects_applied.append(f"+{card.dao_xing_bonus}道行")
        
        if card.cheng_yi_bonus > 0:
            player.cheng_yi = min(15, player.cheng_yi + card.cheng_yi_bonus)
            effects_applied.append(f"+{card.cheng_yi_bonus}诚意")
        
        # 影响力奖励
        if card.influence_bonus > 0:
            zone_data = game_state.board.gua_zones.get(target_gua, {})
            if "markers" in zone_data:
                zone_data["markers"][player.name] = zone_data["markers"].get(player.name, 0) + card.influence_bonus
                effects_applied.append(f"+{card.influence_bonus}影响力于{target_gua}")
        
        # 特殊效果
        if card.special_effect:
            special_result = self._apply_special_effect(player, card, target_gua, game_state)
            if special_result:
                effects_applied.append(special_result)
        
        return {
            "success": True,
            "card_name": card.name,
            "effects": effects_applied,
            "description": card.description
        }
    
    def _apply_special_effect(self, player: Player, card: EnhancedCard, target_gua: str, game_state: GameState) -> str:
        """应用特殊效果"""
        if card.special_effect == "连续使用时效果递增":
            recent_uses = self.combo_tracker.get(player.name, []).count(card.id)
            if recent_uses > 1:
                bonus = recent_uses - 1
                player.qi = min(25, player.qi + bonus)
                return f"连击奖励: +{bonus}气"
        
        elif card.special_effect == "为其他卡牌提供稳定加成":
            # 下一张卡牌效果增强
            return "下一张卡牌效果增强50%"
        
        elif card.special_effect == "可以打断对手的连击":
            # 重置所有对手的连击计数
            for opponent_name in self.combo_tracker:
                if opponent_name != player.name:
                    self.combo_tracker[opponent_name] = []
            return "打断所有对手的连击"
        
        elif card.special_effect == "平衡阴阳，获得额外回合":
            if abs(player.yin_yang_balance.yin - player.yin_yang_balance.yang) <= 1:
                return "阴阳平衡，获得额外行动点"
        
        elif card.special_effect == "根据五行亲和度获得不同效果":
            max_affinity = max(player.wuxing_affinities.values())
            if max_affinity >= 3:
                player.dao_xing = min(20, player.dao_xing + max_affinity)
                return f"五行亲和奖励: +{max_affinity}道行"
        
        elif card.special_effect == "获得所有位置的修行加成":
            # 根据当前位置给予不同奖励
            if player.position == Zone.TIAN:
                player.qi = min(25, player.qi + 3)
                return "天位修行: +3气"
            elif player.position == Zone.REN:
                player.dao_xing = min(20, player.dao_xing + 2)
                return "人位修行: +2道行"
            elif player.position == Zone.DI:
                player.cheng_yi = min(15, player.cheng_yi + 2)
                return "地位修行: +2诚意"
        
        return ""
    
    def _check_combo_effects(self, player_name: str, card: EnhancedCard) -> Optional[str]:
        """检查组合效果"""
        if not card.combo_cards:
            return None
        
        recent_cards = self.combo_tracker.get(player_name, [])
        
        # 检查是否有组合卡牌在最近使用的卡牌中
        for combo_card_id in card.combo_cards:
            if combo_card_id in recent_cards:
                return f"组合效果激活: {card.name} + {combo_card_id}"
        
        return None
    
    def get_available_cards(self, player_name: str) -> List[EnhancedCard]:
        """获取玩家可用的卡牌"""
        if player_name not in self.player_decks:
            self.initialize_player_deck(player_name)
        
        card_ids = self.player_decks[player_name]
        return [self.database.get_card(card_id) for card_id in card_ids if self.database.get_card(card_id)]
    
    def display_card_info(self, card: EnhancedCard):
        """显示卡牌信息"""
        print(f"\n🃏 {card.name} ({card.type.value})")
        print(f"💰 消耗: {card.cost}气")
        print(f"📝 描述: {card.description}")
        print(f"🎯 关联卦象: {', '.join(card.associated_guas)}")
        
        if card.qi_bonus > 0:
            print(f"⚡ 气: +{card.qi_bonus}")
        if card.dao_xing_bonus > 0:
            print(f"📚 道行: +{card.dao_xing_bonus}")
        if card.cheng_yi_bonus > 0:
            print(f"💎 诚意: +{card.cheng_yi_bonus}")
        if card.influence_bonus > 0:
            print(f"🎯 影响力: +{card.influence_bonus}")
        
        if card.special_effect:
            print(f"✨ 特殊效果: {card.special_effect}")
        
        if card.combo_cards:
            print(f"🔗 组合卡牌: {', '.join(card.combo_cards)}")
        
        print("=" * 40)

# 全局增强卡牌系统实例
enhanced_card_system = EnhancedCardSystem()
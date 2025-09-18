"""
增强的胜利条件系统
提供多元化的获胜路径，增加游戏策略深度
"""

from typing import Dict, List, Optional, Tuple
from game_state import GameState, Player
from yijing_mechanics import WuXing

class VictoryTracker:
    """胜利条件追踪器"""
    
    def __init__(self):
        self.divination_count = 0
        self.divination_accuracy = 0.0
        self.wisdom_activated = set()
        self.transformation_count = 0
        self.position_time = {"天": 0, "人": 0, "地": 0}
        self.gua_mastery = set()
        
    def update_divination(self, success: bool):
        """更新占卜统计"""
        self.divination_count += 1
        if success:
            self.divination_accuracy = (self.divination_accuracy * (self.divination_count - 1) + 1.0) / self.divination_count
        else:
            self.divination_accuracy = (self.divination_accuracy * (self.divination_count - 1)) / self.divination_count
    
    def add_wisdom(self, wisdom: str):
        """添加激活的智慧"""
        self.wisdom_activated.add(wisdom)
    
    def add_transformation(self):
        """记录变卦次数"""
        self.transformation_count += 1
    
    def update_position_time(self, position: str):
        """更新位置修行时间"""
        if position in self.position_time:
            self.position_time[position] += 1
    
    def add_gua_mastery(self, gua: str):
        """添加掌握的卦象"""
        self.gua_mastery.add(gua)

def check_enhanced_victory_conditions(player: Player, victory_tracker: VictoryTracker) -> List[str]:
    """检查增强的胜利条件"""
    victories = []
    
    # 1. 大道至简 - 道行达到12
    if player.dao_xing >= 12:
        victories.append("大道至简")
    
    # 2. 太极宗师 - 阴阳平衡≥0.8且道行≥8
    if player.yin_yang_balance.balance_ratio >= 0.8 and player.dao_xing >= 8:
        victories.append("太极宗师")
    
    # 3. 五行圆满 - 所有五行亲和力≥3
    if all(affinity >= 3 for affinity in player.wuxing_affinities.values()):
        victories.append("五行圆满")
    
    # 4. 易经大师 - 成功占卜15次且准确率>80%
    if victory_tracker.divination_count >= 15 and victory_tracker.divination_accuracy > 0.8:
        victories.append("易经大师")
    
    # 5. 智慧导师 - 激活10条不同的智慧格言
    if len(victory_tracker.wisdom_activated) >= 10:
        victories.append("智慧导师")
    
    # 6. 变化之道 - 完成20次变卦且保持平衡
    if victory_tracker.transformation_count >= 20 and player.yin_yang_balance.balance_ratio >= 0.6:
        victories.append("变化之道")
    
    # 7. 天人合一 - 在天、人、地三个位置各修行5回合
    if all(time >= 5 for time in victory_tracker.position_time.values()):
        victories.append("天人合一")
    
    # 8. 卦象精通 - 掌握所有8个基础卦象
    basic_guas = {"乾", "坤", "震", "巽", "坎", "离", "艮", "兑"}
    if basic_guas.issubset(victory_tracker.gua_mastery):
        victories.append("卦象精通")
    
    # 9. 和谐统一 - 同时达到阴阳平衡0.7+五行调和3
    wuxing_harmony = sum(1 for affinity in player.wuxing_affinities.values() if affinity >= 3)
    if player.yin_yang_balance.balance_ratio >= 0.7 and wuxing_harmony >= 3:
        victories.append("和谐统一")
    
    # 10. 资源大师 - 气≥20且诚意≥10且道行≥10
    if player.qi >= 20 and player.cheng_yi >= 10 and player.dao_xing >= 10:
        victories.append("资源大师")
    
    return victories

def get_victory_description(victory_type: str) -> str:
    """获取胜利条件的详细描述"""
    descriptions = {
        "大道至简": "通过深厚的道行修为，领悟大道至简的真谛",
        "太极宗师": "掌握阴阳平衡之道，成为太极宗师",
        "五行圆满": "精通五行相生相克，达到五行圆满境界",
        "易经大师": "通过大量准确的占卜，成为易经预测大师",
        "智慧导师": "激活众多智慧格言，成为智慧的传播者",
        "变化之道": "通过无数次变卦而保持内心平衡，掌握变化之道",
        "天人合一": "在天地人三界都有深度修行，达到天人合一",
        "卦象精通": "精通所有基础卦象，成为卦象解读专家",
        "和谐统一": "同时掌握阴阳平衡与五行和谐，达到完美统一",
        "资源大师": "通过卓越的资源管理能力，积累丰厚的修行资源"
    }
    return descriptions.get(victory_type, "未知的胜利条件")

def get_victory_requirements(victory_type: str) -> str:
    """获取胜利条件的具体要求"""
    requirements = {
        "大道至简": "道行 ≥ 12",
        "太极宗师": "阴阳平衡 ≥ 0.8 且 道行 ≥ 8",
        "五行圆满": "所有五行亲和力 ≥ 3",
        "易经大师": "占卜次数 ≥ 15 且 准确率 > 80%",
        "智慧导师": "激活智慧格言 ≥ 10条",
        "变化之道": "变卦次数 ≥ 20 且 阴阳平衡 ≥ 0.6",
        "天人合一": "天、人、地三个位置各修行 ≥ 5回合",
        "卦象精通": "掌握所有8个基础卦象",
        "和谐统一": "阴阳平衡 ≥ 0.7 且 五行调和 ≥ 3",
        "资源大师": "气 ≥ 20 且 诚意 ≥ 10 且 道行 ≥ 10"
    }
    return requirements.get(victory_type, "未知要求")

def display_victory_progress(player: Player, victory_tracker: VictoryTracker):
    """显示胜利条件进度"""
    print(f"\n📊 {player.name} 的胜利条件进度:")
    print("=" * 50)
    
    # 大道至简
    progress = min(100, (player.dao_xing / 12) * 100)
    print(f"🎯 大道至简: {progress:.1f}% (道行: {player.dao_xing}/12)")
    
    # 太极宗师
    balance_progress = min(100, (player.yin_yang_balance.balance_ratio / 0.8) * 100)
    dao_progress = min(100, (player.dao_xing / 8) * 100)
    taiji_progress = min(balance_progress, dao_progress)
    print(f"☯️ 太极宗师: {taiji_progress:.1f}% (平衡: {player.yin_yang_balance.balance_ratio:.2f}/0.8, 道行: {player.dao_xing}/8)")
    
    # 五行圆满
    wuxing_count = sum(1 for affinity in player.wuxing_affinities.values() if affinity >= 3)
    wuxing_progress = (wuxing_count / 5) * 100
    print(f"🌊 五行圆满: {wuxing_progress:.1f}% (已达标: {wuxing_count}/5)")
    
    # 易经大师
    divination_progress = min(100, (victory_tracker.divination_count / 15) * 100)
    accuracy_progress = min(100, (victory_tracker.divination_accuracy / 0.8) * 100)
    master_progress = min(divination_progress, accuracy_progress)
    print(f"🔮 易经大师: {master_progress:.1f}% (占卜: {victory_tracker.divination_count}/15, 准确率: {victory_tracker.divination_accuracy:.1%})")
    
    # 智慧导师
    wisdom_progress = min(100, (len(victory_tracker.wisdom_activated) / 10) * 100)
    print(f"💡 智慧导师: {wisdom_progress:.1f}% (智慧: {len(victory_tracker.wisdom_activated)}/10)")
    
    # 变化之道
    transform_progress = min(100, (victory_tracker.transformation_count / 20) * 100)
    print(f"🔄 变化之道: {transform_progress:.1f}% (变卦: {victory_tracker.transformation_count}/20)")
    
    # 天人合一
    min_position_time = min(victory_tracker.position_time.values())
    unity_progress = min(100, (min_position_time / 5) * 100)
    print(f"🌌 天人合一: {unity_progress:.1f}% (最少位置时间: {min_position_time}/5)")
    
    # 卦象精通
    gua_progress = min(100, (len(victory_tracker.gua_mastery) / 8) * 100)
    print(f"📚 卦象精通: {gua_progress:.1f}% (掌握卦象: {len(victory_tracker.gua_mastery)}/8)")
    
    print("=" * 50)

class EnhancedVictorySystem:
    """增强胜利系统管理器"""
    
    def __init__(self):
        self.player_trackers: Dict[str, VictoryTracker] = {}
    
    def get_tracker(self, player_name: str) -> VictoryTracker:
        """获取玩家的胜利追踪器"""
        if player_name not in self.player_trackers:
            self.player_trackers[player_name] = VictoryTracker()
        return self.player_trackers[player_name]
    
    def check_all_victories(self, game_state: GameState) -> Dict[str, List[str]]:
        """检查所有玩家的胜利条件"""
        results = {}
        for player in game_state.players:
            tracker = self.get_tracker(player.name)
            victories = check_enhanced_victory_conditions(player, tracker)
            if victories:
                results[player.name] = victories
        return results
    
    def display_all_progress(self, game_state: GameState):
        """显示所有玩家的胜利进度"""
        for player in game_state.players:
            tracker = self.get_tracker(player.name)
            display_victory_progress(player, tracker)
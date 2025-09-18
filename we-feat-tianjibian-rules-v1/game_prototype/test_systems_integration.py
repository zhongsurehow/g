#!/usr/bin/env python3
"""
系统集成测试脚本
测试智慧系统、教学系统和成就系统的集成
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_state import GameState, Player
from wisdom_system import wisdom_system
from tutorial_system import tutorial_system, TutorialType
from achievement_system import achievement_system

def test_wisdom_system():
    """测试智慧系统"""
    print("🧠 测试智慧系统...")
    
    # 创建测试玩家
    player = Player("测试玩家", 0)
    player.dao_xing = 5
    player.qi = 10
    player.cheng_yi = 8
    
    # 测试智慧触发
    quote = wisdom_system.check_triggers(player, "study")
    if quote:
        print(f"✅ 智慧触发成功: {quote.text}")
        wisdom_system.apply_quote_effects(player, quote)
    else:
        print("❌ 智慧触发失败")
    
    # 显示智慧进度
    wisdom_system.display_wisdom_progress("测试玩家")
    print("✅ 智慧系统测试完成\n")

def test_tutorial_system():
    """测试教学系统"""
    print("📚 测试教学系统...")
    
    # 显示教学菜单
    print("教学类别:")
    for i, tutorial_type in enumerate(TutorialType, 1):
        print(f"{i}. {tutorial_type.value}")
    
    # 测试获取课程
    lessons = tutorial_system.get_lessons_by_type(TutorialType.BASIC_RULES)
    print(f"✅ 基础规则课程数量: {len(lessons)}")
    
    # 测试学习进度
    tutorial_system.display_learning_progress("测试玩家")
    print("✅ 教学系统测试完成\n")

def test_achievement_system():
    """测试成就系统"""
    print("🏆 测试成就系统...")
    
    # 初始化玩家成就
    achievement_system.on_game_start("测试玩家")
    
    # 模拟一些游戏行为
    achievement_system.on_study("测试玩家")
    achievement_system.on_meditation("测试玩家")
    achievement_system.on_card_played("测试玩家", "common")
    
    # 更新资源统计
    achievement_system.update_resource_stats("测试玩家", qi=15, dao_xing=8, cheng_yi=10)
    
    # 检查成就解锁
    unlocked = achievement_system.check_achievements("测试玩家")
    if unlocked:
        print(f"✅ 解锁成就: {[ach.title for ach in unlocked]}")
    
    # 显示成就进度
    achievement_system.display_achievement_progress("测试玩家")
    print("✅ 成就系统测试完成\n")

def test_system_integration():
    """测试系统集成"""
    print("🔗 测试系统集成...")
    
    # 创建游戏状态
    game_state = GameState()
    player = Player("集成测试玩家", 0)
    game_state.players.append(player)
    
    # 初始化所有系统
    achievement_system.on_game_start(player.name)
    
    # 模拟学习行为，应该触发多个系统
    print("模拟学习行为...")
    quote = wisdom_system.check_triggers(player, "study")
    if quote:
        wisdom_system.apply_quote_effects(player, quote)
    
    achievement_system.on_study(player.name)
    
    # 模拟冥想行为
    print("模拟冥想行为...")
    quote = wisdom_system.check_triggers(player, "meditate")
    if quote:
        wisdom_system.apply_quote_effects(player, quote)
    
    achievement_system.on_meditation(player.name)
    
    # 检查最终状态
    print(f"玩家最终状态: 气={player.qi}, 道行={player.dao_xing}, 诚意={player.cheng_yi}")
    
    # 检查成就解锁
    unlocked = achievement_system.check_achievements(player.name)
    if unlocked:
        print(f"解锁的成就: {[ach.title for ach in unlocked]}")
    
    print("✅ 系统集成测试完成\n")

def main():
    """主测试函数"""
    print("🚀 开始系统集成测试...\n")
    
    try:
        test_wisdom_system()
        test_tutorial_system()
        test_achievement_system()
        test_system_integration()
        
        print("🎉 所有测试完成！系统集成成功！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
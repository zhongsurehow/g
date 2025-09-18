import random
import sys
from typing import Dict, Any, Optional

from game_state import GameState, Player, AvatarName, BonusType, Zone, Modifiers
from game_data import GAME_DECK, GUA_ZONE_BONUSES, EMPEROR_AVATAR, HERMIT_AVATAR
from tian_shi_cards import TIAN_SHI_CARDS
import actions
from bot_player import get_bot_choice
from yijing_actions import (
    apply_yin_yang_effect, apply_wuxing_effect, enhanced_play_card,
    enhanced_meditate, divine_fortune, consult_yijing, enhanced_study,
    display_yijing_status, check_victory_conditions_enhanced
)
from enhanced_victory import VictoryTracker, check_enhanced_victory_conditions
from wisdom_system import wisdom_system
from tutorial_system import tutorial_system, TutorialType
from achievement_system import achievement_system
from enhanced_cards import enhanced_card_system

def setup_game(num_players: int = 2) -> GameState:
    """Initialize a new game state with specified number of players (1-8)."""
    if not 1 <= num_players <= 8:
        raise ValueError("游戏支持1-8人，请输入正确的人数")
    
    # 可选的头像列表
    available_avatars = [EMPEROR_AVATAR, HERMIT_AVATAR]
    
    # Create players
    players = []
    for i in range(num_players):
        avatar = available_avatars[i % len(available_avatars)]
        player_name = f"玩家{i+1}" if num_players > 1 else "修行者"
        players.append(Player(name=player_name, avatar=avatar))
    
    # Create game state
    game_state = GameState(players=players)
    
    # Create a shuffled deck from GAME_DECK
    deck = GAME_DECK.copy()
    random.shuffle(deck)
    
    # Deal initial hands (optimized for better game flow)
    for player in game_state.players:
        for _ in range(4):  # Increased initial hand size for more options
            if deck:
                player.hand.append(deck.pop())
        # Optimized initial resources for better game experience
        player.qi = 8  # Increased qi for more action choices
        player.dao_xing = 1  # Start with some wisdom
        player.cheng_yi = 2  # Enhanced starting sincerity
    
    return game_state

def show_tutorial_menu(player: Player):
    """显示教学菜单并处理用户选择"""
    while True:
        print(f"\n🎓 教学系统 - {player.name}")
        print("=" * 50)
        print("1. 基础规则教程")
        print("2. 易经知识教程") 
        print("3. 策略指导教程")
        print("4. 高级战术教程")
        print("5. 查看所有课程")
        print("6. 学习进度统计")
        print("0. 返回游戏")
        print("=" * 50)
        
        try:
            choice = input("请选择 (0-6): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                show_tutorial_category(player, TutorialType.BASIC_RULES)
            elif choice == "2":
                show_tutorial_category(player, TutorialType.YIJING_KNOWLEDGE)
            elif choice == "3":
                show_tutorial_category(player, TutorialType.STRATEGY_GUIDE)
            elif choice == "4":
                show_tutorial_category(player, TutorialType.ADVANCED_TACTICS)
            elif choice == "5":
                tutorial_system.show_available_lessons(player.name)
                input("\n按回车键继续...")
            elif choice == "6":
                tutorial_system.display_learning_progress(player.name)
                input("\n按回车键继续...")
            else:
                print("无效选择，请重试")
        except KeyboardInterrupt:
            break

def show_tutorial_category(player: Player, tutorial_type: TutorialType):
    """显示特定类别的教程并处理学习"""
    lessons = tutorial_system.database.get_lessons_by_type(tutorial_type)
    progress = tutorial_system.get_player_progress(player.name)
    
    while True:
        print(f"\n📚 {tutorial_type.value}")
        print("=" * 50)
        
        available_lessons = []
        for i, lesson in enumerate(lessons, 1):
            status = "✅" if progress.get(lesson.id, False) else "⏳"
            print(f"{i}. {status} {lesson.title} ({lesson.level.value})")
            if not progress.get(lesson.id, False):
                available_lessons.append((i, lesson))
        
        print("0. 返回上级菜单")
        print("=" * 50)
        
        try:
            choice = input("选择要学习的课程 (输入数字): ").strip()
            
            if choice == "0":
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(lessons):
                lesson = lessons[choice_num - 1]
                if progress.get(lesson.id, False):
                    print("您已经完成了这个课程！")
                    input("按回车键继续...")
                else:
                    tutorial_system.start_lesson(player, lesson.id)
                    input("\n按回车键继续...")
            else:
                print("无效选择")
        except (ValueError, KeyboardInterrupt):
            break

def show_enhanced_cards_menu(player: Player):
    """显示增强卡牌菜单"""
    print(f"\n=== {player.name} 的增强卡牌 ===")
    
    # 初始化玩家卡组（如果还没有）
    enhanced_card_system.initialize_player_deck(player.name)
    
    # 获取可用卡牌
    available_cards = enhanced_card_system.get_available_cards(player.name)
    
    if not available_cards:
        print("暂无可用的增强卡牌")
        return
    
    print("可用卡牌:")
    for i, card in enumerate(available_cards, 1):
        print(f"{i}. {card.name} ({card.type.value}) - 消耗{card.cost}气")
        print(f"   {card.description}")
    
    print("\n输入卡牌编号查看详细信息，或按回车返回")
    
    try:
        choice = input("选择: ").strip()
        if choice:
            card_index = int(choice) - 1
            if 0 <= card_index < len(available_cards):
                enhanced_card_system.display_card_info(available_cards[card_index])
    except ValueError:
        pass

def use_enhanced_card_action(player: Player):
    """使用增强卡牌的行动"""
    print(f"\n=== 使用增强卡牌 ===")
    
    # 获取可用卡牌
    available_cards = enhanced_card_system.get_available_cards(player.name)
    
    if not available_cards:
        print("暂无可用的增强卡牌")
        return
    
    # 过滤玩家能够使用的卡牌（根据气的消耗）
    usable_cards = [card for card in available_cards if card.cost <= player.qi]
    
    if not usable_cards:
        print("气不足，无法使用任何增强卡牌")
        return
    
    print("可使用的卡牌:")
    for i, card in enumerate(usable_cards, 1):
        print(f"{i}. {card.name} - 消耗{card.cost}气")
        print(f"   {card.description}")
    
    print(f"{len(usable_cards) + 1}. 取消")
    
    try:
        choice = int(input("请选择要使用的卡牌: "))
        if 1 <= choice <= len(usable_cards):
            card = usable_cards[choice - 1]
            success = enhanced_card_system.use_card(player.name, card.id, player)
            if success:
                print(f"✅ 成功使用 {card.name}!")
            else:
                print(f"❌ 使用 {card.name} 失败")
        elif choice == len(usable_cards) + 1:
            print("取消使用卡牌")
        else:
            print("无效选择")
    except ValueError:
        print("请输入有效数字")

def get_current_modifiers(player: Player, game_state: GameState) -> Modifiers:
    """Calculate current modifiers for a player based on controlled zones."""
    mods = Modifiers()
    
    # Check controlled zones for bonuses
    for zone_name, zone_data in game_state.board.gua_zones.items():
        if zone_data.get("controller") == player.name:
            bonus_info = GUA_ZONE_BONUSES.get(zone_name, {})
            bonus_type = bonus_info.get("bonus")
            
            if bonus_type == BonusType.EXTRA_AP:
                mods.extra_ap += 1
            elif bonus_type == BonusType.HAND_LIMIT:
                mods.hand_limit_bonus += 2
            elif bonus_type == BonusType.EXTRA_INFLUENCE:
                mods.extra_influence += 1
            elif bonus_type == BonusType.FREE_STUDY:
                mods.has_free_study = True
            elif bonus_type == BonusType.QI_DISCOUNT:
                mods.qi_discount += 1
            elif bonus_type == BonusType.DAO_XING_ON_TASK:
                mods.extra_dao_xing_on_task += 1
    
    return mods

def run_action_phase(game_state: GameState, player: Player, mods: Modifiers, is_ai_player: bool) -> GameState:
    ap = 2 + mods.extra_ap
    flags = {"task": False, "freestudy": False, "scry": False, "ask_heart": False}

    while ap > 0:
        actions_menu = actions.get_valid_actions(game_state, player, ap, mods, **flags)
        
        if not actions_menu:
            print("No valid actions available.")
            break

        # Display available actions
        print(f"\n{player.name}'s turn - AP: {ap}")
        for key, action_data in actions_menu.items():
            print(f"{key}: {action_data.get('description', 'Unknown action')} (Cost: {action_data.get('cost', 0)} AP)")

        # Get choice from human or bot
        if is_ai_player:
            choice = get_bot_choice(actions_menu)
        else:
            try:
                choice = int(input("Action> "))
            except (ValueError, KeyboardInterrupt):
                print("Invalid input. Please enter a number.")
                continue

        action_data = actions_menu.get(choice)
        if not action_data: 
            print("Invalid action choice.")
            continue

        action_func, cost, args = action_data["action"], action_data["cost"], action_data.get("args", [])
        if action_func == "pass": 
            print(f"{player.name} passes.")
            break

        new_state = None
        
        # Handle different action types
        if isinstance(action_func, str):
            # Handle string-based actions (prompts)
            if action_func == "wisdom_progress":
                wisdom_system.display_wisdom_progress(player.name)
                ap -= cost
                continue
            elif action_func == "tutorial_menu":
                show_tutorial_menu(player)
                ap -= cost
                continue
            elif action_func == "learning_progress":
                tutorial_system.display_learning_progress(player.name)
                ap -= cost
                continue
            elif action_func == "achievement_progress":
                achievement_system.display_achievement_progress(player.name)
                ap -= cost
                continue
            elif action_func == "achievement_list":
                achievement_system.display_available_achievements(player.name)
                ap -= cost
                continue
            elif action_func == "view_enhanced_cards":
                show_enhanced_cards_menu(player)
                ap -= cost
                continue
            elif action_func == "use_enhanced_card":
                use_enhanced_card_action(player)
                ap -= cost
                continue
            else:
                print(f"Executing {action_func}")
                # For now, just continue
                pass
        else:
            # Execute function-based actions
            try:
                new_state = action_func(game_state, *args, mods)
            except Exception as e:
                print(f"Error executing action: {e}")
                continue

        if new_state:
            game_state = new_state
            ap -= cost
            print(f"Action executed successfully. Remaining AP: {ap}")
            
            # Update flags based on action
            if "study" in str(action_func):
                flags["freestudy"] = True
            elif "task" in str(action_func):
                flags["task"] = True
        else:
            print("Invalid action or conditions not met.")

    return game_state

def main_game_loop(bot_mode: bool, num_players: int = 2):
    game_state = setup_game(num_players)
    print("🎮 游戏开始！")
    print("📋 玩家列表:")
    for i, player in enumerate(game_state.players):
        player_type = " (AI)" if bot_mode and i > 0 else ""
        print(f"  {i+1}. {player.name} ({player.avatar.name.value}){player_type}")
        # 初始化成就系统追踪
        achievement_system.on_game_start(player.name)
        # Initialize enhanced card system for each player
        enhanced_card_system.initialize_player_deck(player.name)
    
    turn_count = 0
    max_turns = 50  # Increased for longer games
    
    while turn_count < max_turns:
        turn_count += 1
        print(f"\n=== Turn {turn_count} ===")
        
        for i, player in enumerate(game_state.players):
            print(f"\n--- {player.name}'s Turn ---")
            print(f"Hand size: {len(player.hand)}")
            print(f"Qi: {player.qi}")
            print(f"Dao Xing: {player.dao_xing}")
            print(f"Cheng Yi: {player.cheng_yi}")
            
            # Display Yijing cultivation status
            display_yijing_status(player)
            
            # Calculate modifiers
            mods = get_current_modifiers(player, game_state)
            
            # Determine if this player is AI (in bot_mode, only player 0 is human)
            is_ai_player = bot_mode and i > 0
            
            # Run action phase
            game_state = run_action_phase(game_state, player, mods, is_ai_player)
            
            # 更新成就系统的资源追踪
            achievement_system.on_resource_update(player.name, player.qi, player.dao_xing, player.cheng_yi)
            
            # 检查区域控制数量
            controlled_zones = sum(1 for zone_data in game_state.board.gua_zones.values() 
                                 if zone_data.get("controller") == player.name)
            achievement_system.on_zone_control(player.name, controlled_zones)
            
            # 检查并解锁新成就
            new_achievements = achievement_system.check_achievements(player.name)
            for achievement in new_achievements:
                achievement_system.display_achievement_unlock(achievement)
                achievement_system.award_achievement_rewards(player, achievement)
            
            # Simple end turn logic
            print(f"{player.name}'s turn ended.")
        
        # Check enhanced victory conditions (including Yijing paths)
        winner = check_victory_conditions_enhanced(game_state)
        if winner:
            # 处理游戏结束时的成就
            for player in game_state.players:
                won = (player.name == winner)
                achievement_system.on_game_end(player.name, won)
                
                # 检查最终成就
                final_achievements = achievement_system.check_achievements(player.name)
                for achievement in final_achievements:
                    achievement_system.display_achievement_unlock(achievement)
            return
        
        # Check traditional zone control victory
        for player in game_state.players:
            controlled_zones = 0
            for zone_name, zone_data in game_state.board.gua_zones.items():
                if zone_data.get("controller") == player.name:
                    controlled_zones += 1
            
            if controlled_zones >= 5:
                print(f"\n🏆 {player.name} wins by controlling {controlled_zones} zones! (Zone Control Victory)")
                
                # 处理游戏结束时的成就
                for p in game_state.players:
                    won = (p.name == player.name)
                    achievement_system.on_game_end(p.name, won)
                    
                    # 检查最终成就
                    final_achievements = achievement_system.check_achievements(p.name)
                    for achievement in final_achievements:
                        achievement_system.display_achievement_unlock(achievement)
                return
    
    print("\nGame ended after maximum turns.")

def main():
    print("🎋 欢迎来到天机变 - 易经主题策略游戏!")
    print("1. 单人修行模式 (与AI对弈)")
    print("2. 多人游戏模式 (2-8人)")
    print("3. 退出游戏")
    
    try:
        choice = input("请选择游戏模式 (1-3): ").strip()
        
        if choice == "1":
            main_game_loop(bot_mode=True, num_players=2)  # 玩家 vs AI
        elif choice == "2":
            while True:
                try:
                    num_players = int(input("请输入玩家人数 (2-8): "))
                    if 2 <= num_players <= 8:
                        break
                    else:
                        print("请输入2-8之间的数字")
                except ValueError:
                    print("请输入有效的数字")
            main_game_loop(bot_mode=False, num_players=num_players)
        elif choice == "3":
            print("愿易经智慧伴您前行！再见！")
            return
        else:
            print("Invalid choice. Exiting.")
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

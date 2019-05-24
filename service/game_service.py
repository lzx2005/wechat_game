#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import time

from dao import mysql_dao
from dict import level_exp
from error.AttackError import AttackError

print(level_exp.level_exp)


def my_info(user_name):
    # 找到攻击者在数据库中的信息
    attackers = mysql_dao.find_user_by_user_name(user_name=user_name)
    if len(attackers) < 1:
        raise AttackError('找不到当前用户信息！请联系管理员')
    attacker = attackers[0]
    try:
        hp = attacker[5]
        max_hp = attacker[6]
        power = attacker[7]
        level = attacker[8]
        exp = attacker[9]
        min_damage = attacker[12]
        max_damage = attacker[13]
        critical_pro = attacker[16]
        critical_times = attacker[17]
        acctack_buff = attacker[18]
        dead_buff = attacker[19]
        usr_buff = attacker[20]
        pass_buff = attacker[21]
        result_info = {
            "当前血量": str(hp),
            "最大血量": str(max_hp),
            "力量值": str(power),
            "当前等级": str(level),
            "当前经验值": str(exp),
            "最小伤害": str(min_damage),
            "最大伤害": str(max_damage),
            "暴击概率": str(critical_pro),
            "暴击倍数": str(critical_times),
            "攻击Buff": str(acctack_buff),
            "死亡Buff": str(dead_buff),
            "玩家Buff": str(usr_buff),
            "被动Buff": str(pass_buff)
        }
        return result_info
    except AttackError as ae:
        print("查询信息出错", ae.value)
        error_result = {
            "code": 500,
            "msg": ae.value
        }
        return error_result


def info(group_user_name):
    users = mysql_dao.find_all_user_by_group_user_name(group_user_name=group_user_name)
    try:
        if len(users) < 1:
            raise AttackError('找不到群员信息，请联系管理员')
        result_info = {}
        for user in users:
            nick_name = user[2]
            hp = user[5]
            result_info.update({
                nick_name: str(hp) + "/500"
            })
        return result_info
    except AttackError as ae:
        print("查询信息出错", ae.value)
        error_result = {
            "code": 500,
            "msg": ae.value
        }
        return error_result

#
# result = info(group_user_name="@@661daab861c14fa56704ef379e02485d667af12d801a20c9c3065d040eca3a31")
# infos = "所有群员的血量信息如下："
# for k, v in result.items():
#     infos = infos + "\n" + k + " : " + v
# print(infos)


def attack(user_name, content, group_user_name):

    # 1、从数据库获取攻击者的信息
    # 2、获取攻击者的血量，如果为0则是死亡状态，拒绝攻击
    # 3、分析攻击者当前体力，是否可以攻击（分析时间，是否可以攻击）
    # 4、分析Content语句，获取被攻击者的信息，如果没有获取到被攻击者，则攻击失败，反弹伤害或者其他的。
    # 5、分析Content语句，判断是否为攻击(attack)、使用道具(use、take、kill)等功能，
    # 6、计算伤害，返回结果
    result = {}

    try:
        # 找到攻击者在数据库中的信息
        attackers = mysql_dao.find_user_by_user_name(user_name=user_name)
        if len(attackers) < 1:
            raise AttackError('找不到攻击者信息！请联系管理员')
        attacker = attackers[0]
        # 判断当前用户是否已经死亡
        hp = attacker[5]
        dead_buff = attacker[20]
        if content.startswith('attack'):
            if hp <= 0:
                raise AttackError('你已经死亡，安安静静地不好吗？')
            # 获取当前小时
            t = time.localtime(time.time())
            hour = t.tm_hour  # 当前小时
            last_attack = attacker[14]  # 上一次攻击的时间
            attack_num = attacker[15]
            if last_attack == hour and attack_num >= 3:
                ss = '你当前小时已经攻击了3次了，需要休息一下。' + str(hour+1) + '点再来攻击吧'
                raise AttackError(ss)
            # 1、检查攻击语句是否正确
            contents = content.split(" ")
            # contents需要长度为2或者长度为3
            if len(contents) >= 2:
                # 普通攻击
                # 1、获取被攻击者
                contents1 = contents[1]
                # 2、去掉@标识
                contents1_no_at = contents1[1: len(contents1)]
                # 3、去数据库找到被攻击者
                attackeds = mysql_dao.find_user_by_name(name=contents1_no_at.strip(), group_user_name=group_user_name)
                if len(attackeds) < 1:
                    raise AttackError('你确定你要攻击的人是存在的？')
                attacked = attackeds[0]
                attacked_hp = attacked[5]
                if attacked_hp <= 0:
                    raise AttackError('你要攻击的人已经挂了')

                # 4、开始计算攻击伤害
                damage_result = count_damage(attacker=attacker, attacked=attacked)
                if damage_result['code'] == 0:
                    damage = damage_result['damage']
                    # 计算获得的经验值
                    exp_add = count_exp(attacker=attacker, attacked=attacked, damage=damage)
                    # 计算攻击成功，修改数据库
                    rest_hp = attacked_hp - damage  # 当前血量减去扣的血
                    if rest_hp < 0:
                        rest_hp = 0
                    mysql_dao.give_damage(
                        attacker_id=attacker[0],
                        attacked_id=attacked[0],
                        damage=rest_hp,
                        last_attack=last_attack,
                        now_hour=hour,
                        group_user_name=group_user_name
                    )
                    # 封装攻击成功的消息
                    result.update({
                        "code": 0,
                        "msg": "攻击成功",
                        "damage_type": damage_result['damage_type'],
                        "damage": damage_result['damage'],
                        "damage_to": damage_result['damage_to'],
                        "damage_times": damage_result['damage_times'],
                        "rest_hp": rest_hp,
                        "exp_add": exp_add,
                        "isDead": False
                    })
                    if rest_hp == 0:
                        result.update({
                            "isDead": True
                        })
                    return result
                else:
                    raise AttackError(damage_result['msg'])
            else:
                # 攻击语句出错
                raise AttackError('攻击语句出错')
        elif content.startswith('use'):
            # 使用道具
            if hp <= 0 and dead_buff <= 0:
                raise AttackError('你已经死亡，且没有道具可以复活，安安静静地不好吗？')
        else:
            result.update({
                "code": -1,
                "msg": "不进行攻击"
            })
            return result
    except AttackError as ae:
        print("进行攻击的时候出错", ae.value)
        error_result = {
            "code": 500,
            "msg": ae.value
        }
        return error_result


def count_damage(attacker, attacked):
    # 获取攻击力
    min_damage = attacker[12]
    max_damage = attacker[13]
    base_damage = int(round(random.uniform(min_damage, max_damage), 0))  # 基础伤害随机值
    critical_pro = attacker[16]  # 暴击概率

    damage_result = {
        "damage_type": 1,
        "damage": base_damage,
        "damage_times": 1  # 暴击倍数1
    }  # 普通攻击

    if random.random() < float(critical_pro):
        # 命中暴击概率，计算暴击
        critical_times = attacker[17]  # 获取暴击倍数
        critical_damage = int(round(base_damage * critical_times, 0))
        damage_result.update({
            "damage_type": 2,  # 设置返回信息里面是暴击
            "damage": critical_damage,  # 更新暴击伤害值
            "damage_times": critical_times  # 更新暴击倍数
        })
    damage_result.update({
        "code": 0,
        "msg": "攻击成功",
        "damage_to": attacked[2]
    })
    return damage_result


# 计算获得的经验
def count_exp(attacker, attacked, damage):
    attacked_level = attacked[8]  # 被攻击的等级
    attacked_hp = attacked[5]
    exp_add = round(attacked_level * random.uniform(1, 3))
    rest_hp = attacked_hp - damage  # 当前血量减去扣的血
    if rest_hp <= 0:
        # 造成击杀
        attacker_level = attacker[8]
        # 计算攻击者和被攻击者的等级差别
        level_min = attacked_level - attacker_level
        # 计算次方 击杀的等级越高得到的经验也越高
        exp_add = exp_add * (1.5**level_min)
        # todo 该经验算法待改进
    return exp_add
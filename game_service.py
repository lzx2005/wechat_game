#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import mysql_dao
from AttackError import AttackError


def attack(user_name,content):

    # 1、从数据库获取攻击者的信息
    # 2、获取攻击者的血量，如果为0则是死亡状态，拒绝攻击
    # 3、分析攻击者当前体力，是否可以攻击（分析时间，是否可以攻击）
    # 4、分析Content语句，获取被攻击者的信息，如果没有获取到被攻击者，则攻击失败，反弹伤害或者其他的。
    # 5、分析Content语句，判断是否为攻击(attack)、使用道具(use、take、kill)等功能，
    # 6、计算伤害，返回结果
    result = {}

    try:
        attackers = mysql_dao.find_user_by_user_name(user_name=user_name)
        if len(attackers) < 1:
            raise AttackError('找不到用户')
        attacker = attackers[0]
        if content.startswith('attack'):
            # 1、检查攻击语句是否正确
            contents = content.split(" ")
            #contents需要长度为2或者长度为3
            if len(contents) >= 2:
                # 普通攻击
                # 1、获取被攻击者
                attacked = contents[1]
                # 2、去数据库找到被攻击者
                print("普通攻击")
            else:
                # 攻击语句出错
                raise AttackError('攻击语句出错')
            print()
        elif content.startswith('use'):
            # 使用道具
            print()
    except AttackError as ae:
        error_result = {
            "code": 500,
            "msg": ae.value
        }
        return error_result

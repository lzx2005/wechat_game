level_exp = {
}

# 初始化经验值
for i in range(1, 100):
    level_exp.update({
        str(i): 2**i*100
    })


def get_level_exp():
    return level_exp


def info():
    for k, v in level_exp.items():
        print(k, "级需要", v, "点经验")

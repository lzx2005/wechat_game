level_exp = {
}

for i in range(1,10):
    level_exp.update({
        str(i): 2**i*100
    })


def get_level_exp():
    return level_exp


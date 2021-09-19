import itertools 

def bet_umaren(df,search_id):
    array = df[df["race_id"]==search_id][["win_1","win_2"]].drop_duplicates().values.tolist()[0]
    target = set(array)
    table = df[df["race_id"]==search_id][["horse_number","center","bet"]]
    if len(table[table["center"]==1]) != 0:
        [center] = table[table["center"]==1]["horse_number"].values.tolist()
        center = [center]*4
        bet = table[table["bet"]==1]["horse_number"].values.tolist()
        combination = [[x,y] for x,y in zip(center,bet)]
        win = [df[df["race_id"]==search_id][["return"]].drop_duplicates().values[0][0] for i in combination if set(i)==target]
        if len(win) != 0:
            return win[0]
        else:
            return 0
    else:
        return 0


def bet_sanrenpuku(df,search_id):
    array = df[df["race_id"]==search_id][["win_1","win_2","win_3"]].drop_duplicates().values.tolist()[0]
    target = set(array)
    print(target)
    table = df[df["race_id"]==search_id][["horse_number","center","bet"]]
    if len(table[table["center"]==1]) != 0:
        [center] = table[table["center"]==1]["horse_number"].values.tolist()
        center = [center]*4
        bet = table[table["bet"]==1]["horse_number"].values.tolist()
        bet.remove(center[0])
        combination = [c for c in itertools.combinations(bet,2)]   
        print(combination)
        combinations=[]
        for c in combination:
            c = list(c)
            c.append(center[0])
            set_c = set(c)
            combinations.append(set_c)
        print(combinations)
        win = [df[df["race_id"]==search_id][["return"]].drop_duplicates().values[0][0] for i in combinations if i==target]
        if len(win) != 0:
            return win[0]
        else:
            return 0
    else:
        return 0
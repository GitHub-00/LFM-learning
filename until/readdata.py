import os


def get_item_info(input_file):
    '''
    get item info:[title, genre]
    args:
        input_file: item info file
    return:
        a dict key itemid, value[title, genre]
    '''
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0

    f = open(input_file)
    for line in f:
        if linenum==0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item)<3:
            continue
        if len(item)==3:
            itemid, title, genre = item[0], item[1], item[2]
        if len(item)>3:
            itemid = item[0]
            genre = item[-1]
            title = ','.join(item[1:-1])

        item_info[itemid] = [title,genre]

    f.closed
    return item_info

def get_avg_socre(input_file):
    '''
    get item average ratings score
    args:
        input_file: user ratings file
    return:
        a dict key:itemid, value:avg_score
    '''
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    record_dict = {}
    score_dict = {}
    f = open(input_file)

    for line in f:
        if linenum == 0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item)<4:
            continue
        userid, itemid, rating = item[0], item[1], item[2]
        if itemid not in record_dict:
            record_dict[itemid] = [0,0.0]
        record_dict[itemid][0] += 1
        record_dict[itemid][1] += float(rating)
        f.closed

    for itemid in record_dict:
        score_dict[itemid] = round(record_dict[itemid][1]/record_dict[itemid][1],3)
    return score_dict




if __name__ == '__main__':
    item_dict = get_item_info('../data/movies.csv')
    print(len(item_dict))
    print(item_dict['1'])
    print(item_dict['10'])

    score_dict = get_avg_socre('../data/ratings.csv')
    print(len(score_dict))
    print(score_dict['31'])
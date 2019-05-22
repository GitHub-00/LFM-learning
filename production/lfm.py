
import numpy as np
import sys
import operator
sys.path.append('../until')
import until.readdata as read


def lfm_train(train_data, F, alpha, beta, step):
    '''
    Args:
        train_data: train data fof lfm
        F: user vetor len, item vetor len
        alpha: regulariation factor
        beta: learning rate
        step: iteration num
    Return:
        dick key: itemid value: np.ndarray
        dict key: userid value: np.ndarray
    '''

    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        for data_instance in train_data:
            userid, itemid, label = data_instance
            if userid not in user_vec:
                user_vec[userid] = init_model(F)
            if itemid not in item_vec:
                item_vec[itemid] = init_model(F)
        delta = label - model_predict(user_vec[userid], item_vec[itemid])
        for index in range(F):
            user_vec[userid][index] += beta*(delta*item_vec[itemid][index] - alpha*user_vec[userid][index])
            item_vec[itemid][index] += beta*(delta*user_vec[userid][index] - alpha*item_vec[itemid][index])

        beta = beta*0.9

    return user_vec,item_vec


def init_model(vector_len):
    '''
    Args:
         vector_len: the length if vector
     Return:
         a ndarray
    '''
    return np.random.randn(vector_len)

def model_predict(user_vector, item_vector):
    '''
    Args:
        user_vector: model produce user vector
        item_vector: model produce item vector
    Return:
        a number
    '''

    res = np.dot(user_vector,item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
    return res

def model_train_process():
    '''test model train process'''
    train_data = read.get_train_data('../data/ratings.csv')
    user_vec,item_vec = lfm_train(train_data,50,0.01,0.1,50)
    #for userid in user_vec:
        #recom_result = give_recom_result(user_vec,item_vec,userid)
    recom_result = give_recom_result(user_vec, item_vec, '24')
    ana_recom_result(train_data,'24',recom_result)



def give_recom_result(user_vec, item_vec, userid):
    '''
    use lfm model result give ifx userid recom result
    args:
        user_vec: lfm model result
        item_vec: lfm model result
        userid: fix userid
    return:
        a list[(itemid,score),(itemid2,socre2)...]
    '''
    fix_num = 10
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector)/(np.linalg.norm(user_vector)*np.linalg.norm(item_vector))
        record[itemid] = res
    for zuhe in sorted(record.items(),key = operator.itemgetter(1))[-fix_num:]:
        itemid = zuhe[0]
        score = round(zuhe[1],3)
        recom_list.append((itemid, score))
    return recom_list

def ana_recom_result(train_data, userid, recom_list):
    '''
    test recom result for userid
    Args:
        train_data: train data for lfm model
        userid:fix userid
        recom_list: recom result by lfm
    '''
    item_info = read.get_item_info('../data/movies.csv')
    for data_instance in train_data:
        tmp_userid, itemid, label = data_instance
        if tmp_userid==userid and label == 1:
            print (item_info[itemid])
    print('recom result')
    for zuhe in recom_list:
        print(item_info[zuhe[0]])

if __name__=='__main__':
    model_train_process()
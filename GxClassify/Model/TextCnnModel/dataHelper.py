# coding: utf-8

import pandas
import os
import numpy as np
from gensim import corpora
import tensorflow.contrib.keras as kr
from Log.logger import run_log as log
import pickle
from Application import Application
from sklearn.model_selection import train_test_split
from Model.TextCnnModel import prep
from Model.TextCnnModel.cut import Cut

def readData(panda_all_data):
    """读取文件数据"""
    all_data = panda_all_data['gx_regular_label'][['question','label_2']]
    all_data.dropna()
    all_data['question'] = all_data['question'].apply(prep.pre)

    return all_data

def vocab_exists(vocab_dir):
    if os.path.exists(vocab_dir):
        return True
    else:
        return False

def build_vocab(all_data, vocab_dir='vocab.dict'):
    """根据训练集构建词汇表，存储"""
    question_data = readData(all_data)['question']
    # vocab_data = [[c for c in x] for x in question_data]
    # vocab_data = [jieba.lcut(x) for x in question_data]
    vocab_data = [Cut.cut(x) for x in question_data]
    vocab = corpora.Dictionary([['PAD'],['UN']])
    vocab.add_documents(vocab_data)

    vocab.save(vocab_dir)



def load_vocab( vocab_dir):
    """读取词汇表"""
    try:
        vocab = corpora.Dictionary.load(vocab_dir)
        return vocab
    except Exception as e:
        log.error("加载词典失败：%s"%e)



def build_category(all_data,categories_dir):
    categories = list(set(all_data['label_2']))
    with open(categories_dir, 'wb') as f:
        label_id = dict(zip(categories, range(len(categories))))
        pickle.dump(label_id, f)
    return label_id, categories

def read_category(categories_dir):
    """读取分类目录"""
    try:
        with open(categories_dir, 'rb') as f:
            label_id = pickle.load(f)
            categories = list(label_id.keys())
            return label_id, categories
    except Exception as e:
        log.error("分类字典打开错误：%s"%e)


def category_id(label,categories_dir):

    label_id, _ = read_category(categories_dir=categories_dir)
    id_label = {}
    for k, v in label_id.items():
        id_label[v] = k

    category = []

    for lab in label:
        for l in lab:
            if l in id_label:
                category.append(id_label[l])
            else:
                category.append('-1')
    return category


def process_file(pandas_all_data, vocab_dir,categories_dir, max_length=50):
    """将文件转换为id表示"""
    all_data = readData(pandas_all_data)

    if not vocab_exists(vocab_dir):
        build_vocab(pandas_all_data,vocab_dir)

    vocab = load_vocab(vocab_dir)
    if not os.path.exists(categories_dir):
        label_dict, _ = build_category(all_data,categories_dir)
    else:
        label_dict, _ = read_category(categories_dir)


    # doc2id = lambda s : vocab.doc2idx([x for x in s],unknown_word_index=2)
    # doc2id = lambda s: vocab.doc2idx(jieba.lcut(s), unknown_word_index=2)
    doc2id = lambda s: vocab.doc2idx(Cut.cut(s), unknown_word_index=2)

    lab2id = lambda s :label_dict[s]
    all_data['question'] = all_data['question'].apply(doc2id)
    all_data['label_2'] = all_data['label_2'].apply(lab2id)



    xy_pad_data = pandas.DataFrame({'x':list(kr.preprocessing.sequence.pad_sequences(all_data['question'], max_length,padding='post',value=0)),
                             'y':list(kr.utils.to_categorical(all_data['label_2'], num_classes=len(label_dict)))})

    return xy_pad_data


def build_train_val(data,reset=False):

    train = data
    val = train.sample(frac = 0.3)

    if reset:
        train, test = train_test_split(train, test_size=0.1)
        
        test_dir = Application.base_dir + r'\Model\TextCnnModel\user_dict\test.csv'
        
        with open(test_dir, 'wb') as f:
            pickle.dump(test, f)
        
        val = test
    # train, val = train_test_split(train,test_size=0.1)
    # val = None
    train = train.sample(frac = 1)
    print(train.shape)
    return train,val



def batch_iter(data, batch_size=64):
    """生成批次数据"""
    data_len ,_ = data.shape
    num_batch = int((data_len - 1) / batch_size) + 1


    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)

        yield np.array(data['x'][start_id:end_id]).tolist(), np.array(data['y'][start_id:end_id]).tolist()



def process_sentence(question,vocab_dir):

    vocab = load_vocab(vocab_dir=vocab_dir)

    # question_id = vocab.doc2idx([x for x in question], unknown_word_index=2)
    question_id = vocab.doc2idx(Cut.cut(prep.pre(question)), unknown_word_index=2)

    question_id = list(kr.preprocessing.sequence.pad_sequences([question_id], 100, padding='post', value=0))

    return question_id
#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from  collections import Counter

import os
import time
import jieba
from datetime import timedelta
import pickle
import numpy as np
import tensorflow as tf
from sklearn import metrics
from Model.TextCnnModel import dataHelper
from Application import Application
from Model.TextCnnModel.TextCnnModel import TextCnnModel
from Model.TextCnnModel.TextCnnConfig import TextCnnConfig
import Application as App
from Log.logger import run_log as log
import pandas
from Util.sqlUtil.sqlalchemyUtil import SqlalchemyUtil


class TextCnn(object):

    config = TextCnnConfig()

    def __init__(self):
        log.info('Configuring CNN model...')


    def get_time_dif(self,start_time):
        """获取已使用时间"""
        end_time = time.time()
        time_dif = end_time - start_time
        return timedelta(seconds=int(round(time_dif)))

    def evaluate(self,sess, val, model):
        """评估在某一数据上的准确率和损失"""
        data_len, _ = val.shape
        batch_eval = dataHelper.batch_iter(val, batch_size=128)
        total_loss = 0.0
        total_acc = 0.0
        for batch_x, batch_y in batch_eval:
            batch_len = len(batch_x)
            feed_dict = {model.input_x: batch_x, model.input_y: batch_y}
            loss, acc = sess.run([model.loss, model.acc], feed_dict=feed_dict)
            total_loss += loss * batch_len
            total_acc += acc * batch_len

        return total_loss / data_len, total_acc / data_len

    def reset_train_val(self,train, val):

        data = train.append(val)
        train, val = dataHelper.build_train_val(data,reset=True)

        return train, val

    def train(self):

        Continue = False

        model = TextCnnModel(self.config, keep_prob=self.config.dropout_keep_prob)

        # 配置 Saver
        if not os.path.exists(TextCnnConfig.save_dir):
            os.makedirs(TextCnnConfig.save_dir)

        # 载入训练集与验证集
        start_time = time.time()

        data = dataHelper.process_file(Application.all_data, vocab_dir=TextCnnConfig.vocab_dir,
                                       categories_dir=TextCnnConfig.categories_dir, max_length=TextCnnConfig.seq_length)

        train_data, val_data = dataHelper.build_train_val(data,reset=True)         #全量用True，test是用FALSE



        # 创建session
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            if Continue :
                model.saver.restore(sess=sess, save_path=TextCnnConfig.save_path)
                Continue = False

            print('Training and evaluating...')
            start_time = time.time()
            total_batch = 0  # 总批次
            best_acc_val = 0.0  # 最佳验证集准确率
            last_improved = 0  # 记录上一次提升批次
            require_improvement = 1000  # 如果超过1000轮未提升，提前结束训练
            loss_val =0.0
            acc_val = 0.0

            flag = False
            for epoch in range(self.config.num_epochs):
                print('Train Epoch:', epoch + 1)
                print(val_data.shape)

                # train_data, val_data = self.reset_train_val(train_data,val_data)

                for batch_x, batch_y in dataHelper.batch_iter(train_data):
                    if total_batch >= 800:
                        model.saver.save(sess=sess, save_path=TextCnnConfig.save_path)
                        break
                    feed_dict = {model.input_x: batch_x, model.input_y: batch_y}
                    if total_batch % self.config.print_per_batch == 0:
                        # 每多少轮次输出在训练集和验证集上的性能
                        # feed_dict[model.keep_prob] = 1.0
                        loss_train, acc_train = sess.run([model.loss, model.acc], feed_dict=feed_dict)
                        loss_val, acc_val = self.evaluate(sess, val_data, model)  # todo

                        # if (acc_val + 0.01) > best_acc_val and abs(acc_train-acc_val)<0.02:
                        if acc_val >= best_acc_val:
                            # 保存最好结果
                            best_acc_val = acc_val
                            last_improved = total_batch
                            os.chdir(r"G:\项目3—广西文本分类\GxClassify\Model\TextCnnModel\checkpoints\best_validation")
                            print(os.getcwd())
                            model.saver.save(sess=sess, save_path="./best_validation")
                            improved_str = '*'
                        else:
                            improved_str = ''

                        time_dif = self.get_time_dif(start_time)
                        msg = 'Iter: {0:>6}, Train Loss: {1:>6.2}, Train Acc: {2:>7.2%},' \
                              + ' Val Loss: {3:>6.2}, Val Acc: {4:>7.2%}, Time: {5} {6}'
                        print(msg.format(total_batch, loss_train, acc_train, loss_val, acc_val, time_dif, improved_str))

                    sess.run(model.optim, feed_dict=feed_dict)  # 运行优化
                    total_batch += 1

                    if total_batch - last_improved > require_improvement:
                        # 验证集正确率长期不提升，提前结束训练
                        log.warning("No optimization for a long time, auto-stopping...")
                        flag = True
                        break  # 跳出循环
                if flag:  # 同上
                    break

            # model.saver.save(sess=sess, save_path=TextCnnConfig.save_path)   #最终模型
            log.info('train finish use time :%s'%(self.get_time_dif(start_time)))

    def test(self):

        model = TextCnnModel(self.config, keep_prob=1)

        start_time = time.time()




        with open(self.config.test_dir, 'rb') as f:
            test_data = pickle.load(f)

        test_size, _ = test_data.shape

        _, categories = dataHelper.read_category(categories_dir=TextCnnConfig.categories_dir)
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        model.saver.restore(sess=sess, save_path=TextCnnConfig.save_path)  # 读取保存的模型


        loss_test, acc_test = self.evaluate(sess, test_data,model)
        msg = 'Test Loss: {0:>6.2}, Test Acc: {1:>7.2%}'
        print(msg.format(loss_test, acc_test))

        # y_pred_cls = np.zeros(shape=test_size, dtype=np.int32)  # 保存预测结果
        y_pred_cls = []
        y_test_cls = None
        for x, y in dataHelper.batch_iter(test_data, batch_size=test_size):  # 逐批次处理

            feed_dict = {
                model.input_x: x,
            }
            y_pred_cls = sess.run(model.y_pred_cls, feed_dict=feed_dict)
            y_test_cls = np.argmax(y, 1)

        print(y_pred_cls)

        # 评估
        print("Precision, Recall and F1-Score...")
        print(metrics.classification_report(y_test_cls, y_pred_cls, target_names=list(categories)))


        wc = []
        wct = []
        y_test_cls = y_test_cls.tolist()
        y_pred_cls = y_pred_cls.tolist()

        for i in range(len(y_pred_cls)):
            # wc.append(y_pred_cls[i])
            # wct.append(y_test_cls[i])
            if y_pred_cls[i]-y_test_cls[i] !=0:
                wc.append(y_pred_cls[i])
                wct.append(y_test_cls[i])

        print(wc)
        print(wct)
        print(len(wc))
        # print(dataHelper.category_id([wc],TextCnnConfig.categories_dir))
        # print(dataHelper.category_id([wct], TextCnnConfig.categories_dir))
        # label_id , _ = dataHelper.read_category(TextCnnConfig.categories_dir)
        # print(label_id)
        # test_data = test_data.reset_index()
        # test_data['label_p'] = pandas.Series(np.array(dataHelper.category_id([wc],TextCnnConfig.categories_dir)))
        # test_data['label_T'] = pandas.Series(np.array(dataHelper.category_id([wct], TextCnnConfig.categories_dir)))
        # print(test_data)
        #
        # test_data = test_data.drop('x',1)
        # test_data = test_data.drop('y', 1)
        # print(test_data)
        # SqlalchemyUtil.pandas_to_sql(test_data,table_name='q_label_test')
        time_dif = self.get_time_dif(start_time)
        log.info("Time usage:", time_dif)


    def predict(self, question):

        model = TextCnnModel(self.config, keep_prob=1)


        with tf.Session() as sess:


            sess.run(tf.global_variables_initializer())

            model.saver.restore(sess=sess, save_path=TextCnnConfig.save_path)  # 读取保存的模型

            question_id = dataHelper.process_sentence(question=question, vocab_dir=TextCnnConfig.vocab_dir)

            feed = {model.input_x: question_id}
            label = sess.run([model.y_pred_cls], feed_dict=feed)
            return dataHelper.category_id(label, TextCnnConfig.categories_dir)

    def predict_doc(self,question_list):

        model = TextCnnModel(self.config, keep_prob=1)

        question_id = []
        for question in question_list:
            question_id +=(dataHelper.process_sentence(question=question, vocab_dir=TextCnnConfig.vocab_dir))


        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            model.saver.restore(sess=sess, save_path=TextCnnConfig.save_path)  # 读取保存的模型


            feed = {model.input_x: question_id}
            label = sess.run([model.y_pred_cls], feed_dict=feed)
            return dataHelper.category_id(label, TextCnnConfig.categories_dir)

    def predict_doc_softmax(self,question_list):

        model = TextCnnModel(self.config, keep_prob=1)

        question_id = []
        for question in question_list:
            question_id += (dataHelper.process_sentence(question=question, vocab_dir=TextCnnConfig.vocab_dir))

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            model.saver.restore(sess=sess, save_path=TextCnnConfig.save_path)  # 读取保存的模型

            feed = {model.input_x: question_id}
            logit,p = sess.run([model.r_softmax,model.y_pred_cls], feed_dict=feed)
            print(p)
        return logit

    @classmethod
    def run(cls ,action='predict', question='',question_list = None):



        log.info('action : %s'%action)

        if action == 'train':
            cls.train(cls)
        elif action == 'test':
            cls.test(cls)
        elif action == 'doc':
            return cls.predict_doc(cls,question_list)
        elif action=='softmax':
            return cls.predict_doc_softmax(cls,question_list)
        else:
            return cls.predict(cls,question=question)



if __name__ == '__main__':

    App.tasker()
    t = TextCnn()
    t.train()
#    t.test()
    # t.predict(question='')






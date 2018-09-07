from Application import Application
import os

class TextCnnConfig(object):
    """CNN配置参数"""

    embedding_dim = 200  # 词向量维度
    seq_length = 100  # 序列长度
    num_classes = 36  # 类别数
    num_filters = 128  # 卷积核数目

    vocab_size = 8000  # 词汇表达小

    filter_sizes = [2, 3, 4, 5, 6]

    hidden_dim = 256  # 全连接层神经元

    dropout_keep_prob = 0.4 # dropout保留比例
    learning_rate = 1e-3  # 学习率

    batch_size = 64  # 每批训练大小
    num_epochs = 200  # 总迭代轮次

    print_per_batch = 50  # 每多少轮输出一次结果
    save_per_batch = 10  # 每多少轮存入tensorboard

    l2_reg_lambda = 0.15
    #

    base_dir = Application.base_dir

    save_dir = os.path.join(base_dir, r'Model\TextCnnModel\checkpoints')
    save_path = os.path.join(save_dir, 'best_validation')  # 最佳验证结果保存路径
    vocab_dir = os.path.join(base_dir, r'Model\TextCnnModel\user_dict\vocab.dict')
    categories_dir = os.path.join(base_dir, r'Model\TextCnnModel\user_dict\categories.dict')
    test_dir = os.path.join(base_dir, r'Model\TextCnnModel\user_dict\test')
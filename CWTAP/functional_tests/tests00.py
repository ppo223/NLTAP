class FunctionalTest(object):

    def test_lexical_analysis(self):
        """ 词分析功能测试 """
        # 李雷得知文本分析平台有词分析功能
        # 他正好有一段话需要做分析，所以他详细查看了接口文档
        # 首先他请管理员帮他创建一个租户
        # 然后请管理员帮他创建自己的用户
        # 因为是词分析功能，所以他想查看一下都有哪些词库
        # 发现因为没有登录，导致无法认证用户
        # 然后李雷使用自己的用户进行登录
        # 他先浏览了默认的词库
        # 他发现默认词库中有通用关键词库和停用词库
        # 他发起了一个词分析任务
        # 在查看结果的过程中，发现有些词并没有被分析出来
        # 他创建业务词库，并添加了业务关键词
        # 之后他重新发送了词分析的请求
        # 在结果中，发现了被分析出来的业务关键词
        # 然后他就满意的睡了
        pass

    def test_text_dependency(self):
        """ 句法分析功能测试 """
        # 韩梅梅得知文本分析平台有句法分析功能
        # 她想试一下句法分析的功能
        # 她发送一个句法分析的请求
        # 发现没有用户认证
        # 而后她找到管理员帮助她创建了用户和密码
        # 她登录以后，发送了一个句法分析的功能请求
        # 她看到了想要的结果以后满意的睡了
        pass

    def test_emotion(self):
        """ 情感分析功能测试 """
        # 李雷得知文本分析平台有情感分析功能
        # 他通过登录里面发送了一个情感分析的请求
        # 看到结果以后不太满意
        # 他向管理员请教以后得知可以通过设置情感词来优化结果
        # 他查看现有情感词库中的情感词
        # 他创建了自己的情感词库，并向其中添加了一些情感词
        # 然后他重新发送了一个情感分析的请求
        # 最后他看到了想要的结果以后满意的睡了
        pass

    def test_similarity(self):
        """ 相似度分析功能测试 """
        pass

    def test_word_association_train(self):
        """ 词语联想模型训练功能测试 """
        pass

    def test_word_association_predict(self):
        """ 词语联想模型预测功能测试 """
        pass

    def test_word_discovery(self):
        """ 新词发现功能测试 """
        pass

    def test_classification_train(self):
        """ 分类训练功能测试 """
        pass

    def test_classification_predict(self):
        """ 分类预测功能测试 """
        pass

    def test_cluster_analysis(self):
        """ 聚类分析功能测试 """
        pass

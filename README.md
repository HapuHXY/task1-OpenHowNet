# 基于OpenHowNet的上下文关系自动抽取

OpenHowNet项目存放HowNet核心数据和清华大学自然语言处理实验室（THUNLP）开发的OpenHowNet API，提供方便的义原信息查询、义原树展示、基于义原的词相似度计算等功能。

## 算法思想
* 利用 OpenHowNet API 获取 HowNet 中的词语对应概念的标注，基于义原的标注信息，找到基于义原定义的核心描述词，将其作为词语的上位词
* 使用基于义原的词语相似度度量，获取指定词的同义词或与指定词最 接近的 K 个词，间接获取词语的上下位关系词
* 检索义原之间的存在的上下位关系，对数据集 D 进行扩充

## HowNet核心数据
HowNet核心数据文件（`HowNet.txt`）由223,767个中英文词和词组所代表的概念构成。HowNet为每个概念标注了基于义原的定义以及词性、情感倾向、例句等信息。

## OpenHowNet API
### 运行要求

* Python==3.6
* anytree==2.4.3
* tqdm==4.31.1
* requests==2.22.0

### 安装

* 通过 pip 安装（推荐）

```bash
pip install OpenHowNet
```

### 接口说明 / Interfaces

|接口|功能说明|参数说明|
|---|-------|-------|
|get(self, word, language=None)|检索HowNet中词语对应的概念标注的完整信息|`word`表示待查词，`language`为`en`(英文)或`zh`(中文)，默认双语同时查找|
|get\_sememes\_by\_word(self, word, structured=False, lang='zh', merge=False, expanded_layer=-1)|检索输入词的义原，可以选择是否合并多个义项，也可以选择是否以结构化的方式返回，还可以指定展开层数。|`word`表示待查词，`language`为`en`(英文)或`zh`(中文), `structured`表示是否以结构化的方式返回，`merge`控制是否合并多义项，`expanded_layer`控制展开层数，默认全展开|
|initialize\_sememe\_similarity\_calculation(self)|初始化基于义原的词语相似度计算（需要读取相关文件并有短暂延迟）|
|calculate\_word\_similarity(self, word0, word1)|计算基于义原的词语相似度，调用前必须先调用上一个函数进行初始化|`word0`和`word1`表示待计算相似度的词对|
|get\_nearest\_words\_via\_sememes(self, word, K=10)|在使用基于义原的词语相似度度量下，检索和待查词最接近的K个词|`word`表示待查词，`K`表示K近邻算法取的Top-K|
|get\_sememe\_relation(self, sememe0, sememe1)|获取两个义原之间的关系|`sememem0`和`sememem1`代表待查义原|
|get\_sememe\_via\_relation(self, sememe, relation, lang='zh')|检索和某个义原存在某种关系所有义原|`sememe`代表待查义原，`relation`代表关系，`language`为`en`(英文)或`zh`(中文)|


### 使用示例

#### 初始化

```python
import OpenHowNet
hownet_dict = OpenHowNet.HowNetDict()
```
这里如果没有下载义原数据会报错，需要执行`OpenHowNet.download()`。


#### 获取HowNet中的词语对应概念的标注

默认情况下，api将搜索HowNet中输入词的中文和英文标注，带来不必要的开销。注意，如果目标词在HowNet中无标注，将返回空list。

```python
>>> result_list = hownet_dict.get("苹果")
>>> print("检索数量：",len(result_list))
>>> print("检索结果范例:",result_list[0])
检索数量： 6
检索结果范例: {'Def': '{computer|电脑:modifier={PatternValue|样式值:CoEvent={able|能:scope={bring|携带:patient={$}}}}{SpeBrand|特定牌子}}', 'en_grammar': 'noun', 'zh_grammar': 'noun', 'No': '127151', 'syn': [{'id': '004024', 'text': 'IBM'}, {'id': '041684', 'text': '戴尔'}, {'id': '049006', 'text': '东芝'}, {'id': '106795', 'text': '联想'}, {'id': '156029', 'text': '索尼'}, {'id': '004203', 'text': 'iPad'}, {'id': '019457', 'text': '笔记本'}, {'id': '019458', 'text': '笔记本电脑'}, {'id': '019459', 'text': '笔记本电脑'}, {'id': '019460', 'text': '笔记本电脑'}, {'id': '019461', 'text': '笔记本电脑'}, {'id': '019463', 'text': '笔记簿电脑'}, {'id': '019464', 'text': '笔记簿电脑'}, {'id': '020567', 'text': '便携式电脑'}, {'id': '020568', 'text': '便携式计算机'}, {'id': '020569', 'text': '便携式计算机'}, {'id': '127224', 'text': '平板电脑'}, {'id': '127225', 'text': '平板电脑'}, {'id': '172264', 'text': '膝上型电脑'}, {'id': '172265', 'text': '膝上型电脑'}], 'zh_word': '苹果', 'en_word': 'apple'}

>>> hownet_dict.get("test_for_non_exist_word")
[]
```

### 获取所有HowNet中的词语

```python
>>> zh_word_list = hownet_dict.get_zh_words()
>>> print(zh_word_list[:30])
['', '"', '#', '#号标签', '$', '%', "'", '(', ')', '*', '+', '-', '--', '...', '...出什么问题', '...底', '...底下', '...发生故障', '...发生了什么', '...何如', '...家里有几口人', '...检测呈阳性', '...检测呈阴性', '...来', '...内', '...为止', '...也同样使然', '...以来', '...以内', '...以上']


#### 获取输入词去结构的义原集合

注意：`lang`、`merge`、`expanded_layer`等参数只在`structured = False`时有效。这是因为当处理结构化的数据时，有多种方式解释这些参数，使用者可以自行选择。在下一章节，你将看到如何使用结构化的数据。参数的详细解释在文档中给出。

获取合并过后的多义词的义原

```python
>>> hownet_dict.get_sememes_by_word("苹果",structured=False,lang="zh",merge=True)
{'电脑', '交流', '用具', '水果', '特定牌子', '样式值', '能', '树', '生殖', '携带'}


#### 获取指定词的同义词

相似度计算是基于义原的。

```python
>>> hownet_dict["苹果"][0]["syn"]
[{'id': '004024', 'text': 'IBM'},
 {'id': '041684', 'text': '戴尔'},
 {'id': '049006', 'text': '东芝'},
 {'id': '106795', 'text': '联想'},
 {'id': '156029', 'text': '索尼'},
 {'id': '004203', 'text': 'iPad'},
 {'id': '019457', 'text': '笔记本'},
 {'id': '019458', 'text': '笔记本电脑'},
 {'id': '019459', 'text': '笔记本电脑'},
 {'id': '019460', 'text': '笔记本电脑'},
 {'id': '019461', 'text': '笔记本电脑'},
 {'id': '019463', 'text': '笔记簿电脑'},
 {'id': '019464', 'text': '笔记簿电脑'},
 {'id': '020567', 'text': '便携式电脑'},
 {'id': '020568', 'text': '便携式计算机'},
 {'id': '020569', 'text': '便携式计算机'},
 {'id': '127224', 'text': '平板电脑'},
 {'id': '127225', 'text': '平板电脑'},
 {'id': '172264', 'text': '膝上型电脑'},
 {'id': '172265', 'text': '膝上型电脑'}]
```


#### 获取所有义原

```python
>>> len(hownet_dict.get_all_sememes())
2187
```

#### 查询义原之间的关系

你输入的义原可以使用任意语言：

```python
>>> hownet_dict.get_sememe_relation("音量值", "尖声")
'hyponym'

>>> hownet_dict.get_sememe_relation("尖声", "SoundVolumeValue")
'hyponym'

>>> hownet_dict.get_sememe_relation("shrill", "SoundVolumeValue")
'hypernym'

#### 检索与输入义原存在某种关系的所有义原

你输入的义原可以使用任意语言，但是关系必须为英文小写；同时你可以指定输出的义原的语言，默认为中文。

```python
>>> hownet_dict.get_sememe_via_relation("音量值", "hyponym")
['高声', '低声', '尖声', '沙哑', '无声', '有声']


### 高级功能：通过义原计算词语相似度

实现方法基于以下论文：

> Jiangming Liu, Jinan Xu, Yujie Zhang. An Approach of Hybrid Hierarchical Structure for Word Similarity Computing by HowNet. In Proceedings of IJCNLP

#### 额外初始化

由于计算相似度需要额外的文件，初始化的开销将比之前的大。你可以按照如下方式初始化：

```python
>>> hownet_dict_advanced = OpenHowNet.HowNetDict(use_sim=True)
```

你也可以在需要使用时再进行额外的初始化，这时，初始化的返回值将代表额外的初始化是否成功。

```python
>>> hownet_dict.initialize_sememe_similarity_calculation()
True
```

#### 计算两个指定词的相似度

如果其中的任何一个词不在HowNet中，函数将返回0。

```python
>>> hownet_dict_advanced.calculate_word_similarity("苹果", "梨")
1.0
```




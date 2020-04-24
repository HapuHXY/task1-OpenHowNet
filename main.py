#! /usr/bin/env python3
"""
基于OpenHowNet实现上下位关系自动抽取
	@article{qi2019openhownet,
	  title={OpenHowNet: An Open Sememe-based Lexical Knowledge Base},
	  author={Qi, Fanchao and Yang, Chenghao and Liu, Zhiyuan and Dong, Qiang and Sun, Maosong and Dong, Zhendong},
	  journal={arXiv preprint arXiv:1901.09957},
	  year={2019},
	}
将上下位关系词对写入文件中中，用Tab键隔开，以（下位词，上位词）顺序写入
"""

import OpenHowNet	#初始化，下载义原数据
#OpenHowNet.download()
hownet_dict = OpenHowNet.HowNetDict()
hownet_dict.initialize_sememe_similarity_calculation()    #初始化基于义原的词语相似度计算（需要读取相关文件并有短暂延迟）

f=open("/home/hxy/task1-OpenHowNet/result.txt",'a')

"""
任务一：获得HowNet中所有词语对应概念的标注信息，将其核心描述词作为上位词
任务二：获得词语属于某一释义的同义词，将同义词扩充进去，间接获得上下文关系词对
任务三：检索义原之间的存在的上下位关系，把义原之间的上下文关系补充到数据库中
"""

#获得HowNet中所有词语
zh_word_list=hownet_dict.get_zh_words()
for word in zh_word_list:
	try:
		#获取HowNet中的词语对应概念的标注
		result_list = hownet_dict.get(word, language="zh")	
		if(len(result_list)>0):
			#获得词语的义原集合
			sememes_dict=hownet_dict.get_sememes_by_word(word,structured=False,lang="zh",merge=True)	
		
			for sememe in sememes_dict:
				if(len(hownet_dict.get(sememe)) > 0  and hownet_dict.calculate_word_similarity(word,sememe) >= 0.6):	#计算词语与义原的相似度，将相似度高的义原作为核心描述词
					f.write(word)
					f.write('\t')
					f.write(sememe)
					f.write('\n')
				else:
					continue
		
			for i in range(len(result_list)):
				syn_dict=set()	#存放词语属于某一释义的同义词
				for res in result_list[i]["syn"]:
					syn_dict.add(res["text"])
			
				for syn in syn_dict:	#同义词间接获得上下文关系词对
					if(len(hownet_dict.get(syn))>0):
						for sememe in sememes_dict:
							if(len(hownet_dict.get(sememe)) > 0  and hownet_dict.calculate_word_similarity(syn,sememe) >= 0.6):
								f.write(syn)
								f.write('\t')
								f.write(sememe)
								f.write('\n')
							else:
								continue
	except:
		print("error")
	else:
		continue


all_sememes=hownet_dict.get_all_sememes()		#检索义原之间的存在的上下位关系
for sememe in all_sememes:
	hyper_dict=set(hownet_dict.get_sememe_via_relation(sememe,"hypernym"))
	for hyper in hyper_dict:
		f.write(sememe)
		f.write('\t')
		f.write(hyper)
		f.write('\n')	

f.close()

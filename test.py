#! /usr/bin/env python3

import OpenHowNet	#初始化，下载义原数据
#OpenHowNet.download()
hownet_dict = OpenHowNet.HowNetDict()
hownet_dict.initialize_sememe_similarity_calculation()

pairs=[]
zh_word_list=["矮墙","爱巢","替罪羊","布达拉宫","布什","布衣之交","擦伤","裁判","财产权","堤坝","敌舰","大百科","牛仔","额手礼","恩格尔系数","肥缺","匪酋","废井","暖气","高利贷","高堂","跑鞋","泼水节","湖震","虎克定律","饥馑","科研","脸书","列传","苹果"]
f=open("./result.txt",'a')
for word in zh_word_list:
	try:
		#获取HowNet中的词语对应概念的标注
		result_list = hownet_dict.get(word, language="zh")	
		for i in range(len(result_list)):
			#只抽取名词的上下位关系
			if(result_list[i]["ch_grammar"] != "noun"):
				break
			
			#比较义原树的不同展开层数，获得上位词候选集，展开2、3、4、5层
			sememes_dict=hownet_dict.get_sememes_by_word(word,structured=False,lang="zh",merge=True,expanded_layer=2)	
		
			for sememe in sememes_dict:
				#比较采取不同相似度取值的限制（0.5、0.6、0.7、0.8），对上位词候选作进一步筛选
				if(len(hownet_dict.get(sememe)) > 0 and word!=sememe and hownet_dict.calculate_word_similarity(word,sememe) >= 0.50):	
					pair=[word,sememe]
					if pair not in pairs:
						pairs.append(pair)			
				else:
					continue
	except:
		print("error")
	else:
		continue


for pair in pairs:
	f.write(pair[0]+'\t'+pair[1]+'\n')
f.close()

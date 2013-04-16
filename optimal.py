# -*- coding:utf-8 -*-
'''
optimal是最优生成器，对于一个tic状态给出最优解
'''
import os
import json
import random
from collections import defaultdict
class Optimal(object):
  """用类来实现一个最优解"""
  def __init__(self):
    self.init()

  def init(self):
    #根据 存储文件的数据初始化
    self.para=self.read()

  def read(self):
    data_name='data'
    data_new_name='data_new'
    if os.path.isfile(data_new_name):
      f=open(data_new_name)
      para=json.loads(f.read())
    else:
      f=open(data_name,'wb')
      para={'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0} #9个参数都是0 ps!!!:json要求key必须是str,会被默认转为str
      f.write(json.dumps(para))
      f.close()
    return para
  def assign(self,sche):
    #根据状态赋值
    if sche not in range(9): return None
    return self.para[str(sche)]

  def optimal(self,status):
    #根据status状态算出最优解。
    #基本思路是枚举每个可能的点，然后下每个点后计算分数，取最高的。
    option=self.enum(status)
    score=[]
    if not option: return None
    for i,j in option:
      status[i][j]=1 #下上自己的子
      score.append(self.calc(status)[0]) #只取分数
      status[i][j]=0 #状态回复
    #找出最大的得分,如果有重复,则随机取出一个. 
    score_max=max(score)
    count=score.count( score_max ) #最大值的个数
    ran=random.randrange(count)
    for i in range(len(score)):
      if score[i] == score_max: ran-=1
      if ran < 0: return option[i]

  def calc(self,status):
    #根据status和self.para算出分数
    score=0
    #判断8个行列斜
    res_scheme=defaultdict(int)
    for line in status:
      scheme=self._ca(line) #属于哪种模式
      res_scheme[scheme]+=1
      score+=self.assign(scheme)

    for col in [[li[i] for li in status ] for i in range(3)]: #矩阵转置成列
      scheme=self._ca(col) #属于哪种模式
      res_scheme[scheme]+=1
      score+=self.assign(scheme)

    x1=[status[i][i] for i in range(3)] #对角线
    scheme=self._ca(x1)
    res_scheme[scheme]+=1
    score+=self.assign(scheme)

    x2=[status[i][2-i] for i in range(3)]
    scheme=self._ca(x2)
    res_scheme[scheme]+=1
    score+=self.assign(scheme)
    #返回总得分
    #print status, score, res_scheme
    return score, res_scheme

  def _ca(self,line):
    tmp=defaultdict(int) 
    for i in line:
      tmp[i]+=1
    rule={(0,0):0, #分别表示自己子和对方子的个数,加起来不超过3
          (1,0):1,
          (2,0):2,
          (3,0):3,
          (0,1):4,
          (1,1):5,
          (2,1):6,
          (0,2):7,
          (1,2):8
    }
    x=(tmp[1],tmp[2])
    if x not in rule: return None
    return rule[x]

  def enum(self,status):
    #根据status给出所有的可以下的点
    #status=[[0,0,0],[0,0,0],[0,0,0]]
    res=[]
    for i in range(3):
      for j in range(3):
        if status[i][j]==0:
          res.append((i,j))
    return res
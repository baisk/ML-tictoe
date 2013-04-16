# -*- coding:utf-8 -*-
#泛化器,通过不同状态的判分修正参数的过程
import json
import msgpack
from optimal import Optimal
class Generalize(object):
  """docstring for Generalize"""
  def __init__(self):
    self.op=Optimal()
    self.para=self.op.read()
    pass

  def read_score(self):
    #读取经验
    f=open('Score','rb')
    for line in f:
      score=msgpack.loads(line.strip()) #去除回车等影响
      #print game
      yield score

  def run(self):
    for status, turn, score in self.read_score():
      if turn == 2: #还是将其全部变成1为自身的情况,便于处理
        for i in range(3): 
          for j in range(3):
            if status[i][j] !=0:
              status[i][j] = 3-status[i][j]
      #可以利用optimal中的calc计算权值
      cal_score, scheme = self.op.calc(status)
      for i in range(9): #一共有9个参数
        self.para[str(i)]+=scheme[i]*(score-cal_score)*0.1
      print "new para", self.para
    #写回到data中
    self.update_para()

  def update_para(self):
    open('data_new','wb').write(json.dumps(self.para))
if __name__ == '__main__':
  ge=Generalize()
  ge.run()

    
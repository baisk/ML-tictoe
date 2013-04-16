# -*- coding:utf-8 -*-
#鉴定器
#针对一连串给定的下棋策略给出每个状态判分.
import msgpack
class Verify(object):

  def __init__(self):
    self.file=open('Score','ab')
    pass

  def read_exp(self):
    #读取经验
    f=open('GameSeq','rb')
    for line in f:
      game=msgpack.loads(line.strip()) #去除回车等影响
      #print game
      yield game

  def verify(self):
    for status,turn,seq in self.read_exp():
      #print status,turn,seq
      if len(seq)%2 == 0: #偶数次,说明先玩的输了.
       score=-100
      else: score= 100

      for i,j in seq:
        status[i][j]=turn
        self.write_res(status,turn,score)
        turn = 3-turn
        score = -score

  def write_res(self,status,turn,score):
    print status,turn,score
    score_ver=(status,turn,score)
    self.file.write(msgpack.dumps(score_ver)+'\n')

if __name__ == '__main__':
  ve=Verify()
  ve.verify()
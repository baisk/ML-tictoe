# -*- coding:utf-8 -*-
#执行器
#能够接受任务,生成一连串的对弈过程.
import redis
import time
import cPickle as pickle
from optimal import Optimal
import msgpack

class Executor(object):

  def __init__(self):
    #self.peer=redis.StrictRedis(host='192.168.23.166')
    self.file=open('GameSeq','ab')
    pass

  def get_task(self):
    #从redis中读取任务
    task_name='task'
    tast_str=self.peer.lpop('task_name')
    if tast_str:
      return pickle.loads(tast_str)

  def write_res(self,status,turn,seq):
    #把这些信息写入到redis/文件中,作为训练结果.
    if not self.file: self.file=open('GameSeq','ab')
    one_game=(status,turn,seq)
    print one_game
    self.file.write(msgpack.dumps(one_game)+'\n')


  def run(self):
    #不停运行下去,选取一个任务,然后一直下直到结束,输出下子的序列
    while True:
      time.sleep(3)
      print "working~"
      #task=self.get_task() #得到一个任务,即开始状态
      task=( [[0,0,0],[0,0,0],[0,0,0]], 1) #简单起始任务
      status, turn = task
      seq=self.gen_seq(status,turn)
      self.write_res(status,turn,seq)

  def test_run(self):
    #用来模拟run,只是少了redis的存读,作为单元测试
    print "test~"
    task=( [[0,0,0],[0,0,0],[0,0,0]], 1)
    status, turn = task
    seq=self.gen_seq(status,turn)
    print seq

  def gen_seq(self,status,turn):
    #根据状态和turn来产生序列
    import copy
    if turn not in (1,2): return None
    tmp={}
    tmp[1]=copy.deepcopy(status)
    tmp[2]=copy.deepcopy(status)
    #if turn=1 则 tmp2全颠倒1和2, 否则tmp1颠倒.  暂时只有开始状态,所以不用处理
    op=Optimal()
    seq=[]
    while self.check(tmp[turn]):
      next=op.optimal(tmp[turn])
      if not next: break #没的下了也结束
      seq.append(next)
      tmp[turn][next[0]][next[1]] = 1 #表示走了一步棋
      tmp[3-turn][next[0]][next[1]] = 2 #对方看起来的效果 3-turn表示另一家
      turn = 3-turn #换边
    return seq

  def check(self, status):
    #判断是否游戏结束状态 继续则True,否则False
    #每次判断都是别人刚走完,只要判断2的数量就行了. 如果走满了也结束了
    check_num=2 #判断2的数量,3个就赢了
    win_num=3 
    for line in status:
      if line.count(check_num) == win_num: return False
    for col in [[li[i] for li in status ] for i in range(3)]:
      if col.count(check_num) == win_num: return False
    x1=[status[i][i] for i in range(3)] #对角线
    x2=[status[i][2-i] for i in range(3)]
    if x1.count(check_num)==win_num or x2.count(check_num)==win_num:
      return False
    return True

if __name__ == '__main__':
  ex=Executor()
  ex.run()
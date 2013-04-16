# -*- coding:utf-8 -*-
#单元测试
from collections import defaultdict
from optimal import Optimal
def test_optimal():
  op= Optimal()
  status=[[1, 0, 1], [0, 0, 2], [0, 0, 0]]
  print op.optimal(status)
  return op.optimal(status)

def test_op_random():
  res=[]
  for i in range(100):
    res.append(test_optimal())
  distr=defaultdict(int)
  for i in res:
    distr[i]+=1
  print distr  #结果大致为每个点都是平均的.

def test_exe_run():
  from executor import Executor
  ex=Executor()
  ex.test_run()

if __name__ == '__main__':
  #test_optimal()
  #test_op_random()
  test_exe_run()
  pass
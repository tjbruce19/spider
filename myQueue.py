import time
import threading
from queue import Queue

class Worker(threading.Thread):
    res_queue = Queue()
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()
        # self.res_queue = Queue()
    def run(self):
        # 著名的死循环，保证接着跑下一个任务
        while True:
            # 队列为空则退出线程
            if self.queue.empty():
                break
            # 获取一个项目
            do,args,kwargs= self.queue.get(block=False)
            print(args)
            print(kwargs)
            result = do(*args,**kwargs)
            self.res_queue.put(result)
            # 延时1S模拟你要做的事情
            time.sleep(1)
            # 打印
            # print(self.getName(),':', foo)
            # 告诉系统说任务完成
            self.queue.task_done()

class ThreadQueue():
    def __init__(self):
        pass

    def concurrency_func_with_thread_queue(self,func_list,args_list=None,kwargs_list=None,thread_num=3):
        results = []
        q_thread = Queue()
        for i in range(len(func_list)):
            q_thread.put((func_list[i], args_list[i],kwargs_list[i]))
        for j in range(thread_num):
            Worker(q_thread)
        q_thread.join()
        for n in range(Worker.res_queue.qsize()):
            results = results + Worker.res_queue.get()
        return results
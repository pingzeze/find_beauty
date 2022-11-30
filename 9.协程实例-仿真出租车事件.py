# -*- coding: UTF-8 -*-
import collections
import queue

Event = collections.namedtuple('Event', 'time proc action')  # 定义事件 具名元组


def taxi_process(ident, trips, start_time=0):
    """每次改变状态时创建事件，把控制权让给仿真器"""
    time = yield Event(start_time, ident, 'leave garage')
    for i in range(trips):
        time = yield Event(time, ident, 'pick up passenger')
        time = yield Event(time, ident, 'drop off passenger')
    yield Event(time, ident, 'going home')
    # 出租车进程结束


def compute_duration(previous_action):
    """模拟使用指数分布计算操作的耗时"""
    if previous_action in ['leave garage', 'drop off passenger']:
        # 新状态是四处徘徊
        interval = 10
    elif previous_action == 'pick up passenger':
        # 新状态是行程开始
        interval = 11
    elif previous_action == 'going home':
        interval = 12
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return interval


class Simulator:
    def __init__(self, procs_map):
        self.events = queue.PriorityQueue()  # 优先级队列，传入队列后根据优先级决定先出
        self.procs = dict(procs_map)  # 防御性变量，修改self.procs不会关联修改procs_map

    def run(self, end_time):
        """排定并显示事件，直到时间结束"""
        # 排定各辆出租车的第一个事件
        for _, proc in sorted(self.procs.items()):  # 取出taxis中迭代器
            first_event = next(proc)  # 预激协程
            self.events.put(first_event)  # 队列中放入事件

        # 这个仿真系统的主循环
        sim_time = 0
        while sim_time < end_time:
            if self.events.empty():  # 判断队列中事件是否为空
                print('*** end of events ***')
                break

            current_event = self.events.get()  # 取出事件
            sim_time, proc_id, previous_action = current_event  # time proc action
            print('taxi:', proc_id, proc_id * ' ', current_event)
            active_proc = self.procs[proc_id]  # 获取当前活动的出租车协程
            next_time = sim_time + compute_duration(previous_action)  # compute_duration根据指数分布返回一个时间
            try:
                next_event = active_proc.send(next_time)
            except StopIteration:
                del self.procs[proc_id]  # 迭代器终止就删除这个协程
            else:  # try代码块没有问题后执行，进入except后不执行else
                self.events.put(next_event)  # 事件放入队列
        else:
            msg = '*** end of simulation time: {} events pending ***'
            print(msg.format(self.events.qsize()))  # 返回队列大致大小


taxis = {i: taxi_process(i, (i + 1) * 2, i * 5) for i in range(3)}
"""
taxis = {0: taxi_process(ident=0, trips=2, start_time=0),
         1: taxi_process(ident=1, trips=4, start_time=5),
         2: taxi_process(ident=2, trips=6, start_time=10)}
"""


sim = Simulator(taxis)
sim.run(100)


"""最终输出
taxi: 0  Event(time=0, proc=0, action='leave garage')
taxi: 1   Event(time=5, proc=1, action='leave garage')
taxi: 0  Event(time=10, proc=0, action='pick up passenger')
taxi: 2    Event(time=10, proc=2, action='leave garage')
taxi: 1   Event(time=15, proc=1, action='pick up passenger')
taxi: 2    Event(time=20, proc=2, action='pick up passenger')
taxi: 0  Event(time=21, proc=0, action='drop off passenger')
taxi: 1   Event(time=26, proc=1, action='drop off passenger')
taxi: 0  Event(time=31, proc=0, action='pick up passenger')
taxi: 2    Event(time=31, proc=2, action='drop off passenger')
taxi: 1   Event(time=36, proc=1, action='pick up passenger')
taxi: 2    Event(time=41, proc=2, action='pick up passenger')
taxi: 0  Event(time=42, proc=0, action='drop off passenger')
taxi: 1   Event(time=47, proc=1, action='drop off passenger')
taxi: 0  Event(time=52, proc=0, action='going home')
taxi: 2    Event(time=52, proc=2, action='drop off passenger')
taxi: 1   Event(time=57, proc=1, action='pick up passenger')
taxi: 2    Event(time=62, proc=2, action='pick up passenger')
taxi: 1   Event(time=68, proc=1, action='drop off passenger')
taxi: 2    Event(time=73, proc=2, action='drop off passenger')
taxi: 1   Event(time=78, proc=1, action='pick up passenger')
taxi: 2    Event(time=83, proc=2, action='pick up passenger')
taxi: 1   Event(time=89, proc=1, action='drop off passenger')
taxi: 2    Event(time=94, proc=2, action='drop off passenger')
taxi: 1   Event(time=99, proc=1, action='going home')
taxi: 2    Event(time=104, proc=2, action='pick up passenger')
*** end of simulation time: 1 events pending ***
"""

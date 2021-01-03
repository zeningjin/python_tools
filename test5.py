import os

import test3
class Student:
    def __init__(self):
        self.a='124'

    def speak_language(self):
        data = 123
        print(data, type(data))


print(Student.speak_language)
for action in test3.subtask_action_module:
    exec("import " + action)
fname,fename=os.path.split("E:/lpthw/zedshaw/ex19.py")
cur_dir = os.path.split("/home/zening/文档/工作文档/数据库插数据/发送邮件/企业邮箱.py")[0]
print(os.listdir(cur_dir))

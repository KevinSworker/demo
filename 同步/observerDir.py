# 主要用于监视文件夹的变化，当文件有变化的时候，做出对应的处理

# 先判断进行了什么操作

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import md5
import time
import os
import shutil

REMOTE_PATH = r"\\192.168.123.10\share\user\zhouhan\work\同步"

LOCAL_PATH = r"D:\work\同步文件夹"


class MyDirEventHandler(FileSystemEventHandler):

    def on_moved(self, event):
        print(event)

    def on_created(self, event):
        # print(event)
        self.deal_with_created(event)

    def on_deleted(self, event):
        print(event)

    def on_modified(self, event):
        print("modified:", event, event.src_path)

    def deal_with_move(self, event):
        print("deal with moved file")

        # 先判断是文件还是目录
        # 目录
        if event.is_directory:
            print("move dir")

    def deal_with_created(self, event):
        print("deal with created file")
        # 先判断是文件还是目录
        # 目录
        if event.is_directory:
            relative_path = os.path.relpath(event.src_path, LOCAL_PATH) 
            remote_dir_path = os.path.join(REMOTE_PATH, relative_path)
            if not self.is_dir_exist(remote_dir_path):
                os.makedirs(remote_dir_path)
        else:
            # 文件名称
            file_name = os.path.basename(event.src_path)

            # 根据绝对路径生成远程路径对应文件夹
            path = os.path.abspath(event.src_path)
            local_dir_path = os.path.split(path)[0]
            relative_path = os.path.relpath(local_dir_path, LOCAL_PATH) 
            remote_dir_path = os.path.join(REMOTE_PATH, relative_path)
            remote_file_path = os.path.join(remote_dir_path, file_name)

            if self.is_file_exist(remote_file_path):
                # 远程文件也存在
                local_md5 = md5.get_file_md5(event.src_path)
                remote_md5 = md5.get_file_md5(remote_file_path)
                if local_md5 != remote_md5:
                    print("执行覆盖式拷贝")
                    shutil.copy2(event.src_path, remote_file_path)
            else:
                print("执行拷贝式拷贝")
                # 需要先判断路径是否存在，如果不存在，先创建路径再进行拷贝
                if not self.is_dir_exist(remote_dir_path):
                    os.makedirs(remote_dir_path)
                while True:
                    if md5.file_is_openState(event.src_path):
                        shutil.copy2(event.src_path, remote_file_path)
                        break
                    else:
                        time.sleep(1)


    # 判断文件是否存在
    def is_file_exist(self, file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False

    # 判断文件夹是否存在 
    def is_dir_exist(self, dir_path):
        if os.path.exists(dir_path):
            return True
        else:
            return False


"""
使用watchdog 监控文件的变化
"""
if __name__ == '__main__':
    # 创建观察者对象
    observer = Observer()
    # 创建事件处理对象
    fileHandler = MyDirEventHandler()

    # 为观察者设置观察对象与处理事件对象
    observer.schedule(fileHandler, LOCAL_PATH, True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

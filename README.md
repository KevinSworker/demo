# 同步

>  目标是为了将本机的的一个文件夹上的内容实时存放到网络硬盘上（samba)，需要的功能比较简单就手撸一个。

## 利用到的内容

watchdog：负责监视本地的文件夹，当该文件夹中的内容有修改的时候，能够正常捕获到操作并针对操作进行对远程文件的操作

os：主要用于路径的解析

shutil：主要用于文件的复制与删除

haslib：主要用于文件的校验，判断两边文件是否一致，决定操作行为

# Gunicorn Note

Gunicorn 源码笔记，深入理解Gunicorn工作机制

# Arbiter 
主进程
主进程创建 socket 并监听，使用fork形式创建子进程，此时子进程共享主进程的监听socket
子进程使用已监听的 socket 进行执行后续的accept、read、write、select 等操作

# Sync
同步worker
子进程初始化时，先使用非阻塞IO进行 accept 和 read
直到发现accept 没有连接进来，或者read没有数据进来，开始调用select 使用IO多路复用的方式
当select返回，那么就重复执行accept和read操作
循环以上步骤

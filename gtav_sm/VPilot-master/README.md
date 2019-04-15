#gtav仿真平台使用手册
前期工作：
启动左侧DELL电脑，打开桌面的GTAV游戏，待游戏进入后才可进行步骤二的操作
一、环境准备(与apollo基本相同)
    1. ./docker/scripts/dev_start.sh -l dev-x86_64-20181210_1500    #启动docker环境 sudo docker service start
    2. ./docker/scripts/dev_into.sh #进入docker环境
    3. sudo route add -net 239.255.0.100 netmask 255.255.255.255 eth4	#添加组播路由
    4. ./scripts/bootstrap.sh   #启动前端
    5.  cd gtav_sm/VPilot-master/   #进入指定目录

二、选择不同场景，进入游戏
    目前场景有如下选择：

    1. gtav_hspeed:    python dataset_pool.py -x 2839.82516184 -y 3480.14707588 #高速路

    2. gtav_narrow:    python dataset_pool.py -x 2413.391 -y 3863.607   #偏僻区域

    3. gtav_ramp_double		python dataset_pool.py -x -375.194274902 -y -2105.598632812	#匝道

三、浏览器中选择模式与车辆有一些差异
    1. Standard -> GTAV
    2. --vehicle-- -> GTAV
    3. --map-- -> 根据步骤二中的场景，选择如下地图
        hspeed -> Gtav_Hspeed
        narrow -> Gtav_Narrow
四、快捷键(大约有15s延时才能生效)
    b :快速回到起点
    c :在已搭建的场景中顺序切换



注意事项：
    1.初次与游戏进行连接会将车辆生成在错误的地方，需要使用ctr+c终止python程序，等待2-3秒后再次执行上次指令即可。
    2.客户端与服务器连接时间大约需要几分钟，请耐心等待。
    3.若游戏端发生崩溃现象，请重启游戏，重新连接。


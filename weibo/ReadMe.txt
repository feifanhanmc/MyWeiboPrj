【第一部分：获取数据】微博用户数据的采集有点麻烦，在这里从多个渠道同时采集

1、运行get_raw_uids.py从实验室的数据库中拿取一批raw_uids（保存在raw_uids.txt中）,但是其中可能存在已经注销的用户
2、运行get_non_exist_uids.py从中过滤到已注销的用户的uids,保存在bad_uids.txt中，以及将后续发现信息比较少或活跃度比较低（最近两个月没发微博）的用户uid临时存储到bad_uids.txt中
3、运行clean_uids.py读取raw_uids并从中剔除bad_uids，得到文件uids.txt

4、运行manage_db.py中的相关方法，初始化数据库中的RAW_USER_SHOW、RAW_USER_TAG、RAW_USER_SR表格，分别用于存储未处理的用户数据

5、运行get_api_client.py，得到几个应用的client.json文件（保存在docs/client/文件夹下），里面包含了授权的access_token等数据。之所以加载几个应用的access_token,是因为微博API限制太苛刻，一个应用在一定时间内访问频次受到限制。
6、运行get_user_show.py获取name, gender, created_at, bi_followers_count, province, city, location数据，并导入到数据库RAW_USER_SHOW表中

7、运行get_tag_login_headers.py，得到文件tag_headers.json，里面包含了登陆的cookies，爬取微博网页(weibo.com类型)的时候加载即可达到已登陆的效果
8、运行get_user_tag.py获取tag数据，并导入到数据库RAW_USER_TAG表中

9、运行get_sr_login_headers.py，得到多个sr_headers.json文件（保存在docs/sr_headers/文件夹下），里面包含了登陆的cookies，爬取微博网页(weibo.cn类型)的时候加载即可达到已登陆的效果
10、运行get_user_sr.py获取一定量（最近两个月至多30条）的statuses数据、关注数、粉丝数、微博数，并导入到数据库RAW_USER_SR表中

11、运行manage_db.py中的相关方法，把RAW_USER_SHOW、RAW_USER_TAG、RAW_USER_SR表格中的数据整合到raw_user表中
12、运行manage_db.py中的相关方法，在raw_user表中进行筛选，剔除一些信息比较少或活跃度比较低的用户，直接在数据库raw_user表中将对应记录删除，得到的最终raw_user表

13、该部分最终结果为数据库中raw_user表(共9599条记录)
14、运行manage_db.py中的相关方法，得到含有最终9599条uid的文件final_uids.txt


【第二部分：数据分析】
1、运行get_statuses_sim.py，得到statuses_sim.csv保存在docs/sim/目录下
2、运行get_tags_sim.py，得到tags_sim.csv保存在docs/sim/目录下
3、运行get_location_sim.py，得到location_sim.csv保存在docs/sim/目录下
4、运行get_sr_sim.py，得到sr_sim.csv保存在docs/sim/目录下
5、运行get_gender_sim.py，得到gender_sim.csv保存在docs/sim/目录下
6、运行get_usetime_sim.py，得到usetime_sim.csv保存在docs/sim/目录下




13、运行KMeans_cluster.py，聚类10次，把结果保存在CLUSTER_RESULT表中
14、运行analyse_cluster.py，得出保存在weight.csv中的weight[][]矩阵，weight[i][j]代表了i和j在10次聚类结果中，出现在一类中的次数。
import pymssql

# 连接数据库
conn = pymssql.connect(host='10.1.6.15:30000', user='wtzc_dbo', password='wtzc_dbo', database='URC')

# 创建游标
cursor = conn.cursor()

# 调用储存过程并传入参数
param1 = 'value1'
param2 = 'value2'
cursor.execute("EXEC demo1 @report_custom_no = %s",(10,))

# 读取结果集并转化为列表
result_set = cursor.fetchall()

# 打印结果
print(result_set)

# 关闭游标和连接
cursor.close()
conn.close()

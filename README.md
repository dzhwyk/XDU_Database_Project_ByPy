# XDU_Database_Project_ByPy

西电计科院数据库大作业

已经实现基本功能，需要手动配置数据库并填写配置：
    
```python
    db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "your_database_name",
}
```

后续会继续完善

实现了的基本功能：

1. 录入司机基本信息，如工号、姓名、性别等；
2. 录入汽车基本信息，如车牌号、座数等；
3. 录入司机的违章信息；
4. 查询某个车队下的司机基本信息；
5. 查询某名司机在某个时间段的违章详细信息；
6. 查询某个车队在某个时间段的违章统计信息，如：2次闯红灯、4次未礼让斑马线等。
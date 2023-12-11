import pymysql
import json

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "00000000",
    "database": "safety_system",
}


def table_exists(cursor, table_name):
    # 检查表是否存在
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None


# 创建数据库表
def create_tables(cursor):
    # 创建车队表
    create_team_table_query = """
        CREATE TABLE IF NOT EXISTS team (
            team_id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(255) NOT NULL
        );
    """
    cursor.execute(create_team_table_query)

    # 创建路线表
    create_route_table_query = """
        CREATE TABLE IF NOT EXISTS route (
            route_id INT AUTO_INCREMENT PRIMARY KEY,
            route_name VARCHAR(255) NOT NULL,
            team_id INT,
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        );
    """
    cursor.execute(create_route_table_query)

    # 创建车辆表
    create_vehicle_table_query = """
        CREATE TABLE IF NOT EXISTS vehicle (
            vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
            route_id INT,
            vehicle_capacity INT,
            FOREIGN KEY (route_id) REFERENCES route(route_id)
        );
    """
    cursor.execute(create_vehicle_table_query)

    # 创建队长表
    create_team_captain_table_query = """
        CREATE TABLE IF NOT EXISTS team_captain (
            team_captain_id INT AUTO_INCREMENT PRIMARY KEY,
            team_captain_name VARCHAR(255) NOT NULL,
            team_id INT,
            FOREIGN KEY (team_id) REFERENCES team(team_id)
        );
    """
    cursor.execute(create_team_captain_table_query)

    # 创建司机表
    create_driver_table_query = """
        CREATE TABLE IF NOT EXISTS driver (
            driver_id INT AUTO_INCREMENT PRIMARY KEY,
            driver_name VARCHAR(255) NOT NULL,
            driver_gender VARCHAR(8) CHECK (driver_gender IN ('male', 'female')) NOT NULL,
            is_route_captain BOOLEAN NOT NULL,
            route_id INT,
            FOREIGN KEY (route_id) REFERENCES route(route_id)
        );
    """
    cursor.execute(create_driver_table_query)

    # 创建违规表
    create_violation_table_query = """
        CREATE TABLE IF NOT EXISTS violation (
            violation_id INT AUTO_INCREMENT PRIMARY KEY,
            violation_name VARCHAR(255) NOT NULL,
            violation_time DATETIME NOT NULL,
            driver_id INT,
            vehicle_id INT,
            route_id INT,
            FOREIGN KEY (driver_id) REFERENCES driver(driver_id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id),
            FOREIGN KEY (route_id) REFERENCES route(route_id)
        );
    """
    cursor.execute(create_violation_table_query)

    # 把json文件中的数据导入到数据库中
    with open("data.json", "r") as file:
        data = json.load(file)
        for table_name, table_data in data.items():
            for record in table_data:
                columns = ", ".join(record.keys())
                values = ", ".join(["%s"] * len(record))
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(query, list(record.values()))


# 插入司机信息
# 接受的数据：司机ID，司机姓名，司机性别，是否为路队长，路线ID
def insert_driver_info(cursor):
    driver_id = input("请输入司机ID: ")
    driver_name = input("请输入司机姓名: ")
    driver_gender = input("请输入司机性别: ")
    is_route_captain = input("是否为路队长: ")
    route_id = input("请输入司机所属路线ID: ")

    query = """
        INSERT INTO driver (
            driver_id,driver_name,driver_gender,is_route_captain,route_id
        ) 
        VALUES (
            %s,%s,%s,%s,%s
        );
    """

    try:
        cursor.execute(
            query, (driver_id, driver_name, driver_gender, is_route_captain, route_id)
        )
        print("司机信息录入成功！")
    except pymysql.Error as err:
        print(f"录入司机信息失败: {err}")


# 插入车辆信息
# 接受的数据：车辆ID，车辆所属路线ID
def insert_vhicle_info(cursor):
    vehicle_id = input("请输入车辆ID: ")
    route_id = input("请输入车辆所属路线ID: ")

    query = """
        INSERT INTO vehicle (
            vehicle_id,route_id
        ) 
        VALUES (
            %s,%s
        );
    """

    try:
        cursor.execute(query, (vehicle_id, route_id))
        print("车辆信息录入成功！")
    except pymysql.Error as err:
        print(f"录入车辆信息失败: {err}")


# 插入违规信息
# 接受的数据：违规ID，违规名称，违规时间，违规司机ID，违规车辆ID，违规路线ID
def insert_violation_info(cursor):
    violation_id = input("请输入违规ID: ")
    violation_name = input("请输入违规名称: ")
    violation_time = input("请输入违规时间: ")
    driver_id = input("请输入违规司机ID: ")
    vehicle_id = input("请输入违规车辆ID: ")
    route_id = input("请输入违规路线ID: ")

    query = """
        INSERT INTO violation (
            violation_id,violation_name,violation_time,driver_id,vehicle_id,route_id
        ) 
        VALUES (
            %s,%s,%s,%s,%s,%s
        );
    """

    try:
        cursor.execute(
            query,
            (
                violation_id,
                violation_name,
                violation_time,
                driver_id,
                vehicle_id,
                route_id,
            ),
        )
        print("违规信息录入成功！")
    except pymysql.Error as err:
        print(f"录入违规信息失败: {err}")


# 查询司机信息
# 接受的数据：司机ID
# 输出的数据：司机的基本信息
def serach_driver_info(cursor):
    driver_id = input("请输入司机ID: ")
    query = f"""SELECT * FROM driver WHERE driver_id = {driver_id}"""
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("未找到该司机")
        for row in result:
            format_str = "司机ID: {0}\n司机姓名: {1}\n司机性别: {2}\n是否为路队长: {3}\n路线ID: {4}"
            print(format_str.format(*row))
    except pymysql.Error as err:
        print(f"查询司机信息失败: {err}")


# 查询司机违规信息
# 接受的数据：司机ID，查询起始时间，查询结束时间
# 输出的数据：司机的违规信息
def serach_driver_violation_info(cursor):
    driver_id = input("请输入司机ID: ")
    # violation_time_start=input("请输入查询起始时间: ")
    # violation_time_end=input("请输入查询结束时间: ")
    violation_time_start = "2000-1-1 00:00:00"
    violation_time_end = "2030-1-1 00:00:00"
    query = f"""SELECT * FROM violation
        WHERE driver_id={driver_id}
        AND violation_time BETWEEN
        '{violation_time_start}' AND '{violation_time_end}'
        """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("未找到该司机的违规信息")
        for row in result:
            format_str = "违规ID: {0}\n违规名称: {1}\n违规时间: {2}\n司机ID: {3}\n车辆ID: {4}\n路线ID: {5}"
            print(format_str.format(*row))
    except pymysql.Error as err:
        print(f"查询司机违规信息失败: {err}")


# to be completed
# 查询车队违规信息
# 接受的数据：车队ID
# 输出的数据：车队的违规的统计信息
def serach_violation_info(cursor):
    route_id = input("请输入车队ID: ")
    query = f"""SELECT violation_name, COUNT(*)
        FROM violation JOIN driver on violation.driver_id=driver.driver_id
        WHERE violation.route_id='{route_id}'
        GROUP BY violation.violation_name;
        """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("未找到该车队的违规信息")
        for row in result:
            format_str = "违规名称: {0}\n违规次数: {1}"
            print(format_str.format(*row))
    except pymysql.Error as err:
        print(f"查询车队违规信息失败: {err}")


def main():
    try:
        # 连接到MySQL服务器
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        table_name = "team"
        if not table_exists(cursor, table_name):
            # 如果表不存在，则创建表
            create_tables(cursor)

        # 用户选择调用的函数
        choice = input(
            "请选择要调用的函数：\n1. insert_driver_info\n2. insert_vhicle_info\n3. insert_violation_info\n4. serach_driver_info\n5. serach_driver_violation_info\n6. serach_violation_info\n"
        )
        if choice == "1":
            insert_driver_info(cursor)
        elif choice == "2":
            insert_vhicle_info(cursor)
        elif choice == "3":
            insert_violation_info(cursor)
        elif choice == "4":
            serach_driver_info(cursor)
        elif choice == "5":
            serach_driver_violation_info(cursor)
        elif choice == "6":
            serach_violation_info(cursor)
        else:
            print("无效的选择")

        # 读取数据库中的数据
        # cursor.execute("SELECT * FROM team")
        # print(cursor.fetchall())
        # cursor.execute("SELECT * FROM route")
        # print(cursor.fetchall())
        # cursor.execute("SELECT * FROM vehicle")
        # print(cursor.fetchall())
        # cursor.execute("SELECT * FROM team_captain")
        # print(cursor.fetchall())
        # cursor.execute("SELECT * FROM driver")
        # print(cursor.fetchall())
        # cursor.execute("SELECT * FROM violation")
        # print(cursor.fetchall())

        connection.commit()

    except pymysql.Error as err:
        print(f"Error: {err}")
    finally:
        if "connection" in locals() and connection.open:
            cursor.close()
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()

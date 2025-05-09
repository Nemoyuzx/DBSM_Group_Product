> [!WARNING]
>
> 建议阅读完以下内容后操作



### 使用介绍

1、IDE 工具切换到正确环境 （我用的python3.12的conda环境）

2、conda/python 环境中执行库安装 

```cmd
pip install -r requirements.txt
```

3、更改`config/setting.py`文件

```python
DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME':'DBMS_show', #自己的schema尽量和这个一样
    'USER': 'root', #改为自己的数据库连接用户名
    'PASSWORD': 'Love5nemo', #改为自己的数据库连接密码
    'HOST': '127.0.0.1', 
    'PORT': '3306', #改为自己的数据库连接端口
    }
}
```

4、迁移数据库（如果之前数据库有表需要删除）在 `manager.py` 文件上

```cmd
python manage.py migrate
```

5、运行服务 默认端口在本地8000  在 `manager.py` 文件上

```
python manage.py runserver
```



### 运行建议

使用介绍3和4的执行 建议先在vscode的 `manager.py` 中点击右上执行，会出现类似下面内容

```cmd
(DjangoDBMS) (base) nemoyu@Nemos-MacBook-Pro DBSM_Group_Product % /opt/anaconda3/envs/DjangoDBMS/bin/python /Users/n
emoyu/Desktop/database-数据库系统/小组作业/DBSM_Group_Product/DjangoProject/manage.py

Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[auth]
    changepassword
    createsuperuser

[contenttypes]

...

[sessions]
    clearsessions

[staticfiles]
    collectstatic
    findstatic
    runserver
```

接着在弹出的终端中按向上键恢复上一个指令，再在这条指令后添加 `migrate` 、`runserver` 语句，此操作更快速且避免不同环境和相对或绝对路径产生的报错



### 问题解决

- 如果mac使用pip安装有下面报错

  ```cmd
  Exception: Can not find valid pkg-config name.
        Specify MYSQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS env vars manually
        [end of output]
    
    note: This error originates from a subprocess, and is likely not a problem with pip.
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> See above for output.
  ```

  先执行（假设你装了brew）

  ```cmd
  brew install mysql mysql-connector-c openssl pkg-config
  ```

  再尝试继续执行 pip install 命令
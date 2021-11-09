1.选择python解释器路径，有两个前提：
    a 该解释器路径下安装好pipenv
    b 在系统环境变量下，增加 WORKON_HOME键，键值为 venv
2. pipenv install
3.增加.vscode/settings.json文件，内容如下：
    "code-runner.executorMap": {
        "python": ".\\venv\\crawler-XKK920dK\\Scripts\\python.exe -u",
    }
    其中crawler-XKK920dK 更改为自己的目录
4.切换回venv下的python解释器
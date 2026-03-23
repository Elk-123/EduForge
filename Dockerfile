FROM python:3.12-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 关键修改：使用清华大学镜像源，并添加信任主机
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

# 复制其余代码
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
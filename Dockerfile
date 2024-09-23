# 使用官方 Python 鏡像作為基底
FROM python:3.8-slim

# 設置工作目錄
WORKDIR /app

# 將本地的應用代碼複製到容器中
COPY . /app

# 安裝應用所需的依賴
RUN pip install --no-cache-dir -r requirements.txt

# 指定應用的啟動命令
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]

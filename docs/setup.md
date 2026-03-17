1. 数据库搭建: docker-compose up -d
2. 创建虚拟python环境: conda create -n eduforge python=3.11 -y
3. 显式接受条款: 
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
4. 临时添加conda路径:
(假设你的 Miniconda 安装在默认路径，注意路径前后的空格)
source ~/miniconda3/etc/profile.d/conda.sh
5. 激活环境:conda activate eduforge
6. 基础环境配置:
pip install fastapi "uvicorn[standard]" python-multipart requests pydantic pydantic-settings
pip install sqlalchemy alembic psycopg2-binary asyncpg pgvector
pip install langchain langchain-community langchain-openai langgraph
pip install python-pptx python-docx pymupdf pandas openpyxl
pip install python-dotenv loguru
7. 将环境导出:(不用操作)
pip freeze > requirements.txt
8. 同步我提供的依赖文件:
pip install -r requirements.txt
9. 开启后端服务
python main.py
10. 前端启动
npm install
npm run dev
---
pip install langchain-community faiss-cpu sentence-transformers pymupdf
docker exec -it eduforge_db psql -U postgres -d eduforge
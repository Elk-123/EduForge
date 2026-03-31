1. 创建虚拟python环境: conda create -n eduforge python=3.11 -y
2. 显式接受条款: 
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/msys2
3. 临时添加conda路径:
(假设你的 Miniconda 安装在默认路径，注意路径前后的空格)
source ~/miniconda3/etc/profile.d/conda.sh
4. 激活环境:conda activate eduforge
5. 基础环境配置:
pip install -r requirements.txt
6. 



1. 开启后端服务
python main.py
1.  前端启动
npm install
npm run dev
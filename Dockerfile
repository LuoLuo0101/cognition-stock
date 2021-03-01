FROM python:3.7.3

MAINTAINER wangge <wangge0101@126.com>

# 设置环境变量
ENV APP_ROOT /app
ENV TIME_ZONE="Asia/Shanghai"

# 工作目录
WORKDIR ${APP_ROOT}/

COPY conf/apt-install.txt /app/conf/apt-install.txt

# 环境准备
RUN deps=$(cat /app/conf/apt-install.txt) \
    && set -x \
    && apt update -y \
    && apt-get install -y $deps --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -i https://pypi.douban.com/simple pipenv \
    # 设置时区
    && echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime

# 安装依赖，requirements.txt变化少，pip层就容易被缓存，如果项目全部拷贝的话，这一层需要经常重新制作
COPY Pipfile ${APP_ROOT}/
RUN pipenv install

COPY . ${APP_ROOT}/

EXPOSE 8000

CMD ["gunicorn", "manage:app"]

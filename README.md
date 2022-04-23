# Online Chat

python实验，使用vue3作为前端，fastapi作为服务后端，socket.io作为实时通讯服务。

## 预览

![预览1](./images/image1.png)

![预览2](./images/image2.png)

[在线预览](https://www.topquant.tech/wr_web/online_chat/)

## 部署

### 前端

```bash
cd onlinechat
yarn install
yarn build
```

将打包好的dist文件夹放置于服务器上。

若想要部署的路径不为根路径，修改下面的baseurl为你自己的baseurl后再打包

```ts
/src/router/index.ts

const router = createRouter({
  // TODO: 部署时修改基本路径
  history: createWebHashHistory("/you/base/url"),
  routes,
});
```

### 后端

将backend复制到部署的服务器。

修改数据库连接：

```python
/utils/database
SQLALCHEMY_DATABASE_URL = "you/database/url"
```

#### 物理机部署

安装依赖：

```bash
pip install -r requirements.txt
```

运行：

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

#### docker部署

建立image：

```bash
docker build -t onlinechat:env .
```

运行docker：

```bash
docker run -d \
	-p [port]:23456 \
	--name="onlinechat" \
	onlinechat:env
```

即可通过`服务器ip:port`访问（端口记得开安全组(•ω•`)）
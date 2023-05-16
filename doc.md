# 项目文档

项目采用前后端分离架构，前端采用 Vue 框架，后端采用 Django 框架，数据库使用本地 sqlite3 文件存储。

## 前端

前端采用 Vue 框架，运行在 21486 端口，启动方式：

```console
$ npm install
$ npm run dev
```

前端主要组件及对应 url：
|功能|url|简介|
|-|-|-|
|登录|`/login`|clerk 注册的账户通过账号和密码登录|
|登出|`/logout`|登录的账号通过此 API 销毁 Token 实现登出|
|获取操作面板|`/dashboard`|登录成功后跳转此界面进行相关操作|
|创建账户|`/create-account`|clerk 通过此界面注册账户，需提供用户名、密码和用户类型|
|删除账户|`/delete-account`|clerk 通过此界面删除账户，需提供账户 ID|
|账户收支、余额|`/account/balance`|用户通过此界面查看账户余额和收支情况|
|转账|`/account/transfer`|用户通过此界面向其他账户转账|
|查询收支|`/accounts/transactions`|banlance 页面通过此 API 获取账户交易情况，每 10s 自动更新|

## 后端

后端采用 Django 架构，运行在 21485 端口，启动方式：

```console
$ pip install -r requirements.txt
$ python3 manage.py runserver 21485
```

后端主要功能实现在 [api/views.py](https://github.com/efJerryYang/banking-system/blob/main/banking_system_backend/api/views.py) 文件，负责对前端的请求进行处理并返回结果。

数据库操作主要通过 django.db 提供的 models 模块实现，本项目共含三个 models（对应三张数据库表）：

+ Users：记录银行系统的用户信息，包含以下字段：
  + username：用户名
  + password：密码
  + userType：用户类型（普通用户或 clerk）
  + balance：用户的账户余额
+ Transaction：记录银行的转账信息，包含以下字段：
  + sender：转账的发起方
  + receiver：转账的接收方
  + amount：转账的数额
  + timestamp：转账的发起时间
+ Token：记录登录用户的 session 信息，包含以下字段：
  + user：用户名
  + key：返回给用户的 sessionId
  + created：Token 的创建时间
  + expires：Token 的过期时间

## 权限鉴定

本项目最重要的功能是判定前端发送的请求和请求发送者身份是否一致，以避免普通用户查看他人账户信息或冒充 clerk 对银行系统进行操作。一般来说此类鉴权采用的方案有 cookie 和 session 两类，我们的项目采用了 session 的方案：

+ 后端定义了 Token 类，记录 sessionId、用户和 session 的过期时间；
+ 通过 Django 的 db 库，建立起 sessionId 到 Token 类的映射关系；
+ 后端在前端发送登录请求并成功登录后，新建一个对应 Token 并将 sessionId 返回前端；
+ 前端将 sessionId 通过 localStorage 记录到本地，并在后续的请求中将 sessionId 带到 HTTP 请求头部的 authorization 字段；
+ 后端通过前端请求的 sessionId 找到对应 Token 并判断该请求是否为假冒；
+ Token 未过期时前端对主页面的访问无需登录，后端将直接前端可以通过 `/api/logout` 接口让自己的 Token 直接过期

后端给前端返回的 sessionId 是随机生成的数字和字母组成的长字符串，因此只要用户不泄露自己的 sessionId，前端就无法对齐进行假冒从而越权。

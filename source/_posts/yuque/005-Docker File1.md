---
title: 005-Docker File1
urlname: gqdl3o
date: '2021-12-28 01:32:15 +0800'
tags: []
categories: []
---

### 从 dockerfile 创建镜像【推荐】

```dockerfile
FROM ubuntu:21.04
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y python3.9 python3-pip python3.9-dev
ADD hello.py /
CMD ["python3", "/hello.py"]
```

构建：docker image build -t hello .
分享：push 到 docker hub

- docker image tag local-image:tagname new-repo:tagname
- docker login:登录
- docker push docker_hub_id/image_name:tag

---

### 通过 commit 创建镜像:在容器的基础上构建

`docker container commit container_id new_container_name:new_container_tag`
![1640657399(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640657409098-f52eb25c-2a99-4a92-9b13-abc87007ddb7.png#clientId=u78e3bb24-4b7c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=284&id=u7c1837bf&margin=%5Bobject%20Object%5D&name=1640657399%281%29.png&originHeight=567&originWidth=1022&originalType=binary∶=1&rotation=0&showTitle=true&size=58356&status=done&style=none&taskId=u848b41ff-6bfc-4c49-a488-2f5c8f38988&title=%E4%BF%AE%E6%94%B9%E5%AE%B9%E5%99%A8%E5%86%85%E5%AE%B9&width=511 "修改容器内容")
![1640658068(1).png](https://cdn.nlark.com/yuque/0/2021/png/115484/1640658072744-687b21b6-d9f1-4a07-9753-bdbfac1d7657.png#clientId=u78e3bb24-4b7c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=124&id=uc04e60b4&margin=%5Bobject%20Object%5D&name=1640658068%281%29.png&originHeight=247&originWidth=783&originalType=binary∶=1&rotation=0&showTitle=true&size=26844&status=done&style=none&taskId=u7ce53deb-3aa0-49b8-a883-353542c0bf6&title=%E4%BB%8E%E5%AE%B9%E5%99%A8%E5%88%9B%E5%BB%BA%E9%95%9C%E5%83%8F&width=391.5 "从容器创建镜像")

---

### 常见报错：

> Error response from daemon: conflict: unable to delete 101239f587fa (must be forced) - image is referenced in multiple repositories

出现该问题的原因是：docker rmi image_id 两个镜像拥有同一个 id，
解决方法：docker image rm image_name:tag

---

`docker image history image_name`:查看镜像的 layer 分层

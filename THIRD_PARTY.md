# 来源与许可证

知序人事（ZHIXU）为开源衍生项目。产品品牌、视觉与本地交付能力由本项目修改；保留所使用代码的来源与许可。

| 组件 | 来源 | 基线 | 许可证 |
|---|---|---|---|
| 人事业务与前后端 | https://github.com/quuuuj/hrm | c792149707036b74f75a5dd83f69cf6af8aa47d9 | GPL-3.0，见根目录 LICENSE |
| MinIO 对象存储 | https://github.com/minio/minio | RELEASE.2025-04-22T22-12-26Z | AGPL-3.0，见 delivery/vendor 中官方源码的 LICENSE |

MinIO 官方源码包：https://codeload.github.com/minio/minio/tar.gz/refs/tags/RELEASE.2025-04-22T22-12-26Z

源码压缩包 SHA-256：`1a63209927b9d1fb239b2a776b7b01d1902eff19379a108f4bc7005edcc0968c`。

MinIO 在独立容器中运行，不修改其业务源码。正式分发该镜像时保留上述对应源码下载路径和许可证。Java、Node 与 Docker 依赖沿用各自许可证，具体版本见 pom.xml、package-lock.json 与 compose.delivery.yaml。

保留原始作者注释与 README.upstream.md。本项目仓库为 https://github.com/tclear450-max/zhixu-admin ，使用独立的初始提交发布当前衍生源码。上游远程仓库保留为 `upstream`，没有向原仓库推送；应用服务仍只在本机运行。

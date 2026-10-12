# 组件与许可证

知序人事（ZHIXU）采用 GPL-3.0 许可证，见根目录 LICENSE。下列组件分别遵循各自的许可证。

| 组件 | 来源 | 基线 | 许可证 |
|---|---|---|---|
| MinIO 对象存储 | https://github.com/minio/minio | RELEASE.2025-04-22T22-12-26Z | AGPL-3.0，见 delivery/vendor 中官方源码的 LICENSE |

MinIO 官方源码包：https://codeload.github.com/minio/minio/tar.gz/refs/tags/RELEASE.2025-04-22T22-12-26Z

源码压缩包 SHA-256：`1a63209927b9d1fb239b2a776b7b01d1902eff19379a108f4bc7005edcc0968c`。

MinIO 在独立容器中运行，不修改其业务源码。正式分发该镜像时保留上述对应源码下载路径和许可证。Java、Node 与 Docker 依赖沿用各自许可证，具体版本见 pom.xml、package-lock.json 与 compose.delivery.yaml。

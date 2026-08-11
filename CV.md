<div style="display: flex; justify-content: space-between; align-items: flex-start;">
  <div>
    <h1>闫军儒</h1>
    <p><strong>25届毕业生 | 硕士 | 26岁 | 男</strong></p>
    <p>📧 196****@qq.com | 📱 +86 157****3647</p>
  </div>
  <div>
    <img src="./resource/self.jpg" alt="个人照片" width="120" style="border: 1px solid #ddd; padding: 4px;">
  </div>
</div>

---

## 教育经历

**杭州电子科技大学 · 计算机技术** - 硕士 <span style="float: right;">2022.9 - 2025.6</span>

**哈尔滨理工大学 · 工程力学** - 本科 <span style="float: right;">2018.9 - 2022.6</span>

---



## 工作经历

**腾讯云计算（武汉）有限责任公司** - 实习生 <span style="float: right;">2024.6 - 2024.9</span>

地图平台部 / 渲染产品中心 / 渲染技术组

**无线生活（北京）有限责任公司** - C++开发<span style="float: right;">2025.6 - 至今</span>

微店科技部 / 工程 / 微店24流媒体

1. ZLMediaKit 的二次开发与维护

基于 ZLMediaKit 二次开发并维护录像回放、实时监控及录制文件管理等核心能力，完成本地盘与外置盘录像检索、清理和多文件连续回放。

- 高倍速回放：
    - 设计并实现最高 16 倍速录像回放链路：源视频按 N 倍速解封装与 RKMPP 硬解，解码后均匀抽帧，以原始帧率 RKMPP 硬编并按 1 倍速稳定推流；同步压缩媒体时间戳与 duration，保证客户端播放进度与实际录像时间一致。
    - 打通 H.264/H.265“RKMPP 硬解码 → NV12 MppFrame/DMA-BUF → RKMPP 硬编码”零拷贝链路，复用解码帧并传递真实 stride 与帧生命周期，避免 CPU 侧 YUV 拷贝、颜色转换及软件编解码开销。
    - 将 RKMPP 编解码改造为 0ms 非阻塞、批量异步流水线，通过 MppTask 多帧在途、独立输出缓冲与时间戳绑定、背压即时 drain/retry 及异常上下文重建，避免高倍速任务阻塞 ZLMediaKit EventPoller。
    - 解决多录像文件衔接、动态分辨率切换及倍速切换中的卡顿、断流和时间轴跳变问题，通过 DTS 基准归一与跨文件 offset 累加、编码器按分辨率重建及首帧 IDR/参数集恢复，提升长时间回放稳定性。

2. 视频混流SDK的开发与维护

- 负责跨平台视频混流 SDK 的设计、开发与维护，统一 FFmpeg 解封装、硬件解码、画面合成、硬件编码及封装推流流程，支持监控多分屏与 JSON 灵活布局。
- 完成 RK3588 零拷贝混流链路：FFmpeg 解封装 → RKMPP 硬件解码 → DMA-BUF/EGLImage 导入 → OpenGL ES 离屏合成 → RGBA DMA-BUF → RGA 转换 NV12 → RKMPP 硬件编码 → FFmpeg 封装推流，实现视频主链路端到端零拷贝。
- 完成海思 Ascend 310P 零拷贝混流链路：FFmpeg 解封装 → HiMPP VDEC 硬件解码 → NV12/DVPP VB 设备帧 → DVPP VPC 裁剪、缩放与贴图合成 → HiMPP VENC 硬件编码 → FFmpeg 封装推流，实现无 EGL/GL 环境下的设备内存零拷贝合成。
- 针对不同硬件能力抽象统一合成接口，在 RK 平台使用 GPU Shader 提供灵活图层渲染，在海思平台使用 DVPP VPC 专用硬件完成 NV12 画布合成，降低 CPU 像素拷贝和颜色转换开销。


---

## 个人作品

- [FluxPlayer](https://github.com/Amaz1ngJR/FluxPlayer)
  - 基于 FFmpeg + OpenGL 的跨平台视频播放器，支持硬件加速解码、网络流播放（RTSP/RTMP/HLS）、GPU 渲染、内嵌字幕和录制功能。C++17 实现，ImGui 控制界面
- [AgentLab](https://github.com/Amaz1ngJR/AgentLab)
  - AgentLab 是一个面向 macOS 和 Windows 的本地 Agent 开发框架，目标是把大模型从“聊天助手”升级为可持续执行任务的个人 Agent。它支持本地模型与云端模型切换，内置文件、代码搜索、Shell、浏览器控制等工具能力，并可接入 Skill 与 MCP Server 扩展外部系统。AgentLab 提供多 Agent / Session 管理、长期记忆、上下文压缩、任务拆解与 Loop Engineering 机制，让 Agent 能围绕明确目标持续规划、执行、验证、修复和沉淀经验，同时通过权限审批、工作区隔离和审计机制保障本地电脑、远程设备和敏感数据的安全。

---

## 个人链接

- **Github主页** : https://github.com/Amaz1ngJR
- **技术学习主页**: https://github.com/Amaz1ngJR/Technology
- **算法学习主页**: https://github.com/Amaz1ngJR/Data-structures-and-algorithms
- **力扣主页**: https://leetcode.cn/u/amaz1ng-b/---


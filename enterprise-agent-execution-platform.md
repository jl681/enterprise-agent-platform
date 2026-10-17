# Enterprise Agent Execution Platform
## 项目开发与学习路线图

### 一、项目目标

**项目名称：** Enterprise Agent Execution Platform

**项目定位：** 从一个具体的业务 Agent 出发，逐步开发支持多个业务场景的通用 Agent 执行平台。

**职业目标：**
- 短期：AI Backend Engineer / Agent Systems Engineer
- 中期：Agent Runtime / Harness Engineer
- 长期：Agent Platform / Infrastructure Engineer

**学习方式：** Project-Based Learning（边做边学）

每个任务按照以下流程推进：

1. 明确功能需求和验收标准。
2. 学习实现功能所必需的技术知识。
3. 独立编写代码并运行。
4. 编写测试，验证正常和异常场景。
5. 进行 Code Review，理解设计取舍。
6. 整理文档并提交 GitHub。

**预计周期：** 14–16 周，每周投入约 12–15 小时。根据实际学习进度调整。

---

### 二、整体技术架构

**第一层：Business Applications**
- Order Operations Agent
- 第二个简单业务 Agent（后期引入，用于验证 Runtime 的可复用性）

**第二层：Agent Service**
- Python
- FastAPI
- Pydantic
- LLM API
- Tool Calling
- LangGraph

**第三层：Agent Runtime**
- Agent Loop
- Tool Registry / Tool Executor
- Context Manager
- State Management
- Checkpoint / Recovery
- Approval Manager
- Budget Controller
- Trace Recorder

**第四层：Business Backend**
- Java
- Spring Boot
- REST API
- PostgreSQL
- Kafka（按实际需求引入）

**第五层：Infrastructure**
- Docker / Docker Compose
- Observability
- Evaluation
- Kubernetes（后期可选）

原则：不提前引入没有明确用途的技术组件。

---

### Phase 1：Python Backend & LLM Integration

**预计时间：第 1–2 周**

**阶段目标：**

熟悉 Python 后端项目开发，掌握 FastAPI、Pydantic、测试与依赖管理，并实现最基础的 LLM 集成。

**需要学习：**
- Python 项目结构、包和模块
- uv、pyproject.toml、虚拟环境
- Python Type Hints
- FastAPI
- Pydantic
- pytest、httpx
- Python 异常处理
- HTTP API 开发
- LLM API 基础
- Messages、Tokens、Model Parameters
- Structured Outputs
- 基础 API 错误处理

**开发任务：**

Task 01：初始化 Python 项目
- 创建 GitHub Repository。
- 使用 uv 管理项目依赖。
- 创建 FastAPI 项目。
- 定义 Order Pydantic Model。
- 使用内存模拟订单数据。
- 实现 GET /orders/{order_id}。
- 正确处理订单不存在的情况。
- 编写 API 自动化测试。

Task 02：集成 LLM API
- 配置模型 API Key。
- 实现独立的 Model Client。
- 发送用户消息并获取模型响应。
- 理解 System / User / Assistant Messages。
- 处理模型调用异常。
- 记录基本 Token Usage。
- 确保 API Key 不提交到 GitHub。

Task 03：实现 Structured Outputs
- 定义 Pydantic Response Schema。
- 让模型输出结构化订单查询意图。
- 验证模型返回的数据。
- 处理无效或不完整的模型输出。

**阶段交付成果：**
- 一个可以运行的 Python FastAPI 服务。
- 一个可调用 LLM 的 Model Client。
- 一组自动化测试。
- README 和运行说明。

**验收标准：**
- FastAPI 服务正常运行。
- 订单查询 API 返回正确数据和状态码。
- 可以成功调用 LLM API。
- 模型能够返回符合 Schema 的结构化结果。
- 异常场景得到合理处理。
- 所有自动化测试通过。

---

### Phase 2：Tool Calling & Agent Loop

**预计时间：第 3–4 周**

**阶段目标：**

理解 Agent 的基本执行机制，先独立实现最小 Agent Loop，再学习如何使用 Agent Framework。

**需要学习：**
- Function Calling / Tool Calling
- Tool Schema
- Tool Argument Validation
- Agent Loop
- Model / Tool / Environment 的职责划分
- Tool Execution
- Agent Termination Conditions
- Max Steps
- Timeout / Retry
- LangGraph 基础
- Workflow / State Graph

**开发任务：**

Task 04：实现订单查询工具
- 定义 get_order_status 工具。
- 定义 get_order_events 工具。
- 定义 check_inventory 工具。
- 将工具与模拟订单数据连接。
- 使用 Pydantic 验证工具参数。

Task 05：实现最小 Agent Loop
- 向模型提供工具定义。
- 解析模型返回的 Tool Calls。
- 执行指定工具。
- 将工具结果返回给模型。
- 允许模型继续选择工具。
- 支持模型返回最终答案。
- 加入最大执行步数限制。
- 处理未知工具和非法参数。

Task 06：实现订单异常诊断
- 支持用户使用自然语言询问订单异常。
- Agent 根据需要选择多个工具。
- 根据工具返回的事实生成诊断报告。
- 不允许模型虚构订单状态或事件。

Task 07：使用 LangGraph 重构
- 学习 Node、Edge、State。
- 将现有 Agent Loop 表达为 Graph。
- 比较手写 Agent Loop 与 LangGraph。
- 记录两种实现的设计差异。

**阶段交付成果：**
- 一个能够执行多步骤任务的 Order Operations Agent。
- 一个手写 Agent Loop。
- 一个 LangGraph 实现版本。
- 工具调用与错误处理测试。

**验收标准：**
- Agent 可以自主选择正确的工具。
- 能完成需要多个工具的订单诊断任务。
- 工具参数经过验证。
- 能正确处理工具执行失败。
- 不会无限循环。
- 能解释 Agent Loop 的工作原理。

---

### Phase 3：State Management, Checkpoint & Reliability

**预计时间：第 5–7 周**

**阶段目标：**

将简单 Agent 升级为具有持久化状态、任务恢复和人工审批能力的可靠执行系统。

**需要学习：**
- Stateful Agent
- Execution State
- State Persistence
- PostgreSQL
- Checkpoint
- Interrupt / Resume
- Human-in-the-Loop
- Idempotency
- Timeout / Retry
- Failure Recovery
- Business State vs Agent Execution State
- Docker Compose

**开发任务：**

Task 08：引入 PostgreSQL
- 将订单数据从内存迁移到数据库。
- 设计订单表与事件表。
- 实现数据库访问。
- 编写数据库相关测试。

Task 09：实现 Agent Execution State
- 为每次 Agent 执行生成唯一 ID。
- 保存执行状态。
- 记录当前任务步骤。
- 记录工具调用结果。
- 支持查询任务执行状态。

Task 10：实现 Checkpoint 与恢复
- 在关键执行节点保存 Checkpoint。
- 模拟 Agent 执行过程中服务崩溃。
- 重启后恢复未完成任务。
- 避免重复执行已经完成的操作。

Task 11：实现人工审批
- 添加 resubmit_order 工具。
- 在执行订单修改前暂停 Agent。
- 向用户展示待执行操作。
- 用户批准后继续执行。
- 用户拒绝后终止操作。
- 在业务服务端实施权限和状态校验。

Task 12：实现可靠性保护
- 工具执行超时。
- 有界重试与退避策略。
- 幂等性校验。
- 错误分类。
- 执行失败后的状态处理。

**阶段交付成果：**
- Stateful Order Operations Agent。
- PostgreSQL 持久化。
- Checkpoint / Resume。
- Human Approval。
- 故障恢复测试。

**验收标准：**
- 服务重启后可以恢复未完成任务。
- 已执行的不可逆业务操作不会因重试而重复生效。
- 未经授权或审批的操作无法执行。
- 工具失败不会造成无法解释的任务状态。
- 能说明 Agent State 与业务状态的区别。

---

### Phase 4：Evaluation, Tracing & Observability

**预计时间：第 8–9 周**

**阶段目标：**

建立可评测、可调试、可观测的 Agent 系统。

**需要学习：**
- Agent Evaluation
- Task Success Rate
- Tool Call Accuracy
- Trajectory Evaluation
- Golden Dataset
- Regression Testing
- Tracing
- Structured Logging
- Metrics
- OpenTelemetry 基础
- Latency / Token Usage / Cost

**开发任务：**

Task 13：建立 Agent Evaluation Dataset
- 设计至少 50 个订单相关测试场景。
- 包括正常查询、复杂诊断、工具失败和权限拒绝。
- 定义每个场景的预期结果。
- 区分确定性测试与模型行为评测。

Task 14：实现 Evaluation Runner
- 批量执行测试场景。
- 检查任务是否完成。
- 检查关键工具是否被正确调用。
- 记录失败原因。
- 输出评测报告。

Task 15：实现 Tracing
- 记录每次 Agent Execution。
- 记录 Model Call。
- 记录 Tool Call。
- 记录执行耗时。
- 记录错误。
- 关联同一次任务的执行步骤。

Task 16：建立基础 Observability
- 统计任务成功率。
- 统计工具失败率。
- 统计模型调用次数。
- 记录 Token Usage。
- 估算模型调用成本。
- 对比不同版本的 Agent 表现。

**阶段交付成果：**
- Evaluation Dataset。
- Evaluation Runner。
- Agent Execution Traces。
- 基础质量与性能报告。

**验收标准：**
- 可以重复运行评测。
- 可以识别工具调用错误。
- 可以定位任务失败的执行步骤。
- 能比较两次代码修改前后的表现。
- 能解释 Agent Evaluation 与普通 Unit Testing 的区别。

---

### Phase 5：MCP, Context Engineering & Tool Infrastructure

**预计时间：第 10–11 周**

**阶段目标：**

学习标准化工具接入、上下文管理与工具安全，为构建通用 Agent Runtime 做准备。

**需要学习：**
- Model Context Protocol（MCP）
- MCP Server / Client
- Tool Discovery
- Tool Registry
- Context Window
- Context Engineering
- Context Truncation / Summarization
- Token Budget
- Tool Permissions
- Prompt Injection
- Tool Result Validation

**开发任务：**

Task 17：开发 MCP Server
- 将订单查询能力封装为 MCP Tools。
- 实现 MCP Server。
- 让 Agent 通过 MCP Client 调用工具。
- 与原有工具调用方式进行比较。

Task 18：实现 Context Management
- 跟踪 Agent 的消息历史。
- 记录上下文 Token 使用情况。
- 设计上下文裁剪策略。
- 尝试摘要压缩。
- 确保关键任务状态不会因为上下文裁剪而丢失。

Task 19：实现 Tool Permission Controls
- 区分只读工具与写操作工具。
- 限制 Agent 可调用的工具。
- 在执行层验证权限。
- 处理工具返回的不可信内容。
- 测试 Prompt Injection 场景。

**阶段交付成果：**
- 可运行的 MCP Server。
- Context Management 组件。
- Tool Permission Controls。
- 安全与上下文管理测试。

**验收标准：**
- Agent 能够调用 MCP Tools。
- 工具参数与返回结果经过验证。
- 未授权工具调用被拒绝。
- 长任务可以控制上下文规模。
- 不依赖 Prompt 来强制执行安全权限。

---

### Phase 6：Mini Agent Runtime / Harness

**预计时间：第 12–16 周**

**阶段目标：**

将前面开发的 Agent 功能逐步抽象为可复用的执行基础设施。

**需要学习：**
- Agent Runtime Architecture
- Harness Design
- Interface / Abstraction Design
- Model Client Abstraction
- Tool Registry
- Tool Executor
- State Store
- Checkpoint Manager
- Budget Controller
- Approval Manager
- Trace Recorder
- Runtime Lifecycle
- Reusable Component Design

**开发任务：**

Task 20：重构 Agent Runtime
- 将业务逻辑与 Agent 执行逻辑分离。
- 定义 Model Client 接口。
- 定义 Tool Registry。
- 定义 Tool Executor。
- 定义 State Store。
- 将执行循环抽取为独立组件。

Task 21：实现 Runtime Reliability
- 集中管理工具执行。
- 集中管理超时与重试。
- 集中管理 Checkpoint。
- 集中管理 Approval。
- 集中管理 Token / Step Budget。
- 集中记录执行轨迹。

Task 22：接入第二个 Agent
- 选择一个简单的第二业务场景，例如公开资料研究 Agent。
- 复用同一套 Runtime。
- 使用不同的工具与任务配置。
- 不复制原有 Agent Loop 和执行基础设施代码。

Task 23：完成 Runtime 对比与文档
- 对比自实现 Runtime 与 LangGraph。
- 记录架构决策。
- 分析组件职责与边界。
- 记录已知限制。
- 整理 GitHub README。
- 绘制系统架构图。
- 编写项目演示说明。

**阶段交付成果：**
- Mini Agent Runtime / Harness。
- 两个使用同一 Runtime 的业务 Agent。
- Runtime 架构文档。
- 完整测试与演示。
- 可用于面试讨论的项目作品集。

**验收标准：**
- 两个业务 Agent 复用核心执行组件。
- Runtime 不依赖特定业务领域。
- 支持 Tool Execution、State、Checkpoint 和 Tracing。
- 可以解释各组件的职责。
- 可以解释为什么使用或不使用现有 Agent Framework。
- 能够演示故障恢复与安全控制。
- 项目可以按照 README 在本地运行。

---

### 三、后续扩展方向（不属于首个项目的必做范围）

完成以上阶段后，可以根据招聘需求和个人兴趣进一步扩展。

**Agent Platform Infrastructure**
- Distributed Agent Execution
- Task Queue / Scheduling
- Worker Pool
- Multi-tenancy
- Sandbox / Execution Isolation
- Resource Quotas
- Rate Limiting
- Cost Governance
- Kubernetes Deployment
- Platform Monitoring

**可选扩展项目：**
- Distributed Agent Task Scheduler
- Sandbox-based Tool Execution Service
- Multi-tenant Agent Runtime
- Agent Evaluation Platform

这些属于下一阶段的专业化项目，不建议在第一个 Agent 尚未稳定运行时提前实现。

---

### 四、项目工程规范

从第一阶段开始遵循以下原则：

1. 所有代码使用 Git 版本管理。
2. 每个功能尽量有对应测试。
3. 不在代码中硬编码 API Key。
4. 使用模拟业务数据，不使用原雇主的内部数据或代码。
5. 重要技术决策记录在 README 或 ADR 中。
6. 优先保证功能正确性和可维护性。
7. 不为了展示技术栈而增加无必要的组件。
8. 明确区分个人项目实践与真实生产经验。
9. 每完成一个阶段，保留可运行版本。
10. 每个阶段结束后进行一次 Code Review 和技术复盘。

---

### 五、最终希望获得的能力

**AI Backend Engineering**
- 能独立开发 Python AI 后端服务。
- 能集成 LLM API 和外部工具。
- 能实现基本的 Agent Workflow。

**Agent Systems Engineering**
- 理解 Agent Loop。
- 能设计 Stateful Agent。
- 能实现 Checkpoint、Recovery 和 Approval。
- 能构建 Evaluation 与 Tracing。
- 能处理常见可靠性和安全问题。

**Agent Runtime / Platform Engineering**
- 能理解 Agent Runtime 的核心组件。
- 能设计通用 Tool Execution 机制。
- 能抽象可复用的 Agent 执行基础设施。
- 能分析现有框架的设计取舍。
- 为进一步学习分布式调度、Sandbox 和多租户平台打下基础。

---

### 六、当前进度

**当前阶段：** Phase 1 — Python Backend & LLM Integration

**当前任务：** Task 01 — 初始化 Python 项目并开发订单查询 API

**当前状态：** 待开发

**下一步：**
- 完成 Task 01。
- 提交代码或 GitHub 链接。
- 进行 Code Review。
- 通过验收后进入 Task 02。

**执行原则：每次只推进一个明确的开发任务，边实现、边学习、边验证。**
# Repository Guidelines

## Workspace Structure

This directory is a lightweight workspace entry Git repository containing four independent project Git repositories. The entry repository tracks root documentation, tools, and exact recovery commits in `workspace.json`; child directories are ignored rather than embedded or managed as submodules. Use `bash tools/workspace_git.sh ...` for entry Git operations in managed environments with a protected `.git/`; see `WORKSPACE.md`. `project-control/` holds project plans, requirements, engineering rules, and task records. `soc-ap/` is the SoC application scaffold, with `core/`, `config/`, `specs/`, and `tests/`. `mcu-p3/` contains the dual MCU firmware scaffold under `mc/` and `th/`. `test_harness/` keeps independent QA assets in `static_checks/`, `hil/`, and `test_cases/`. Coordination rules and board files are duplicated in the root `.agents/` and `project-control/.agents/`; `project-control/` is marked canonical in `manifest.yaml`, so confirm the authoritative copy before editing either set.

Treat existing symbolic links inside this workspace as local workspace paths: follow them to read or edit their intended target content. Keep access within the linked directory; a link does not authorize exploring unrelated paths outside its target.

## Independent QA

All pending and new QA reviews and verification must use independent Codex sessions. Follow the canonical policy in `project-control/.agents/rules/codex_qa_review.md`, including the independent review of QA-authored artifacts. Preserve completed historical signatures; planned session aliases do not indicate a running reviewer or approval.

## Build and Test

The repositories are currently scaffolds and do not define a workspace-wide build, test, or lint command. Check the target repository's README and the applicable task contract before running commands. Run Git operations from the relevant repository, for example `git -C soc-ap status`; each project repository has its own history. Do not report a build or test as passing unless it was actually run against the relevant implementation.

## Style and Documentation

Follow established conventions in the target module. Keep changes focused and put executable contracts and tests beside the code they govern; keep cross-project plans and decisions in `project-control/`. Existing project documentation is primarily Chinese, uses Markdown, and records task scope, prerequisites, evidence, and acceptance conditions. Preserve those conventions when editing these documents. No repository-wide formatter or linter is configured yet.

## Coding Standards and Methodological Invariants (代码编写规范与硬性门禁)

All code written across repositories (`soc-ap/`, `mcu-p3/`, `test_harness/`) must strictly comply with the engineering protocols absorbed from `/home/sushaohua/agents/mcu-p3/AGENTS.md` and canonicalized in `project-control/.agents/rules/c_cpp_coding_standard.md`:
1. **函数规模硬性门禁**：**严禁编写超 50 行的自研非结构体函数**。单个自研函数必须保持单一职责并控制在 50 行以内；复杂逻辑必须按阶段拆解为带 `static` 修饰的内部辅助函数。
2. **入参个数硬性门禁**：**严禁编写超 4 个入参的自研非结构体函数**。自研函数参数严禁超过 4 个；若初始化、配置或执行需要较多参数，必须封装为专用结构体指针传入（如 `const config_t*` 或 `context_t*`）。
3. **存量代码豁免原则**：自研新增代码 100% 严格执行上述门禁；第三方开源或继承自历史社区的存量代码（如 Marlin 运动控制器、系统库）以**最小修改预算 (Minimal Diff Budget)** 优先，严禁大范围无关重构或修改已有外部接口。若冻结 ABI 需兼容历史多参入口，公共包装函数必须将实现拆解委托给符合 $\le 50$ 行且 $\le 4$ 参的静态辅助函数。
4. **内存与指针安全**：
   - 指针显式化，严禁压缩指针运算黑魔法（如禁止 `*dst++ = *src++`，统一使用数组下标或分步拆行递增）。
   - 严禁使用超过二级的多重指针（禁止 `***ptr`），指针解引用与取地址操作必须独立成行。
   - 裸机及嵌入式 C++ 零动态堆内存分配（严禁 `new`, `delete`, `malloc`, `free` 及动态 STL 容器）。
   - 禁用异常与 RTTI（`-fno-exceptions -fno-rtti`），显式两阶段初始化，编译期 `static_assert` 结构体布局校验。
5. **控制流与接口防御**：
   - 函数入参在前、出参在后，只读入参必须加 `const`。
   - 对外公开函数入口第一行必须进行防御性空指针校验（Guard Clause），非法指针立即返回错误码。
   - 状态返回值统一度量（强类型错误码或 `bool`），业务数据统一通过末尾出参传出。
   - 卫语句优先，函数嵌套严禁超过 3 层；禁用嵌套三元运算符；复合逻辑条件拆解为具名临时布尔变量。
6. **硬件与外设操作安全**：
   - 寄存器读-改-写分步执行（Clear 后 Set），严禁单行合并清除与置位。
   - 硬件轮询等待强制超时保护（严禁 `while(!FLAG);` 空死等循环，必须展开带超时计数器退出）。
   - 严禁硬编码数值与魔数，位操作统一使用显式移位（`(1U << bit)`）或标准库位掩码宏。

## Changes and Reviews

Use concise, scoped commit subjects. Existing history uses Conventional Commit prefixes such as `docs:` and `chore:`. Keep each commit within one project repository and one logical change. For code work, follow the assigned task's repository and path boundaries, preserve independent QA evidence, and include affected modules plus build or hardware evidence in the review description. For documentation-only changes, identify the documents reviewed and any unverified assumptions.

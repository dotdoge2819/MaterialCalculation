MaterialCalculator - 材料合成统计工具
MaterialCalculator 是一款基于 WPF (C#) 前端界面与 Python 计算引擎相结合的桌面工具。它专门用于处理复杂的多层级合成表（BOM），通过 Excel 维护配方，并能自动计算材料缺口、生成合成树以及按层级规划生产任务。

🚀 核心功能
    可视化合成树：一目了然地展示从成品到最基础原料的完整拆解过程。

    智能库存抵扣：输入当前库存，系统会自动计算扣除库存后的实际材料需求。

    层级生产规划：按照逻辑层级（Level）统计生产任务，指导用户按部就班完成合成。

    灵活数据管理：通过标准的 bom.xlsx 文件管理配方，无需修改代码即可更新游戏数据。



📂 项目结构
    运行本程序需要以下文件位于同一目录下：

    MaterialCalculator.exe：主程序，提供图形化用户界面。

    bridge.exe：Python 核心算法包（已封装所有逻辑依赖）。

    Newtonsoft.Json.dll：程序运行必需的 JSON 解析组件。

    bom.xlsx：配方数据库。



🛠 如何使用
    维护配方：
        打开 bom.xlsx，按照 [产物, 原料, 数量] 的格式填入你的合成公式。

    启动程序：
        双击运行 MaterialCalculator.exe。

    配置库存：
        在界面左侧点击 + 号添加你当前拥有的材料及其数量。

    开始计算：
        在顶部输入目标产物名称和需求数量，点击 “开始计算”。

    查看结果：

        左侧：查看合成树结构。

        右上：查看最终需要准备的基础材料总数。

        右下：查看分层级的详细生产步骤。



🔧 技术架构
    本项目采用了混合架构开发，兼顾了 UI 的响应速度与算法的灵活性：

    前端 (UI)：.NET Framework 4.7.2 / WPF

    后端 (Logic)：Python 3.x (集成 Pandas, Openpyxl)

    通信层：通过标准进程调用与 JSON 数据流进行 C# 与 Python 的异步交互。



⚠️ 注意事项
    环境依赖：用户需安装 .NET Framework 4.7.2 或更高版本（Windows 10/11 已内置）。

    文件完整性：请勿重命名 bom.xlsx 或删除 Newtonsoft.Json.dll，否则会导致程序崩溃。
    
    Excel 编辑：编辑配方表时，请确保没有其他程序（如 Excel 软件）正在占用该文件，否则计算可能失败。



📝 开发者备注
    本项目通过 PyInstaller 将多模块 Python 脚本压缩为单文件 bridge.exe，实现了免 Python 环境运行。

    如果你对配方逻辑感兴趣，核心算法位于：

    bomcore.py (基础计算)

    bomtreecore.py (树状递归)

    bomlevelcore.py (层级统计)

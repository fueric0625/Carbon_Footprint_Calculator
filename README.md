# 第 9 组 · Semester Footprint（个人碳足迹计算器）

SDG2410J Carbon Accounting，2026 秋。核算对象是虚拟学生李明。第 9 组现在只有一个人。

上台用四样东西：`roadshow/Group9_Roadshow_Slides.pptx`、`roadshow/Group9_Roadshow_Script.md`、`calculators/Group9_Final_Calculator.html`，外加手拿的一页 `roadshow/Group9_Roadshow_Card.pdf`，iPad 上翻 `roadshow/Group9_Script_Cards.pdf`（17 页，一页一段）。幻灯片讲约两分钟，中间停在计算器上，最后回到幻灯片只讲单位。上限 8 分钟。

所有作业都还没交，已向老师申请晚交。

## 文件夹

| 文件夹 | 里面是什么 |
|---|---|
| `calculators/` | 三版计算器，都是单文件 HTML，双击用浏览器打开 |
| `roadshow/` | 路演幻灯片、同一内容的网页版、讲稿、排练画布 |
| `logs/` | 已经交过的复查日志和 AI 日志 PDF |
| `notes/` | 提示词、交接说明、课程项目的中文讲解 |
| `design/SDG2410J/` | 老师发的大纲、课件、阅读、项目原件 |
| `requirement/` | 各里程碑作业说明截图，以及空白日志模板 |

## calculators

| 文件 | 作用 |
|---|---|
| `Group9_Prototype0.html` | Milestone 1c。按 Prompt V2 生成的第一版可运行页面，保留不改 |
| `Group9_Prototype1.html` | 复查用的上一版。最终版相对它只改了学期周数和标题单位。不要再改 |
| `Group9_Final_Calculator.html` | Milestone 3b，教室里打开的最终计算器，产品名 **Semester Footprint**。单文件、无外部库、断网能开。2026-11-10 改成浅色主题、字减半，数字一个没动 |

最终版默认 18 周是 **783.7 kg reported**。改成 16 周是 **699.3 kg**，高铁仍是 880 km。结果页顶部 Reset 回到 18 周。

## roadshow

| 文件 | 作用 |
|---|---|
| `Group9_Roadshow_Slides.pptx` | 要上传 Canvas 的幻灯片，九页。第 8 页是单位与气体细节（可略），第 9 页是出处。浅色，Georgia + Segoe UI，没有视频 |
| `Group9_Roadshow_Card.pdf` | 一页 A4 手拿卡：三组数字加七条被问到再答。和幻灯片同一套配色 |
| `build_deck.py` | 生成幻灯片的脚本。改文案改这里，再跑一次 `python roadshow/build_deck.py` |
| `build_card.py` | 生成手拿卡的脚本，跑完用 LibreOffice 导成 PDF |
| `build_logs.py` | 生成 3a 两份日志（含 11-10 追加节）的 docx，再导成 logs/ 里的 PDF |
| `.backup/Group9_Roadshow_Slides_dark.pptx` | 改版前那套深色幻灯片，留着对照 |
| `Group9_Roadshow_Slides.html` | 同一套七页的浏览器版。教室优先用 pptx |
| `Group9_Roadshow_Script.md` | 7 分 30 秒讲稿，含默写数字和问答备用答案 |
| `Group9_Script_Cards.pdf` | 17 页讲稿卡，一页一段，上台带 iPad 翻。含时间轴、应急页、问答两页 |
| `Group9_Script_Cards.html` | 上面那份卡的源文件，改完用 Edge 的 `--print-to-pdf` 重出 |
| `group9-roadshow.canvas.tsx` | 排练用的路演画布源文件。数字和问答与讲稿一致 |

九页的顺序：标题，两个需求，功能单位，因子和归因，页面对需求的回应，三站演示路线，单位这一次复查，单位与气体的细节页（可略），出处。第 12 讲融资排放不放上幻灯片。

## logs

| 文件 | 作用 |
|---|---|
| `Group9_M2a_Review_Log.pdf` | Milestone 2a 计算器复查日志 |
| `Group9_M2a_AI_Log.pdf` | Milestone 2a 的 AI 修改与决定日志 |
| `Group9_M3a_Revisit2_Log.pdf` | 3a 复查日志，对象是 Prototype 1，2026-11-09；末尾有 D 节「Post-review changes, 2026-11-10」 |
| `Group9_M3a_AI2_Log.pdf` | 3a AI 日志。Revision 1–2 用 Cursor（Grok），Revision 3 是 11-10 的份量模型改版 |
| `src/Group9_M3a_Revisit2_Log.docx` | 上面那份复查日志的 Word 源文件，改完用 `roadshow/build_logs.py` 重出 PDF |
| `src/Group9_M3a_AI2_Log.docx` | 上面那份 AI 日志的 Word 源文件 |
| `.backup/` | 11-10 之前的两份旧 PDF |

## notes

| 文件 | 作用 |
|---|---|
| `prompt_v1.md` | Milestone 1a。小组自己写的第一版提示词，按要求当时不用 AI 写 |
| `prompt_v2.md` | Milestone 1b。审过 AI 建议之后定下的提示词，用来生成 Prototype 0 |
| `Group9_Continue_From_Here.md` | 交接说明：做到哪、哪些数不能改、评分点、问答原话 |
| `Group9_M3c_Reflection.md` | Milestone 3c 个人反思正文（143 词），可直接粘到 Canvas |
| `Group9_Worklog_2026-11-10.md` | 11-10 夜间改版的逐步记录：改了为什么这么改、没做什么、早上接着做什么 |
| `project_explain-1012.md` | 用中文把课程项目讲清楚：要交什么、李明的共享事实、哪些数字不能改 |

3c 个人反思写在 `notes/Group9_M3c_Reflection.md`，143 词，口径和台上 6:00–7:30 那段一致。交的时候粘正文，不交文件。

## design/SDG2410J/Course Files

| 文件 | 作用 |
|---|---|
| `CarbonAccounting_2026-2027 Autumn Syllabus.pdf` | 课程大纲：学习目标、进度、成绩比重 |
| `Wechat Group：IB carbon accounting.png` | 课程微信群二维码 |

## design/SDG2410J/Course Project

老师发的项目原件。`requirement/` 里有一份相同的空白日志模板，旁边放着作业截图。

| 文件 | 作用 |
|---|---|
| `CO-STAR Worksheet - From Design Brief to Prompt V1.docx` | 把设计简报写成提示词的工作表。Context、Objective、Style、Tone、Audience、Response |
| `Shared_Student_Profile_Handout.pdf` | 全班共用的李明画像。默认数字以这份为准 |
| `Instructions_for_a_Demo_Presentation_Carbon_Accounting.pdf` | 路演格式：约 1 分钟介绍、约 5 分钟演示、1–2 分钟只讲一次复查，上限 8 分钟 |
| `Final_Web_App_Peer_Evaluation.pdf` | 网页互评表，占课程成绩 15%。可用性、需求回应、功能、结果与建议、核算可信度 |
| `Final_Presentation_and_QA_Peer_Evaluation_Instructor.pdf` | 演示和问答评分表，占课程成绩 5% |
| `Project_Activity_Prototype_1_Revisit_v2.pdf` | Prototype 1 复查的课堂活动说明 |
| `Revisit 1_Calculator_Review_and_Revision_Log_Revisit_1.docx` | 第 1 次复查日志的空白模板 |
| `Revisit 1_AI_Revision_and_Decision_Log_1.docx` | 第 1 次 AI 日志的空白模板 |
| `Revisit 2 Log.docx` | 第 2 次复查日志的空白模板 |
| `Revisit 2_AI Interaction 2 Logs.docx` | 第 2 次 AI 日志的空白模板 |

## design/SDG2410J/Slides

课堂课件，按上课顺序。

| 文件 | 作用 |
|---|---|
| `InClass_CA_GC M1 Lecture 1 Intro.pdf` | 课程结构和学生排放的第一问。同济 3.84 与北大 2.54 t CO₂e/学生/年不能直接比 |
| `InClass_CA_GC M1 Lecture 2 What and Why.pdf` | 碳核算的广义和狭义，自上而下与自下而上，以及估计要适合使用者和目的 |
| `InClass_CA_GC M1 Lecture 3 How.pdf` | 温室气体、GWP、CO₂e。活动数据乘排放因子。碳、CO₂、CO₂e 不能混加 |
| `InClass_CA_GC M1 Lecture 4 Attribution vs Consequential.pdf` | 归因清单描述一个账户；后果核算估计一项决定造成的变化 |
| `InClass_CA_GC M2 Lecture 5 National Inventory.pdf` | 国家清单：领土边界、IPCC、方法分级、生产侧与消费侧 |
| `InClass_CA_GC M2 Lecture 6 City Inventory.pdf` | 城市清单和 GPC。进口电力归用电的城市，不按发电厂所在地一刀切 |
| `InClass_CA_GC M2 Lecture 7 and 8 Organizational Inventory.pdf` | 组织边界、Scope 1/2/3、因子要匹配地区年份和技术，以及宝马的公司清单 |
| `InClass_CA_GC M2 Lecture 9 and 10 Product Carbon Footprint.pdf` | 产品碳足迹：功能单位、生命周期边界、热点。宝马整车研究用 200,000 km |
| `InClass_CA_GC M2 Lecture 11 Project and Policy.pdf` | 项目和政策的后果核算：基线减项目。饮食建议不是这种评估 |
| `InClass_CA_GC M2 Lecture 12 Financial.pdf` | 物理风险、转型风险、TCFD 和融资排放。路演不要主动讲 |

## design/SDG2410J/Readings

| 文件 | 作用 |
|---|---|
| `AAA_V1_1_Ch1_Introduction.pdf` | 核算入门阅读 |
| `nclimate1560 GigatonGap.pdf` | 关大博等，中国国家二氧化碳清单之间的十亿吨级差距 |
| `nature14677 reduced carbon emissions.pdf` | 减排相关的 Nature 阅读 |
| `Carbon footprint analysis of student behavior for a sustainable university campus in China.pdf` | 中国高校学生行为碳足迹论文，对应同济那个学生年均数字的来源之一 |
| `Zhu 等 - 2026 - From intention to action Modeling student lifestyle carbon emissions and reduction scenarios.pdf` | 学生生活方式排放与减排情景，对应北大那个学生年均数字的来源 |
| `BMW Educator Copy_HS.pdf` | 宝马脱碳的教学案例，公司清单和产品足迹都用到 |
| `BMW_Vehicle_Footprint_X5_EN_MY_2026.pdf` | 柴油 X5 的车辆足迹材料。只在被问到电动车是否一定更低时用 |
| `BMW_Vehicle_Footprint_iX5_EN_MY_2026.pdf` | iX5 的车辆足迹材料。同样只在被问到时用，不是计算器的输入 |

## requirement

每一里程碑一张作业说明截图。docx 是空白模板，和 `design/SDG2410J/Course Project/` 里的原件相同。填好并导出的 PDF 在 `logs/`。

| 文件 | 作用 |
|---|---|
| `Milestone 1/Milestone 1a.png` | Prompt V1 的作业要求 |
| `Milestone 1/Milestone 1b.png` | Prompt V2 的作业要求 |
| `Milestone 1/Milestone 1c.png` | Prototype 0 的作业要求 |
| `Milestone 2/Milestone 2a.png` | 第 1 次复查和日志的作业要求 |
| `Milestone 2/Milestone 2b.png` | Prototype 1 的提交要求：一个 HTML，文件名 `Group9_Prototype1.html`，要体现 2a 里记下的修改 |
| `Milestone 2/Milestone 2c.png` | 个人 Exit ticket，100–180 词，写在 Canvas 文本框里 |
| `Milestone 2/Calculator_Review_and_Revision_Log_Revisit_1.docx` | 第 1 次复查日志空白模板 |
| `Milestone 2/AI_Revision_and_Decision_Log_Revisit_1.docx` | 第 1 次 AI 日志空白模板 |
| `Milestone 3/Milestone 3a.png` | 第 2 次复查的作业要求 |
| `Milestone 3/Milestone 3b.png` | 最终计算器的作业要求 |
| `Milestone 3/Milestone 3c.png` | 个人反思的作业要求，100–150 词 |
| `Milestone 3/Revisit 2 Log.docx` | 第 2 次复查日志空白模板 |
| `Milestone 3/Revisit 2_AI Interaction 2 Logs.docx` | 第 2 次 AI 日志空白模板 |

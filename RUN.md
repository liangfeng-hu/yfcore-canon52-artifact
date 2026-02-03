# RUN — Minimal Runnable Adjudicator + Vector Packs

## 0) 你需要什么
- Python 3.10+（推荐）
- 无需安装任何第三方库（零依赖）

## 1) 文件位置必须如下
- `src/canon52_minimal.py`
- `vectors/canon_vectors.json`
- `vectors/adjud_vectors.json`

## 2) Windows 运行（最简单）
1. 打开仓库文件夹
2. 在空白处按住 Shift → 右键 → 选择“在此处打开 PowerShell 窗口”
3. 运行：

   `python src\canon52_minimal.py all`

你应该看到：
- `[CanonSelfTest] OK=16 FAIL=0`
- `[AdjudTest] OK=9 FAIL=0`
- `[ALL] PASS`

## 3) macOS / Linux
- `python3 src/canon52_minimal.py all`

## 4) 常用命令
- 全量自测：`python src/canon52_minimal.py all`
- 只跑 CanonSelfTest：`python src/canon52_minimal.py selftest`
- 只跑裁决向量：`python src/canon52_minimal.py adjudicate`
- 打印锚点：`python src/canon52_minimal.py anchors`
- 生成默认向量文件：`python src/canon52_minimal.py dump`

## 5) 你修改向量/代码后必须做的两步
1) 先跑：`python src\canon52_minimal.py all`（必须 PASS）
2) 再跑：`python src\canon52_minimal.py anchors`  
   把打印出来的 hash 覆盖写回 `SPEC_ANCHORS.md`（防 CRLF/LF 或复制导致漂移）

## 6) 双盲投稿提示（如 CCS/USENIX/S&P 双盲期）
- 暂时删除 README/CITATION 中的作者与公司名
- 不要放任何能关联身份的链接
- 用 zip 或匿名镜像提交 artifact

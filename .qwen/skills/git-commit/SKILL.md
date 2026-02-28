# Git Commit Skill - 同步到云端

## 功能
智能分析 Git 变更，按模块/类型分批提交，确保每个阶段都可独立回滚。

## 唤醒方式
- **自动调用**：每完成一个功能模块后
- **手动调用**：用户说以下任意指令：
  - "commit"
  - "提交代码"
  - "同步到云端"
  - "push"
  - "上传代码"

## 执行流程

### 1. 检查变更
```bash
git status
git diff --stat
```

### 2. 智能分组
根据变更内容自动分组：
- **按目录分组** - 不同模块分开提交
- **按类型分组** - 代码/测试/文档分开提交
- **按功能分组** - 独立功能分开提交
- **按依赖分组** - requirements.txt / package.json 单独提交

### 3. 依赖安装（如需要）
如果检测到依赖文件变更：
```bash
# Python 依赖
if requirements.txt 变更:
    pip install -r requirements.txt

# Node.js 依赖
if package.json 变更:
    npm install
```

### 4. 分批提交和推送
对每个分组执行：
```bash
git add <该组文件>
git commit -m "类型：模块描述"
git push  # 每批提交后必须 push，确保可回滚
```

### 5. 报告结果
显示每批提交的信息和状态

## 分组策略

### 示例 1：多模块变更
```
变更文件:
- src/auth/login.py
- src/auth/logout.py
- src/report/tax.py
- tests/test_login.py
- README.md

分组提交:
1. feat(auth): 添加登录登出功能 (src/auth/*)
2. feat(report): 更新税务计算 (src/report/*)
3. test: 添加登录测试 (tests/*)
4. docs: 更新文档 (README.md)
```

### 示例 2：配置和代码分离
```
变更文件:
- src/app.py
- config.json
- requirements.txt
- .env.example

分组提交:
1. chore: 更新依赖配置 (config.json, requirements.txt)
2. feat: 更新应用功能 (src/app.py)
3. chore: 更新环境示例 (.env.example)
```

## 提交信息规范
- `feat:` - 新功能
- `fix:` - 修复 bug
- `docs:` - 文档更新
- `style:` - 代码格式
- `refactor:` - 重构
- `test:` - 测试相关
- `chore:` - 配置/工具

## 注意事项
- **每批提交后必须 push**，确保可回滚
- 如果某批 push 失败，停止并报告
- 检测到敏感信息时阻止提交并警告
- **必须包含 git push 动作**，确保代码同步到云端

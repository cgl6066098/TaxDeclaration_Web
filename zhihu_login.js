const { chromium } = require('playwright');

(async () => {
    console.log('启动浏览器...');
    const browser = await chromium.launch({ 
        headless: false,
        channel: 'ms-edge'  // 使用 Microsoft Edge
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    const page = await context.newPage();
    
    // 步骤 1: 打开知乎首页
    console.log('步骤 1: 导航到知乎首页...');
    await page.goto('https://www.zhihu.com', { waitUntil: 'networkidle' });
    console.log('知乎首页已加载');
    
    // 等待页面稳定
    await page.waitForTimeout(3000);
    
    // 截图保存当前状态
    await page.screenshot({ path: 'step1_homepage.png', fullPage: false });
    console.log('已保存首页截图：step1_homepage.png');
    
    // 获取当前页面信息
    const pageTitle = await page.title();
    console.log('当前页面标题:', pageTitle);
    
    // 查找登录按钮
    console.log('\n查找登录按钮...');
    const loginButton = page.locator('button:has-text("登录"), a:has-text("登录"), .Login:has-text("登录"), [role="button"]:has-text("登录")').first();
    
    try {
        await loginButton.waitFor({ state: 'visible', timeout: 5000 });
        console.log('找到登录按钮');
        
        // 步骤 2: 点击登录按钮
        console.log('步骤 2: 点击登录按钮...');
        await loginButton.click();
        await page.waitForTimeout(2000);
        
        // 截图
        await page.screenshot({ path: 'step2_after_login_click.png', fullPage: false });
        console.log('已保存点击登录后的截图：step2_after_login_click.png');
        
        // 步骤 3: 查找并点击"密码登录"选项
        console.log('\n步骤 3: 查找密码登录选项...');
        
        // 尝试多种选择器查找密码登录
        const passwordLoginSelectors = [
            'text=密码登录',
            'button:has-text("密码登录")',
            'a:has-text("密码登录")',
            '[role="tab"]:has-text("密码登录")',
            '.tab:has-text("密码登录")',
            'span:has-text("密码登录")',
            'div:has-text("密码登录")'
        ];
        
        let passwordLoginFound = false;
        for (const selector of passwordLoginSelectors) {
            try {
                const passwordLoginBtn = page.locator(selector).first();
                await passwordLoginBtn.waitFor({ state: 'visible', timeout: 3000 });
                console.log(`找到密码登录选项 (使用选择器：${selector})`);
                
                console.log('点击密码登录...');
                await passwordLoginBtn.click();
                await page.waitForTimeout(2000);
                passwordLoginFound = true;
                break;
            } catch (e) {
                continue;
            }
        }
        
        if (!passwordLoginFound) {
            console.log('未找到明确的"密码登录"选项，可能已经是密码登录界面');
        }
        
        // 截图
        await page.screenshot({ path: 'step3_password_login.png', fullPage: false });
        console.log('已保存密码登录界面截图：step3_password_login.png');
        
    } catch (e) {
        console.log('点击登录按钮时出错:', e.message);
        await page.screenshot({ path: 'error_state.png', fullPage: false });
    }
    
    // 获取当前页面状态
    console.log('\n========== 当前页面状态 ==========');
    console.log('URL:', page.url());
    console.log('标题:', await page.title());
    
    // 获取页面上的主要元素
    const elements = await page.evaluate(() => {
        const result = {
            buttons: [],
            inputs: [],
            links: [],
            tabs: []
        };
        
        document.querySelectorAll('button').forEach((el, i) => {
            if (el.offsetParent !== null && el.innerText.trim()) {
                result.buttons.push(el.innerText.trim());
            }
        });
        
        document.querySelectorAll('input').forEach((el, i) => {
            if (el.offsetParent !== null) {
                result.inputs.push({
                    type: el.type,
                    placeholder: el.placeholder,
                    name: el.name
                });
            }
        });
        
        document.querySelectorAll('a[href]').forEach((el, i) => {
            if (el.offsetParent !== null && el.innerText.trim()) {
                result.links.push(el.innerText.trim());
            }
        });
        
        document.querySelectorAll('[role="tab"], .tab, [class*="tab"]').forEach((el, i) => {
            if (el.offsetParent !== null && el.innerText.trim()) {
                result.tabs.push(el.innerText.trim());
            }
        });
        
        return result;
    });
    
    console.log('\n可用按钮:', elements.buttons.slice(0, 20));
    console.log('可用输入框:', elements.inputs);
    console.log('可用标签页:', elements.tabs);
    
    console.log('\n====================================');
    console.log('浏览器保持打开状态，请勿关闭脚本...');
    console.log('按 Ctrl+C 关闭浏览器');
    
    // 保持浏览器打开，等待用户操作
    await page.waitForTimeout(300000); // 等待 5 分钟
    
    await browser.close();
})();

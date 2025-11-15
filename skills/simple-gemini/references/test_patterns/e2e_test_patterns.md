# 端到端测试模式 (E2E Test Patterns)

> **用途**: 提供端到端测试的标准模板和示例代码（Playwright / Cypress）。

---


## 端到端测试模式

### E2E 测试模板 (Playwright / Cypress)

```javascript
// tests/e2e/userFlow.spec.js
import { test, expect } from '@playwright/test';

test.describe('User Registration and Login Flow', () => {
  test.beforeEach(async ({ page }) => {
    // 每个测试前访问首页
    await page.goto('http://localhost:3000');
  });

  test('should complete full user registration flow', async ({ page }) => {
    // Step 1: 导航到注册页面
    await page.click('text=Sign Up');
    await expect(page).toHaveURL(/.*\/register/);

    // Step 2: 填写注册表单
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');
    await page.fill('input[name="confirmPassword"]', 'SecurePass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证注册成功
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('text=Welcome, testuser')).toBeVisible();
  });

  test('should show error for invalid email', async ({ page }) => {
    // Step 1: 导航到注册页面
    await page.click('text=Sign Up');

    // Step 2: 填写无效邮箱
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'Pass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证错误提示
    await expect(page.locator('text=Invalid email format')).toBeVisible();
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    // Prerequisite: 假设用户已注册
    // （在真实 E2E 测试中，可能需要先注册或使用测试数据库）

    // Step 1: 导航到登录页面
    await page.click('text=Login');

    // Step 2: 填写登录表单
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');

    // Step 3: 提交表单
    await page.click('button[type="submit"]');

    // Step 4: 验证登录成功
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('text=Welcome back')).toBeVisible();
  });

  test('should persist user session after page refresh', async ({ page }) => {
    // Step 1: 登录
    await page.click('text=Login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'SecurePass123');
    await page.click('button[type="submit"]');

    // Step 2: 刷新页面
    await page.reload();

    // Step 3: 验证会话保持
    await expect(page).toHaveURL(/.*\/dashboard/);
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });
});
```

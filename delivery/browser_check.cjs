// Optional browser acceptance. Set PLAYWRIGHT_MODULE / CHROMIUM_PATH if needed.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright')
const { execFileSync } = require('node:child_process')
const path = require('node:path')
const assert = require('node:assert/strict')
const root = path.resolve(__dirname, '..')
let browser
;(async () => {
  browser = await chromium.launch({ headless: true, ...(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {}) })
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } })
  const errors = []
  page.on('pageerror', error => errors.push(error.message))
  await page.goto('http://localhost:18080/login', { waitUntil: 'networkidle' })
  assert.equal(await page.title(), '知序人事 · ZHIXU')
  await page.screenshot({ path: path.join(__dirname, '知序登录.png'), fullPage: true })
  await page.setViewportSize({ width: 390, height: 844 })
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth))
  await page.screenshot({ path: path.join(__dirname, '知序移动登录.png'), fullPage: true })
  await page.setViewportSize({ width: 1440, height: 1000 })
  const captcha = JSON.parse(execFileSync('docker', ['compose', '-f', path.join(root, 'compose.delivery.yaml'), 'exec', '-T', 'redis', 'redis-cli', '--raw', 'get', 'validate:code'], { encoding: 'utf8', cwd: root }))
  await page.locator('input[autocomplete="current-password"]').fill('Zx@123456')
  await page.getByPlaceholder('输入右侧数字').fill(captcha)
  await page.getByRole('button', { name: /进入工作空间/ }).click()
  await page.waitForURL('**/home')
  await page.getByText('每一天，从有序开始。').waitFor()
  await page.getByText('你好，知序管理员。组织动态、工作流程和制度知识，都在这里。').waitFor()
  await page.waitForLoadState('networkidle')
  // ECharts animates its first render after the API requests finish.
  await page.waitForTimeout(1200)
  console.log('Home render data:', await page.evaluate(() => {
    const nodes = [document.querySelector('#app').__vue__]
    while (nodes.length) {
      const component = nodes.pop()
      if (component.$options.name === 'Home') return { attendanceDays: component.attendanceData.list.length, cities: component.cityOption.dataset.source.length, departments: component.departmentOption.series[0].data.length }
      nodes.push(...component.$children)
    }
    return null
  }))
  await page.screenshot({ path: path.join(__dirname, '知序工作台.png'), fullPage: true })
  const cookies = await page.context().cookies()
  assert(cookies.find(c => c.name === 'token' && c.httpOnly))
  assert(cookies.find(c => c.name === 'refreshToken' && c.path === '/api/refresh' && c.httpOnly))
  const refresh = await page.evaluate(async () => (await (await fetch('/api/refresh', { method: 'POST', credentials: 'include' })).json()).code)
  assert.equal(refresh, 200)
  await page.goto('http://localhost:18080/chat', { waitUntil: 'networkidle' })
  await page.getByPlaceholder('输入你想咨询的人事制度或政策问题...', { exact: false }).fill('报销需要哪些材料？')
  await page.locator('.chat-input-actions button').click()
  await page.locator('.assistant .chat-text').filter({ hasText: '发票' }).waitFor({ timeout: 30000 })
  await page.getByText('参考来源', { exact: true }).waitFor()
  await page.screenshot({ path: path.join(__dirname, '知序制度问答.png'), fullPage: true })
  await page.reload({ waitUntil: 'networkidle' })
  await page.locator('.conversation-item').first().click()
  await page.locator('.assistant .chat-text').filter({ hasText: '发票' }).waitFor()
  assert.equal(errors.length, 0, errors.join('\n'))
  await browser.close()
  console.log('PASS desktop/mobile branding, actual login, HttpOnly cookies, refresh, home, complete chat answer, citations, and history after reload')
})().catch(async error => { console.error(error); if (browser) await browser.close(); process.exitCode = 1 })

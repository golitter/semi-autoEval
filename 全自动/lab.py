from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time  
import random
import configparser
def wait_millisecond():
    return random.randint(100, 5000)

def save_screenshot(driver, filename):
    """
    保存当前页面的截图到指定路径。
    :param driver: WebDriver 对象
    :param filename: 保存截图的文件名（包括路径）
    """
    try:
        # 保存截图
        driver.save_screenshot(filename)
        print(f"截图已保存：{filename}")
    except Exception as e:
        print(f"截图保存失败: {e}")

def init_browser():
    """
    初始化 Selenium 浏览器。
    :return: WebDriver 对象
    """
    options = webdriver.ChromeOptions()
    # 配置 Chrome 浏览器忽略 SSL 错误
    options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
    options.add_argument("--allow-insecure-localhost")  # 允许不安全的 localhost 连接
    # options.add_argument('--headless')  # 无头模式，后台运行
    # options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--lang=en")  # 设置语言为英语


    driver = webdriver.Chrome(options=options)
    return driver

def login_to_site(driver, login_url, username, password):
    """
    模拟登录到评教网站。
    :param driver: WebDriver 对象
    :param login_url: 登录页面的 URL
    :param username: 用户名
    :param password: 密码
    """
    driver.get(login_url)
    print("正在加载登录页面...")
    
    try:
        # 等待用户名输入框加载完成
        WebDriverWait(driver, wait_millisecond()).until(
            EC.presence_of_element_located((By.ID, 'username'))  # 假设用户名输入框的 name 是 'username'
        )
        driver.find_element(By.ID, 'username').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
        print("登录成功！")
    except Exception as e:
        print(f"登录失败: {e}")
    
     # 展示登录后的页面 URL 或进行截图验证
    print(f"当前页面 URL: {driver.current_url}")  # 输出当前页面的 URL
        
    # 可选：截图保存到本地文件
    # save_screenshot(driver,f'{login_to_site.__name__}.png')


def navigate_to_all_evaluations(driver, evaluation_form_url):
    """
    点击所有评教链接并进行后续操作。
    :param driver: WebDriver 对象
    """
    time.sleep(1)
    # 打开评教表单页面
    driver.get(evaluation_form_url)
    print("正在加载评教表单页面...")
    try:
        # 等待所有评教链接加载
        WebDriverWait(driver, wait_millisecond()).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "evaluationLesson.id") and contains(@href, "teacher.id")]'))
        )

        # 获取所有符合条件的链接元素
        eval_links = driver.find_elements(By.XPATH, '//a[contains(@href, "evaluationLesson.id") and contains(@href, "teacher.id")]')
        print(f"共找到 {len(eval_links)} 个评教链接。")
        eval_links_len = len(eval_links)

        # 遍历每个评教链接并点击
        idx = 1
        for link in eval_links:
            print(f"正在点击第 {idx} / {eval_links_len} 个评教链接：{link.text}")
            link.click()

            print(f"第 {idx} 个评教页面已加载。")

            # 进行评教操作
            evaluate_teacher(driver)       
            
            idx += 1
            
            # 返回到评教链接列表页
            driver.get(evaluation_form_url)
            # driver.back()
            driver.refresh()
            print("正在返回评教链接列表页：" + driver.current_url)
            save_screenshot(driver,f'{navigate_to_all_evaluations.__name__}.png')
            WebDriverWait(driver, wait_millisecond()).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "evaluationLesson.id") and contains(@href, "teacher.id")]'))
            )
            eval_links = driver.find_elements(By.XPATH, '//a[contains(@href, "evaluationLesson.id") and contains(@href, "teacher.id")]')

        print("所有评教链接已处理完成。")
    
    except Exception as e:
        print(f"操作失败: {e}")

def evaluate_teacher(driver):
    """
    进行评教操作。
    :param driver: WebDriver 对象
    """
    print("正在加载" + driver.current_url)
    try:

        ###
        # 等待页面中所有客观题加载
        ##
        WebDriverWait(driver, wait_millisecond()).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'qBox.objective.required'))
        )

        # 获取所有客观题元素
        questions = driver.find_elements(By.CLASS_NAME, 'qBox.objective.required')

        print(f"共找到 {len(questions)} 个问题。")

        # 遍历每个客观题
        for idx, question in enumerate(questions, start=1):
            print(f"正在处理第 {idx} 个问题...")
            time.sleep(1)
            # 查找问题的选项列表
            options = question.find_elements(By.CLASS_NAME, 'option-item')

            # 获取最高分的选项（最后一个选项）
            highest_option = options[-1].find_element(By.TAG_NAME, 'input')
            highest_option.click()  # 选择最高分

            # value 下标从 0 开始，所以需要 +1
            print(f"第 {idx} 个问题已选择最高分：{int(highest_option.get_attribute('value') ) + 1}")
        # 等待页面中所有客观问题加载
        WebDriverWait(driver, wait_millisecond()).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'qBox.objective.required'))
        )


        ###
        # 等待页面中所有主观题加载
        ###
        WebDriverWait(driver, wait_millisecond()).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'qBox.subjective.required'))
        )

        # 获取所有主观问题元素
        subjective_questions = driver.find_elements(By.CLASS_NAME, 'qBox.subjective.required')

        print(f"共找到 {len(subjective_questions)} 个主观问题。")

        # 遍历每个主观问题
        for idx, question in enumerate(subjective_questions, start=1):
            print(f"正在处理第 {idx} 个主观问题...")

            # 查找问题的文本框（textarea）
            textarea = question.find_element(By.CLASS_NAME, 'answer-textarea')
            time.sleep(1)
            if textarea:
                # 在文本框中输入答案
                answer = f"授课很好"
                textarea.send_keys(answer)
                print(f"第 {idx} 个主观问题已回答。")
            else:
                print(f"第 {idx} 个问题没有找到文本框。")

        save_screenshot(driver,f'{evaluate_teacher.__name__}.png')

        WebDriverWait(driver, wait_millisecond()).until(
            EC.presence_of_element_located((By.ID, "sub"))  # 等待提交按钮可用
        )

        # 定位提交按钮
        submit_button = driver.find_element(By.ID, "sub")

        # 点击提交按钮
        submit_button.click()

        # 等待警告框弹出
        WebDriverWait(driver, wait_millisecond()).until(EC.alert_is_present())
    
        # 获取警告框
        alert = Alert(driver)
 
        WebDriverWait(driver, 10).until(
            EC.url_changes(driver.current_url)  # 等待页面 URL 发生变化，表示提交成功
        )
        # 如果你想接受警告框（点击“确定”）
        alert.accept()        
        print("评教已完成并提交。")

    except Exception as e:
        print(f"评教操作失败: {e}")

if __name__ == '__main__':
    # 配置部分
    LOGIN_URL = 'https://login.sust.edu.cn/cas/login?service=http%3A%2F%2Fbkjw.sust.edu.cn%3A80%2Feams%2Fsso%2Flogin.action%3FtargetUrl%3Dbase64aHR0cDovL2Jrancuc3VzdC5lZHUuY246ODAvZWFtcy9ob21lLmFjdGlvbg%3D%3D'  # 登录页面 URL
    EVALUATION_URL = 'https://bkjw.sust.edu.cn/eams/quality/stdEvaluate.action'  # 评教页面 URL
    config = configparser.ConfigParser()
    config.read('config.ini')
    USERNAME = config['Settings']['USERNAME']
    PASSWORD = config['Settings']['PASSWORD']
    print(f"用户名: {USERNAME}")
    print(f"密码: {PASSWORD}")
    exit(0)
    # 初始化浏览器
    driver = init_browser()
    try:
        # 登录
        login_to_site(driver, LOGIN_URL, USERNAME, PASSWORD)

        # 导航到评教页面进行评教
        navigate_to_all_evaluations(driver, EVALUATION_URL)
    finally:
        driver.quit()

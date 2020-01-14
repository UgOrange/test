from selenium import webdriver
import winsound
import time

class searchClasses:

    def alarm(self):
        #提醒声音
        winsound.Beep(1000,5000)

    def inform(self):
        # 发邮件提醒
        self.browser.get("https://mail.qq.com")
        browser = self.browser
        username = browser.find_element_by_id("u")
        password = browser.find_element_by_id('p')

        username_text = "1103895721"
        password_text = "f1f2f3f4f5@"

        username.send_keys(username_text)
        password.send_keys(password_text)

        submit_button = browser.find_element_by_id("login_button")
        submit_button.click()

    #创建并进入网页
    def __init__(self, url="http://jwms.bit.edu.cn/jsxsd/framework/main.jsp"):
        self.browser = webdriver.Chrome()  # 事前将webdriver下载并与添加路径，同时复制到python根目录下
        self.browser.get("http://jwms.bit.edu.cn/jsxsd/framework/main.jsp")
        self.current_page="login"
        return super().__init__()
    
    def login(self, password_text="",username_text="1120173304"):
        #登陆账号
        if(self.current_page!="login"):
            print("Not in a login page!")
            return 0

        browser=self.browser
        password_text="LCH990511lyx"

        username=browser.find_element_by_id("username")
        password=browser.find_element_by_id("password")

        username.send_keys(username_text)
        password.send_keys(password_text)

        login=browser.find_element_by_class_name("btn_image")
        login.click()

        self.current_page="homepage"

    def enter_select(self):
        #进入选课
        browser=self.browser

        if(self.current_page!="homepage"):
            print("Not in homepage!")
            return 0

        entrance=browser.find_element_by_class_name("block2")
        entrance.click()

        start=browser.find_elements_by_tag_name("td")[5]
        start.click()

        center=browser.find_element_by_tag_name("center")
        ass=center.find_elements_by_tag_name("a")[1]
        ass.click()

        #切换到选课标签页
        handles=browser.window_handles
        browser.switch_to.window(handles[1])

        self.current_page="select_parent"

    def enter_section(self, section=1):
        #切换到本学期计划选课
        if(self.current_page!="select_parent"):
            print("Not in select_parent page!")
            return 0
        
        browser=self.browser

        tag=browser.find_elements_by_xpath("/html/body/div[1]/div[1]/ul/li[2]/a")[section]
        tag.click()
        browser.switch_to.frame("mainFrame")
        #self.browser.get("http://jwms.bit.edu.cn/jsxsd/xsxkkc/comeInBxqjhxk")
        ls=["专业选修","公选课"]
        self.current_page="sub_selectpage"+ls[section-1]

    def back_to_parentsection(self):
        ls=["专业选修","公选课"]
        if(self.current_page!="sub_selectpage"+ls[1] and self.current_page!="sub_selectpage"+ls[2]):
            print("Not in a subpage!")
            return 0
        self.browser.switch_to.parent_frame()
        self.current_page="select_parent"

    def traverse(self):
        #找到课程列表，遍历寻找
        if(self.current_page!="sub_selectpage"+"专业选修"):
            print("Not in 专业选修!")
            return 0
        print("1111")
        browser=self.browser

        tables=browser.find_element_by_id("dataView_left")
        wanted_lists=["H0074403", "H0074803"]
        while(True):
            try:
                for classid in wanted_lists:
                    time.sleep(0.3)
                    li=tables.find_element_by_id(classid)
                    li.click()
                    view=browser.find_element_by_id("dataView_right")
                    info=(view.find_elements_by_tag_name("td")[4])
                    info_text=info.text.split("/")
                    already=int(info_text[0])
                    full=int(info_text[1])
                    if(already<full):
                        while(True):
                            self.alarm()
            except:
                print("An exception!")
    
    def search(self, keyword="机器学习理论和实践"):
        #搜索刷新选课
        ls=["专业选修","公选课"]
        if(self.current_page!="sub_selectpage"+"公选课"):
            print("Not in 公选课!")
            return 0

        browser=self.browser

        key_input=browser.find_element_by_id("kcxx")
        key_input.send_keys(keyword)
        body=browser.find_element_by_tag_name("body")
        ll=body.find_elements_by_tag_name("div")[1]
        submit_button=ll.find_element_by_xpath("//input[@value='查询']")
        submit_button.click()

        while(True):
            try:
                submit_button.click()
                view=browser.find_element_by_id("dataView")
                info=(view.find_elements_by_tag_name("td")[10])
                info_text=info.text.split("/")
                left=int(info_text[0])
                full=int(info_text[1])
                if(left>0):
                    while(true):
                        self.alarm()
            except:
                print("An exception!")
    
    def auto(self,section):
        self.login()
        self.enter_select()
        self.enter_section(section)
        if(section==1):
            self.traverse()
        elif(section==2):
            self.search()

    def close(self):
        self.browser.close()

if __name__ == '__main__':
    s = searchClasses()
    try:
        s.auto(1)
    except:
        print("Close.")
        s.close()
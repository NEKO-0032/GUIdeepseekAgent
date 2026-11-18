import main,wx,threading
link = main.tuo_zhan()

#临时设置数据
times_ = link.get_last_id()


main_control  = main.main_control()
class gui_using():
    def show_history(self,times,panel,sizer,font):
        for i in range(times):
            sizer_ = wx.BoxSizer(wx.HORIZONTAL)
            a = wx.Button(panel,id = (i+1)*2,label = f"对话{i+1}")
            a.Bind(wx.EVT_BUTTON,self.history_name_touch)
            a.SetFont(font)
            b = wx.Button(panel,id = i+1 ,label = "管理")
            b.Bind(wx.EVT_BUTTON,self.history_name_setting)
            b.SetFont(font)
            sizer_.Add(a,proportion = 0,flag = wx.ALIGN_TOP,border = 1)
            sizer_.Add(b, proportion=0, flag=wx.ALIGN_TOP, border=3)
            sizer.Add(sizer_,proportion =0 ,flag = wx.ALIGN_TOP,border = 10)

    def history_name_setting(self,event):

        main_control.using_id = event.Id
        use = main.tuo_zhan()
        chat_role = use.search_position(id = event.Id)[0][2]
        pos = use.search_position(id = event.Id)[0][1]
        print(pos)
        main_control.position = pos

        frame_setting = wx.Frame(parent = None,size =(500,400),pos = (800,400),title = f"对话{main_control.using_id}的管理界面")#创建设置窗口

        panel_setting = wx.Panel(frame_setting)#创建画板
        sizer_chat_setting = wx.BoxSizer(wx.VERTICAL)#创建竖向主控


        sizer_setting_1 = wx.BoxSizer(wx.HORIZONTAL)#创建第一行控制器
        text_role_setting = wx.StaticText(panel_setting,label ='设置AI对话设定')#文本控件
        text_role_setting.SetFont(font)
        self.ctrl_role_setting = wx.TextCtrl(panel_setting, style=wx.TE_MULTILINE| wx.HSCROLL | wx.VSCROLL)#创建设定输入框
        self.ctrl_role_setting.SetValue(chat_role)

        sizer_setting_1.Add(text_role_setting,proportion = 1,flag = wx.ALIGN_CENTER,border = 5)
        sizer_setting_1.Add(self.ctrl_role_setting, proportion=3, flag=wx.EXPAND, border=5)

        sizer_setting_2 = wx.BoxSizer(wx.HORIZONTAL)#创建第二行管理器
        save_setting_button = wx.Button(panel_setting,label = "保存")#创建保存按钮
        save_setting_button.Bind(wx.EVT_BUTTON,self.chat_setting_save)
        save_setting_button.SetFont(font)
        delete_button = wx.Button(panel_setting,label = '删除')
        delete_button.SetFont(font)
        delete_button.Bind(wx.EVT_BUTTON,self.delete_check)

        sizer_setting_2.Add(save_setting_button,proportion = 1,flag = wx.EXPAND,border = 10)
        sizer_setting_2.Add(delete_button,proportion = 1,flag = wx.EXPAND,border = 10 )

        sizer_chat_setting.Add(sizer_setting_1, proportion =3,flag = wx.ALIGN_CENTER,border = 10)#将第一行控制器加入到主控
        sizer_chat_setting.Add(sizer_setting_2, proportion=3, flag=wx.EXPAND, border=10)#将第二行控制器加入到主控

        panel_setting.SetSizer(sizer_chat_setting)
        frame_setting.Show()
        #这里的需求：
        #1.
        #2.聊天设定
        #3.文件所在位置
        #这里需要传递给后端的数据
        #1.聊天记录的编号
        #2.聊天设定
        #实现计划  点击管理按钮后弹出管理窗口


    def chat_setting_save(self,event):

        link.save_setting_chat_role(id = main_control.using_id,text=  self.ctrl_role_setting.GetValue())
        wx.MessageBox("已成功保存")

    def history_name_touch(self,event):

        main_control.using_id = event.Id/2

        id_ = event.Id/2
    #print(id_)
        use = main.tuo_zhan()
        pos = use.search_position(id=id_)[0][1]
        print(pos)
        history_text = use.history_get_(pos)

        chat_display.SetValue(history_text)
        chat_display.ShowPosition(chat_display.GetLastPosition())
        main_control.using_history = history_text
        main_control.talking_display_open = 1
        main_control.position = pos
        main_control.role_setting = link.search_position(id=main_control.using_id)[0][2]
        main_control.max_send = int(link.search_settings()[1][1])

    def text_send(self,event):


        if main_control.talking_display_open == 1:#如果显示器正在显示对话记录
            self.text = talk_input.GetValue()#获取发送文本
            talk_input.SetValue('')#将输入框设置为空值
            result = main_control.using_history +"用户："+ '\n'+self.text+"\n"+'--------------------------------------------------------------------------------'+"\n"#将显示结果改为 历史记录+值
            chat_display.SetValue(result)#将显示结果显示出来
            chat_display.ShowPosition(chat_display.GetLastPosition())#下拉显示框
            main_control.using_history = result#刷新内存中的对话记录



            thread = threading.Thread(target=self.thread_send_and_show)

            thread.start()
        else:
            wx.MessageBox('请先从左侧列表中选择对话！')




    def thread_send_and_show(self):
        global talk_send
        talk_send.Disable()
        thread_use = main.tuo_zhan()

        print(self.text,main_control.position,main_control.role_setting,main_control.max_send,main_control.using_api)
        ai_chat = thread_use.send_text(ask=self.text, where=main_control.position,
                                 role_setting=main_control.role_setting
                                 , high=main_control.max_send,api = main_control.using_api
                                 )

        result = main_control.using_history + "DeepSeek-R1：" + '\n' + ai_chat[0] + "\n" + '--------------------------------------------------------------------------------' + "\n"  # 将显示结果改为 历史记录+值，#显示回复
        chat_display.SetValue(result)  # 将显示结果显示出来
        chat_display.ShowPosition(chat_display.GetLastPosition())  # 下拉显示框
        main_control.using_history = result#刷新历史记录

        result = main_control.using_history + "思考过程：" + '\n' + ai_chat[
            1] + "\n" + '--------------------------------------------------------------------------------' + "\n"  # 将显示结果改为 历史记录+值，#显示回复
        chat_display.SetValue(result)  # 将显示结果显示出来
        chat_display.ShowPosition(chat_display.GetLastPosition())  # 下拉显示框
        main_control.using_history = result  # 刷新历史记录
        talk_send.Enable()


    def api_save(self,event):


        api = str(api_input.GetValue()).strip()

        link.save_api(api = api)
        wx.MessageBox('保存成功')
        main_control.using_api = link.get_api()
    def max_send_save(self,event):
        self.yingshe = {"24":"24","36":"36","72":"72","无限制":"9999999"}
        max = self.yingshe[max_send_input.GetValue()]
        link.save_MaxSend(max=max)



    def create_new_chat(self,event):
        link.create_history()
        wx.MessageBox("创建完成，重启软件以刷新对话列表")

    def delete_check(self,event):
        global frame
        frame.Disable()

        frame_delete_check = wx.Frame(parent = None,size = (200,200),pos = (600,300),title = "确认要删除吗？")
        panel_delete_check = wx.Panel(frame_delete_check)
        sizer_check_all = wx.BoxSizer(wx.VERTICAL)
        sizer_check_text = wx.BoxSizer(wx.HORIZONTAL)
        check_text = wx.StaticText(panel_delete_check,label = "确定要删除此对话？\n！将永久失去记录！")
        sizer_delete_check = wx.BoxSizer(wx.HORIZONTAL)
        sure_button = wx.Button(panel_delete_check,label = '确定')
        sure_button.Bind(wx.EVT_BUTTON,self.accept_delete)
        no_button = wx.Button(panel_delete_check,label = '取消')
        no_button.Bind(wx.EVT_BUTTON,self.cancel_delete)

        sizer_check_all.Add(sizer_check_text,proportion =0,flag = wx.EXPAND,border = 0)
        sizer_check_all.Add(sizer_delete_check,proportion = 0 ,flag = wx.EXPAND,border = 0)
        sizer_check_text.Add(check_text,proportion = 0,flag = wx.ALIGN_CENTER,border= 10)
        sizer_delete_check.Add(sure_button,proportion = 1,flag= wx.EXPAND,border = 10)
        sizer_delete_check.Add(no_button,proportion = 1,flag = wx.EXPAND,border = 10)

        panel_delete_check.SetSizer(sizer_check_all)

        frame_delete_check.Show()
        main_control.opening_check = frame_delete_check

    def cancel_delete(self,event):
        global frame
        frame.Enable()
        main_control.opening_check.Close()
        main_control.opening_check = ''

    def accept_delete(self,event):
        print(main_control.using_id)
        if main_control.using_id == 1:
            wx.MessageBox("该对话暂不支持删除！")

        else:
            link.delete_history(pos = main_control.position)
            wx.MessageBox("该对话已删除，请重启软件以刷新列表")

        frame.Enable()




gui_using = gui_using()
main_control.using_api = link.get_api()


app = wx.App()
icon = wx.Icon('maid2.ico', wx.BITMAP_TYPE_ICO)
frame =wx.Frame(parent = None,size = (840,680),pos = (550,200),title = "DeepSeek桌面版")
frame.SetIcon(icon)


notebook = wx.Notebook(frame)#创建表

font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)#普通字体

font_small = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)#小字体
font_chat = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)#聊天小字体
font_biggest = wx.Font(36, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)



notebook.SetFont(font)#设置字体

panel_chat = wx.Panel(notebook)#创建聊天版

sizer_chat_part = wx.BoxSizer(wx.HORIZONTAL)#聊天板块的主控制
sizer_history_show = wx.BoxSizer(wx.VERTICAL)#左侧聊天列表条控制系统
gui_using.show_history(panel=panel_chat,sizer=sizer_history_show,times=times_,font= font_small)#刷新左侧聊天记录条
create_new_button = wx.Button(panel_chat,label = "新建")#设置新建聊天记录的按钮
create_new_button.Bind(wx.EVT_BUTTON,gui_using.create_new_chat)
sizer_chat_part.Add(sizer_history_show,proportion =1 ,flag = wx.ALIGN_CENTER,border = 0)#将左侧管理器设置到主控下
sizer_history_show.Add(create_new_button,proportion =1 ,flag = wx.EXPAND,border = 0)#将新建聊天记录按钮添加到聊天列表管理器

sizer_history_display_part = wx.BoxSizer(wx.VERTICAL)#右侧聊天框的管理器
chat_display = wx.TextCtrl(panel_chat, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL,value = "请先点击左侧对话选项")#创建聊天框显示器
chat_display.SetFont(font_chat)                                                                                #设置字体
sizer_history_display_part.Add(chat_display,proportion = 4,flag = wx.EXPAND,border = 1)#将聊天框添加到右侧控制器
sizer_talk_input = wx.BoxSizer(wx.HORIZONTAL)#设置横向的输入框与发送按钮管理器
talk_input = wx.TextCtrl(panel_chat,style =wx.TE_MULTILINE | wx.HSCROLL | wx.VSCROLL )#设置输入框控件
talk_send = wx.Button(panel_chat,label = "发送")#设置发送按钮
talk_send.Bind(wx.EVT_BUTTON,gui_using.text_send)#绑定发送事件
sizer_talk_input.Add(talk_input,proportion = 8,flag = wx.EXPAND,border = 1)#将输入框添加到横向输入框与发送按钮管理器
sizer_talk_input.Add(talk_send,proportion = 2,flag = wx.EXPAND,border =10)#将发送按钮添加到横向输入框与发送按钮管理器
sizer_history_display_part.Add(sizer_talk_input,proportion = 1,flag = wx.EXPAND,border = 1)
sizer_chat_part.Add(sizer_history_display_part,proportion = 10,flag=wx.EXPAND | wx.ALL,border = 0)#将右侧管理器添加到主控



notebook.AddPage(panel_chat, "聊天")#交流界面

panel_chat.SetSizer(sizer_chat_part)


panel_control = wx.Panel(notebook)#管理界面的画板设置
sizer_control_page = wx.BoxSizer(wx.VERTICAL)#竖向管理界面sizer
sizer_api = wx.BoxSizer(wx.HORIZONTAL)#横向api组件控制
sizer_button = wx.BoxSizer(wx.HORIZONTAL)#横线按钮控制器
sizer_max_send = wx.BoxSizer(wx.HORIZONTAL)#横向最大发送数据控制器


api_static = wx.StaticText(panel_control,label = "在此输入你的APIkey：")#api的文本
sizer_api.Add(api_static,proportion = 1,flag = wx.ALIGN_CENTER,border = 10)#将api输入提示文本加入第一行横向控制器
api_input = wx.TextCtrl(panel_control,value = link.get_api())#设置输入框
api_input.SetFont(font)#设置字体
sizer_api.Add(api_input,proportion = 8,flag = wx.EXPAND,border = 5)#将输入框加入第一行横向控制器

save_api_button = wx.Button(panel_control,label = '保存')#设置保存按钮
save_api_button.Bind(wx.EVT_BUTTON,gui_using.api_save)#
sizer_button.Add(save_api_button,proportion = 0,flag = wx.ALIGN_TOP|wx.TOP,border = 20)#将保存按钮加入第二行


choices = ['24','36','72',"无限制"]
max_send_text = wx.StaticText(panel_control,label = "AI最大聊天记录记忆" )
max_send_text_2 = wx.StaticText(panel_control,label = "条")

def max_send_value():
    a= link.search_settings()[1][1]
    if a == '9999999':
        return '无限制'
    else:
        return a

max_send_input = wx.ComboBox(panel_control,value = max_send_value(),choices = choices)#设置最大聊天记录输入条
timer = wx.Timer(panel_control)#初始化计时器
panel_control.Bind(wx.EVT_TIMER,gui_using.max_send_save,timer)#为管理界面画板增加定时保存最大聊天记录发送限制
timer.Start(1000)
sizer_max_send.Add(max_send_text,proportion = 0,flag = wx.ALIGN_TOP|wx.TOP,border = 40)#最大记录记忆文本加入到第三行控制器
sizer_max_send.Add(max_send_input,proportion = 0 , flag = wx.ALIGN_TOP|wx.TOP,border = 40)#选择器加入到控制器
sizer_max_send.Add(max_send_text_2,proportion = 0,flag = wx.ALIGN_TOP|wx.TOP,border = 40)


sizer_control_page.Add(sizer_api,proportion = 1,flag = wx.ALIGN_CENTER,border = 5)#将第一行控制器加入到主控
sizer_control_page.Add(sizer_button,proportion = 1,flag = wx.ALIGN_CENTER,border = 5)#将第二行加入主控
sizer_control_page.Add(sizer_max_send,proportion = 8,flag = wx.ALIGN_CENTER,border = 5)#将第三行加入主控
notebook.AddPage(panel_control,"管理")#设置管理界面
panel_control.SetSizer(sizer_control_page)#使用主控





frame.Show()
app.MainLoop()
link.finish()
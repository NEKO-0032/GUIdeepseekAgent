

from openai import OpenAI
import openai
import sqlite3
import os
import requests



#print( more_line(ask=str(input('输入询问'))))

role_set = {"1":"你是一名编程助手"}
role_set_code = "1"
#file  = open('聊天记录.txt','a',encoding='utf-8')
#file.write('\na')
#file.close()

def more_line_sql(where:str,role_setting:str,ask:str,high = 10,search = 0,code = 1,type_ = 'send'):#code1是发送，2是查询  #code是屎山残留，默认填1

    #where是指定聊天记录的所在相对位置
    #role_setting 是聊天设定
    #ask是询问内容
    #search是冗余，默认0就行

    #写这个函数的时候以为sql只能存储一行文本，所以写了很麻烦的逻辑把文本拆分成行分别存储
    #chat_history.db存储聊天记录 其中表user_chat是用户发出的内容 表assistant_chat是ai发出的内容
    #列times是int类型，记录对话轮数，text是varchar，记录文本
    na = where

    conn = sqlite3.connect(na)
    cu = conn.cursor()


    message_dict_list = []
    if type_ == 'send':#屎山判断，不用管
        try:
            cu.execute('select * from user_chat')
            user_chat_tuple = cu.fetchall()
        #print(user_chat_tuple)
            cu.execute('select * from assistant_chat')
            assistant_chat_tuple = cu.fetchall()
        #print(assistant_chat_tuple)
        except:
            cu.execute('create table user_chat (times int(9999), text varchar(40))')
            cu.execute('create table assistant_chat (times int(9999), text varchar(40))')
            cu.execute('select * from user_chat')
            user_chat_tuple = cu.fetchall()
            cu.execute('select * from assistant_chat')
            assistant_chat_tuple = cu.fetchall()


        if not user_chat_tuple:#如果聊天记录为空
            ask = ask
            print('已发送，请耐心等待')

            message_dict_list.append({"role": "system", "content": role_setting})
            message_dict_list.append({"role": "user", "content": ask})
            cu.execute(f'insert into user_chat(times,text) values (?,?)',('1',ask))
            conn.commit()
            cu.close()
            conn.close()
            if code == 1:

                return message_dict_list
            if code == 2:
                return "还没有聊天记录喔"
        else:
            message_dict_list = []
            message_dict_list.append({'role':'system','content':role_setting})
            if code == 2:
                search_result = "\n"
            for m in range(user_chat_tuple[-1][0]):
            #print(user_chat_tuple)

                times = m+1
                message_dict_us = {'role':'user'}
                message_dict_as = {'role':'assistant'}
                user_history_list= []

            #整合用户对话
                for  i,s in enumerate(user_chat_tuple):
                    if s[0] == times:#判断是否为同一轮对话
                        user_history_list.append(s[1])
            #print(user_history_list)
                user_history_result = r'\n'.join(user_history_list)#将多行列表数据换为单行的数据

                user_history_result_show = '\n'.join(user_history_list)#展示聊天记录用
                if code == 2:
                    print('用户：',user_history_result_show)
                    print('_____________***********_____________')

                    message_dict_us['content'] = user_history_result#设置用户字典中content的值
                    message_dict_list.append(message_dict_us)
                else:
                    message_dict_us['content'] = user_history_result  # 设置用户字典中content的值
                    message_dict_list.append(message_dict_us)



            #整合ai对话
                assistant_history_list = []
                for i,s in enumerate(assistant_chat_tuple):
                #print(s[0])
                    if s[0] == times :#判断是否是同一轮的对话
                        assistant_history_list.append(s[1])
                assistant_result = r'\n'.join(assistant_history_list)
                message_dict_as['content'] = assistant_result
                message_dict_list.append(message_dict_as)

                assistant_result_show = '\n'.join(assistant_history_list)


            #print(assistant_history_list)



        ask = ask
        print('准备')

        message_dict_list.append({'role':'user','content':ask})
        cu.execute(f'insert into user_chat(times,text) values (?,?)', (str(int(user_chat_tuple[-1][0])+1), ask))
        print(1514)
        conn.commit()
        cu.close()
        conn.close()

            #high是最大组数，每组数包含2个记录，因此乘以2，加上新对话与设定，于是+2
        if len(message_dict_list)>= high*2+2 and (len(message_dict_list)-2)%2 == 0:#为节约经费，对聊天记录大小作限制#当大于最大组数并且为双数时
            for i in range(1,len(message_dict_list)-17):
                message_dict_list.pop(1)

        return message_dict_list






        #for i in range(user_chat_tuple[-1][0]):

#more_line_sql(ask=0)






def deepseek_(where:str,role_setting,ask,api,high = 8):
    print(where)
    #key = str(api)
    key = "sk-1bae42c249c54cb1b40aaac2458cddbe"
    print(key,role_setting,ask,high)
    conn = sqlite3.connect(where)
    cu = conn.cursor()
    cu.execute('select * from assistant_chat')
    list = cu.fetchall()

    try:
        times = str(int(list[-1][0]) + 1)#防止空聊天记录文件
    except:
        times = 1


    try:
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com/v1")


        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages= more_line_sql(where = where,high = high,ask=ask,role_setting= role_setting),#上传聊天记录，并询问
            stream=False
        )



        text_list = response.choices[0].message.content.split('\n')
        for x,y in enumerate(text_list):
            cu.execute(f'insert into assistant_chat (times,text) values(?,?)',(times,y))
        conn.commit()
        cu.close()
        conn.close()
        result = [response.choices[0].message.content.replace('\\n', '\n'),response.choices[0].message.reasoning_content]
        return result
    except openai.AuthenticationError:
        conn = sqlite3.connect(where)
        cu = conn.cursor()
        cu.execute("DELETE FROM user_chat WHERE times = ?",(times,))
        conn.commit()
        cu.close()
        conn.close()
        result = ["未能成功发送","\b错误！请确保你的APIkey是正确的"]
        return result

    except openai.APIConnectionError as p:
        conn = sqlite3.connect(where)
        cu = conn.cursor()
        cu.execute("DELETE FROM user_chat WHERE times = ?",(times,))
        conn.commit()
        cu.close()
        conn.close()



        response = requests.get("https://api.deepseek.com/v1", timeout=5)

        err = response.status_code

        res_2 = requests.get("https://www.baidu.com/",timeout= 5)
        if err == 400 and res_2.status_code == 200:
            result = [f"错误{p}",f"\b正在网络连接检测……\ndeepseek官网返回码：{err}\n百度返回码：{res_2.status_code}\n请检查你设置的api密钥格式正确\n"]
        else:
            result = [f"错误{p}",f"\b正在网络连接检测……\ndeepseek官网返回码：{err}\n百度返回码：{res_2.status_code}"]




        return result

mode = 1








class tuo_zhan():


    conn = sqlite3.connect('chat_lists.db')
    cu = conn.cursor()


    def history_get_(self,pos):
        #新版

        conn = sqlite3.connect(pos)
        cu = conn.cursor()
        cu.execute("select * from user_chat")
        try:
            max_times = cu.fetchall()[-1][0]
        except:
            max_times = 0
        history_text = ""
        for i in range(1,max_times+1):
            cu.execute("select * from user_chat where times = ?",(i,))
            user_cu_select_result = cu.fetchall()
            re_user_list = []

            for x in user_cu_select_result:

                re_user_list.append(x[1])



            cu.execute("select * from assistant_chat where times = ?",(i,))
            assistant_cu_select_result = cu.fetchall()
            re_assistant_list = []
            for y in assistant_cu_select_result:
                re_assistant_list.append(y[1])


            history_text = history_text+"用户："+"\n"+"\n".join(re_user_list)+"\n"+"----------"+'\n'
            history_text = history_text + "DeepSeek-R1：" + "\n" + "\n".join(re_assistant_list) + "\n"+"----------"+'\n'
        return history_text



    def search_settings(self):


        self.cu.execute("select * from gui_settings")
        list_gui = self.cu.fetchall()
        print(list_gui)
        return list_gui

    def search_position(self,id = 1):
        self.cu.execute("select * from list_of_histories where id = ?",(id,))
        result = self.cu.fetchall()
        print(result)
        return result
    def get_last_id(self):
        self.cu.execute('select * from list_of_histories')
        a = self.cu.fetchall()
        result = a[-1][0]
        return result
    def save_setting_chat_role(self,id,text):
        self.cu.execute("update list_of_histories set chat_role = ? where id = ?",(text,id))
        self.conn.commit()
    def send_text(self,ask,where,role_setting,high,api):
        return deepseek_(where=where,ask=ask,role_setting= role_setting,high=high,api = api)



    def save_api(self,api):
        api = api.strip()
        self.cu.execute('update gui_settings set  text = ?  where kind = "api_key"',(api,))
        self.conn.commit()

    def save_MaxSend(self,max):
        self.cu.execute('update gui_settings set  text = ?  where kind = "max_send"', (max,))
        self.conn.commit()
        
    def get_api(self):
        self.cu.execute('select * from gui_settings')
        re_1 = self.cu.fetchall()
        return re_1[0][1]
    def create_history(self):
        id_ = str(int(self.get_last_id())+1)
        pos = "all_history/chat_history_{}.db".format(id_)
        self.cu.execute("insert into list_of_histories (id,position,chat_role) values(?,?,?)",(id_,pos,"null"))
        conn = sqlite3.connect(pos)
        cu = conn.cursor()
        cu.execute('create table user_chat (times int(9999), text varchar(40))')
        cu.execute('create table assistant_chat (times int(9999), text varchar(40))')
        conn.commit()
        cu.close()
        conn.commit()

    def delete_history(self,pos):
        os.remove(pos)
        self.cu.execute("delete from list_of_histories where position = ?",(pos,))
        self.conn.commit()


    def finish(self):
        self.cu.close()
        self.conn.close()



class main_control():
    def __init__(self):
        self.talking_display_open = 0
        self.using_id = 0
        self.using_history = ''
        self.position = ''
        self.role_setting = ''
        self.max_send = 0
        self.opening_check = ''
        self.using_api = ''


if __name__ == "__main__" and mode == 0:#调试
    p = tuo_zhan()
    pos = p.search_position(id = 1)[0][1]

    print(p.history_get_(pos))

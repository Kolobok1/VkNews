import time
from vk_api import VkUpload
from bs4 import BeautifulSoup
import requests
import vk_api
import os

class Post_news():
    
    def __new__(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "info", "Token.txt")
        
        with open(file_path, 'r', encoding='utf-8') as f:
           token = f.read()
        return token
    
    def get_grop(groop_url):
        data = {
            'link': groop_url,
            'button': 'Определить ID'
        }
        
        url = 'https://regvk.com/id/'
        r = requests.post(url=url, data=data)
        src = r.text
        soup = BeautifulSoup(src, "lxml")
        id_grop = soup.find_all('td')
        id_grop = id_grop[1].text
        id_grop = id_grop.partition(':')[2]
        id_grop = id_grop.replace(' ','-')
        
        return id_grop

    def vk_post(post, photo, token):
        
        session = vk_api.VkApi(token=token)

        upload = VkUpload(session) 
        
        try:
            if photo != None and photo != '' and photo != []:
                photo_list = upload.photo_wall(photo)
                attachment = ','.join('photo{owner_id}_{id}'.format(**item) for item in photo_list)

            else:
                attachment = None
        except Exception:
                pass
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "info", "Group links.txt") # такое себе
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            if lines == []:
                return 'Группы не указаны'
            for line in lines:
                try:
                    groop_url = line.rstrip('\n') 

                    groop_id = Post_news.get_grop(groop_url)
                    time.sleep(1)

                    session.method('wall.post', {
                        'owner_id': groop_id,
                        'message' : post,
                        'attachments': attachment
                    })
                    
                except Exception as err:
                    if str(err) == '[214] Access to adding post denied: access to the wall is closed':
                        
                        err = f'Доступ для {line} закрыт '
                    elif str(err) == '[100] One of the parameters specified was missing or invalid: invalid message param':
                        
                        err = 'Не указан ни один из параметров для поста'
                        return err
        return None


    def main(post=None, photo = None):

        token = Post_news()
        if token == '':
            print('Токен не указан')
            err = 'Токен не указан'
            return err
        end = Post_news.vk_post(post,photo,token)

        if end == None:
            end = 'Программа завершена'
        print(end)
        return end

# if __name__ == '__main__':
#     Post_news.main()

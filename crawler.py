import requests
import re
import os

def save_img_and_tags(img_dir, tags_dir, img_id, img_url, img_tags):
    img_data = requests.get(img_url)
    img_format = ".jpge"
    
    if img_url[-4: -1] == ".pn":
        img_format = ".png"
        

    img_file = open(img_dir + "/" + img_id + img_format, 'wb')
    img_file.write(img_data.content)
    img_file.close()

    tags_file = open(tags_dir + "/" + img_id + ".txt", 'w')
    for tag in img_tags:
        tags_file.write(tag + "\n")

    tags_file.close()

'''
获取该网站中特定imgId的图片和tags
@Params String imgId 
'''
def get_target_message(image_dir, tags_dir, img_id):
    detail_url = "http://animepicsx.net/" + img_id
    detail_html = requests.get(detail_url)
    detail_html_text = detail_html.text
    # print(detail_html_text)

    re_pattern = re.compile('<img\nsrc="(https://pics\.animepicsx\.net/images/.*?)" class="z-depth-4 responsive-img">')
    detail_img = re_pattern.findall(detail_html_text)
    #print(detail_img)
    if len(detail_img) != 1:
        raise Exception("图片获取失败")
    else:
        print("imgurl: " + detail_img[0])
        img_url = detail_img[0]
    

    re_pattern = re.compile('<a\nhref="/site/tag\?tag=(.*?)">#.*?</a>')
    detail_tags = re_pattern.findall(detail_html_text)
    print("tags: ", detail_tags)
    
    save_img_and_tags(image_dir, tags_dir, img_id, img_url, detail_tags)

def main():
    # 创建文件夹
    root_dir = "D:/program/humanPos2D"
    image_dir = root_dir + "/image"
    tags_dir = root_dir + "/tags"
    # 规定网站图片张数，与网站更新到的索引有关,目前最大约37300
    image_arrange = [30000, 30010]
    
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    if not os.path.exists(tags_dir):
        os.makedirs(tags_dir)
    
    for i in range(image_arrange[0], image_arrange[1]):
        try:
            get_target_message(image_dir, tags_dir, str(i))
            print(str(i) + " succeed!")
        except Exception as e:
            print(str(i) + " error: ", e)

main()
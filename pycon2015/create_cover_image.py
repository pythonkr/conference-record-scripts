#!/usr/bin/env python
# coding=utf-8
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#font = ImageFont.truetype("./SpoqaHanSans_all/SpoqaHanSans_original/Spoqa Han Sans Regular.ttf",25)
font = ImageFont.truetype("./SpoqaHanSans_all/SpoqaHanSans_original/Spoqa Han Sans Bold.ttf",32)
# 2122 x 716,
logo_img_org = Image.open('pycon_kr_2015.png')
# 1532 x 506
#logo_img = logo_img_org.resize((766,253))
logo_img = logo_img_org.resize((1061,358), Image.ANTIALIAS)
logo_img = logo_img.convert('RGBA')

image_width=1280
image_height=720

def create_cover_image(present_date, subject, speakers):
    img=Image.new("RGBA", (1280,720),'white')

    logo_left = image_width/2 - logo_img.size[0]/2
    logo_top = (image_height- logo_img.size[1])/2-150

    img.paste(logo_img,(logo_left, logo_top), logo_img)

    draw = ImageDraw.Draw(img)
    # draw.text((0, 0),subject,(255,255,0),font=font)
    # get text size
    sub_w, sub_h = draw.textsize(subject, font)
    subject_top = logo_top + logo_img.size[1] + 50
    subject_left = ( image_width - sub_w ) / 2
    print subject_top, subject_left
    draw.text((subject_left, subject_top),subject,'black',font=font)
    #
    sp_w, sp_h = draw.textsize(speakers, font)
    speaker_top = subject_top + sub_h + 20
    speaker_left = ( image_width - sp_w ) / 2
    draw.text((speaker_left, speaker_top),speakers,'black',font=font)
    draw = ImageDraw.Draw(img)
    return img


if __name__ == '__main__':
    img = create_cover_image('2015/05/20',u"파이콘 한국 2015 발표제목",u" 발표자1번 " )
    img.save('test.png')


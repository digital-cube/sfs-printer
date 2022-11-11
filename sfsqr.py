import json
import qrcode
import PIL
import PIL.Image, PIL.ImageDraw

    
def gen(r):

    img = PIL.Image.new("1", (100,100), (255))
    
    img_draw = PIL.ImageDraw.Draw(img)

    text = r['first_name']
    if r['last_name']:
        text += ' ' + r['last_name']
    
    for fsize in (48, 42, 36, 32, 24, 16):
    
        font = PIL.ImageFont.truetype("font.ttf", fsize)
        width = font.getsize(text)[0]
        height = font.getsize(text)[1]
    
        if width < img.size[0]:
            break
    
    #print(f'addig {text} using {fsize}')
    img_draw.text((img.size[0] / 2 - width / 2, 0), text, fill='black', font=font)

    #print('x',img.save('res.png'))
    
    
def generate2(r):

    qr_code = r['data']['qr_code']

    width = 720
    height = 480
    
    bckg = PIL.Image.new("1", (width, height), (255))
    
    qrimg = qrcode.make(qr_code)
    qrimg = qrimg.resize((int(220*1.2),int(220*1.2)),PIL.Image.ANTIALIAS)

    if True:
        sfsimg = PIL.Image.open("sfs2022.png")

        sx = 0.85*0.9
        s = sfsimg.size
        s = (int(s[0]*sx), int(s[1]*sx))
        sfsimg = sfsimg.resize(s)


    img_draw = PIL.ImageDraw.Draw(bckg)

    fsize=60
    font = PIL.ImageFont.truetype("font-bold.ttf", fsize)    
    font2 = PIL.ImageFont.truetype("font.ttf", fsize)    

    dname = r['data']['first_name']+' '+r['data']['last_name']

#    import pdb
#    pdb.set_trace()
    if len(dname)>18:
        img_draw.text((32,32), r['data']['first_name'], fill='black', font=font)  
        img_draw.text((32,108), r['data']['last_name'], fill='black', font=font)  
        if 'organization' in r['data'] and r['data']['organization']:
            img_draw.text((32,184), r['data']['organization'], fill='black', font=font2)  
            print("img_draw.text((32,184), r['data']['organization'], fill='black', font=font2)  ")
    else:
        img_draw.text((32,32), r['data']['first_name']+' '+r['data']['last_name'], fill='black', font=font)  
    
        if 'organization' in r['data'] and r['data']['organization']:
            img_draw.text((32,108), r['data']['organization'], fill='black', font=font2)  
            print("img_draw.text((32,108), r['data']['organization'], fill='black', font=font2)  ")

    
    bckg.paste(qrimg,(bckg.size[0]-10-qrimg.size[0],
                      bckg.size[1]-10-qrimg.size[1]))
    
    bckg.paste(sfsimg,(32, 350))
    
    


    fname = f'/tmp/label-{qr_code}.png'
    bckg.save(fname)

    return fname
    
def main():
    r = {
    "callback": {
        "id": "7355e8bd-1c7a-4b42-b5d0-7df1a2a03901",
        "url": "https://opencon.dev.digitalcube.dev/api/print/callback/7355e8bd-1c7a-4b42-b5d0-7df1a2a03901"
    },
    "data": 
 {"qr_code": "ad8e4e32-ae98-46d3-8375-195213a7c66c", "last_name": "Peric", "first_name": "Petar", "display_name": "Petar Peric", "organization": "DC"}

    ,
        "status": "print"
    }

    a  = generate2(r)
    print(a)
    
if __name__=='__main__':
    main()
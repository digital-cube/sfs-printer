import json
import qrcode
import PIL
import PIL.Image, PIL.ImageDraw

def main():
    r = {
    "callback": {
        "id": "7355e8bd-1c7a-4b42-b5d0-7df1a2a03901",
        "url": "https://opencon.dev.digitalcube.dev/api/print/callback/7355e8bd-1c7a-4b42-b5d0-7df1a2a03901"
    },
    "data": {
        "qrcodeid": "033e2cb9-5581-42cd-9aa7-05259568cf85",
        "title": "SFSCon 2021",
        "first_name": "Jakob",
        "last_name": "Schwienbacher",
        "company": "Telmekom",
    },
        "status": "print"
    }

    #gen(r)
    a  = generate2(r)
    #print("A",a)
    
def gen(r):

    img = PIL.Image.new("1", (100,100), (255))
    
    img_draw = PIL.ImageDraw.Draw(img)

    text = r['data']['first_name']
    if r['data']['last_name']:
        text += ' ' + r['data']['last_name']
    
    for fsize in (48, 42, 36, 32, 24, 16):
    
        font = PIL.ImageFont.truetype("font.ttf", fsize)
        width = font.getsize(text)[0]
        height = font.getsize(text)[1]
    
        if width < img.size[0]:
            break
    
    #print(f'addig {text} using {fsize}')
    img_draw.text((img.size[0] / 2 - width / 2, 0), text, fill='black', font=font)

    #print('x',img.save('res.png'))
    
    
def generate(r):
    
    qrcodeid = r['data']['qrcodeid']
    
    img = qrcode.make(qrcodeid)
    
    img2 = PIL.Image.new("1", (img.size[0], 100 + img.size[1] + 400), (255))

    noi = PIL.Image.open('noi.png')#.convert('RGB')

    #print("SHOW")

    
    img_draw = PIL.ImageDraw.Draw(img2)
#    img_draw = PIL.ImageDraw.Draw(noi)
    
    offset = 0
    
    for fsize in (48, 42, 36, 32, 24, 16):
        font = PIL.ImageFont.truetype("font.ttf", fsize)
        tw, th = font.getsize(r['data']['title'])
        if tw < img.size[0]:
            break
    
#    img_draw.text((img.size[0] / 2 - tw / 2, 0), r['data']['title'], fill='black', font=font)   
#    offset += th + 20

    #print(noi.size)

    x=0.075
        
    size=(int(noi.size[0]*x), int(noi.size[1]*x))    
    
    #print(size)

    noi = noi.resize( size, PIL.Image.BICUBIC)
    
    img2.paste(noi, (int((img.size[0]-noi.size[0])/2), offset))
    offset += size[1]
    img2.paste(img, (0, offset))
    
    offset += img.size[1]
    
    text = r['data']['first_name']
    if r['data']['last_name']:
        text += ' ' + r['data']['last_name']
    
    for fsize in (48, 42, 36, 32, 24, 16):
    
        font = PIL.ImageFont.truetype("font.ttf", fsize)
        width = font.getsize(text)[0]
        height = font.getsize(text)[1]
    
        if width < img2.size[0]:
            break
    
    #print(f'addig {text} using {fsize}')
    img_draw.text((img.size[0] / 2 - width / 2, offset), text, fill='black', font=font)
    offset += height + 10
    
    if r['data']['company']:
    
        text = r['data']['company']
    
        for fsize in (48, 42, 36, 32, 24, 16):
            font = PIL.ImageFont.truetype("font.ttf", fsize)
    
            cwidth = font.getsize(text)[0]
            cheight = font.getsize(text)[1]
    
            if cwidth < img2.size[0]:
                break
    
        #print(f'addig {text} using {fsize}')
        img_draw.text((img.size[0] / 2 - cwidth / 2, offset), text, fill='black', font=font)
    
        offset += cheight + 10
    
    img2 = img2.crop((0, 0, img2.size[0], offset))
    
    fname = f'/tmp/label-{qrcodeid}.png'
    img2.save(fname)
    return fname
    
    
def generate2(r):
    
    qrcodeid = r['data']['qrcodeid']

    width = 720
    height = 480
    
    bckg = PIL.Image.new("1", (width, height), (255))
    
    qrimg = qrcode.make(qrcodeid)
    qrimg = qrimg.resize((int(220*1.2),int(220*1.2)),PIL.Image.ANTIALIAS)

    with open('sfs2021.png') as f:
        sfsimg = PIL.Image.open("sfs2021.png")

        sx = 0.85*0.9
        #print(sfsimg.size)
        s = sfsimg.size
        s = (int(s[0]*sx), int(s[1]*sx))
        sfsimg = sfsimg.resize(s)
        #print(s)


    img_draw = PIL.ImageDraw.Draw(bckg)

    fsize=60
    font = PIL.ImageFont.truetype("font-bold.ttf", fsize)    
    font2 = PIL.ImageFont.truetype("font.ttf", fsize)    

    dname = r['data']['first_name']+' '+r['data']['last_name']

    if len(dname)>18:
        img_draw.text((32,32), r['data']['first_name'], fill='black', font=font)  
        img_draw.text((32,108), r['data']['last_name'], fill='black', font=font)  
        img_draw.text((32,184), r['data']['company'], fill='black', font=font2)  
    else:
        img_draw.text((32,32), r['data']['first_name']+' '+r['data']['last_name'], fill='black', font=font)  
        img_draw.text((32,108), r['data']['company'], fill='black', font=font2)  

    
    bckg.paste(qrimg,(bckg.size[0]-10-qrimg.size[0],
                      bckg.size[1]-10-qrimg.size[1]))
    
    bckg.paste(sfsimg,(32, 350))
    
    


    fname = f'/tmp/label-{qrcodeid}.png'
    bckg.save(fname)

    return fname
    
if __name__=='__main__':
    main()
    
if __name__=='__main__':
    main()
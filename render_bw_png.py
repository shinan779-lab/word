from PIL import Image,ImageDraw,ImageFont
W,H=1200,1570; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
ser='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
rows=["OOOOOOGGGYG","GGGGGGOOYGG","GGGGGGGGGOO","OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO","OOOOOOGGGYY","GGGGGGOOOGY","GYGGGGYOYOO","OOOOOOGGGYY","GGGGGGOOYGO","YYGGGGYGOOO","OOOOOOYYGYY","YYYGGGOYOYY","GYGGGGOOOOO","OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO"]
groups=['SPEI−30','SPEI−60','SPEI−90','SPEI−180','SPEI−270','SPEI−360']; cols=['ET','Prec','PET','Tmax','Tmin','Tmean','AO','NAO','PNA','SM','Wind']
lx,mx,rx=7,97,1088; top=1; rh=66.2; cw=90.1
f34=ImageFont.truetype(ser,34); f30=ImageFont.truetype(ser,30); f27=ImageFont.truetype(ser,27)
def centertext(box,text,font,fill='#111'):
 x0,y0,x1,y1=box; bb=d.textbbox((0,0),text,font=font); d.text(((x0+x1-bb[2])/2,(y0+y1-bb[3])/2-2),text,font=font,fill=fill)
def vertical(box,text):
 tmp=Image.new('RGBA',(220,60),(0,0,0,0)); q=ImageDraw.Draw(tmp); bb=q.textbbox((0,0),text,font=f34); q.text(((220-bb[2])/2,(60-bb[3])/2-3),text,font=f34,fill='#111'); tmp=tmp.rotate(90,expand=True); x0,y0,x1,y1=box; im.paste(tmp,(int((x0+x1-tmp.width)/2),int((y0+y1-tmp.height)/2)),tmp)
def ball(cx,cy,k,r=27):
 box=(cx-r,cy-r,cx+r,cy+r)
 if k=='O': d.ellipse(box,fill='#111',outline='#000',width=2)
 elif k=='G': d.ellipse(box,fill='#999',outline='#111',width=2)
 else:
  d.ellipse(box,fill='#f7f7f7',outline='#111',width=2)
  # diagonal hatch, clipped analytically to circle
  for t in range(-2*r,2*r+1,8):
   pts=[]
   for x in range(-r,r+1):
    y=x+t
    if x*x+y*y<=r*r: pts.append((cx+x,cy+y))
   if len(pts)>1:d.line((pts[0],pts[-1]),fill='#555',width=2)
  d.ellipse(box,outline='#111',width=2)
for g,name in enumerate(groups):
 y=top+g*3*rh; box=(lx,int(y),97,int(y+3*rh)); d.rectangle(box,fill='white',outline='black',width=2); vertical(box,name)
 for rr in range(3):
  py=int(y+rr*rh); b=(rx,py,1177,int(y+(rr+1)*rh)); d.rectangle(b,fill='white',outline='black',width=2); centertext(b,f'PC{rr+1}',f30)
# Draw a clear horizontal rule for every data row across the middle matrix.
# Rules are placed behind the balls so every marker remains legible.
for r in range(19):
 y=int(top+r*rh)
 d.line((97,y,1088,y),fill='#111',width=2)
for r,row in enumerate(rows):
 for c,k in enumerate(row):ball(int(139+c*cw),int(36+r*rh),k)
hy=1191; b=(7,hy,97,1256); d.rectangle(b,fill='white',outline='black',width=2); centertext(b,'n',f30)
for c,name in enumerate(cols):
 x=int(mx+c*cw); b=(x,hy,int(mx+(c+1)*cw),1256); shade='white'; d.rectangle(b,fill=shade,outline='black',width=2); centertext(b,name,f27)
b=(1088,hy,1177,1256); d.rectangle(b,fill='white',outline='black',width=2); centertext(b,'PCs',f27)
for x,k in [(37,'O'),(426,'Y'),(839,'G')]:ball(x,1351,k,34)
for x,shade in [(1,'white'),(394,'white'),(808,'white')]:d.rectangle((x,1491,x+63,1539),fill=shade,outline='#111',width=2)
im.save('球_黑白版.png',dpi=(300,300))

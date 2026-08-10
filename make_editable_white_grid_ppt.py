from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

rows=["OOOOOOGGGYG","GGGGGGOOYGG","GGGGGGGGGOO","OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO","OOOOOOGGGYY","GGGGGGOOOGY","GYGGGGYOYOO","OOOOOOGGGYY","GGGGGGOOYGO","YYGGGGYGOOO","OOOOOOYYGYY","YYYGGGOYOYY","GYGGGGOOOOO","OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO"]
groups=['SPEI−30','SPEI−60','SPEI−90','SPEI−180','SPEI−270','SPEI−360']
cols=['ET','Prec','PET','Tmax','Tmin','Tmean','AO','NAO','PNA','SM','Wind']
prs=Presentation(); prs.slide_width=Inches(9); prs.slide_height=Inches(11.775)
sl=prs.slides.add_slide(prs.slide_layouts[6])
B=RGBColor(20,20,20); W=RGBColor(255,255,255); G=RGBColor(160,160,160)
def box(x,y,w,h,fill=W,lw=0.8):
 s=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h)); s.fill.solid(); s.fill.fore_color.rgb=fill; s.line.color.rgb=B; s.line.width=Pt(lw); return s
def text(s,t,size=12,rot=0):
 tf=s.text_frame; tf.clear(); tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0; tf.vertical_anchor=MSO_ANCHOR.MIDDLE
 p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER; r=p.add_run(); r.text=t; r.font.name='Times New Roman'; r.font.size=Pt(size); r.font.color.rgb=B; s.rotation=rot
# geometry
left=.05; gw=.67; mx=left+gw; top=.02; cw=.675; rh=.495; pcw=.66
# every middle cell is a white editable rectangle, creating all row and column rules
for r in range(18):
 for c in range(11): box(mx+c*cw,top+r*rh,cw,rh,W,.75)
for g,n in enumerate(groups):
 y=top+g*3*rh; s=box(left,y,gw,3*rh,W,1); text(s,n,15,270)
 for rr in range(3):
  s=box(mx+11*cw,y+rr*rh,pcw,rh,W,.9); text(s,f'PC{rr+1}',13)
# ball symbols. Y uses a white circle with editable diagonal lines; all other markers are native circles.
def ball(cx,cy,k,r=.205):
 s=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(cx-r),Inches(cy-r),Inches(2*r),Inches(2*r)); s.fill.solid(); s.line.color.rgb=B; s.line.width=Pt(1.1)
 if k=='O': s.fill.fore_color.rgb=B
 elif k=='G': s.fill.fore_color.rgb=G
 else:
  s.fill.fore_color.rgb=W; s.line.width=Pt(1.3)
  # Short diagonal strokes stay inside the circle and remain individually editable.
  import math
  for q in [-.13,-.07,-.01,.05,.11]:
   a=math.sqrt(max(0,r*r-q*q))/math.sqrt(2)
   ln=sl.shapes.add_connector(1,Inches(cx+q-a),Inches(cy-q+a),Inches(cx+q+a),Inches(cy-q-a)); ln.line.color.rgb=B; ln.line.width=Pt(.8)
for r,row in enumerate(rows):
 for c,k in enumerate(row): ball(mx+(c+.5)*cw,top+(r+.5)*rh,k)
# bottom labels retain three original color families as three grayscale tones
hy=top+18*rh
s=box(left,hy,gw,rh,W,1); text(s,'n',13)
shades=[RGBColor(232,232,232)]*6+[RGBColor(201,201,201)]*3+[RGBColor(169,169,169)]*2
for c,n in enumerate(cols):
 s=box(mx+c*cw,hy,cw,rh,shades[c],1); text(s,n,11.5)
s=box(mx+11*cw,hy,pcw,rh,W,1); text(s,'PCs',12)
# editable legend geometry below, matching the source layout
ly=10.2
for x,k in [(.27,'O'),(3.2,'Y'),(6.3,'G')]: ball(x,ly,k,.25)
for x,shade in [(.02,shades[0]),(2.96,shades[6]),(6.06,shades[9])]: box(x,11.18,.47,.36,shade,1)
prs.save('monochrome_figure_editable_white_grid.pptx')
print('saved',len(sl.shapes),'editable shapes')

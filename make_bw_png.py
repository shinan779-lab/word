import subprocess
from xml.sax.saxutils import escape
W,H=1200,1570
rows=[
"OOOOOOGGGYG","GGGGGGOOYGG","GGGGGGGGGOO",
"OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO",
"OOOOOOGGGYY","GGGGGGOOOGY","GYGGGGYOYOO",
"OOOOOOGGGYY","GGGGGGOOYGO","YYGGGGYGOOO",
"OOOOOOYYGYY","YYYGGGOYOYY","GYGGGGOOOOO",
"OOOOOOGGGYG","GGGGGGOOYGG","GYGGGGGGGOO"]
groups=['SPEI−30','SPEI−60','SPEI−90','SPEI−180','SPEI−270','SPEI−360']
cols=['ET','Prec','PET','Tmax','Tmin','Tmean','AO','NAO','PNA','SM','Wind']
S=[]
def add(x): S.append(x)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('''<defs>
 <pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#f7f7f7"/><line x1="0" y1="0" x2="0" y2="8" stroke="#555" stroke-width="2"/></pattern>
 <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="2" dy="2" stdDeviation="1.3" flood-color="#fff" flood-opacity=".32"/></filter>
</defs>''')
add('<rect width="1200" height="1570" fill="#000"/>')
# geometry follows original: left 7..96; matrix starts 97, right labels 1088..1176
lx,mx,rx=7,97,1088; top=1; rh=66.2; cw=90.1
# left group cells
for g,name in enumerate(groups):
 y=top+g*3*rh
 add(f'<rect x="{lx}" y="{y:.1f}" width="90" height="{3*rh:.1f}" fill="#dedede" stroke="#000" stroke-width="1.5"/>')
 cx=52; cy=y+1.5*rh
 add(f'<text x="{cx}" y="{cy:.1f}" transform="rotate(-90 {cx} {cy:.1f})" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman,serif" font-size="34" fill="#111">{escape(name)}</text>')
 for rr in range(3):
  py=y+rr*rh
  add(f'<rect x="{rx}" y="{py:.1f}" width="89" height="{rh:.1f}" fill="#dedede" stroke="#000" stroke-width="1.3"/>')
  add(f'<text x="1132.5" y="{py+rh/2:.1f}" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman,serif" font-size="30" fill="#111">PC{rr+1}</text>')
# circles, same centers and diameter as original
for r,row in enumerate(rows):
 cy=36+r*rh
 for c,k in enumerate(row):
  cx=139+c*cw
  if k=='O': fill='#f8f8f8'; stroke='#222'; sw=2
  elif k=='Y': fill='url(#hatch)'; stroke='#111'; sw=2.2
  else: fill='#777'; stroke='#eee'; sw=1.8
  add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="27" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" filter="url(#shadow)"/>')
# bottom header row
hy=1191
add(f'<rect x="7" y="{hy}" width="90" height="65" fill="#dedede" stroke="#000" stroke-width="1.3"/>')
add(f'<text x="52" y="{hy+33}" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman,serif" font-size="30">n</text>')
for c,name in enumerate(cols):
 x=mx+c*cw
 # grayscale families retain the original category grouping without color
 shade='#c6c6c6' if c<6 else ('#e3e3e3' if c<9 else '#b0b0b0')
 add(f'<rect x="{x:.1f}" y="{hy}" width="{cw:.1f}" height="65" fill="{shade}" stroke="#000" stroke-width="1.3"/>')
 add(f'<text x="{x+cw/2:.1f}" y="{hy+33}" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman,serif" font-size="27">{name}</text>')
add(f'<rect x="{rx}" y="{hy}" width="89" height="65" fill="#dedede" stroke="#000" stroke-width="1.3"/>')
add(f'<text x="1132.5" y="{hy+33}" text-anchor="middle" dominant-baseline="middle" font-family="Times New Roman,serif" font-size="27">PCs</text>')
# preserve original lower legend geometry, only convert symbols to monochrome
legend=[(37,'O'),(426,'Y'),(839,'G')]
for x,k in legend:
 if k=='O': fill='#f8f8f8'; stroke='#222'
 elif k=='Y': fill='url(#hatch)'; stroke='#111'
 else: fill='#777'; stroke='#eee'
 add(f'<circle cx="{x}" cy="1351" r="34" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
# lower squares retain positions
for x,shade in [(1,'#c6c6c6'),(394,'#e3e3e3'),(808,'#b0b0b0')]:
 add(f'<rect x="{x}" y="1491" width="63" height="48" fill="{shade}" stroke="#111" stroke-width="1.5"/>')
add('</svg>')
open('球_黑白版.svg','w',encoding='utf-8').write('\n'.join(S))
subprocess.run(['convert','-background','black','球_黑白版.svg','球_黑白版.png'],check=True)
print('generated 球_黑白版.png')

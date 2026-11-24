g={}; exec(open("../vincinni/vc.py").read().split("\nimport")[0] if False else open("../vincinni/vc.py").read(), g) if False else None
def load(p,name):
    src=open(p).read(); d={}
    # execute only the data definitions (up to the first function/def or import of runtime libs)
    lines=[]; 
    for l in src.splitlines():
        if l.startswith(("def ","import ","from ","for ","if __name__")) and lines and name+" = [" in "\n".join(lines): break
        lines.append(l)
    exec("\n".join(l for l in lines if not l.startswith(("import ","from "))), d); return d[name]
V=load("../vincinni/vc.py","V"); F=load("../fotonspec/fs.py","F")
VO={}
for cid,title,tag,anchor,beats in V: VO["vincinni_"+cid]=("mk","Kore" if cid=="vc1" else "Charon",[b[4] for b in beats])
VO["foton_specs"]=("mk","Charon",[f[3] for f in F])
VO["foton_specs"]=("mk","Charon",[
 "Tunland V9. Моќ што се чувствува.",
 "Два литри турбо дизел и хибриден помошник од четириесет и осум волти.",
 "Сто дваесет и девет киловати и четиристотини и педесет њутн-метри, плус уште педесет од хибридот.",
 "Цврста рамка, погон на сите четири тркала, електрична блокада.",
 "Кабина како салон: екран од четиринаесет и пол инчи и кожни седишта.",
 "Цена од четириесет и две илјади и деветстотини евра. Пет години гаранција. Закажи тест возење."])
from vo_lines import VO as _B
VO["concord"]=_B["concord"]

# BIG DOGMA site: the brand-neutral LTX material used by the gallery, sector, image-to-motion and build-up sections.
# Shared by build_media.py (encodes) and gen_site.py (markup + MK/EN copy).
# Every clip below was checked frame by frame (6 frames per clip): no brand text or logos, no client concepts, no obvious
# AI morphing. Rejected (not listed): br_c03_s1to2 (ghosted worker), br_c05_s3 (cropped head), br_c05_s4 (box pops in),
# br_c06_s4 (cloth warps), br_c07_s4 ("EST. 1920" crate text and bottle labels), br_c10_s1to2 (paper rolls morph),
# br_c12_s1 (draped figure morphs into a woman), fit_v2 (debris flies in), st_01_wave1 (sofa grows out of the floor),
# tl_05_finish (building un-builds), x_con_x2 (crane load warps), x_int_x1 (headless framing), x_steel_x2 (truck cab melts),
# con_06_fitout (plasterboard stacks multiply); everything comm_*, prop_*, foton_*, vc1/vc2, fs*, ltx_t2v_* (client concepts),
# S/kf (another project), v3raw, oldtv_out.
S = "/tmp/claude-0/-home-user-3p4e/50442171-da10-52d9-9948-b5cc07f6bc8a/scratchpad"
L25, L610, CON = "ltx25", "ltx610", "construction/out"

# sector key -> (MK, EN)
SECTORS = [
 ("con", "Градежништво", "Construction"),
 ("re", "Недвижности", "Real estate"),
 ("int", "Ентериери", "Interiors"),
 ("food", "Храна и малопродажба", "Food and retail"),
 ("wine", "Вино", "Wine"),
 ("steel", "Индустрија и челик", "Industry and steel"),
 ("auto", "Автомобилска индустрија", "Automotive"),
 ("pharma", "Фармација и логистика", "Pharma and logistics"),
 ("energy", "Енергетика и патишта", "Energy and roads"),
 ("rec", "Вработување", "Recruitment"),
 ("prod", "Производи и настани", "Products and events"),
]

# clip id -> (source dir, sector, caption MK, caption EN). Each becomes media/g/<id>.mp4 (960x528, 5 s, muted) + media/g/<id>.jpg
CLIPS = [
 ("con_01_excavation", CON, "con", "Багер и камиони на празен плац во зори", "An excavator and trucks on an empty plot at dawn"),
 ("con_02_foundation", CON, "con", "Бетонирање на темелната плоча", "Pouring the foundation slab"),
 ("con_03_structure", CON, "con", "Бетонскиот скелет расте кат по кат", "The concrete frame rises floor by floor"),
 ("con_05_mep", CON, "con", "Застаклена зграда, светлата се палат", "A glazed building as the lights come on"),
 ("x_con_x1", L610, "con", "Бетонирање кат над градот при изгрејсонце", "Pouring an upper floor above the city at sunrise"),
 ("br_c09_s1to2", L25, "con", "Од плац до скеле: тајмлапс на градба", "From plot to scaffolding: a construction timelapse"),
 ("tl_03_frame", L25, "con", "Столбови и плочи, тајмлапс", "Columns and slabs, timelapse"),
 ("con_08_handover", CON, "con", "Готова зграда во златниот час", "The finished building at golden hour"),
 ("x_re_x1", L610, "re", "Лоби со рецепција, станари пристигнуваат", "A lobby with a concierge desk as residents arrive"),
 ("x_re_x2", L610, "re", "Кровна тераса над градот на зајдисонце", "A rooftop terrace above the city at sunset"),
 ("br_c09_s3to4", L25, "re", "Новата зграда добива градина и паркинг", "The new building gets gardens and parking"),
 ("tl_06_handover", L25, "re", "Станбена зграда, прозорците светат", "A residential building with glowing windows"),
 ("con_07_facade", CON, "re", "Фасада и уредено зеленило", "Facade and fresh landscaping"),
 ("br_c10_s3to4", L25, "int", "Лофт се стилизира, светлото се затоплува", "A loft is styled as the light warms"),
 ("br_c10_s2to3", L25, "int", "Празен лофт станува дневна соба", "An empty loft becomes a living room"),
 ("x_int_x2", L610, "int", "Дизајнерка уредува спална соба", "A designer styles a bedroom"),
 ("x_apt_x1", L610, "int", "Кујна со трпезарија се опремува", "A kitchen-diner is furnished"),
 ("x_apt_x2", L610, "int", "Празна соба станува спална", "An empty room becomes a bedroom"),
 ("st_03_styled", L25, "int", "Дневна соба добива завршни детали", "A living room gets its finishing touches"),
 ("apt_04_styled", CON, "int", "Стан подготвен за вселување, вечер", "An apartment ready to move into, evening"),
 ("fit_v3", L25, "int", "Канцелариски кат од груба градба до готово", "An office floor from shell to finished"),
 ("x_ren_x1", L610, "int", "Стара кујна се реновира", "An old kitchen is renovated"),
 ("x_ren_x2", L610, "int", "Стара бања станува модерна", "An old bathroom turns modern"),
 ("br_c03_s2to3", L25, "int", "Соба по реновирање", "A room after renovation"),
 ("br_c06_s1", L25, "food", "Свежи состојки на дрвена маса", "Fresh ingredients on a wooden table"),
 ("br_c06_s2", L25, "food", "Тесто на производна линија", "Dough on a production line"),
 ("br_c06_s3", L25, "food", "Пакување свежа храна", "Packing fresh food"),
 ("x_food_x1", L610, "food", "Линија за полнење шишиња млеко", "A milk bottling line"),
 ("x_food_x2", L610, "food", "Готвач го сервира јадењето", "A chef plates a dish"),
 ("tl2_store_1", L610, "food", "Празен локал добива полици и каса", "An empty unit gets shelving and a checkout"),
 ("tl2_store_2", L610, "food", "Полиците се полнат пред отворањето", "Shelves are stocked before opening day"),
 ("br_c07_s1", L25, "wine", "Лозја на зајдисонце", "Vineyards at sunset"),
 ("br_c07_s2", L25, "wine", "Берба на грозје", "The grape harvest"),
 ("br_c07_s3", L25, "wine", "Винар во визба со бочви", "A winemaker in a cellar with barrels"),
 ("x_wine_x1", L610, "wine", "Црвено вино во чаша", "Red wine poured into a glass"),
 ("x_wine_x2", L610, "wine", "Винарија меѓу лозја, од воздух", "A winery among vineyards, from the air"),
 ("br_c08_s1", L25, "steel", "Каменолом со камиони во прашина", "A quarry with trucks in the dust"),
 ("br_c08_s2", L25, "steel", "Леење усвитен метал", "Pouring molten metal"),
 ("br_c08_s3", L25, "steel", "Усвитена шипка во валавница", "A glowing bar in a rolling mill"),
 ("br_c08_s4", L25, "steel", "Челични греди на зајдисонце", "Steel beams at sunset"),
 ("x_steel_x1", L610, "steel", "Заварувач и искри", "A welder and sparks"),
 ("br_c04_s1", L25, "auto", "Фабрика во зори, камион пристигнува", "A plant at dawn as a truck arrives"),
 ("br_c04_s2", L25, "auto", "Производна линија за кабловски снопови", "A wiring-harness production line"),
 ("br_c04_s3", L25, "auto", "Прецизно кримпување конектор", "Precision crimping of a connector"),
 ("br_c04_s4", L25, "auto", "Тест-станица, зелени светла", "A test station with green lights"),
 ("br_c04_s5", L25, "auto", "Готов кабловски сноп", "A finished wiring harness"),
 ("x_auto_x1", L610, "auto", "Роботска рака на производна линија", "A robot arm on a production line"),
 ("x_auto_x2", L610, "auto", "Контрола на квалитет во погонот", "Quality control on the factory floor"),
 ("br_c05_s1", L25, "pharma", "Чиста просторија и херметичка врата", "A cleanroom and its airlock"),
 ("br_c05_s2", L25, "pharma", "Подготовка на формулација", "Preparing a formulation"),
 ("x_pharma_x1", L610, "pharma", "Автоматско полнење ампули", "Automated vial filling"),
 ("x_pharma_x2", L610, "pharma", "Робот во автоматизиран магацин", "A robot in an automated warehouse"),
 ("tl2_solar_1", L610, "energy", "Монтажа на соларни панели на покрив", "Installing solar panels on a roof"),
 ("tl2_solar_2", L610, "energy", "Целиот покрив покриен со панели", "The whole roof covered with panels"),
 ("tl2_road_1", L610, "energy", "Асфалтирање пат низ ридовите", "Paving a road through the hills"),
 ("tl2_road_2", L610, "energy", "Готовиот пат, првите возила", "The finished road and its first cars"),
 ("br_c11_s1", L25, "rec", "Модерен кампус, смената пристигнува", "A modern campus as the shift arrives"),
 ("br_c11_s2", L25, "rec", "Тим во лабораторија", "A team in the lab"),
 ("br_c11_s3", L25, "rec", "Колеги на заеднички ручек", "Colleagues sharing lunch"),
 ("x_rec_x1", L610, "rec", "Техничар му покажува на практикант", "A technician shows an apprentice the controls"),
 ("x_rec_x2", L610, "rec", "Крај на смената, во златно светло", "End of the shift, in golden light"),
 ("br_c12_s2", L25, "prod", "Производ во светло од прозорец", "A product in window light"),
 ("br_c12_s3", L25, "prod", "Утро во дрвена куќа", "Morning in a wooden cabin"),
 ("x_prod_x1", L610, "prod", "Стаклено шише на влажна површина", "A glass bottle on a wet surface"),
 ("x_prod_x2", L610, "prod", "Отпакување премиум производ", "Unboxing a premium product"),
 ("tl2_expo_1", L610, "prod", "Монтажа на саемски штанд", "Building an exhibition stand"),
 ("tl2_expo_2", L610, "prod", "Саемскиот штанд е готов", "The exhibition stand is finished"),
]
# clips that only appear in the build-up viewer (not in the gallery wall)
EXTRA = [("con_04_envelope", CON), ("apt_01_shell", CON), ("apt_02_furniture1", CON), ("apt_03_furniture2", CON),
         ("tl2_garden_1", L610), ("tl2_garden_2", L610)]
SRC = {c[0]: c[1] for c in CLIPS} | dict(EXTRA)

# sector demo film -> 3 extra shots shown beside it
SECTOR_SHOTS = [
 ("sector_automotive", ["br_c04_s1", "br_c04_s3", "x_auto_x1"]),
 ("sector_food", ["br_c06_s1", "x_food_x1", "x_food_x2"]),
 ("sector_pharma", ["br_c05_s1", "x_pharma_x1", "x_pharma_x2"]),
 ("sector_wine", ["br_c07_s2", "br_c07_s3", "x_wine_x2"]),
 ("sector_steel_cement", ["br_c08_s2", "br_c08_s3", "x_steel_x1"]),
 ("sector_real_estate", ["x_re_x1", "x_re_x2", "br_c09_s3to4"]),
 ("sector_recruitment", ["br_c11_s2", "br_c11_s3", "x_rec_x2"]),
 ("sector_product_launch", ["br_c12_s2", "x_prod_x1", "x_prod_x2"]),
]

# image -> motion pairs: key frame (extras/kf/<k>.png, the clip's first frame) and its LTX clip; prompt MK / EN (shortened)
I2V = [
 ("x_ren_x1", "extras/kf/ren_x1.png", "Стара кујна", "An old kitchen",
  "Старите шкафови заминуваат, доаѓаат нови бели елементи, камена плоча и висечки светилки.", "The old cabinets go, new white units, a stone worktop and pendant lights arrive."),
 ("x_apt_x2", "extras/kf/apt_x2.png", "Празна соба", "An empty room",
  "Се појавуваат кревет, ноќни масички, завеси и тепих; вечерното светло ја затоплува собата.", "A bed, bedside tables, curtains and a rug appear; evening light warms the room."),
 ("x_ren_x2", "extras/kf/ren_x2.png", "Стара бања", "An old bathroom",
  "Плочките се симнуваат, доаѓаат големи сиви плочки, стаклен туш и лебдечки лавабо.", "The tiles come off; large grey tiles, a glass shower and a floating vanity go in."),
 ("x_apt_x1", "extras/kf/apt_x1.png", "Празна кујна", "An empty kitchen",
  "Кујнски остров, столчиња, трпезариска маса и светилки се наместуваат на своите места.", "A kitchen island, bar stools, a dining table and lamps settle into place."),
 ("x_wine_x1", "extras/kf/wine_x1.png", "Винар во визба", "A winemaker in the cellar",
  "Виното тече во чашата, се врти и смирува, а светлото од свеќата игра на работ.", "Wine streams into the glass, swirls and settles as candlelight glints on the rim."),
 ("x_auto_x1", "extras/kf/auto_x1.png", "Роботска рака", "A robot arm",
  "Роботот зема дел, го ротира и прецизно го спушта на подвижната лента.", "The robot picks a part, rotates it and places it precisely on the moving belt."),
]

# build-up projects: (key, MK, EN, stages = [(key frame path, clip id or None, label MK, label EN)])
CK = "construction/kf"; TK = "tl2/kf"
BUILDS = [
 ("bld", "Станбена зграда", "Residential building", [
   (f"{CK}/con_01_excavation_start.png", "con_01_excavation", "Ископ", "Excavation"),
   (f"{CK}/con_02_foundation_start.png", "con_02_foundation", "Темели", "Foundation"),
   (f"{CK}/con_03_structure_start.png", "con_03_structure", "Конструкција", "Structure"),
   (f"{CK}/con_04_envelope_start.png", "con_04_envelope", "Обвивка", "Envelope"),
   (f"{CK}/con_05_mep_start.png", "con_05_mep", "Инсталации", "Services"),
   (f"{CK}/con_07_facade_start.png", "con_07_facade", "Фасада", "Facade"),
   (f"{CK}/con_08_handover_start.png", "con_08_handover", "Предавање", "Handover")]),
 ("apt", "Опремување стан", "Apartment staging", [
   (f"{CK}/apt_01_shell_start.png", "apt_01_shell", "Празен стан", "Empty shell"),
   (f"{CK}/apt_02_furniture1_start.png", "apt_02_furniture1", "Прв мебел", "First furniture"),
   (f"{CK}/apt_03_furniture2_start.png", "apt_03_furniture2", "Опремено", "Furnished"),
   (f"{CK}/apt_04_styled_start.png", "apt_04_styled", "Стилизирано", "Styled")]),
 ("solar", "Соларен покрив", "Solar roof", [
   (f"{TK}/solar_1.png", "tl2_solar_1", "Празен покрив", "Bare roof"),
   (f"{TK}/solar_2.png", "tl2_solar_2", "Половина панели", "Half the panels"),
   (f"{TK}/solar_3.png", None, "Цел покрив", "Full roof")]),
 ("road", "Пат", "Road", [
   (f"{TK}/road_1.png", "tl2_road_1", "Насип", "Graded earth"),
   (f"{TK}/road_2.png", "tl2_road_2", "Прв асфалт", "First asphalt"),
   (f"{TK}/road_3.png", None, "Готов пат", "Finished road")]),
 ("garden", "Градина", "Garden", [
   (f"{TK}/garden_1.png", "tl2_garden_1", "Гола земја", "Bare soil"),
   (f"{TK}/garden_2.png", "tl2_garden_2", "Патеки и садници", "Paths and saplings"),
   (f"{TK}/garden_3.png", None, "Готова градина", "Finished garden")]),
 ("store", "Продавница", "Store", [
   (f"{TK}/store_1.png", "tl2_store_1", "Празен локал", "Empty unit"),
   (f"{TK}/store_2.png", "tl2_store_2", "Опрема", "Fit-out"),
   (f"{TK}/store_3.png", None, "Отворање", "Opening day")]),
 ("expo", "Саемски штанд", "Expo stand", [
   (f"{TK}/expo_1.png", "tl2_expo_1", "Празна хала", "Empty hall"),
   (f"{TK}/expo_2.png", "tl2_expo_2", "Конструкција", "Frame"),
   (f"{TK}/expo_3.png", None, "Готов штанд", "Finished stand")]),
]
def kf_id(path): return path.rsplit("/", 1)[1].rsplit(".", 1)[0].replace("_start", "")
KEYFRAMES = sorted({p for _, _, _, st in BUILDS for p, *_ in st} | {k for _, k, *_ in I2V})

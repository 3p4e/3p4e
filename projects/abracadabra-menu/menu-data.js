/*
  ABRACADABRA — податоци за дигиталното мени.
  Менувај ги цените/артиклите тука ИЛИ преку admin.html (има копче „Преземи menu-data.js“).

  Правила:
  - price: null  -> артиклот НЕ се прикажува (празно поле на старото мени).
  - available: false -> привремено скриен (пр. „нема денес“).
  - badge: "ХИТ" | "НОВО" | "ВЕГЕ" | "" -> мала ознака покрај името.
  - screen: на кој екран оди категоријата (1 = лев, 2 = десен).
  - promos[].video: анимација на маскотата за таа промоција (fox_burger, fox_waffle, fox_wrap).
*/
window.MENU_DATA = {
  currency: "ден",
  // Опционално: линк до Google Sheet објавен како CSV (File > Share > Publish to web > CSV).
  // Ако е пополнет, цените/артиклите се читаат од табелата и се освежуваат автоматски.
  sheetCsvUrl: "",
  refreshMinutes: 5,
  // Од колку часот екраните преминуваат во „ноќен неон“ режим (маскота + магента).
  nightFrom: 19,
  nightTo: 6,

  promos: [
    { title: "АБРАКАДАБРА БУРГЕР", subtitle: "Нашиот магичен специјалитет + помфрит", price: 350, video: "fox_burger" },
    { title: "ДРПАН БУРГЕР", subtitle: "Сочно дрпано месо + помфрит", price: 250, video: "fox_burger" },
    { title: "АБРАКАДАБРА ВАФЛА", subtitle: "Слатка магија за крај", price: 130, video: "fox_waffle" },
    { title: "ДРПАНО ЈУНЕШКО", subtitle: "Врап полн со вкус", price: 200, video: "fox_wrap" }
  ],

  categories: [
    { id: "burgeri", screen: 1, name: "Бургери", note: "+ помфрит", color: "red", items: [
      { name: "Хамбургер", price: 170 },
      { name: "Чизбургер", price: 200 },
      { name: "Абракадабра бургер", price: 350, badge: "ХИТ" },
      { name: "Хамбургер со јајце", price: 200 },
      { name: "Чикен бургер", price: 160 },
      { name: "Чикен чизбургер", price: 180 },
      { name: "Дрпан бургер", price: 250 },
      { name: "Смачкан бургер", price: 200 },
      { name: "Веге бургер", price: null, badge: "ВЕГЕ" }
    ]},
    { id: "sendvichi", screen: 1, name: "Сендвичи", note: "+ помфрит", color: "lime", items: [
      { name: "Пилешка шунка и кашкавал", price: 150 },
      { name: "Врат и кашкавал", price: 160 },
      { name: "Кулен и кашкавал", price: 170 },
      { name: "Свинска шунка и кашкавал", price: 150 },
      { name: "Сланина и кашкавал", price: null },
      { name: "Суџук и кашкавал", price: null },
      { name: "Хот дог", price: 100 },
      { name: "Корн дог", price: 50 },
      { name: "Кроасан со виршла", price: null }
    ]},
    { id: "tostovi", screen: 1, name: "Тостови", note: "+ помфрит", color: "orange", items: [
      { name: "Пилешка шунка и кашкавал", price: 150 },
      { name: "Врат и кашкавал", price: 160 },
      { name: "Кулен и кашкавал", price: 170 },
      { name: "Свинска шунка и кашкавал", price: 150 },
      { name: "Сланина и кашкавал", price: null },
      { name: "Суџук и кашкавал", price: null }
    ]},
    { id: "pohovano", screen: 1, name: "Поховано", note: "", color: "yellow", items: [
      { name: "Пилешки стек", price: null },
      { name: "Пилешки копан", price: null },
      { name: "Пилешки крилца", price: null },
      { name: "Кашкавал", price: null }
    ]},
    { id: "vege", screen: 1, name: "Веге оброци", note: "", color: "green", items: [
      { name: "Веге оброк", price: null, badge: "ВЕГЕ" }
    ]},

    { id: "vrapovi", screen: 2, name: "Врапови", note: "", color: "orange", items: [
      { name: "Дрпано јунешко", price: 200, badge: "ХИТ" },
      { name: "Дрпано пилешко", price: 150 },
      { name: "Поховано пилешко", price: null },
      { name: "Веге врап", price: null, badge: "ВЕГЕ" }
    ]},
    { id: "skara", screen: 2, name: "Скара", note: "", color: "red", items: [
      { name: "Пилешки ражнич", price: null },
      { name: "Телешки ражнич", price: null },
      { name: "Ражнич со пилешки џигер", price: 30 },
      { name: "Кебапче", price: 20 },
      { name: "Домашен колбас", price: null }
    ]},
    { id: "salati", screen: 2, name: "Салати", note: "", color: "lime", items: [
      { name: "Цезар", price: null },
      { name: "Абракадабра", price: null }
    ]},
    { id: "deserti", screen: 2, name: "Десерти", note: "", color: "magenta", items: [
      { name: "Вафла со нутела и банани", price: 100 },
      { name: "Вафла со мармелад", price: 50 },
      { name: "Вафла со крем од ф'стак", price: 100 },
      { name: "Абракадабра вафла", price: 130, badge: "ХИТ" },
      { name: "Сутлијаш", price: 50 }
    ]},
    { id: "dodatoci", screen: 2, name: "Додатоци", note: "", color: "yellow", items: [
      { name: "Лепче", price: 20 },
      { name: "Помфрит мал", price: 50 },
      { name: "Помфрит голем", price: 70 },
      { name: "Чипс", price: 50 },
      { name: "Сосови", price: null }
    ]},
    { id: "kafe", screen: 2, name: "Кафе", note: "", color: "brown", items: [
      { name: "Нес-кафе", price: 50 },
      { name: "Еспресо", price: null },
      { name: "Макијато", price: null },
      { name: "Капучино", price: null },
      { name: "Фрапе", price: 40 }
    ]},
    { id: "pijaloci", screen: 2, name: "Пијалоци", note: "", color: "magenta", items: [
      { name: "Милкшејк", price: 80 },
      { name: "Смути", price: null },
      { name: "Чај", price: null },
      { name: "Бабл чај", price: null },
      { name: "Цеден сок", price: null },
      { name: "Сок", price: 50 },
      { name: "Вода", price: null }
    ]}
  ]
};

#import "@preview/polylux:0.4.0": *

#show link: set text(blue)
#set text(font: "IBM Plex Sans", size: 20pt)
#show raw: set text(font: "IBM Plex Mono")
#show math.equation: set text(font: "IBM Plex Math")

#set document(
  title: "π kiszámítása közelítése segítségével",
  author: "Sebe Zsolt (ACC02G)",
  date: datetime(year: 2025, month: 2, day: 25), // ekkor kell előadni
)

#let my-stroke = stroke(
  thickness: 2pt,
  paint: rgb("750e13"),
  cap: "round",
)

#set page(
  paper: "presentation-16-9",
  margin: 2cm,
  footer: [
    #set text(size: .6em)
    #set align(horizon)

    #h(1fr) #toolbox.slide-number
  ],
  header: box(stroke: (bottom: my-stroke), inset: 8pt)[
    #h(1fr)
  ],

  fill: rgb("dde1e6")
)

#show heading: set block(below: 2em)

#let new-section-slide(title) = slide[
  #set page(footer: none, header: none)
  #set align(horizon)
  #set text(size: 1.5em)
  #strong(title)
  #line(stroke: my-stroke, length: 50%)
  #toolbox.register-section(title)
]

#slide[
  #set page(footer: none, header: none)
  #set align(horizon)
  #text(size: 2em, weight: "bold")[
    #toolbox.side-by-side(columns: (auto, 1fr))[
      #text($pi$, 6em)
    ][
      közelítése gyufák segítségével
    ]
  ]

  #line(stroke: my-stroke, length: 100%)

  //Egy Monte Carlo módszer

  Sebe Zsolt, Február 25, 2025
]

#new-section-slide[Bevezetés]

#slide[
	#toolbox.side-by-side[
    = A probléma lényege

		Véletlenszerűen ledobott gyufák és párhuzamos vonalak metszése alapján lehet $pi$-t becsülni.
	][
		#image("gyufák.jpg")
	]
]

#slide[
  = Matematikai háttér

  - $L$: a gyufa hossza
  - $d$: a párhuzamos vonalak távolsága
  - $p$: annak a valsége, hogy van metszés $(N_"metszés" / N)$

  $
    p = 2/pi dot L/d quad #uncover(2, text($=> pi approx (2 dot L dot N) / (d dot N_"metszés")$, 2em))
  $
]

#slide[
  = Matematikai háttér

  Ha $d = 2L$ (azaz a gyufa pont fele olyan hosszú mint a vonalak közötti távolság), akkor:

  $
    pi approx (2 dot L dot N) / (2 dot L dot N_"metszés") quad #uncover(2, text($=> pi approx N / N_"metszés"$, 2em))
  $
]

#new-section-slide[Implementáció]

#slide[
  = Áttekintés

  - Egy C++ kód generálja a random $(x_0, y_0, x_1, y_1, c)$ párost, majd ezt átadja a Python kódnak, vagy kiírja egy file-be (opcionális).
  - A Python kód a C++ kóddól kapott párosokból, vagy a file-ból kiolvasva megcsinálja a plot-ot.
  - *Figyelem:* Ha túl sok minta van, a plot le fog fagyni.
  - Ha csak az eredmény érdekel, akkor a C++ kód ki tudja számítani azt a párosok generálása nélkül.
]

#slide[
  #toolbox.side-by-side[
    = Áttekintés

    - $(x_0, y_0)$ a gyufa egyik végének koordinátái. Értékük random
    - $(x_1, y_1)$ a gyufa másik koordinátái, Értékük az előző koordinátától és a $theta$ szögtől függ.
    - $theta$ egy egyenletes eloszlású szög. (ez nincs benne a kimenetben, mert csak a másik véghez kell)
    - $c in {0, 1}$ megmondja, hogy a gyufánk átmegy-e a vonalon.
  ][
    #image("impl.svg", width: 100%)
  ]
]

#slide[
  = A szimuláció paraméterei

  - $L = 1$, $d = 2$
  - *Gyufa:*

  $
    x_0   &<- "uniform_random"(0, 8) \
    y_0   &<- "uniform_random"(0, 8) \
    theta &<- "uniform_random"(0, 360degree) \
    x_1   &<- x_0 + sin theta \
    y_1   &<- y_0 + cos theta \
    c     &<- 1 "ha van metszés, különben" 0
  $
]

#slide[
  #toolbox.side-by-side[
    = Problémák a módszerrel

    - *Nem hatékony:* 10 milliárd próba után is csak 3 tizedesjegyik jó \ ($approx 3.141623$, err = -0.00003034), és úgy tűnik hogy innentől már nem javul
    - *Függőség:* a szimulációnak alapból tudni kell $pi$ értékét, bár ez helyettesíthető lenne.
    - *Nem realisztikus:* A valóságban ha random dobunk gyufákat nem lesz egyenletes az eloszlás.
  ][
    #image("hot-cpu.png")
  ]
]

#slide[
  = Források

  - _Buffon's needle problem_, Wikipédia \ https://en.wikipedia.org/wiki/Buffon%27s_needle_problem
  - _why it works 8_, \@tylerschannel \ https://youtu.be/puDKR0lZRZM
]

#new-section-slide[Vége]

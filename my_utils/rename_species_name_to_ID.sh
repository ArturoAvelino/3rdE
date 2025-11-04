# Convert species names to species IDs using the latest label tree
# provided by Emilie on 25 sept 2025.
#
# To run this script, in a terminal go where the files are located
# and the type:
#     bash thisfile.sh

find . -type f -name "*.csv" -exec sed -i '' 's/\"Unclassified\"/1/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dirt\"/2/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metazoa\"/3/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arachnida\"/4/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acari\"/5/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Araneae +5mm\"/6/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Araneae -5mm\"/7/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoscorpiones\"/8/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Opiliones\"/9/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Palpigradi\"/10/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Crustacea\"/11/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isopoda\"/12/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Myriapoda\"/13/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplopoda +5mm\"/14/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplopoda -5mm\"/15/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chilopoda +5mm\"/16/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chilopoda -5mm\"/17/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Symphyla\"/18/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pauropoda\"/19/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hexapoda\"/20/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplura\"/21/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protura\"/22/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Collembola\"/23/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Insecta\"/24/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Coleoptera\"/25/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diptera adult\"/26/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diptera larva\"/27/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenoptera\"/28/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenoptera Formicidae\"/29/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hemiptera\"/30/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Psocoptera\"/31/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thysanoptera\"/32/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Embioptera\"/33/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dermaptera\"/34/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Campodeoidea\"/35/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Japygoidea\"/36/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattodea\"/37/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Corydiidae\"/38/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isoptera\"/39/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattidae\"/40/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orthoptera\"/41/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cantharidae\"/42/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabidae\"/43/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Curculionidae\"/44/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Elateridae\"/45/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scarabaeidae\"/46/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Silphidae\"/47/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Staphylinidae\"/48/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tenebrionidae\"/49/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Auchenorrhyncha\"/50/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteroptera\"/51/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sternorrhyncha\"/52/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobryomorpha\"/53/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobryidae\"/54/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya\"/55/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya lanuginosa\"/56/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya nivalis\"/57/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus\"/58/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus curvicollis\"/59/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus cyaneus\"/60/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus lignorum\"/61/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus violaceus\"/62/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella\"/63/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella alba\"/64/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella anderseni\"/65/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomidae\"/66/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurophorus\"/67/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurophorus alpinus\"/68/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ballistura\"/69/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ballistura borealis\"/70/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria\"/71/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria nivalis\"/72/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria tadzhika\"/73/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia\"/74/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia bisetosa\"/75/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia candida\"/76/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia decemoculata\"/77/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia dovrensis\"/78/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia inoculata\"/79/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia manolachei\"/80/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia palaearctica\"/81/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia penicula\"/82/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia quadrioculata\"/83/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia spinosa\"/84/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomides\"/85/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomides aylloensis\"/86/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma\"/87/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma anglicana\"/88/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma caerulea\"/89/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma viridis\"/90/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella\"/91/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella minor\"/92/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella paraminor\"/93/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus\"/94/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus cassagnaui\"/95/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus graminis\"/96/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus palustris\"/97/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus punctiferus\"/98/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma\"/99/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma agrelli\"/100/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma notabilis\"/101/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Proisotoma\"/102/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus\"/103/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus binoculatus\"/104/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus quadrioculatus\"/105/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma\"/106/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma monochaeta\"/107/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma sensibilis\"/108/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella\"/109/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella gallica\"/110/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella schalleri\"/111/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus\"/112/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus asiaticus\"/113/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus ciliatus\"/114/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopoduridae\"/115/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopodura\"/116/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopodura crassicornis\"/117/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesellidae\"/118/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteromurus\"/119/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteromurus nitidus\"/120/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella\"/121/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella bifasciata\"/122/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella quinquefasciata\"/123/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella villosa\"/124/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paronellidae\"/125/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cyphoderus\"/126/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cyphoderus albinus\"/127/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomoceridae\"/128/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pogonognathellus\"/129/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pogonognathellus flavescens\"/130/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerina\"/131/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerina varia\"/132/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus\"/133/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus minor\"/134/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus vulgaris\"/135/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelipleona\"/136/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelidae\"/137/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax\"/138/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax minimus\"/139/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax willemi\"/140/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelides\"/141/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelides minutus\"/142/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelus\"/143/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelus murinus\"/144/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poduromorpha\"/145/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomellidae\"/146/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella\"/147/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella curvula\"/148/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella parvula\"/149/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastruridae\"/150/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella\"/151/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella armata\"/152/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella denticulata\"/153/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella gibbosa\"/154/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella impedita\"/155/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella laricis\"/156/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella stercoraria\"/157/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Choreutinula\"/158/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Choreutinula inermis\"/159/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura\"/160/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura crassaegranulata\"/161/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura serrata\"/162/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura socialis\"/163/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura\"/164/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura pallida\"/165/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura parva\"/166/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schaefferia\"/167/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schaefferia emucronata\"/168/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schoettella\"/169/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schoettella ununguiculata\"/170/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia\"/171/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia anophthalma\"/172/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia densi\"/173/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia  anophthalma\"/174/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla\"/175/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla acauda\"/176/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla brevicauda\"/177/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanuridae\"/178/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurida\"/179/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurida granaria\"/180/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea\"/181/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea albida\"/182/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea atypica\"/183/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea emucronata\"/184/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea inermis\"/185/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea mirabilis\"/186/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea pseudodecipiens\"/187/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea truncata\"/188/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea villanuevai\"/189/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida\"/190/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida anophthalmica\"/191/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida pygmaea\"/192/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanura\"/193/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanura muscorum\"/194/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina\"/195/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina angelieri\"/196/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina meridionalis\"/197/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes\"/198/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes dubius\"/199/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes minor\"/200/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes palmiensis\"/201/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes subcrassus\"/202/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontellidae\"/203/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Superodontella\"/204/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenyllodes\"/205/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenyllodes armatus\"/206/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Onychiuridae\"/207/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Detriturus\"/208/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Detriturus jubilarius\"/209/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuteraphorura\"/210/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuteraphorura silvaria\"/211/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura\"/212/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura nova\"/213/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura polonica\"/214/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kalaphorura\"/215/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kalaphorura carpenteri\"/216/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura\"/217/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura armata\"/218/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura aurantiaca\"/219/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura bicampata\"/220/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura campata\"/221/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura cancellata\"/222/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura fimata\"/223/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura subuliginata\"/224/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura tricampata\"/225/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Supraphorura\"/226/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Supraphorura furcifera\"/227/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thalassaphorura\"/228/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thalassaphorura tovtrensis\"/229/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tullbergiidae\"/230/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Karlstejnia\"/231/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Karlstejnia montana\"/232/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesaphorura\"/233/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesaphorura krausbaueri\"/234/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura\"/235/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura affinis\"/236/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura incisa\"/237/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paratullbergia\"/238/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paratullbergia callipygos\"/239/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura\"/240/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura denisi\"/241/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura japygiformis\"/242/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura lubbocki\"/243/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura quadrispina\"/244/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Symphypleona\"/245/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalitidae\"/246/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalites\"/247/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalites caecus\"/248/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites\"/249/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites benitus\"/250/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites secundarius\"/251/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites spinosus\"/252/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiellidae\"/253/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella\"/254/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella arvalis\"/255/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella hortensis\"/256/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella pistilla\"/257/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella radula\"/258/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuterosminthurus\"/259/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuterosminthurus sulphureus\"/260/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus\"/261/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus diffusus\"/262/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus insignis\"/263/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus novemlineatus\"/264/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomidae\"/265/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtoma\"/266/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtoma fusca\"/267/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomina\"/268/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomina minuta\"/269/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Katiannidae\"/270/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gisinianus\"/271/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gisinianus flammeolus\"/272/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus\"/273/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus alpinus\"/274/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus aureus\"/275/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus elegans\"/276/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthuridae\"/277/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma\"/278/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma fusca\"/279/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma gallica\"/280/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lipothrix\"/281/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lipothrix lubbocki\"/282/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus\"/283/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus ghilarovi\"/284/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus viridis\"/285/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurididae\"/286/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides\"/287/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides malmgreni\"/288/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides parvulus\"/289/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides schoetti\"/290/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides signatus\"/291/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia\"/292/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia furcata\"/293/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia leutrensis\"/294/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia pumilis\"/295/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Other Acari\"/296/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesostigmata (Gamase)\"/297/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ascidae\"/298/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius\"/299/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius magnanalis\"/300/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius pristinus\"/301/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca\"/302/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca aphidioides\"/303/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca bicornis\"/304/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leioseius\"/305/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leioseius bicolor\"/306/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconopsis\"/307/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconopsis n. sp.\"/308/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattisociidae\"/309/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius\"/310/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius borealis\"/311/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius curtipes\"/312/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius dungeri\"/313/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius longipes\"/314/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius serratus\"/315/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyseius\"/316/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyseius italicus\"/317/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicriidae\"/318/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius\"/319/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius canestrinii\"/320/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius mollis\"/321/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius n. sp.\"/322/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphididae\"/323/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphis\"/324/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphis ostrinus\"/325/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Loricaseius\"/326/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Loricaseius lepontinus\"/327/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Laelapidae\"/328/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis\"/329/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) aculeifer\"/330/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) angusta\"/331/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) nolli\"/332/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Holostaspis) forcipata\"/333/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Laelaspis) astronomica\"/334/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Pneumolaelaps) sp.\"/335/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis sp.\"/336/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudolaelaps\"/337/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudolaelaps doderoi\"/338/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus\"/339/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus germanicus\"/340/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus placentulus\"/341/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus sellnicki\"/342/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrochelidae\"/343/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis\"/344/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis alpinus\"/345/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis longispinosus\"/346/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis mandibularis\"/347/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles\"/348/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles (Macrholaspis) terreus\"/349/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles (Macrocheles) montanus\"/350/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrocheles\"/351/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrocheles tridentinus\"/352/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelapidae\"/353/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Olopachys\"/354/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Olopachys suecicus\"/355/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus\"/356/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus sculptus\"/357/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus vexillifer\"/358/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps dubius\"/359/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps imitans\"/360/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps longulus\"/361/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps multidentatus\"/362/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps pectinifer\"/363/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps sp.\"/364/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps\"/365/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps troglophilus\"/366/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus\"/367/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus singularis\"/368/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus Pseudopachyseiulus ? n. sp.\"/369/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius\"/370/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius angustiventris\"/371/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius humeralis\"/372/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius subhumeralis\"/373/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitidae\"/374/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus\"/375/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus hamatus\"/376/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus mirabilis\"/377/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus\"/378/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus armatus\"/379/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus celticus\"/380/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus digitulus\"/381/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus finilocatus\"/382/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus humusorum\"/383/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus minorleitnerae\"/384/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus n. sp.\"/385/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus orthogynellus\"/386/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus parrunciger\"/387/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus runcatellus\"/388/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus schweizeri\"/389/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus sp.\"/390/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus truncellus\"/391/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus truncus\"/392/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus vagabundus\"/393/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus wasmanni\"/394/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eugamasus\"/395/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eugamasus berlesei\"/396/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus\"/397/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus calcaratus\"/398/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus n. sp.\"/399/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus rotulifer\"/400/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus sp.\"/401/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus stramenti\"/402/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holzmannia\"/403/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holzmannia (Juvaria) n. sp.\"/404/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus\"/405/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus alstoni\"/406/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus oxygynelloides\"/407/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus sp.\"/408/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus suecicus\"/409/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus\"/410/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus furcatus\"/411/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus halophilus\"/412/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus lunulatus\"/413/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus\"/414/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus crassipes\"/415/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus longicornis\"/416/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus primorellus\"/417/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus quisquiliarum\"/418/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tanygamasus\"/419/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tanygamasus sp.\"/420/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus\"/421/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus kraepelini\"/422/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus sp.\"/423/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phytoseiidae\"/424/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius\"/425/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius longulus\"/426/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius neobernhardi\"/427/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius obtusus\"/428/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinidae\"/429/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinum\"/430/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinum pacificum\"/431/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacaridae\"/432/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gamasellus\"/433/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gamasellus falciger\"/434/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctodendrolaelaps\"/435/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctodendrolaelaps rotundus\"/436/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus\"/437/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus aequalis\"/438/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus calcarulatus\"/439/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus coronatus\"/440/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaiidae\"/441/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia\"/442/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia cerva\"/443/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia nemorensis\"/444/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia planicola\"/445/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia transisalae\"/446/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconidae\"/447/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parazercon\"/448/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parazercon radiatus\"/449/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon\"/450/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon fimbriatus\"/451/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon n. sp.\"/452/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon sellnicki\"/453/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon\"/454/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon badensis\"/455/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon berlesei\"/456/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon fageticola\"/457/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon gurensis\"/458/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon lischanni\"/459/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon peltatus\"/460/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon romagniolus\"/461/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon vacuus\"/462/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sarcoptiformes (Oribate)\"/463/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteriidae\"/464/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria\"/465/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria coleoptrata\"/466/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria nitens\"/467/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parachipteria\"/468/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parachipteria willmanni\"/469/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Astegistidae\"/470/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cultroribula\"/471/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cultroribula bicultrata\"/472/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Furcoribula\"/473/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Furcoribula furcillata\"/474/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Autognetidae\"/475/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Conchogneta\"/476/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Conchogneta dalecarlica\"/477/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belbodamaeidae\"/478/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hungarobelba\"/479/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hungarobelba pyrenaica\"/480/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Porobelba\"/481/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Porobelba spinosa\"/482/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachychthoniidae\"/483/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius\"/484/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius hystricinus\"/485/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius lapponicus\"/486/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius muscorum\"/487/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius neglectus\"/488/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius sellnicki\"/489/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius strenzkei\"/490/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius tuxeni\"/491/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poecilochthonius\"/492/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poecilochthonius spiciger\"/493/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius\"/494/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius formosus\"/495/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius hungaricus\"/496/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius immaculatus\"/497/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius suecicus\"/498/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeidae\"/499/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeus\"/500/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeus monilipes\"/501/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisiidae\"/502/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisia\"/503/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisia horrida\"/504/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heminothrus\"/505/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heminothrus targionii\"/506/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus\"/507/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus peltifer\"/508/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus thori\"/509/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodidae\"/510/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes\"/511/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes coriaceus\"/512/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes labyrinthicus\"/513/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes marginatus\"/514/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes ornatus\"/515/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes reticulatus\"/516/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes rugosior\"/517/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes schatzi\"/518/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes tenuis\"/519/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontocepheus\"/520/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontocepheus elongatus\"/521/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheidae\"/522/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheus\"/523/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheus cepheiformis\"/524/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tritegeus\"/525/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tritegeus bisulcatus\"/526/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetidae\"/527/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes\"/528/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes gracilis\"/529/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes mediocris\"/530/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes minimus\"/531/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes peritus\"/532/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes psammophilus\"/533/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes thienemanni\"/534/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Edwardzetes\"/535/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Edwardzetes edwardsi\"/536/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes\"/537/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes fuscipes\"/538/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes setosus\"/539/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes tatricus\"/540/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Melanozetes\"/541/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Melanozetes mollicomus\"/542/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oromurcia\"/543/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oromurcia sudetica\"/544/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaerozetes\"/545/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaerozetes orbicularis\"/546/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates\"/547/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates incisellus\"/548/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates trimaculatus\"/549/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobatidae\"/550/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates\"/551/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates borealis\"/552/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates cuspidatus\"/553/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates voigtsi\"/554/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelbidae\"/555/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelba\"/556/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelba pectinigera\"/557/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeidae\"/558/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeus\"/559/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeus cymba\"/560/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeidae\"/561/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belba\"/562/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belba bartosi\"/563/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caenobelba\"/564/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caenobelba montana\"/565/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeobelba\"/566/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeobelba minutissima\"/567/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus\"/568/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus (Adamaeus) onustus\"/569/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus (Paradamaeus) clavipes\"/570/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus crispatus\"/571/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus riparius\"/572/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kunstidamaeus\"/573/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kunstidamaeus tecticola\"/574/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metabelba\"/575/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metabelba propexa\"/576/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolidae\"/577/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolus\"/578/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolus asperatus\"/579/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fosseremus\"/580/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fosseremus laciniatus\"/581/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthoniidae\"/582/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthonius\"/583/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthonius minutissimus\"/584/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmanniidae\"/585/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia\"/586/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia minima\"/587/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia styriaca\"/588/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmanniidae\"/589/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmannia\"/590/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmannia ribagai\"/591/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracaridae\"/592/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia\"/593/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia ardua\"/594/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia duplicata\"/595/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetidae\"/596/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetes\"/597/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetes globulus\"/598/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumnidae\"/599/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrogalumna\"/600/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrogalumna longipluma\"/601/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna\"/602/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna lanceata\"/603/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna obvia\"/604/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna\"/605/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna altera\"/606/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna nervosa\"/607/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pilogalumna\"/608/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pilogalumna tenuiclava\"/609/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeidae\"/610/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeus\"/611/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeus bicostatus\"/612/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Haplozetidae\"/613/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloribates\"/614/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloribates longipilosus\"/615/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protoribates\"/616/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protoribates capucinus\"/617/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermanniidae\"/618/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermannia\"/619/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermannia gibba\"/620/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthoniidae\"/621/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius\"/622/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius luteus\"/623/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius rufulus\"/624/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacaridae\"/625/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Adoristes\"/626/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Adoristes ovatus\"/627/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dorycranosus\"/628/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dorycranosus acutus\"/629/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus\"/630/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus coracinus\"/631/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus subterraneus\"/632/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus\"/633/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus discrepans\"/634/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus salamoni\"/635/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus tegeocranus\"/636/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeidae\"/637/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeus\"/638/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeus pulcherrimus\"/639/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetidae\"/640/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetes\"/641/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetes ciliatus\"/642/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuellidae\"/643/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuella\"/644/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuella bilineata\"/645/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothridae\"/646/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothrus\"/647/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothrus monodactylus\"/648/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trimalaconothrus\"/649/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trimalaconothrus foveolatus\"/650/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetidae\"/651/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetes\"/652/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetes petrocoriensis\"/653/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobatidae\"/654/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes\"/655/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes pseudofusiger\"/656/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes semirufus\"/657/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobates\"/658/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobates parmeliae\"/659/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates\"/660/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates punctum\"/661/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates sellnicki\"/662/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zachvatkinibates\"/663/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zachvatkinibates (Alpizetes) perlongus\"/664/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermanniidae\"/665/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia\"/666/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia comitalis\"/667/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia coronata\"/668/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia elegantula\"/669/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia nana\"/670/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia sellnicki\"/671/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoliodidae\"/672/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyliodes\"/673/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyliodes scaliger\"/674/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothridae\"/675/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus\"/676/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus anauniensis\"/677/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus borussicus\"/678/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus palustris\"/679/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus pratensis\"/680/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus silvestris\"/681/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiidae\"/682/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella\"/683/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella bicarinata\"/684/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella conjucta\"/685/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella hauseri\"/686/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina\"/687/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina ornata\"/688/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina signata\"/689/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microppia\"/690/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microppia minus\"/691/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia\"/692/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia (Confinoppia) confinis tenuiseta\"/693/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia confinis\"/694/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella\"/695/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Moritzoppia) keilbachi\"/696/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Moritzoppia) unicarinata\"/697/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) falcata\"/698/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) nova\"/699/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) propinqua\"/700/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) uliginosa\"/701/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Rhinoppia) obsoleta\"/702/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Rhinoppia) subpectinata\"/703/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ramusella\"/704/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ramusella insculpta\"/705/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Subiasella\"/706/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Subiasella quadrimaculata\"/707/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatellidae\"/708/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ophidiotricus\"/709/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ophidiotricus vindobodensis\"/710/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatella\"/711/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatella calcarata\"/712/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula\"/713/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula amblyptera\"/714/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula interrupta\"/715/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula longelamellata\"/716/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula tibialis\"/717/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zygoribatula\"/718/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zygoribatula exilis\"/719/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Palaeacaridae\"/720/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paleacarus\"/721/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paleacarus hystricinus\"/722/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parakalummidae\"/723/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoribates\"/724/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoribates aurantiacus\"/725/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetidae\"/726/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes\"/727/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes africanus\"/728/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes intermedius\"/729/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes perforatus\"/730/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloppiidae\"/731/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia\"/732/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia bipilis\"/733/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia sexpilosa\"/734/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phenopelopidae\"/735/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops\"/736/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops acromios\"/737/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops occultus\"/738/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops plicatus\"/739/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops subuliger\"/740/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops tardus\"/741/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops torulosus\"/742/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloptulus\"/743/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloptulus phaenotus\"/744/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracaridae\"/745/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracarus\"/746/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracarus cribrarius\"/747/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hoplophthiracarus\"/748/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hoplophthiracarus illinoisensis\"/749/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus\"/750/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus boresetosus\"/751/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus ferrugineus\"/752/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus globosus\"/753/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus laevigatus\"/754/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus lentulus\"/755/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus longulus\"/756/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus nitens\"/757/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus peristomaticus\"/758/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus sp.\"/759/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus\"/760/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Atropacarus) striculus\"/761/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) applicatus\"/762/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) herculeanus\"/763/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) magnus (forma magna)\"/764/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) sp.\"/765/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) spinosus\"/766/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) vernaculus\"/767/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Tropacarus) carinatus (forma carinata)\"/768/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus herculeanus\"/769/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus hirsutus\"/770/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus sp.\"/771/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiidae\"/772/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia\"/773/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia hammerae\"/774/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia longisetosa\"/775/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia maritalis\"/776/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia monstruosa\"/777/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia quadricarinata\"/778/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribatidae\"/779/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia\"/780/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia humerata\"/781/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia pannonica\"/782/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates\"/783/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Hemileius) initialis\"/784/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) labyrinthicus\"/785/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) laevigatus\"/786/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) pallidulus\"/787/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) quintus\"/788/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Topobates) helveticus\"/789/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates labyrinthicus\"/790/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutoverticidae\"/791/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutovertex\"/792/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutovertex minutus\"/793/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbidae\"/794/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allosuctobelba\"/795/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allosuctobelba ornithorhyncha\"/796/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba\"/797/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba altvateri\"/798/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba atomaria\"/799/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba secta\"/800/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba trigona\"/801/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella\"/802/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella acutidens\"/803/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella alloenasuta\"/804/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella arcana\"/805/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella baloghi\"/806/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella diffissa\"/807/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella falcata\"/808/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella forsslundi\"/809/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella nasalis\"/810/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella palustris\"/811/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella perforata\"/812/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella sarekensis\"/813/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella similis\"/814/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella subcornigera\"/815/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella subtrigona\"/816/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheidae\"/817/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus\"/818/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus minor\"/819/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus alatus\"/820/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus sarekensis\"/821/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus velatus\"/822/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tegoribatidae\"/823/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidozetes\"/824/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidozetes singularis\"/825/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thyrisomidae\"/826/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pantelozetes\"/827/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pantelozetes paolii\"/828/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthoniidae\"/829/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthonius\"/830/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthonius tectorum\"/831/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimidae\"/832/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimus\"/833/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimus furcatus\"/834/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestidae\"/835/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetorchestes\"/836/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetorchestes emeryi\"/837/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestes\"/838/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestes falzonni\"/839/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Coleoptera larva\"/840/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Other larva\"/841/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidoptera\"/842/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidoptera larva\"/843/g' {} +

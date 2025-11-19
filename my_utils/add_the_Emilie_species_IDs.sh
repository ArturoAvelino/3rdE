# ADD the species IDs using the latest label tree
# provided by Emilie on 25 sept 2025.
#
# To run this script, in a terminal go where the files are located
# and the type:
#     bash thisfile.sh

# Add the header column of the species ID:
find . -type f -name "*.csv" -exec sed -i '' 's/label_id/label_id,class/g' {} +

# Add the species ID's:
find . -type f -name "*.csv" -exec sed -i '' 's/\"Unclassified\"/1,\"Unclassified\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dirt\"/2,\"Dirt\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metazoa\"/3,\"Metazoa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arachnida\"/4,\"Arachnida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acari\"/5,\"Acari\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Araneae +5mm\"/6,\"Araneae +5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Araneae -5mm\"/7,\"Araneae -5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoscorpiones\"/8,\"Pseudoscorpiones\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Opiliones\"/9,\"Opiliones\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Palpigradi\"/10,\"Palpigradi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Crustacea\"/11,\"Crustacea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isopoda\"/12,\"Isopoda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Myriapoda\"/13,\"Myriapoda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplopoda +5mm\"/14,\"Diplopoda +5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplopoda -5mm\"/15,\"Diplopoda -5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chilopoda +5mm\"/16,\"Chilopoda +5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chilopoda -5mm\"/17,\"Chilopoda -5mm\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Symphyla\"/18,\"Symphyla\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pauropoda\"/19,\"Pauropoda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hexapoda\"/20,\"Hexapoda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diplura\"/21,\"Diplura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protura\"/22,\"Protura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Collembola\"/23,\"Collembola\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Insecta\"/24,\"Insecta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Coleoptera\"/25,\"Coleoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diptera adult\"/26,\"Diptera adult\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Diptera larva\"/27,\"Diptera larva\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenoptera\"/28,\"Hymenoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenoptera Formicidae\"/29,\"Hymenoptera Formicidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hemiptera\"/30,\"Hemiptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Psocoptera\"/31,\"Psocoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thysanoptera\"/32,\"Thysanoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Embioptera\"/33,\"Embioptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dermaptera\"/34,\"Dermaptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Campodeoidea\"/35,\"Campodeoidea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Japygoidea\"/36,\"Japygoidea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattodea\"/37,\"Blattodea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Corydiidae\"/38,\"Corydiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isoptera\"/39,\"Isoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattidae\"/40,\"Blattidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orthoptera\"/41,\"Orthoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cantharidae\"/42,\"Cantharidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabidae\"/43,\"Carabidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Curculionidae\"/44,\"Curculionidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Elateridae\"/45,\"Elateridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scarabaeidae\"/46,\"Scarabaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Silphidae\"/47,\"Silphidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Staphylinidae\"/48,\"Staphylinidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tenebrionidae\"/49,\"Tenebrionidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Auchenorrhyncha\"/50,\"Auchenorrhyncha\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteroptera\"/51,\"Heteroptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sternorrhyncha\"/52,\"Sternorrhyncha\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobryomorpha\"/53,\"Entomobryomorpha\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobryidae\"/54,\"Entomobryidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya\"/55,\"Entomobrya\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya lanuginosa\"/56,\"Entomobrya lanuginosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Entomobrya nivalis\"/57,\"Entomobrya nivalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus\"/58,\"Lepidocyrtus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus curvicollis\"/59,\"Lepidocyrtus curvicollis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus cyaneus\"/60,\"Lepidocyrtus cyaneus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus lignorum\"/61,\"Lepidocyrtus lignorum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidocyrtus violaceus\"/62,\"Lepidocyrtus violaceus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella\"/63,\"Pseudosinella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella alba\"/64,\"Pseudosinella alba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudosinella anderseni\"/65,\"Pseudosinella anderseni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomidae\"/66,\"Isotomidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurophorus\"/67,\"Anurophorus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurophorus alpinus\"/68,\"Anurophorus alpinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ballistura\"/69,\"Ballistura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ballistura borealis\"/70,\"Ballistura borealis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria\"/71,\"Desoria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria nivalis\"/72,\"Desoria nivalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Desoria tadzhika\"/73,\"Desoria tadzhika\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia\"/74,\"Folsomia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia bisetosa\"/75,\"Folsomia bisetosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia candida\"/76,\"Folsomia candida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia decemoculata\"/77,\"Folsomia decemoculata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia dovrensis\"/78,\"Folsomia dovrensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia inoculata\"/79,\"Folsomia inoculata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia manolachei\"/80,\"Folsomia manolachei\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia palaearctica\"/81,\"Folsomia palaearctica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia penicula\"/82,\"Folsomia penicula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia quadrioculata\"/83,\"Folsomia quadrioculata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomia spinosa\"/84,\"Folsomia spinosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomides\"/85,\"Folsomides\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Folsomides aylloensis\"/86,\"Folsomides aylloensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma\"/87,\"Isotoma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma anglicana\"/88,\"Isotoma anglicana\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma caerulea\"/89,\"Isotoma caerulea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotoma viridis\"/90,\"Isotoma viridis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella\"/91,\"Isotomiella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella minor\"/92,\"Isotomiella minor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomiella paraminor\"/93,\"Isotomiella paraminor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus\"/94,\"Isotomurus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus cassagnaui\"/95,\"Isotomurus cassagnaui\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus graminis\"/96,\"Isotomurus graminis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus palustris\"/97,\"Isotomurus palustris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Isotomurus punctiferus\"/98,\"Isotomurus punctiferus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma\"/99,\"Parisotoma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma agrelli\"/100,\"Parisotoma agrelli\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parisotoma notabilis\"/101,\"Parisotoma notabilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Proisotoma\"/102,\"Proisotoma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus\"/103,\"Pseudanurophorus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus binoculatus\"/104,\"Pseudanurophorus binoculatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudanurophorus quadrioculatus\"/105,\"Pseudanurophorus quadrioculatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma\"/106,\"Pseudisotoma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma monochaeta\"/107,\"Pseudisotoma monochaeta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudisotoma sensibilis\"/108,\"Pseudisotoma sensibilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella\"/109,\"Tetracanthella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella gallica\"/110,\"Tetracanthella gallica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tetracanthella schalleri\"/111,\"Tetracanthella schalleri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus\"/112,\"Vertagopus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus asiaticus\"/113,\"Vertagopus asiaticus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vertagopus ciliatus\"/114,\"Vertagopus ciliatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopoduridae\"/115,\"Oncopoduridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopodura\"/116,\"Oncopodura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oncopodura crassicornis\"/117,\"Oncopodura crassicornis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesellidae\"/118,\"Orchesellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteromurus\"/119,\"Heteromurus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heteromurus nitidus\"/120,\"Heteromurus nitidus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella\"/121,\"Orchesella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella bifasciata\"/122,\"Orchesella bifasciata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella quinquefasciata\"/123,\"Orchesella quinquefasciata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orchesella villosa\"/124,\"Orchesella villosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paronellidae\"/125,\"Paronellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cyphoderus\"/126,\"Cyphoderus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cyphoderus albinus\"/127,\"Cyphoderus albinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomoceridae\"/128,\"Tomoceridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pogonognathellus\"/129,\"Pogonognathellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pogonognathellus flavescens\"/130,\"Pogonognathellus flavescens\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerina\"/131,\"Tomocerina\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerina varia\"/132,\"Tomocerina varia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus\"/133,\"Tomocerus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus minor\"/134,\"Tomocerus minor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tomocerus vulgaris\"/135,\"Tomocerus vulgaris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelipleona\"/136,\"Neelipleona\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelidae\"/137,\"Neelidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax\"/138,\"Megalothorax\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax minimus\"/139,\"Megalothorax minimus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Megalothorax willemi\"/140,\"Megalothorax willemi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelides\"/141,\"Neelides\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelides minutus\"/142,\"Neelides minutus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelus\"/143,\"Neelus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neelus murinus\"/144,\"Neelus murinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poduromorpha\"/145,\"Poduromorpha\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomellidae\"/146,\"Brachystomellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella\"/147,\"Brachystomella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella curvula\"/148,\"Brachystomella curvula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachystomella parvula\"/149,\"Brachystomella parvula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastruridae\"/150,\"Hypogastruridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella\"/151,\"Ceratophysella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella armata\"/152,\"Ceratophysella armata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella denticulata\"/153,\"Ceratophysella denticulata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella gibbosa\"/154,\"Ceratophysella gibbosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella impedita\"/155,\"Ceratophysella impedita\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella laricis\"/156,\"Ceratophysella laricis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratophysella stercoraria\"/157,\"Ceratophysella stercoraria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Choreutinula\"/158,\"Choreutinula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Choreutinula inermis\"/159,\"Choreutinula inermis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura\"/160,\"Hypogastrura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura crassaegranulata\"/161,\"Hypogastrura crassaegranulata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura serrata\"/162,\"Hypogastrura serrata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypogastrura socialis\"/163,\"Hypogastrura socialis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura\"/164,\"Orogastrura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura pallida\"/165,\"Orogastrura pallida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Orogastrura parva\"/166,\"Orogastrura parva\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schaefferia\"/167,\"Schaefferia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schaefferia emucronata\"/168,\"Schaefferia emucronata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schoettella\"/169,\"Schoettella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Schoettella ununguiculata\"/170,\"Schoettella ununguiculata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia\"/171,\"Willemia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia anophthalma\"/172,\"Willemia anophthalma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia densi\"/173,\"Willemia densi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Willemia  anophthalma\"/174,\"Willemia  anophthalma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla\"/175,\"Xenylla\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla acauda\"/176,\"Xenylla acauda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenylla brevicauda\"/177,\"Xenylla brevicauda\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanuridae\"/178,\"Neanuridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurida\"/179,\"Anurida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anurida granaria\"/180,\"Anurida granaria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea\"/181,\"Friesea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea albida\"/182,\"Friesea albida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea atypica\"/183,\"Friesea atypica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea emucronata\"/184,\"Friesea emucronata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea inermis\"/185,\"Friesea inermis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea mirabilis\"/186,\"Friesea mirabilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea pseudodecipiens\"/187,\"Friesea pseudodecipiens\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea truncata\"/188,\"Friesea truncata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Friesea villanuevai\"/189,\"Friesea villanuevai\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida\"/190,\"Micranurida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida anophthalmica\"/191,\"Micranurida anophthalmica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Micranurida pygmaea\"/192,\"Micranurida pygmaea\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanura\"/193,\"Neanura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neanura muscorum\"/194,\"Neanura muscorum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina\"/195,\"Pseudachorudina\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina angelieri\"/196,\"Pseudachorudina angelieri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorudina meridionalis\"/197,\"Pseudachorudina meridionalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes\"/198,\"Pseudachorutes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes dubius\"/199,\"Pseudachorutes dubius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes minor\"/200,\"Pseudachorutes minor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes palmiensis\"/201,\"Pseudachorutes palmiensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudachorutes subcrassus\"/202,\"Pseudachorutes subcrassus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontellidae\"/203,\"Odontellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Superodontella\"/204,\"Superodontella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenyllodes\"/205,\"Xenyllodes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenyllodes armatus\"/206,\"Xenyllodes armatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Onychiuridae\"/207,\"Onychiuridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Detriturus\"/208,\"Detriturus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Detriturus jubilarius\"/209,\"Detriturus jubilarius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuteraphorura\"/210,\"Deuteraphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuteraphorura silvaria\"/211,\"Deuteraphorura silvaria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura\"/212,\"Hymenaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura nova\"/213,\"Hymenaphorura nova\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hymenaphorura polonica\"/214,\"Hymenaphorura polonica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kalaphorura\"/215,\"Kalaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kalaphorura carpenteri\"/216,\"Kalaphorura carpenteri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura\"/217,\"Protaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura armata\"/218,\"Protaphorura armata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura aurantiaca\"/219,\"Protaphorura aurantiaca\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura bicampata\"/220,\"Protaphorura bicampata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura campata\"/221,\"Protaphorura campata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura cancellata\"/222,\"Protaphorura cancellata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura fimata\"/223,\"Protaphorura fimata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura subuliginata\"/224,\"Protaphorura subuliginata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protaphorura tricampata\"/225,\"Protaphorura tricampata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Supraphorura\"/226,\"Supraphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Supraphorura furcifera\"/227,\"Supraphorura furcifera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thalassaphorura\"/228,\"Thalassaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thalassaphorura tovtrensis\"/229,\"Thalassaphorura tovtrensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tullbergiidae\"/230,\"Tullbergiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Karlstejnia\"/231,\"Karlstejnia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Karlstejnia montana\"/232,\"Karlstejnia montana\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesaphorura\"/233,\"Mesaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesaphorura krausbaueri\"/234,\"Mesaphorura krausbaueri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura\"/235,\"Metaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura affinis\"/236,\"Metaphorura affinis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metaphorura incisa\"/237,\"Metaphorura incisa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paratullbergia\"/238,\"Paratullbergia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paratullbergia callipygos\"/239,\"Paratullbergia callipygos\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura\"/240,\"Stenaphorura\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura denisi\"/241,\"Stenaphorura denisi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura japygiformis\"/242,\"Stenaphorura japygiformis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura lubbocki\"/243,\"Stenaphorura lubbocki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Stenaphorura quadrispina\"/244,\"Stenaphorura quadrispina\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Symphypleona\"/245,\"Symphypleona\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalitidae\"/246,\"Arrhopalitidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalites\"/247,\"Arrhopalites\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arrhopalites caecus\"/248,\"Arrhopalites caecus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites\"/249,\"Pygmarrhopalites\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites benitus\"/250,\"Pygmarrhopalites benitus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites secundarius\"/251,\"Pygmarrhopalites secundarius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pygmarrhopalites spinosus\"/252,\"Pygmarrhopalites spinosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiellidae\"/253,\"Bourletiellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella\"/254,\"Bourletiella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella arvalis\"/255,\"Bourletiella arvalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella hortensis\"/256,\"Bourletiella hortensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella pistilla\"/257,\"Bourletiella pistilla\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Bourletiella radula\"/258,\"Bourletiella radula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuterosminthurus\"/259,\"Deuterosminthurus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Deuterosminthurus sulphureus\"/260,\"Deuterosminthurus sulphureus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus\"/261,\"Heterosminthurus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus diffusus\"/262,\"Heterosminthurus diffusus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus insignis\"/263,\"Heterosminthurus insignis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heterosminthurus novemlineatus\"/264,\"Heterosminthurus novemlineatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomidae\"/265,\"Dicyrtomidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtoma\"/266,\"Dicyrtoma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtoma fusca\"/267,\"Dicyrtoma fusca\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomina\"/268,\"Dicyrtomina\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dicyrtomina minuta\"/269,\"Dicyrtomina minuta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Katiannidae\"/270,\"Katiannidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gisinianus\"/271,\"Gisinianus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gisinianus flammeolus\"/272,\"Gisinianus flammeolus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus\"/273,\"Sminthurinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus alpinus\"/274,\"Sminthurinus alpinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus aureus\"/275,\"Sminthurinus aureus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurinus elegans\"/276,\"Sminthurinus elegans\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthuridae\"/277,\"Sminthuridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma\"/278,\"Allacma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma fusca\"/279,\"Allacma fusca\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allacma gallica\"/280,\"Allacma gallica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lipothrix\"/281,\"Lipothrix\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lipothrix lubbocki\"/282,\"Lipothrix lubbocki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus\"/283,\"Sminthurus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus ghilarovi\"/284,\"Sminthurus ghilarovi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurus viridis\"/285,\"Sminthurus viridis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurididae\"/286,\"Sminthurididae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides\"/287,\"Sminthurides\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides malmgreni\"/288,\"Sminthurides malmgreni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides parvulus\"/289,\"Sminthurides parvulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides schoetti\"/290,\"Sminthurides schoetti\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sminthurides signatus\"/291,\"Sminthurides signatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia\"/292,\"Sphaeridia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia furcata\"/293,\"Sphaeridia furcata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia leutrensis\"/294,\"Sphaeridia leutrensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaeridia pumilis\"/295,\"Sphaeridia pumilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Other Acari\"/296,\"Other Acari\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mesostigmata (Gamase)\"/297,\"Mesostigmata (Gamase)\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ascidae\"/298,\"Ascidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius\"/299,\"Arctoseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius magnanalis\"/300,\"Arctoseius magnanalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Arctoseius pristinus\"/301,\"Arctoseius pristinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca\"/302,\"Asca\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca aphidioides\"/303,\"Asca aphidioides\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Asca bicornis\"/304,\"Asca bicornis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leioseius\"/305,\"Leioseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leioseius bicolor\"/306,\"Leioseius bicolor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconopsis\"/307,\"Zerconopsis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconopsis n. sp.\"/308,\"Zerconopsis n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Blattisociidae\"/309,\"Blattisociidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius\"/310,\"Cheiroseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius borealis\"/311,\"Cheiroseius borealis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius curtipes\"/312,\"Cheiroseius curtipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius dungeri\"/313,\"Cheiroseius dungeri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius longipes\"/314,\"Cheiroseius longipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cheiroseius serratus\"/315,\"Cheiroseius serratus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyseius\"/316,\"Platyseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyseius italicus\"/317,\"Platyseius italicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicriidae\"/318,\"Epicriidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius\"/319,\"Epicrius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius canestrinii\"/320,\"Epicrius canestrinii\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius mollis\"/321,\"Epicrius mollis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epicrius n. sp.\"/322,\"Epicrius n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphididae\"/323,\"Eviphididae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphis\"/324,\"Eviphis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eviphis ostrinus\"/325,\"Eviphis ostrinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Loricaseius\"/326,\"Loricaseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Loricaseius lepontinus\"/327,\"Loricaseius lepontinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Laelapidae\"/328,\"Laelapidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis\"/329,\"Hypoaspis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) aculeifer\"/330,\"Hypoaspis (Geolaelaps) aculeifer\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) angusta\"/331,\"Hypoaspis (Geolaelaps) angusta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Geolaelaps) nolli\"/332,\"Hypoaspis (Geolaelaps) nolli\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Holostaspis) forcipata\"/333,\"Hypoaspis (Holostaspis) forcipata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Laelaspis) astronomica\"/334,\"Hypoaspis (Laelaspis) astronomica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis (Pneumolaelaps) sp.\"/335,\"Hypoaspis (Pneumolaelaps) sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypoaspis sp.\"/336,\"Hypoaspis sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudolaelaps\"/337,\"Pseudolaelaps\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudolaelaps doderoi\"/338,\"Pseudolaelaps doderoi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus\"/339,\"Pseudoparasitus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus germanicus\"/340,\"Pseudoparasitus germanicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus placentulus\"/341,\"Pseudoparasitus placentulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pseudoparasitus sellnicki\"/342,\"Pseudoparasitus sellnicki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrochelidae\"/343,\"Macrochelidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis\"/344,\"Geholaspis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis alpinus\"/345,\"Geholaspis alpinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis longispinosus\"/346,\"Geholaspis longispinosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Geholaspis mandibularis\"/347,\"Geholaspis mandibularis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles\"/348,\"Machrocheles\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles (Macrholaspis) terreus\"/349,\"Machrocheles (Macrholaspis) terreus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machrocheles (Macrocheles) montanus\"/350,\"Machrocheles (Macrocheles) montanus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrocheles\"/351,\"Macrocheles\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Macrocheles tridentinus\"/352,\"Macrocheles tridentinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelapidae\"/353,\"Pachylaelapidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Olopachys\"/354,\"Olopachys\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Olopachys suecicus\"/355,\"Olopachys suecicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus\"/356,\"Pachydellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus sculptus\"/357,\"Pachydellus sculptus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachydellus vexillifer\"/358,\"Pachydellus vexillifer\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps dubius\"/359,\"Pachylaelaps dubius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps imitans\"/360,\"Pachylaelaps imitans\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps longulus\"/361,\"Pachylaelaps longulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps multidentatus\"/362,\"Pachylaelaps multidentatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps pectinifer\"/363,\"Pachylaelaps pectinifer\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps sp.\"/364,\"Pachylaelaps sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps\"/365,\"Pachylaelaps\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachylaelaps troglophilus\"/366,\"Pachylaelaps troglophilus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus\"/367,\"Pachyseiulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus singularis\"/368,\"Pachyseiulus singularis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseiulus Pseudopachyseiulus ? n. sp.\"/369,\"Pachyseiulus Pseudopachyseiulus ? n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius\"/370,\"Pachyseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius angustiventris\"/371,\"Pachyseius angustiventris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius humeralis\"/372,\"Pachyseius humeralis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pachyseius subhumeralis\"/373,\"Pachyseius subhumeralis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitidae\"/374,\"Parasitidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus\"/375,\"Amblygamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus hamatus\"/376,\"Amblygamasus hamatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblygamasus mirabilis\"/377,\"Amblygamasus mirabilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus\"/378,\"Anidogamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus armatus\"/379,\"Anidogamasus armatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus celticus\"/380,\"Anidogamasus celticus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus digitulus\"/381,\"Anidogamasus digitulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus finilocatus\"/382,\"Anidogamasus finilocatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus humusorum\"/383,\"Anidogamasus humusorum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus minorleitnerae\"/384,\"Anidogamasus minorleitnerae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus n. sp.\"/385,\"Anidogamasus n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus orthogynellus\"/386,\"Anidogamasus orthogynellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus parrunciger\"/387,\"Anidogamasus parrunciger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus runcatellus\"/388,\"Anidogamasus runcatellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus schweizeri\"/389,\"Anidogamasus schweizeri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus sp.\"/390,\"Anidogamasus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus truncellus\"/391,\"Anidogamasus truncellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus truncus\"/392,\"Anidogamasus truncus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus vagabundus\"/393,\"Anidogamasus vagabundus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Anidogamasus wasmanni\"/394,\"Anidogamasus wasmanni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eugamasus\"/395,\"Eugamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eugamasus berlesei\"/396,\"Eugamasus berlesei\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus\"/397,\"Holoparasitus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus calcaratus\"/398,\"Holoparasitus calcaratus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus n. sp.\"/399,\"Holoparasitus n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus rotulifer\"/400,\"Holoparasitus rotulifer\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus sp.\"/401,\"Holoparasitus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holoparasitus stramenti\"/402,\"Holoparasitus stramenti\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holzmannia\"/403,\"Holzmannia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Holzmannia (Juvaria) n. sp.\"/404,\"Holzmannia (Juvaria) n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus\"/405,\"Leptogamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus alstoni\"/406,\"Leptogamasus alstoni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus oxygynelloides\"/407,\"Leptogamasus oxygynelloides\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus sp.\"/408,\"Leptogamasus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Leptogamasus suecicus\"/409,\"Leptogamasus suecicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus\"/410,\"Parasitus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus furcatus\"/411,\"Parasitus furcatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus halophilus\"/412,\"Parasitus halophilus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parasitus lunulatus\"/413,\"Parasitus lunulatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus\"/414,\"Pergamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus crassipes\"/415,\"Pergamasus crassipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus longicornis\"/416,\"Pergamasus longicornis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus primorellus\"/417,\"Pergamasus primorellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergamasus quisquiliarum\"/418,\"Pergamasus quisquiliarum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tanygamasus\"/419,\"Tanygamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tanygamasus sp.\"/420,\"Tanygamasus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus\"/421,\"Vulgarogamasus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus kraepelini\"/422,\"Vulgarogamasus kraepelini\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Vulgarogamasus sp.\"/423,\"Vulgarogamasus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phytoseiidae\"/424,\"Phytoseiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius\"/425,\"Amblyseius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius longulus\"/426,\"Amblyseius longulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius neobernhardi\"/427,\"Amblyseius neobernhardi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Amblyseius obtusus\"/428,\"Amblyseius obtusus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinidae\"/429,\"Podocinidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinum\"/430,\"Podocinum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Podocinum pacificum\"/431,\"Podocinum pacificum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacaridae\"/432,\"Rhodacaridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gamasellus\"/433,\"Gamasellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gamasellus falciger\"/434,\"Gamasellus falciger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctodendrolaelaps\"/435,\"Punctodendrolaelaps\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctodendrolaelaps rotundus\"/436,\"Punctodendrolaelaps rotundus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus\"/437,\"Rhodacarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus aequalis\"/438,\"Rhodacarus aequalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus calcarulatus\"/439,\"Rhodacarus calcarulatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Rhodacarus coronatus\"/440,\"Rhodacarus coronatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaiidae\"/441,\"Veigaiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia\"/442,\"Veigaia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia cerva\"/443,\"Veigaia cerva\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia nemorensis\"/444,\"Veigaia nemorensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia planicola\"/445,\"Veigaia planicola\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Veigaia transisalae\"/446,\"Veigaia transisalae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zerconidae\"/447,\"Zerconidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parazercon\"/448,\"Parazercon\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parazercon radiatus\"/449,\"Parazercon radiatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon\"/450,\"Prozercon\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon fimbriatus\"/451,\"Prozercon fimbriatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon n. sp.\"/452,\"Prozercon n. sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Prozercon sellnicki\"/453,\"Prozercon sellnicki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon\"/454,\"Zercon\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon badensis\"/455,\"Zercon badensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon berlesei\"/456,\"Zercon berlesei\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon fageticola\"/457,\"Zercon fageticola\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon gurensis\"/458,\"Zercon gurensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon lischanni\"/459,\"Zercon lischanni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon peltatus\"/460,\"Zercon peltatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon romagniolus\"/461,\"Zercon romagniolus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zercon vacuus\"/462,\"Zercon vacuus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sarcoptiformes (Oribate)\"/463,\"Sarcoptiformes (Oribate)\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteriidae\"/464,\"Achipteriidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria\"/465,\"Achipteria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria coleoptrata\"/466,\"Achipteria coleoptrata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Achipteria nitens\"/467,\"Achipteria nitens\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parachipteria\"/468,\"Parachipteria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parachipteria willmanni\"/469,\"Parachipteria willmanni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Astegistidae\"/470,\"Astegistidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cultroribula\"/471,\"Cultroribula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cultroribula bicultrata\"/472,\"Cultroribula bicultrata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Furcoribula\"/473,\"Furcoribula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Furcoribula furcillata\"/474,\"Furcoribula furcillata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Autognetidae\"/475,\"Autognetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Conchogneta\"/476,\"Conchogneta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Conchogneta dalecarlica\"/477,\"Conchogneta dalecarlica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belbodamaeidae\"/478,\"Belbodamaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hungarobelba\"/479,\"Hungarobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hungarobelba pyrenaica\"/480,\"Hungarobelba pyrenaica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Porobelba\"/481,\"Porobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Porobelba spinosa\"/482,\"Porobelba spinosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Brachychthoniidae\"/483,\"Brachychthoniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius\"/484,\"Liochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius hystricinus\"/485,\"Liochthonius hystricinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius lapponicus\"/486,\"Liochthonius lapponicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius muscorum\"/487,\"Liochthonius muscorum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius neglectus\"/488,\"Liochthonius neglectus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius sellnicki\"/489,\"Liochthonius sellnicki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius strenzkei\"/490,\"Liochthonius strenzkei\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liochthonius tuxeni\"/491,\"Liochthonius tuxeni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poecilochthonius\"/492,\"Poecilochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Poecilochthonius spiciger\"/493,\"Poecilochthonius spiciger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius\"/494,\"Sellnickochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius formosus\"/495,\"Sellnickochthonius formosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius hungaricus\"/496,\"Sellnickochthonius hungaricus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius immaculatus\"/497,\"Sellnickochthonius immaculatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sellnickochthonius suecicus\"/498,\"Sellnickochthonius suecicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeidae\"/499,\"Caleremaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeus\"/500,\"Caleremaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caleremaeus monilipes\"/501,\"Caleremaeus monilipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisiidae\"/502,\"Camisiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisia\"/503,\"Camisia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Camisia horrida\"/504,\"Camisia horrida\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heminothrus\"/505,\"Heminothrus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Heminothrus targionii\"/506,\"Heminothrus targionii\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus\"/507,\"Platynothrus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus peltifer\"/508,\"Platynothrus peltifer\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platynothrus thori\"/509,\"Platynothrus thori\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodidae\"/510,\"Carabodidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes\"/511,\"Carabodes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes coriaceus\"/512,\"Carabodes coriaceus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes labyrinthicus\"/513,\"Carabodes labyrinthicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes marginatus\"/514,\"Carabodes marginatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes ornatus\"/515,\"Carabodes ornatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes reticulatus\"/516,\"Carabodes reticulatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes rugosior\"/517,\"Carabodes rugosior\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes schatzi\"/518,\"Carabodes schatzi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Carabodes tenuis\"/519,\"Carabodes tenuis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontocepheus\"/520,\"Odontocepheus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Odontocepheus elongatus\"/521,\"Odontocepheus elongatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheidae\"/522,\"Cepheidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheus\"/523,\"Cepheus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cepheus cepheiformis\"/524,\"Cepheus cepheiformis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tritegeus\"/525,\"Tritegeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tritegeus bisulcatus\"/526,\"Tritegeus bisulcatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetidae\"/527,\"Ceratozetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes\"/528,\"Ceratozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes gracilis\"/529,\"Ceratozetes gracilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes mediocris\"/530,\"Ceratozetes mediocris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes minimus\"/531,\"Ceratozetes minimus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes peritus\"/532,\"Ceratozetes peritus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes psammophilus\"/533,\"Ceratozetes psammophilus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratozetes thienemanni\"/534,\"Ceratozetes thienemanni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Edwardzetes\"/535,\"Edwardzetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Edwardzetes edwardsi\"/536,\"Edwardzetes edwardsi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes\"/537,\"Fuscozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes fuscipes\"/538,\"Fuscozetes fuscipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes setosus\"/539,\"Fuscozetes setosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fuscozetes tatricus\"/540,\"Fuscozetes tatricus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Melanozetes\"/541,\"Melanozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Melanozetes mollicomus\"/542,\"Melanozetes mollicomus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oromurcia\"/543,\"Oromurcia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oromurcia sudetica\"/544,\"Oromurcia sudetica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaerozetes\"/545,\"Sphaerozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Sphaerozetes orbicularis\"/546,\"Sphaerozetes orbicularis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates\"/547,\"Trichoribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates incisellus\"/548,\"Trichoribates incisellus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trichoribates trimaculatus\"/549,\"Trichoribates trimaculatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobatidae\"/550,\"Chamobatidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates\"/551,\"Chamobates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates borealis\"/552,\"Chamobates borealis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates cuspidatus\"/553,\"Chamobates cuspidatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Chamobates voigtsi\"/554,\"Chamobates voigtsi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelbidae\"/555,\"Ctenobelbidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelba\"/556,\"Ctenobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ctenobelba pectinigera\"/557,\"Ctenobelba pectinigera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeidae\"/558,\"Cymbaeremaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeus\"/559,\"Cymbaeremaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Cymbaeremaeus cymba\"/560,\"Cymbaeremaeus cymba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeidae\"/561,\"Damaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belba\"/562,\"Belba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Belba bartosi\"/563,\"Belba bartosi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caenobelba\"/564,\"Caenobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Caenobelba montana\"/565,\"Caenobelba montana\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeobelba\"/566,\"Damaeobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeobelba minutissima\"/567,\"Damaeobelba minutissima\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus\"/568,\"Damaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus (Adamaeus) onustus\"/569,\"Damaeus (Adamaeus) onustus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus (Paradamaeus) clavipes\"/570,\"Damaeus (Paradamaeus) clavipes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus crispatus\"/571,\"Damaeus crispatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeus riparius\"/572,\"Damaeus riparius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kunstidamaeus\"/573,\"Kunstidamaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Kunstidamaeus tecticola\"/574,\"Kunstidamaeus tecticola\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metabelba\"/575,\"Metabelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Metabelba propexa\"/576,\"Metabelba propexa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolidae\"/577,\"Damaeolidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolus\"/578,\"Damaeolus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Damaeolus asperatus\"/579,\"Damaeolus asperatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fosseremus\"/580,\"Fosseremus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Fosseremus laciniatus\"/581,\"Fosseremus laciniatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthoniidae\"/582,\"Eniochthoniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthonius\"/583,\"Eniochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eniochthonius minutissimus\"/584,\"Eniochthonius minutissimus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmanniidae\"/585,\"Epilohmanniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia\"/586,\"Epilohmannia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia minima\"/587,\"Epilohmannia minima\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Epilohmannia styriaca\"/588,\"Epilohmannia styriaca\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmanniidae\"/589,\"Eulohmanniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmannia\"/590,\"Eulohmannia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eulohmannia ribagai\"/591,\"Eulohmannia ribagai\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracaridae\"/592,\"Euphthiracaridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia\"/593,\"Acrotritia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia ardua\"/594,\"Acrotritia ardua\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrotritia duplicata\"/595,\"Acrotritia duplicata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetidae\"/596,\"Euzetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetes\"/597,\"Euzetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euzetes globulus\"/598,\"Euzetes globulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumnidae\"/599,\"Galumnidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrogalumna\"/600,\"Acrogalumna\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Acrogalumna longipluma\"/601,\"Acrogalumna longipluma\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna\"/602,\"Galumna\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna lanceata\"/603,\"Galumna lanceata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Galumna obvia\"/604,\"Galumna obvia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna\"/605,\"Pergalumna\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna altera\"/606,\"Pergalumna altera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pergalumna nervosa\"/607,\"Pergalumna nervosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pilogalumna\"/608,\"Pilogalumna\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pilogalumna tenuiclava\"/609,\"Pilogalumna tenuiclava\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeidae\"/610,\"Gymnodamaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeus\"/611,\"Gymnodamaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Gymnodamaeus bicostatus\"/612,\"Gymnodamaeus bicostatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Haplozetidae\"/613,\"Haplozetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloribates\"/614,\"Peloribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloribates longipilosus\"/615,\"Peloribates longipilosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protoribates\"/616,\"Protoribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Protoribates capucinus\"/617,\"Protoribates capucinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermanniidae\"/618,\"Hermanniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermannia\"/619,\"Hermannia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hermannia gibba\"/620,\"Hermannia gibba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthoniidae\"/621,\"Hypochthoniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius\"/622,\"Hypochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius luteus\"/623,\"Hypochthonius luteus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hypochthonius rufulus\"/624,\"Hypochthonius rufulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacaridae\"/625,\"Liacaridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Adoristes\"/626,\"Adoristes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Adoristes ovatus\"/627,\"Adoristes ovatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dorycranosus\"/628,\"Dorycranosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dorycranosus acutus\"/629,\"Dorycranosus acutus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus\"/630,\"Liacarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus coracinus\"/631,\"Liacarus coracinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liacarus subterraneus\"/632,\"Liacarus subterraneus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus\"/633,\"Xenillus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus discrepans\"/634,\"Xenillus discrepans\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus salamoni\"/635,\"Xenillus salamoni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Xenillus tegeocranus\"/636,\"Xenillus tegeocranus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeidae\"/637,\"Licnodamaeidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeus\"/638,\"Licnodamaeus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Licnodamaeus pulcherrimus\"/639,\"Licnodamaeus pulcherrimus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetidae\"/640,\"Limnozetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetes\"/641,\"Limnozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Limnozetes ciliatus\"/642,\"Limnozetes ciliatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuellidae\"/643,\"Machuellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuella\"/644,\"Machuella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Machuella bilineata\"/645,\"Machuella bilineata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothridae\"/646,\"Malaconothridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothrus\"/647,\"Malaconothrus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Malaconothrus monodactylus\"/648,\"Malaconothrus monodactylus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trimalaconothrus\"/649,\"Trimalaconothrus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trimalaconothrus foveolatus\"/650,\"Trimalaconothrus foveolatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetidae\"/651,\"Microzetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetes\"/652,\"Microzetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetes petrocoriensis\"/653,\"Microzetes petrocoriensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobatidae\"/654,\"Mycobatidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes\"/655,\"Minunthozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes pseudofusiger\"/656,\"Minunthozetes pseudofusiger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Minunthozetes semirufus\"/657,\"Minunthozetes semirufus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobates\"/658,\"Mycobates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Mycobates parmeliae\"/659,\"Mycobates parmeliae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates\"/660,\"Punctoribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates punctum\"/661,\"Punctoribates punctum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Punctoribates sellnicki\"/662,\"Punctoribates sellnicki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zachvatkinibates\"/663,\"Zachvatkinibates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zachvatkinibates (Alpizetes) perlongus\"/664,\"Zachvatkinibates (Alpizetes) perlongus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermanniidae\"/665,\"Nanhermanniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia\"/666,\"Nanhermannia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia comitalis\"/667,\"Nanhermannia comitalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia coronata\"/668,\"Nanhermannia coronata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia elegantula\"/669,\"Nanhermannia elegantula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia nana\"/670,\"Nanhermannia nana\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nanhermannia sellnicki\"/671,\"Nanhermannia sellnicki\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoliodidae\"/672,\"Neoliodidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyliodes\"/673,\"Platyliodes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Platyliodes scaliger\"/674,\"Platyliodes scaliger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothridae\"/675,\"Nothridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus\"/676,\"Nothrus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus anauniensis\"/677,\"Nothrus anauniensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus borussicus\"/678,\"Nothrus borussicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus palustris\"/679,\"Nothrus palustris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus pratensis\"/680,\"Nothrus pratensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Nothrus silvestris\"/681,\"Nothrus silvestris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiidae\"/682,\"Oppiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella\"/683,\"Berniniella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella bicarinata\"/684,\"Berniniella bicarinata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella conjucta\"/685,\"Berniniella conjucta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Berniniella hauseri\"/686,\"Berniniella hauseri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina\"/687,\"Dissorhina\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina ornata\"/688,\"Dissorhina ornata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Dissorhina signata\"/689,\"Dissorhina signata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microppia\"/690,\"Microppia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microppia minus\"/691,\"Microppia minus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia\"/692,\"Neotrichoppia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia (Confinoppia) confinis tenuiseta\"/693,\"Neotrichoppia (Confinoppia) confinis tenuiseta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neotrichoppia confinis\"/694,\"Neotrichoppia confinis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella\"/695,\"Oppiella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Moritzoppia) keilbachi\"/696,\"Oppiella (Moritzoppia) keilbachi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Moritzoppia) unicarinata\"/697,\"Oppiella (Moritzoppia) unicarinata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) falcata\"/698,\"Oppiella (Oppiella) falcata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) nova\"/699,\"Oppiella (Oppiella) nova\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) propinqua\"/700,\"Oppiella (Oppiella) propinqua\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Oppiella) uliginosa\"/701,\"Oppiella (Oppiella) uliginosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Rhinoppia) obsoleta\"/702,\"Oppiella (Rhinoppia) obsoleta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oppiella (Rhinoppia) subpectinata\"/703,\"Oppiella (Rhinoppia) subpectinata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ramusella\"/704,\"Ramusella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ramusella insculpta\"/705,\"Ramusella insculpta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Subiasella\"/706,\"Subiasella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Subiasella quadrimaculata\"/707,\"Subiasella quadrimaculata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatellidae\"/708,\"Oribatellidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ophidiotricus\"/709,\"Ophidiotricus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ophidiotricus vindobodensis\"/710,\"Ophidiotricus vindobodensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatella\"/711,\"Oribatella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatella calcarata\"/712,\"Oribatella calcarata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula\"/713,\"Oribatula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula amblyptera\"/714,\"Oribatula amblyptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula interrupta\"/715,\"Oribatula interrupta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula longelamellata\"/716,\"Oribatula longelamellata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Oribatula tibialis\"/717,\"Oribatula tibialis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zygoribatula\"/718,\"Zygoribatula\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zygoribatula exilis\"/719,\"Zygoribatula exilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Palaeacaridae\"/720,\"Palaeacaridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paleacarus\"/721,\"Paleacarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Paleacarus hystricinus\"/722,\"Paleacarus hystricinus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Parakalummidae\"/723,\"Parakalummidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoribates\"/724,\"Neoribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Neoribates aurantiacus\"/725,\"Neoribates aurantiacus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetidae\"/726,\"Passalozetidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes\"/727,\"Passalozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes africanus\"/728,\"Passalozetes africanus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes intermedius\"/729,\"Passalozetes intermedius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Passalozetes perforatus\"/730,\"Passalozetes perforatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloppiidae\"/731,\"Peloppiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia\"/732,\"Ceratoppia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia bipilis\"/733,\"Ceratoppia bipilis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Ceratoppia sexpilosa\"/734,\"Ceratoppia sexpilosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phenopelopidae\"/735,\"Phenopelopidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops\"/736,\"Eupelops\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops acromios\"/737,\"Eupelops acromios\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops occultus\"/738,\"Eupelops occultus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops plicatus\"/739,\"Eupelops plicatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops subuliger\"/740,\"Eupelops subuliger\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops tardus\"/741,\"Eupelops tardus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Eupelops torulosus\"/742,\"Eupelops torulosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloptulus\"/743,\"Peloptulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Peloptulus phaenotus\"/744,\"Peloptulus phaenotus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracaridae\"/745,\"Phthiracaridae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracarus\"/746,\"Euphthiracarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Euphthiracarus cribrarius\"/747,\"Euphthiracarus cribrarius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hoplophthiracarus\"/748,\"Hoplophthiracarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Hoplophthiracarus illinoisensis\"/749,\"Hoplophthiracarus illinoisensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus\"/750,\"Phthiracarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus boresetosus\"/751,\"Phthiracarus boresetosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus ferrugineus\"/752,\"Phthiracarus ferrugineus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus globosus\"/753,\"Phthiracarus globosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus laevigatus\"/754,\"Phthiracarus laevigatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus lentulus\"/755,\"Phthiracarus lentulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus longulus\"/756,\"Phthiracarus longulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus nitens\"/757,\"Phthiracarus nitens\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus peristomaticus\"/758,\"Phthiracarus peristomaticus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Phthiracarus sp.\"/759,\"Phthiracarus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus\"/760,\"Steganacarus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Atropacarus) striculus\"/761,\"Steganacarus (Atropacarus) striculus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) applicatus\"/762,\"Steganacarus (Steganacarus) applicatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) herculeanus\"/763,\"Steganacarus (Steganacarus) herculeanus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) magnus (forma magna)\"/764,\"Steganacarus (Steganacarus) magnus (forma magna)\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) sp.\"/765,\"Steganacarus (Steganacarus) sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) spinosus\"/766,\"Steganacarus (Steganacarus) spinosus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Steganacarus) vernaculus\"/767,\"Steganacarus (Steganacarus) vernaculus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus (Tropacarus) carinatus (forma carinata)\"/768,\"Steganacarus (Tropacarus) carinatus (forma carinata)\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus herculeanus\"/769,\"Steganacarus herculeanus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus hirsutus\"/770,\"Steganacarus hirsutus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Steganacarus sp.\"/771,\"Steganacarus sp.\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiidae\"/772,\"Quadroppiidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia\"/773,\"Quadroppiia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia hammerae\"/774,\"Quadroppiia hammerae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia longisetosa\"/775,\"Quadroppiia longisetosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia maritalis\"/776,\"Quadroppiia maritalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia monstruosa\"/777,\"Quadroppiia monstruosa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Quadroppiia quadricarinata\"/778,\"Quadroppiia quadricarinata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribatidae\"/779,\"Scheloribatidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia\"/780,\"Liebstadia\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia humerata\"/781,\"Liebstadia humerata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Liebstadia pannonica\"/782,\"Liebstadia pannonica\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates\"/783,\"Scheloribates\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Hemileius) initialis\"/784,\"Scheloribates (Hemileius) initialis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) labyrinthicus\"/785,\"Scheloribates (Scheloribates) labyrinthicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) laevigatus\"/786,\"Scheloribates (Scheloribates) laevigatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) pallidulus\"/787,\"Scheloribates (Scheloribates) pallidulus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Scheloribates) quintus\"/788,\"Scheloribates (Scheloribates) quintus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates (Topobates) helveticus\"/789,\"Scheloribates (Topobates) helveticus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scheloribates labyrinthicus\"/790,\"Scheloribates labyrinthicus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutoverticidae\"/791,\"Scutoverticidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutovertex\"/792,\"Scutovertex\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Scutovertex minutus\"/793,\"Scutovertex minutus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbidae\"/794,\"Suctobelbidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allosuctobelba\"/795,\"Allosuctobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Allosuctobelba ornithorhyncha\"/796,\"Allosuctobelba ornithorhyncha\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba\"/797,\"Suctobelba\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba altvateri\"/798,\"Suctobelba altvateri\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba atomaria\"/799,\"Suctobelba atomaria\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba secta\"/800,\"Suctobelba secta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelba trigona\"/801,\"Suctobelba trigona\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella\"/802,\"Suctobelbella\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella acutidens\"/803,\"Suctobelbella acutidens\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella alloenasuta\"/804,\"Suctobelbella alloenasuta\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella arcana\"/805,\"Suctobelbella arcana\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella baloghi\"/806,\"Suctobelbella baloghi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella diffissa\"/807,\"Suctobelbella diffissa\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella falcata\"/808,\"Suctobelbella falcata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella forsslundi\"/809,\"Suctobelbella forsslundi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella nasalis\"/810,\"Suctobelbella nasalis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella palustris\"/811,\"Suctobelbella palustris\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella perforata\"/812,\"Suctobelbella perforata\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella sarekensis\"/813,\"Suctobelbella sarekensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella similis\"/814,\"Suctobelbella similis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella subcornigera\"/815,\"Suctobelbella subcornigera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Suctobelbella subtrigona\"/816,\"Suctobelbella subtrigona\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheidae\"/817,\"Tectocepheidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus\"/818,\"Tectocepheus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus minor\"/819,\"Tectocepheus minor\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus alatus\"/820,\"Tectocepheus velatus alatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus sarekensis\"/821,\"Tectocepheus velatus sarekensis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tectocepheus velatus velatus\"/822,\"Tectocepheus velatus velatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Tegoribatidae\"/823,\"Tegoribatidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidozetes\"/824,\"Lepidozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidozetes singularis\"/825,\"Lepidozetes singularis\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Thyrisomidae\"/826,\"Thyrisomidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pantelozetes\"/827,\"Pantelozetes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Pantelozetes paolii\"/828,\"Pantelozetes paolii\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthoniidae\"/829,\"Trhypochthoniidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthonius\"/830,\"Trhypochthonius\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Trhypochthonius tectorum\"/831,\"Trhypochthonius tectorum\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimidae\"/832,\"Zetomimidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimus\"/833,\"Zetomimus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetomimus furcatus\"/834,\"Zetomimus furcatus\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestidae\"/835,\"Zetorchestidae\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetorchestes\"/836,\"Microzetorchestes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Microzetorchestes emeryi\"/837,\"Microzetorchestes emeryi\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestes\"/838,\"Zetorchestes\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Zetorchestes falzonni\"/839,\"Zetorchestes falzonni\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Coleoptera larva\"/840,\"Coleoptera larva\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Other larva\"/841,\"Other larva\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidoptera\"/842,\"Lepidoptera\"/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/\"Lepidoptera larva\"/843,\"Lepidoptera larva\"/g' {} +

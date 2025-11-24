# Convert species (Emilie's) ID's used in Roboflow to Emilie's species names.
#
# To run this script, in a terminal go where the files are located
# and the type:
#     bash thisfile.sh

find . -type f -name "*.csv" -exec sed -i '' 's/,in1,/,Unclassified,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in2,/,Dirt,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in5,/,Acari,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in6,/,Araneae +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in7,/,Araneae -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in8,/,Pseudoscorpiones,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in12,/,Isopoda,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in14,/,Diplopoda +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in15,/,Diplopoda -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in16,/,Chilopoda +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in17,/,Chilopoda -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in18,/,Symphyla,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in20,/,Hexapoda,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in21,/,Diplura,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in22,/,Protura,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in23,/,Collembola,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in25,/,Coleoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in26,/,Diptera adult,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in27,/,Diptera larva,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in28,/,Hymenoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in29,/,Hymenoptera Formicidae,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in30,/,Hemiptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in32,/,Thysanoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in34,/,Dermaptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in48,/,Staphylinidae,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in91,/,Isotomiella,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in463,/,Sarcoptiformes (Oribate),/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in840,/,Coleoptera larva,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,in841,/,Other larva,/g' {} +

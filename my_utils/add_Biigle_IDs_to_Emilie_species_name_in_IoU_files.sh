# Add Biigle IDs column to the Emilie species names.

# To run this script, in a terminal go where the files are located
# and the type:
#     bash thisfile.sh


# Add the header
find . -type f -name "*.csv" -exec sed -i '' 's/,label_name,/,label_id,label_name,/g' {} +


# Add the Biigle ID's for each Emilie's species names.
find . -type f -name "*.csv" -exec sed -i '' 's/,Acari,/,4200,Acari,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Araneae +5mm,/,4201,Araneae +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Araneae -5mm,/,4202,Araneae -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Chilopoda +5mm,/,4211,Chilopoda +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Chilopoda -5mm,/,4212,Chilopoda -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Coleoptera,/,4220,Coleoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Coleoptera larva,/,5035,Coleoptera larva,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Collembola,/,4218,Collembola,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Dermaptera,/,4229,Dermaptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Diplopoda +5mm,/,4209,Diplopoda +5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Diplopoda -5mm,/,4210,Diplopoda -5mm,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Diplura,/,4216,Diplura,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Diptera adult,/,4221,Diptera adult,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Diptera larva,/,4222,Diptera larva,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Dirt,/,4197,Dirt,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Hemiptera,/,4225,Hemiptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Hexapoda,/,4215,Hexapoda,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Hymenoptera,/,4223,Hymenoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Hymenoptera Formicidae,/,4224,Hymenoptera Formicidae,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Isopoda,/,4207,Isopoda,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Isotomiella,/,4286,Isotomiella,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Other larva,/,5036,Other larva,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Protura,/,4217,Protura,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Pseudoscorpiones,/,4203,Pseudoscorpiones,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Sarcoptiformes (Oribate),/,4658,Sarcoptiformes (Oribate),/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Staphylinidae,/,4243,Staphylinidae,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Symphyla,/,4213,Symphyla,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Thysanoptera,/,4227,Thysanoptera,/g' {} +
find . -type f -name "*.csv" -exec sed -i '' 's/,Unclassified,/,4196,Unclassified,/g' {} +

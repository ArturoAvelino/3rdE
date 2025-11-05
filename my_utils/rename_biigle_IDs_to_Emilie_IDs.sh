# Convert species ID's from biigle to Emilie's IDs.
#
# To run this script, in a terminal go where the files are located
# and the type:
#     bash thisfile.sh

find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4200,Acari,/,5,Acari,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4201,Araneae +5mm,/,6,Araneae +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4202,Araneae -5mm,/,7,Araneae -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4211,Chilopoda +5mm,/,16,Chilopoda +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4212,Chilopoda -5mm,/,17,Chilopoda -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4220,Coleoptera,/,25,Coleoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,5035,Coleoptera larva,/,840,Coleoptera larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4218,Collembola,/,23,Collembola,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4229,Dermaptera,/,34,Dermaptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4209,Diplopoda +5mm,/,14,Diplopoda +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4210,Diplopoda -5mm,/,15,Diplopoda -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4216,Diplura,/,21,Diplura,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4221,Diptera adult,/,26,Diptera adult,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4222,Diptera larva,/,27,Diptera larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4197,Dirt,/,2,Dirt,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4225,Hemiptera,/,30,Hemiptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4215,Hexapoda,/,20,Hexapoda,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4223,Hymenoptera,/,28,Hymenoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4224,Hymenoptera Formicidae,/,29,Hymenoptera Formicidae,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4207,Isopoda,/,12,Isopoda,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4286,Isotomiella,/,91,Isotomiella,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,5036,Other larva,/,841,Other larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4217,Protura,/,22,Protura,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4203,Pseudoscorpiones,/,8,Pseudoscorpiones,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4658,Sarcoptiformes (Oribate),/,463,Sarcoptiformes (Oribate),/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4243,Staphylinidae,/,48,Staphylinidae,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4213,Symphyla,/,18,Symphyla,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4227,Thysanoptera,/,32,Thysanoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4196,Unclassified,/,1,Unclassified,/g' {} +


# Apply the transformations also when the species's names are enclosed in quotation marks

find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4201,\"Araneae +5mm\",/,6,Araneae +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4202,\"Araneae -5mm\",/,7,Araneae -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4211,\"Chilopoda +5mm\",/,16,Chilopoda +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4212,\"Chilopoda -5mm\",/,17,Chilopoda -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4220,\"Coleoptera\",/,25,Coleoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,5035,\"Coleoptera larva\",/,840,Coleoptera larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4218,\"Collembola\",/,23,Collembola,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4229,\"Dermaptera\",/,34,Dermaptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4209,\"Diplopoda +5mm\",/,14,Diplopoda +5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4210,\"Diplopoda -5mm\",/,15,Diplopoda -5mm,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4216,\"Diplura\",/,21,Diplura,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4221,\"Diptera adult\",/,26,Diptera adult,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4222,\"Diptera larva\",/,27,Diptera larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4197,\"Dirt\",/,2,Dirt,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4225,\"Hemiptera\",/,30,Hemiptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4215,\"Hexapoda\",/,20,Hexapoda,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4223,\"Hymenoptera\",/,28,Hymenoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4224,\"Hymenoptera Formicidae\",/,29,Hymenoptera Formicidae,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4207,\"Isopoda\",/,12,Isopoda,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4286,\"Isotomiella\",/,91,Isotomiella,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,5036,\"Other larva\",/,841,Other larva,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4217,\"Protura\",/,22,Protura,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4203,\"Pseudoscorpiones\",/,8,Pseudoscorpiones,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4658,\"Sarcoptiformes (Oribate)\",/,463,Sarcoptiformes (Oribate),/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4243,\"Staphylinidae\",/,48,Staphylinidae,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4213,\"Symphyla\",/,18,Symphyla,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4227,\"Thysanoptera\",/,32,Thysanoptera,/g' {} +
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,4196,\"Unclassified\",/,1,Unclassified,/g' {} +


# Special case: there in an additional space after the name but still between the quotation marks.
find . -type f -name "2025_11_03_annotations_Emilie_IDs.csv" -exec sed -i '' 's/,5036,\"Other larva \",/,841,Other larva,/g' {} +


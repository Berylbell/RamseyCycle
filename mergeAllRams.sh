#merge all ramsey outputs
mkdir all
for d in *_out/ ; do
    echo "$d"
    cp merge_all.c $d/
    cd $d
    root -q merge_all.c
    rm -rf merge_all.c
    cd ..

    cp $d/out.root all/
    mv all/out.root all/${d/_out\//.root}

done
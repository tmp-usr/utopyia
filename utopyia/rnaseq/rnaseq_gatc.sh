



input_dir=/home/adilm/projects/low_carb/raw_data/
tmp_dir=/proj/b2016253/nobackup/kemal/projects/low_carb
output_dir=$HOME/projects/low_carb/outputs/alignment

cd $input_dir

for d in $(ls -d */)
do 
    
    mkdir -R $tmp_dir/$d
    mkdir -R $tmp_dir/$d    

done


cd $input_dir

for f in *.bz2
do
    echo $f 
    echo $tmp_dir/${f/%.bz2/}
done
    
#bzcat -dkf $f ${f/%bz2/}




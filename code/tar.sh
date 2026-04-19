tar -cvf nya.tar -C ../android $(ls ../android) --transform='s|^|ime_data_dir/|'

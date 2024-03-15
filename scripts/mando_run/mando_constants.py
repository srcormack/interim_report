class MandoConstants:
    SUFFIX_CONCAT_FASTQ = ".concat.fastq"
    SUFFIX_QUANT = ".quant"
    WORKING_DIRECTORY = "/home/scormack/Mandalorion/Mandalorion"
    CMD_MANDO = f'{WORKING_DIRECTORY}/Mando.py \
    -p "{{out_mando}}" \
    -g "{{annotation}}" \
    -G "{{genome}}" \
    -f "{{fastq_file}}" \
    -t "{{n_cores}}" \
    -W "basic,SIRV"' 
    
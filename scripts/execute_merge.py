import os
import sys
from mando_run import mando_merge_expression
#from . import merge_sqanti

if __name__ == "__main__":
    #script_path = sys.argv[1] 
    # assembler = sys.argv[2] 
    # destination = sys.argv[3]    
    #sys.argv[2] = "mando"
    #sys.argv[3] = "/home/scormack/NIH_REPORT/data"
    assembler = "mando"
    destination = "/home/scormack/NIH_REPORT/data"
    script_path = "/home/scormack/src/benchmark/mando_run/mando_merge_expression.R"
    print(script_path)
    mando_merge_expression.main(script_path)
    print(f"Now merging {assembler} gtf files with SQANTI3... \n")
    print(f"Output directory: {destination} \n")  
    #merge_sqanti.main(assembler, destination)


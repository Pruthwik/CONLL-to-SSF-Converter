# This code works for a single or multiple files.
This code convert CONLL files into SSF files.
* For converting only POS files
	- python convert_conll_files_into_ssf_format.py --input sample_pos_conll.txt --opr 0 --output sample_pos_ssf.txt
* For converting POS and Chunk files
	- python convert_conll_files_into_ssf_format.py --input sample_pos_chunk_conll.txt --opr 1 --output sample_pos_chunk_ssf.txt
* For converting POS, Chunk, and morph files
	- python convert_conll_files_into_ssf_format.py --input sample_pos_chunk_morph_conll.txt --opr 2 --output sample_pos_chunk_morph_ssf.txt
* To execute the code for multiple files, just change the input and output arguments

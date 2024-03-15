from pathlib import Path


class NIHPaths:
    """
    Stores useful paths within the project directory and
    Garnatxa storage system.

    Uses pathlib.Path wherever possible;
    attributes that point to individual files end in _file;
    """

    # base paths
    benchmark = Path(__file__).parent
    scripts = benchmark.parent
    base_root = Path("/home/scormack")
    assembly_algorithms = base_root / "Assembly_algorithms"
    
    # storage paths
    storage_root = Path("/storage/gge")

    storage_genomes = storage_root / "genomes"
    mouse_refs = storage_genomes / "mouse_ref_NIH" / "reference_genome"
    mouse_genome_file = mouse_refs / "mm39_SIRV.fa"
    mouse_annot_file = mouse_refs / "mm39.ncbiRefSeq_SIRV.gtf"
    storage_nih = storage_root / "nih"
    illumina = storage_nih / "Illumina_short_reads" / "short_reads"
    pacbio_isoseq = storage_nih / "PacBio_IsoSeq"

    # repo paths
    metadata = base_root / "data" / "metadata"
    mouse_metadata_file = metadata / "mouse_samples_metadata.tsv"
    mouse_pooled_metadata_file = metadata / "mouse_pooled_metadata.tsv"
    
    output = base_root / "data" / "output"
    out_test = output / "test"
    out_detect = output / "isoform_detection"
    out_quant = output / "quantification"

    #Flair directories
    flair_wd = assembly_algorithms / "Flair"
    out_detect_flair = out_detect / "flair"
    out_quant_flair = out_quant / "flair"

    #Mando directories
    mando_wd = assembly_algorithms / "Mandalorion" / "Mandalorion"
    out_quant_mando = out_quant / "mando"
    mando_tama = out_quant_mando / "TAMAIsoforms"
    mando_merge = out_quant_mando / "mando_merge"
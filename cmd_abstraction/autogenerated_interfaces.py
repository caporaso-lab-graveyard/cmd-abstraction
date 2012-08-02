
#!/usr/bin/env python
from __future__ import division

from cmd_abstraction.util import (QiimeCommand)

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ['Greg Caporaso']
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

from qiime.util import parse_command_line_parameters
from qiime.util import make_option
from biom.parse import parse_biom_table
from qiime.parse import parse_taxonomy_to_otu_metadata
from qiime.format import format_biom_table

class PickOtusThroughOtuTable(QiimeCommand):
    """class defining pick_otus_through_otu_table script interface"""
    
    
    from qiime.util import make_option
    from os import makedirs
    from qiime.util import (load_qiime_config, 
                            parse_command_line_parameters,
                            get_options_lookup)
    from qiime.parse import parse_qiime_parameters
    from qiime.workflow import (run_qiime_data_preparation, print_commands,
        call_commands_serially, print_to_stdout, no_status_updates,
        validate_and_set_jobs_to_start)
    
    qiime_config = load_qiime_config()
    options_lookup = get_options_lookup()
    _brief_description = """A workflow script for picking OTUs through building OTU tables"""
    _script_description = """This script takes a sequence file and performs all processing steps through building the OTU table."""
    
    _script_usage = []
    
    _script_usage.append(("""Simple example""","""The following command will start an analysis on seqs.fna (-i), which is a post-split_libraries fasta file. The sequence identifiers in this file should be of the form <sample_id>_<unique_seq_id>. The following steps, corresponding to the preliminary data preparation, are applied: Pick de novo OTUs at 97%; pick a representative sequence for each OTU (the OTU centroid sequence); align the representative set with PyNAST; assign taxonomy with RDP classifier; filter the alignment prior to tree building - remove positions which are all gaps, and specified as 0 in the lanemask; build a phylogenetic tree with FastTree; build an OTU table. All output files will be written to the directory specified by -o, and subdirectories as appropriate. ALWAYS SPECIFY ABSOLUTE FILE PATHS (absolute path represented here as $PWD, but will generally look something like /home/ubuntu/my_analysis/).""","""%prog -i $PWD/seqs.fna -o $PWD/otus/"""))
    
    _script_usage_output_to_remove = ['$PWD/otus/']
    
    _output_description ="""This script will produce an OTU mapping file (pick_otus.py), a representative set of sequences (FASTA file from pick_rep_set.py), a sequence alignment file (FASTA file from align_seqs.py), taxonomy assignment file (from assign_taxonomy.py), a filtered sequence alignment (from filter_alignment.py), a phylogenetic tree (Newick file from make_phylogeny.py) and a biom-formatted OTU table (from make_otu_table.py)."""
    
    _required_options = [
        make_option('-i','--input_fp',type='existing_filepath',
            help='the input fasta file [REQUIRED]'),
        make_option('-o','--output_dir',type='new_dirpath',
            help='the output directory [REQUIRED]'),
        ]
    
    _optional_options = [\
     make_option('-p','--parameter_fp',type='existing_filepath',
        help='path to the parameter file, which specifies changes'+\
            ' to the default behavior. '+\
            'See http://www.qiime.org/documentation/file_formats.html#qiime-parameters .'+\
            ' [if omitted, default values will be used]'),
     make_option('-f','--force',action='store_true',\
            dest='force',help='Force overwrite of existing output directory'+\
            ' (note: existing files in output_dir will not be removed)'+\
            ' [default: %default]'),\
     make_option('-w','--print_only',action='store_true',\
            dest='print_only',help='Print the commands but don\'t call them -- '+\
            'useful for debugging [default: %default]',default=False),\
     make_option('-a','--parallel',action='store_true',\
            dest='parallel',default=False,\
            help='Run in parallel where available [default: %default]'),
     options_lookup['jobs_to_start_workflow']
    ]
    _version = __version__
    
    def run_command(self,opts,args):
    
        verbose = opts['verbose']
        
        input_fp = opts['input_fp']
        output_dir = opts['output_dir']
        verbose = opts['verbose']
        print_only = opts['print_only']
        
        parallel = opts['parallel']
        # No longer checking that jobs_to_start > 2, but
        # commenting as we may change our minds about this.
        #if parallel: raise_error_on_parallel_unavailable()
        
        if opts['parameter_fp']:
            try:
                parameter_f = open(opts['parameter_fp'])
            except IOError:
                raise IOError,\
                 "Can't open parameters file (%s). Does it exist? Do you have read access?"\
                 % opts['parameter_fp']
            params = parse_qiime_parameters(parameter_f)
        else:
            params = parse_qiime_parameters([]) 
            # empty list returns empty defaultdict for now
        
        jobs_to_start = opts['jobs_to_start']
        default_jobs_to_start = qiime_config['jobs_to_start']
        validate_and_set_jobs_to_start(params,
                                       jobs_to_start,
                                       default_jobs_to_start,
                                       parallel,
                                       option_parser)
        
        try:
            makedirs(output_dir)
        except OSError:
            if opts['force']:
                pass
            else:
                # Since the analysis can take quite a while, I put this check
                # in to help users avoid overwriting previous output.
                print "Output directory already exists. Please choose "+\
                 "a different directory, or force overwrite with -f."
                exit(1)
            
        if print_only:
            command_handler = print_commands
        else:
            command_handler = call_commands_serially
        
        if verbose:
            status_update_callback = print_to_stdout
        else:
            status_update_callback = no_status_updates
        
        run_qiime_data_preparation(
         input_fp, 
         output_dir,
         command_handler=command_handler,
         params=params,
         qiime_config=qiime_config,
         parallel=parallel,\
         status_update_callback=status_update_callback)
    





class AddTaxa(QiimeCommand):
    """class defining add_taxa script interface"""
    
     
    

    
    _brief_description="""Add taxa to OTU table"""
    _script_description="""This script adds taxa to a biom-formatted OTU table."""
    _script_usage=[]
    
    _script_usage.append(("""Example:""","""Given an input otu table with no metadata (otu_table_no_tax.biom) and a tab-separated text file mapping OTU ids to taxonomic assignments and scores associated with those assignments (tax.txt), generate a new otu table that includes taxonomic assignments (otu_table_w_tax.biom).""","""%prog -i otu_table_no_tax.biom -o otu_table_w_tax.biom -t tax.txt"""))
    
    _script_usage.append(("""Example:""","""Given an input otu table with no metadata (otu_table_no_tax.biom) and a tab-separated text file mapping OTU ids to taxonomic assignments and scores associated with those assignments (tax.txt), generate a new otu table that includes taxonomic assignments (otu_table_w_tax.biom) with alternate metadata identifiers.""","""%prog -i otu_table_no_tax.biom -o otu_table_w_alt_labeled_tax.biom -t tax.txt -l "Consensus Lineage,Score" """))
    
    _script_usage.append(("""Example:""","""Given an input otu table with no metadata (otu_table_no_tax.biom) and a tab-separated text file mapping OTU ids to some value, generate a new otu table that includes that metadata category labeled as "Score" (otu_table_w_score.biom).""","""%prog -i otu_table_no_tax.biom -o otu_table_w_score.biom -t score_only.txt -l "Score" --all_strings"""))
    
    _output_description="""An OTU table in biom format is written to the file specified as -o."""
    _required_options=[\
        make_option('-i','--input_fp',type='existing_filepath',
                    help='path to input otu table file in biom format'),
        make_option('-o','--output_fp',type='new_filepath',
                    help='path to output file in biom format'),
        make_option('-t','--taxonomy_fp',type='existing_filepath',
                    help='path to input taxonomy file (e.g., as generated by assign_taxonomy.py)'),
    ]
    
    _optional_options=[
        make_option('-l','--labels',type='string',default='taxonomy,score',
                    help='labels to be assigned to metadata in taxonomy_fp'),
        make_option('--all_strings',action='store_true',default=False,
                    help='treat all metadata as strings, rather than casting to lists/floats (useful with --labels for adding arbitrary observation metadata) [default:%default]')]
    _version = __version__
    
    def run_command(self,opts,args):
        
        labels = opts['labels'].split(',')
        if opts['all_strings']:
            process_fs = [str] * len(labels)
            observation_metadata = parse_taxonomy_to_otu_metadata(\
                                open(opts['taxonomy_fp'],'U'),labels=labels,process_fs=process_fs)
        else:
            observation_metadata = parse_taxonomy_to_otu_metadata(\
                                open(opts['taxonomy_fp'],'U'),labels=labels)
        
    
        otu_table = parse_biom_table(open(opts['input_fp'],'U'))
        
        if otu_table.ObservationMetadata != None:
            # if there is already metadata associated with the 
            # observations, confirm that none of the metadata names
            # are already present
            existing_keys = otu_table.ObservationMetadata[0].keys()
            for label in labels:
                if label in existing_keys:
                    option_parser.error(\
                     "%s is already an observation metadata field." 
                     " Can't add it, so nothing is being added." % label)
        
        otu_table.addObservationMetadata(observation_metadata)
        
        output_f = open(opts['output_fp'],'w')
        output_f.write(format_biom_table(otu_table))
        output_f.close()
        
        
        
    




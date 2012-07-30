#!/usr/bin/env python
# File created on 30 Jul 2012
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2011, The QIIME project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "1.5.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"

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

def cmd_main(cmd_constructor):
    
    cmd = cmd_constructor()
    script_info = cmd.getScriptInfo()
    
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)
    
    try:
        cmd(option_parser, opts, args)
    except QiimeCommandError, e:
        option_parser.error(e)

class QiimeCommandError(IOError):
    pass

class QiimeCommand(object):
    """ Base class for abstracted QIIME command
    """
    
    _brief_description = """ """
    _script_description = """ """
    _script_usage = []
    _script_usage_output_to_remove = []
    _output_description = """ """
    _required_options = []
    _optional_options = []
    _version = __version__
    
    def __init__(self):
        """
        """
        pass
    
    def __call__(self):
        """
        """
        raise NotImplementedError, "All subclasses must implement __call__."

    def getScriptInfo(self):
        result = {}
        result['brief_description'] = self._brief_description
        result['script_description'] = self._script_description
        result['script_usage'] = self._script_usage
        result['script_usage_output_to_remove'] = self._script_usage_output_to_remove
        result['output_description'] = self._output_description
        result['required_options'] = self._required_options
        result['optional_options'] = self._optional_options
        result['version'] = self._version
        return result

class PickOtusThroughOtuTable(QiimeCommand):
    """
    """
    _brief_description = """A workflow script for picking OTUs through building OTU tables"""
    _script_description = """This script takes a sequence file and performs all processing steps through building the OTU table."""
    _script_usage = [("""Simple example""","""The following command will start an analysis on seqs.fna (-i), which is a post-split_libraries fasta file. The sequence identifiers in this file should be of the form <sample_id>_<unique_seq_id>. The following steps, corresponding to the preliminary data preparation, are applied: Pick de novo OTUs at 97%; pick a representative sequence for each OTU (the OTU centroid sequence); align the representative set with PyNAST; assign taxonomy with RDP classifier; filter the alignment prior to tree building - remove positions which are all gaps, and specified as 0 in the lanemask; build a phylogenetic tree with FastTree; build an OTU table. All output files will be written to the directory specified by -o, and subdirectories as appropriate. ALWAYS SPECIFY ABSOLUTE FILE PATHS (absolute path represented here as $PWD, but will generally look something like /home/ubuntu/my_analysis/).""","""%prog -i $PWD/seqs.fna -o $PWD/otus/""")]
    _script_usage_output_to_remove = ['$PWD/otus/']
    _output_description = """This script will produce an OTU mapping file (pick_otus.py), a representative set of sequences (FASTA file from pick_rep_set.py), a sequence alignment file (FASTA file from align_seqs.py), taxonomy assignment file (from assign_taxonomy.py), a filtered sequence alignment (from filter_alignment.py), a phylogenetic tree (Newick file from make_phylogeny.py) and a biom-formatted OTU table (from make_otu_table.py)."""
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

    def __call__(self, option_parser, opts, args):

        verbose = opts.verbose
    
        input_fp = opts.input_fp
        output_dir = opts.output_dir
        verbose = opts.verbose
        print_only = opts.print_only
    
        parallel = opts.parallel
        # No longer checking that jobs_to_start > 2, but
        # commenting as we may change our minds about this.
        #if parallel: raise_error_on_parallel_unavailable()
    
        if opts.parameter_fp:
            try:
                parameter_f = open(opts.parameter_fp)
            except IOError:
                raise QiimeCommandError,\
                 "Can't open parameters file (%s). Does it exist? Do you have read access?"\
                 % opts.parameter_fp
            params = parse_qiime_parameters(parameter_f)
        else:
            params = parse_qiime_parameters([]) 
            # empty list returns empty defaultdict for now
    
        jobs_to_start = opts.jobs_to_start
        default_jobs_to_start = qiime_config['jobs_to_start']
        validate_and_set_jobs_to_start(params,
                                       jobs_to_start,
                                       default_jobs_to_start,
                                       parallel,
                                       option_parser)
    
        try:
            makedirs(output_dir)
        except OSError:
            if opts.force:
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

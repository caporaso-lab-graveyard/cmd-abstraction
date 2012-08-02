fixers
===============

These are custom fixers that can be used with `2to3` to code auto-conversion of the QIIME script `main()` functions to `QiimeCommand.run_command()` methods. Unfortunately I haven't had a lot of luck getting `2to3` to recognize my custom fixers, so have been applying the following (absurd) steps to get this working. 

```bash
cd /Users/caporaso/code/
svn co http://svn.python.org/projects/sandbox/trunk/2to3/
ln -s /Users/caporaso/code/cmd-abstraction/fixers/fix_replace_args.py /Users/caporaso/code/2to3/lib2to3/fixes/

# then an example call to apply the ReplaceArgs fixer to a python file
python ~/code/2to3/2to3 -f replace_args pick_otus_through_otu_table.py
```

I beginning to realize that this is going to be extremely complicated, so trying this with a python script for now.
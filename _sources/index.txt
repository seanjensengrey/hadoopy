1;2703;0c..  Hadoopy documentation master file, created by
    sphinx-quickstart on Sat Jan 15 20:41:41 2011.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to Hadoopy's documentation!
===================================

..  toctree::
    :maxdepth: 2

..  function:: hadoopy.run(mapper=None, reducer=None, combiner=None, **kw)

    This is to be called in all Hadoopy job's.  Handles arguments passed in, calls the provided functions with input, and stores the output.

    TypedBytes are used if (os.environ['stream_map_input'] == 'typedbytes') which is a jobconf variable set in all jobs Hadoop is using TypedBytes with.

    It is *highly* recommended that TypedBytes be used for all non-trivial tasks.  Keep in mind that the semantics of what you can safely emit from your functions is limited when using Text (i.e., no \\t or \\n).  You can use the base64 module to ensure that your output is clean.

    **Command Interface**

    The command line switches added to your script (e.g., script.py) are

    python script.py map
        Use the provided mapper
    python script.py reduce
        Use the provided reducer
    python script.py combine
        Use the provided combiner
    python script.py freeze <tar_path> <-Zadd_file0 -Zadd_file1...> <cx_Freeze args>
        Freeze the script to a tar file specified by <tar_path>.  The extension may be .tar or .tar.gz.  All files are placed in the root of the tar. Files specified with -Z will be added to the tar root.  Additional cx_Freeze arguments may be passed in.
    
    **Specification of mapper/reducer/combiner**
    
    Input Key/Value Types
    ::
        For TypedBytes, the type will be the decoded typed
        For Text, the type will be text assuming key0\\tvalue0\\nkey1\\tvalue1\\n

    Output Key/Value Types
    ::
        For TypedBytes, anything Pickle-able can be used
        For Text, types are converted to string.  Note that neither may contain \\t or \\n as these are used in the encoding.  Output is key\\tvalue\\n
    
    Expected arguments
    ::
        mapper(key, value) or mapper.map(key, value)
        reducer(key, values) or reducer.reduce(key, values)
        combiner(key, values) or combiner.combine(key, values)

    Optional methods
    ::
        func.configure(): Call first.  Returns None.
        func.close():  Call last.  Returns Iterator of (key, value) or None

    Expected return
    ::
        Iterator of (key, value) or None

    :param mapper: Function or class instance following the above spec
    :param reducer: Function or class instance following the above spec
    :param combiner: Function or class instance following the above spec
    :param doc: If specified, on error print this and call sys.exit(1)
    :rtype: True on error, else False (may not return if doc is set and
        there is an error)

..  autofunction:: hadoopy.status
..  autofunction:: hadoopy.counter
..  autofunction:: hadoopy.launch
..  autofunction:: hadoopy.launch_frozen
..  autofunction:: hadoopy.cat
..  autofunction:: hadoopy.ls
..  autoclass:: hadoopy.GroupedValues
    :members:
..  autoclass:: hadoopy.Test
    :members:
..  autoclass:: hadoopy.TypedBytesFile
    :members:

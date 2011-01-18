..  Hadoopy documentation master file, created by
    sphinx-quickstart on Sat Jan 15 20:41:41 2011.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to Hadoopy's documentation!
===================================



..  toctree::
    :maxdepth: 2

Example - Hello Wordcount!
-------
Python Source (wc.py) ::

    import hadoopy

    def mapper(key, value):
        for word in value.split():
            yield word, 1

    def reducer(key, values):
        accum = 0
        for count in values:
            accum += int(count)
        yield key, accum

    if __name__ == "__main__":
        hadoopy.run(mapper, reducer)

Command line test (map) ::

    $ echo "a b a a b c" | python wc.py map
    a    1
    b    1
    a    1
    a    1
    b    1
    c    1

Command line test (map/sort) ::

    $ echo "a b a a b c" | python wc.py map | sort
    a    1
    a    1
    a    1
    b    1
    b    1
    c    1

Command line test (map/sort/reduce) ::

    $ echo "a b a a b c" | python wc.py map | sort | python wc.py reduce
    a    3
    b    2
    c    1

Here are a few test files ::

    $ hadoop fs -ls playground/
    Found 3 items
    -rw-r--r--   2 brandyn supergroup     259835 2011-01-17 18:56 /user/brandyn/playground/wc-input-alice.tb
    -rw-r--r--   2 brandyn supergroup     167529 2011-01-17 18:56 /user/brandyn/playground/wc-input-alice.txt
    -rw-r--r--   2 brandyn supergroup      60638 2011-01-17 18:56 /user/brandyn/playground/wc-input-alice.txt.gz

We can also get these in Python

    >>> import hadoopy
    >>> hadoopy.ls('playground/')
    ['/user/brandyn/playground/wc-input-alice.tb', '/user/brandyn/playground/wc-input-alice.txt', '/user/brandyn/playground/wc-input-alice.txt.gz']

Lets put wc-input-alice.txt through the word counter using Hadoop

    >>> cmd = hadoopy.launch('playground/wc-input-alice.txt', 'playground/out/', 'wc.py')
    HadooPY: Running[hadoop jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2+737.jar -output playground/out/ -input playground/wc-input-alice.txt -mapper "python wc.py map" -reducer "python wc.py reduce" -file wc.py -jobconf mapred.job.name=python wc.py -io typedbytes -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat -    inputformat AutoInputFormat]
    11/01/17 20:22:31 WARN streaming.StreamJob: -jobconf option is deprecated, please use -D instead.
    packageJobJar: [wc.py, /var/lib/hadoop-0.20/cache/brandyn/hadoop-unjar464849802654976085/] [] /tmp/streamjob1822202887260165136.jar tmpDir=null
    11/01/17 20:22:32 INFO mapred.FileInputFormat: Total input paths to process : 1
    11/01/17 20:22:32 INFO streaming.StreamJob: getLocalDirs(): [/var/lib/hadoop-0.20/cache/brandyn/mapred/local]
    11/01/17 20:22:32 INFO streaming.StreamJob: Running job: job_201101141644_0723
    11/01/17 20:22:32 INFO streaming.StreamJob: To kill this job, run:
    11/01/17 20:22:32 INFO streaming.StreamJob: /usr/lib/hadoop-0.20/bin/hadoop job  -Dmapred.job.tracker=vitrieve03.pc.umiacs.umd.edu:8021 -kill job_201101141644_0723
    11/01/17 20:22:32 INFO streaming.StreamJob: Tracking URL: http://vitrieve03.pc.umiacs.umd.edu:50030/jobdetails.jsp?jobid=job_201101141644_0723
    11/01/17 20:22:33 INFO streaming.StreamJob:  map 0%  reduce 0%
    11/01/17 20:22:40 INFO streaming.StreamJob:  map 50%  reduce 0%
    11/01/17 20:22:41 INFO streaming.StreamJob:  map 100%  reduce 0%
    11/01/17 20:22:52 INFO streaming.StreamJob:  map 100%  reduce 100%
    11/01/17 20:22:55 INFO streaming.StreamJob: Job complete: job_201101141644_0723
    11/01/17 20:22:55 INFO streaming.StreamJob: Output: playground/out/

Output is the command used

    >>> print(cmd)
    hadoop jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2+737.jar -output playground/out/ -input playground/wc-input-alice.txt -mapper "python wc.py map" -reducer "python wc.py reduce" -file wc.py -jobconf mapred.job.name=python wc.py -io typedbytes -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat -inputformat AutoInputFormat

Lets see what the output looks like

    >>> out = list(hadoopy.cat('playground/out'))
    >>> out[:10]
    [('*', 60), ('-', 7), ('3', 2), ('4', 1), ('A', 8), ('I', 260), ('O', 1), ('a', 662), ('"I', 7), ("'A", 9)]
    >>> out.sort(lambda x, y: cmp(x[1], y[1]))
    >>> out[-10:]
    [('was', 329), ('it', 356), ('in', 401), ('said', 416), ('she', 484), ('of', 596), ('a', 662), ('to', 773), ('and', 780), ('the', 1664)]


API
---

..  function:: hadoopy.run(mapper=None, reducer=None, combiner=None, **kw)

    This is to be called in all Hadoopy job's.  Handles arguments passed in, calls the provided functions with input, and stores the output.

    TypedBytes are used if (os.environ['stream_map_input'] == 'typedbytes') which is a jobconf variable set in all jobs Hadoop is using TypedBytes with.

    It is *highly* recommended that TypedBytes be used for all non-trivial tasks.  Keep in mind that the semantics of what you can safely emit from your functions is limited when using Text (i.e., no \\t or \\n).  You can use the base64 module to ensure that your output is clean.

    | **Command Interface**
    | The command line switches added to your script (e.g., script.py) are

    python script.py map
        Use the provided mapper
    python script.py reduce
        Use the provided reducer
    python script.py combine
        Use the provided combiner
    python script.py freeze <tar_path> <-Zadd_file0 -Zadd_file1...> <cx_Freeze args>
        Freeze the script to a tar file specified by <tar_path>.  The extension may be .tar or .tar.gz.  All files are placed in the root of the tar. Files specified with -Z will be added to the tar root.  Additional cx_Freeze arguments may be passed in.
    
    | **Specification of mapper/reducer/combiner** 
    | Input Key/Value Types

        | For TypedBytes, the type will be the decoded typed
        | For Text, the type will be text assuming key0\\tvalue0\\nkey1\\tvalue1\\n

    Output Key/Value Types

        | For TypedBytes, anything Pickle-able can be used
        | For Text, types are converted to string.  Note that neither may contain \\t or \\n as these are used in the encoding.  Output is key\\tvalue\\n
    
    Expected arguments

        | mapper(key, value) or mapper.map(key, value)
        | reducer(key, values) or reducer.reduce(key, values)
        | combiner(key, values) or combiner.combine(key, values)

    Optional methods

        | func.configure(): Call first.  Returns None.
        | func.close():  Call last.  Returns Iterator of (key, value) or None

    Expected return
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

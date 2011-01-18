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
Python Source (fully documented version in tests/wc.py) ::

    """Hadoopy Wordcount Demo"""
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
        hadoopy.run(mapper, reducer, doc=__doc__)

Command line test (run without args, it prints the docstring and quits because of doc=__doc__) ::

    $ python wc.py
    Hadoopy Wordcount Demo

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

We can also do this in Python

    >>> import hadoopy
    >>> hadoopy.ls('playground/')
    ['/user/brandyn/playground/wc-input-alice.tb', '/user/brandyn/playground/wc-input-alice.txt', '/user/brandyn/playground/wc-input-alice.txt.gz']

Lets put wc-input-alice.txt through the word counter using Hadoop.  Each node in the cluster has Hadoopy installed (later we will show that it isn't necessary with launch_frozen).  Note that it is using typedbytes, SequenceFiles, and the AutoInputFormat by default.

    >>> cmd = hadoopy.launch('playground/wc-input-alice.txt', 'playground/out/', 'wc.py')
    HadooPY: Running[hadoop jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2+737.jar -output playground/out/ -input playground/wc-input-alice.txt -mapper "python wc.py map" -reducer "python wc.py reduce" -file wc.py -jobconf mapred.job.name=python wc.py -io typedbytes -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat -    inputformat AutoInputFormat]
    11/01/17 20:22:31 WARN streaming.StreamJob: -jobconf option is deprecated, please use -D instead.
    packageJobJar: [wc.py, /var/lib/hadoop-0.20/cache/brandyn/hadoop-unjar464849802654976085/] [] /tmp/streamjob1822202887260165136.jar tmpDir=null
    11/01/17 20:22:32 INFO mapred.FileInputFormat: Total input paths to process : 1
    11/01/17 20:22:32 INFO streaming.StreamJob: getLocalDirs(): [/var/lib/hadoop-0.20/cache/brandyn/mapred/local]
    11/01/17 20:22:32 INFO streaming.StreamJob: Running job: job_201101141644_0723
    11/01/17 20:22:32 INFO streaming.StreamJob: To kill this job, run:
    11/01/17 20:22:32 INFO streaming.StreamJob: /usr/lib/hadoop-0.20/bin/hadoop job  -Dmapred.job.tracker=umiacs.umd.edu:8021 -kill job_201101141644_0723
    11/01/17 20:22:32 INFO streaming.StreamJob: Tracking URL: http://umiacs.umd.edu:50030/jobdetails.jsp?jobid=job_201101141644_0723
    11/01/17 20:22:33 INFO streaming.StreamJob:  map 0%  reduce 0%
    11/01/17 20:22:40 INFO streaming.StreamJob:  map 50%  reduce 0%
    11/01/17 20:22:41 INFO streaming.StreamJob:  map 100%  reduce 0%
    11/01/17 20:22:52 INFO streaming.StreamJob:  map 100%  reduce 100%
    11/01/17 20:22:55 INFO streaming.StreamJob: Job complete: job_201101141644_0723
    11/01/17 20:22:55 INFO streaming.StreamJob: Output: playground/out/

Return value is the command used

    >>> print(cmd)
    hadoop jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2+737.jar -output playground/out/ -input playground/wc-input-alice.txt -mapper "python wc.py map" -reducer "python wc.py reduce" -file wc.py -jobconf mapred.job.name=python wc.py -io typedbytes -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat -inputformat AutoInputFormat

Lets see what the output looks like.

    >>> out = list(hadoopy.cat('playground/out'))
    >>> out[:10]
    [('*', 60), ('-', 7), ('3', 2), ('4', 1), ('A', 8), ('I', 260), ('O', 1), ('a', 662), ('"I', 7), ("'A", 9)]
    >>> out.sort(lambda x, y: cmp(x[1], y[1]))
    >>> out[-10:]
    [('was', 329), ('it', 356), ('in', 401), ('said', 416), ('she', 484), ('of', 596), ('a', 662), ('to', 773), ('and', 780), ('the', 1664)]

Note that the output is stored in SequenceFiles and each key/value is stored encoded as TypedBytes, by using cat you don't have to worry about any of that (if the output was compressed it would also be decompressed here).  This can also be done inside of a job for getting additional side-data off of HDFS.

What if we don't want to install python, numpy, scipy, or your-custom-code-that-always-changes on every node in the cluster?  We have you covered there too.  I'll remove hadoopy from all nodes except for the one executing the job. ::

    $ sudo rm -r /usr/local/lib/python2.6/dist-packages/hadoopy*

Now it's gone

    >>> import hadoopy
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: No module named hadoopy

The rest of the nodes were cleaned up the same way.  We modify the command, note that we now get the output from cx_Freeze at the top ::

    >>> cmd = hadoopy.launch_frozen('playground/wc-input-alice.txt', 'playground/out_frozen/', 'wc.py')
    Missing modules:
    ? _md5 imported from hashlib
    ? _scproxy imported from urllib
    ? _sha imported from hashlib
    ? _sha256 imported from hashlib
    ? _sha512 imported from hashlib

    HadooPY: Running[hadoop jar /usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2+737.jar -output playground/out_frozen/ -input playground/wc-input-alice.txt -mapper "wc map" -reducer "wc reduce" -file frozen/_codecs_tw.so -file frozen/_codecs_cn.so -file frozen/sgmlop.so -file frozen/_codecs_iso2022.so -file frozen/_main.so -file frozen/_ssl.so -file frozen/_codecs_hk.so -file frozen/_codecs_jp.so -file frozen/_multibytecodec.so -file frozen/datetime.so -file frozen/_codecs_kr.so -file frozen/mmap.so -file frozen/readline.so -file frozen/_heapq.so -file frozen/bz2.so -file frozen/_typedbytes.so -file frozen/_ctypes.so -file frozen/_hashlib.so -file frozen/_multiprocessing.so -file frozen/pyexpat.so -file frozen/libpython2.6.so.1.0 -file frozen/termios.so -file frozen/wc -jobconf mapred.job.name=wc -io typedbytes -outputformat org.apache.hadoop.mapred.SequenceFileOutputFormat -inputformat AutoInputFormat]
    11/01/17 20:55:00 WARN streaming.StreamJob: -jobconf option is deprecated, please use -D instead.
    packageJobJar: [frozen/_codecs_tw.so, frozen/_codecs_cn.so, frozen/sgmlop.so, frozen/_codecs_iso2022.so, frozen/_main.so, frozen/_ssl.so, frozen/_codecs_hk.so, frozen/_codecs_jp.so, frozen/_multibytecodec.so, frozen/datetime.so, frozen/_codecs_kr.so, frozen/mmap.so, frozen/readline.so, frozen/_heapq.so, frozen/bz2.so, frozen/_typedbytes.so, frozen/_ctypes.so, frozen/_hashlib.so, frozen/_multiprocessing.so, frozen/pyexpat.so, frozen/libpython2.6.so.1.0, frozen/termios.so, frozen/wc, /var/lib/hadoop-0.20/cache/brandyn/hadoop-unjar6437825264052222661/] [] /tmp/streamjob9089438158340520087.jar tmpDir=null
    11/01/17 20:55:02 INFO mapred.FileInputFormat: Total input paths to process : 1
    11/01/17 20:55:02 INFO streaming.StreamJob: getLocalDirs(): [/var/lib/hadoop-0.20/cache/brandyn/mapred/local]
    11/01/17 20:55:02 INFO streaming.StreamJob: Running job: job_201101141644_0724
    11/01/17 20:55:02 INFO streaming.StreamJob: To kill this job, run:
    11/01/17 20:55:02 INFO streaming.StreamJob: /usr/lib/hadoop-0.20/bin/hadoop job  -Dmapred.job.tracker=umiacs.umd.edu:8021 -kill job_201101141644_0724
    11/01/17 20:55:02 INFO streaming.StreamJob: Tracking URL: http://umiacs.umd.edu:50030/jobdetails.jsp?jobid=job_201101141644_0724
    11/01/17 20:55:03 INFO streaming.StreamJob:  map 0%  reduce 0%
    11/01/17 20:55:09 INFO streaming.StreamJob:  map 50%  reduce 0%
    11/01/17 20:55:11 INFO streaming.StreamJob:  map 100%  reduce 0%
    11/01/17 20:55:21 INFO streaming.StreamJob:  map 100%  reduce 100%
    11/01/17 20:55:24 INFO streaming.StreamJob: Job complete: job_201101141644_0724
    11/01/17 20:55:24 INFO streaming.StreamJob: Output: playground/out_frozen/

And lets check the output

    >>> out = list(hadoopy.cat('playground/out_frozen'))
    >>> out[:10]
    [('*', 60), ('-', 7), ('3', 2), ('4', 1), ('A', 8), ('I', 260), ('O', 1), ('a', 662), ('"I', 7), ("'A", 9)]
    >>> out.sort(lambda x, y: cmp(x[1], y[1]))
    >>> out[-10:]
    [('was', 329), ('it', 356), ('in', 401), ('said', 416), ('she', 484), ('of', 596), ('a', 662), ('to', 773), ('and', 780), ('the', 1664)]

We can also generate a tar of the frozen script (useful when working with Oozie).  Note the 'wc' is not wc.py, it is actually a self contained executable. ::

    $ python wc.py freeze wc.tar.gz
    Missing modules:
    ? _md5 imported from hashlib
    ? _scproxy imported from urllib
    ? _sha imported from hashlib
    ? _sha256 imported from hashlib
    ? _sha512 imported from hashlib
    $ tar -tzf wc.tar.gz 
    _codecs_tw.so
    _codecs_cn.so
    sgmlop.so
    _codecs_iso2022.so
    _main.so
    _codecs_hk.so
    _codecs_jp.so
    _multibytecodec.so
    datetime.so
    _codecs_kr.so
    mmap.so
    readline.so
    _heapq.so
    bz2.so
    _typedbytes.so
    _ctypes.so
    _multiprocessing.so
    pyexpat.so
    libpython2.6.so.1.0
    termios.so
    wc

Lets open it up and try it out ::

    $ tar -xzf wc.py
    $ ./wc
    Hadoopy Wordcount Demo
    $ python wc.py 
    Hadoopy Wordcount Demo
    $ hexdump -C wc | head -n5
    00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
    00000010  02 00 3e 00 01 00 00 00  80 41 40 00 00 00 00 00  |..>......A@.....|
    00000020  40 00 00 00 00 00 00 00  50 04 16 00 00 00 00 00  |@.......P.......|
    00000030  00 00 00 00 40 00 38 00  09 00 40 00 1d 00 1c 00  |....@.8...@.....|
    00000040  06 00 00 00 05 00 00 00  40 00 00 00 00 00 00 00  |........@.......|


That's a quick tour of Hadoopy.

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

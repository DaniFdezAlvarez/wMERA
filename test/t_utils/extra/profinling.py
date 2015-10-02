__author__ = 'Dani'
try:
    import cProfile as Prof
except:
    import profile as Prof

Prof.run("import test.test_generators.generate_large_ttl_discogs_release", sort='cumulative')

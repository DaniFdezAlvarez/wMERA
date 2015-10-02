import json
import math

from wmera.word_utils import extract_unique_ngrams


correct_arr = ["Correct", "correct", "Complete and Correct"]
out = {"listdocs": {}, "index": {}}

with open("../files/discogs_artist.tsv", "r") as tsv_artist:
    docid = 0
    err_count = 0
    with open("../files/fulltext.data", "w") as result_file:
        for line in tsv_artist:  # Iterator retrieving lines of the file
            candidate_line = line.lower().replace("\n", "").replace("\r", "").split("\t")
            # Filtering empty results

            if len(candidate_line) != 5:
                err_count += 1
            else:
                # Potential arrays (real_name, name_vars, aliases) are turned into an array
                # even if they are empty (empty array) or formed by a single element (array of one element)
                name = candidate_line[0]
                real_name = candidate_line[1].split("|")
                data_quality = candidate_line[2]
                name_variations = candidate_line[3].split("|")
                aliases = candidate_line[4].split("|")

                # Filtering results of non max quality
                if data_quality in correct_arr:
                    # We are going to have a "document" per alias, name variation, etc.
                    documents = [name]
                    for var in real_name:
                        if "" != var:
                            documents.append(var)
                    for var in name_variations:
                        if "" != var:
                            documents.append(var)
                    for var in aliases:
                        if "" != var:
                            documents.append(var)

                    # We process each document
                    ngrams_dict = {}
                    for doc in documents:
                        # We obtain n-grams but we are only interested if they are
                        # present or not in a given "document", not how many times
                        # they appear
                        ngrams = extract_unique_ngrams(doc)
                        # However, we need to known in how many variations for an
                        # artist's name each ngram appears.
                        for ng in ngrams:
                            if ng in ngrams_dict:
                                ngrams_dict[ng] += 1
                            else:
                                ngrams_dict[ng] = 1
                    
                    # We need to associate each document id with an artist's name
                    # As Labra said, much better using an URI instead of a name.
                    #
                    # We also store the number of "documents" associated with each
                    # artist. That will be used later to "normalize" the scores.
                    # The idea is to avoid a "total artist" (one having plenty of
                    # names and aliases) to match every possible query.

                    out["listdocs"][str(docid) + "|" + str(len(documents))] = name

                    # We store the documents associated with a given document id
                    # This will be used later during searching.
                    result_file.write(str(docid) + "\t" + json.dumps(documents) + "\n")

                    # The information about weights (aka TF) is stored for each
                    # pair (document, ngram).
                    # IDF values are, obviously, computed in a later phase, once
                    # we know how many artis are in the database.

                    for ngram in ngrams_dict:
                        if ngram not in out["index"]:
                            out["index"][ngram] = {}
                        out["index"][ngram][docid] = ngrams_dict[ngram]

                    if docid % 1000 == 0:
                        print name + "\t" + str(docid)

                    docid += 1


# Now we have to compute IDF (inverse document frequency)...

out["idfs"] = {}
numdocs = len(out["listdocs"])
for ngram in out["index"]:
    if len(out["index"][ngram]) > 1:
        out["idfs"][ngram] = math.log(numdocs / len(out["index"][ngram]))


# We store the index in a file

with open("../files/index.data", "w") as index_file:
    line_arr = []
    for docid in out["listdocs"]:
        line_arr.append(docid + ":" + str(out["listdocs"][docid]))
    index_file.write("\t".join(line_arr) + "\n")

print "Index saved"

with open("../files/index.data", "a") as index_file:
    # Then the IDF values for each ngram
    line_arr = []
    for ngram in out["idfs"]:
        line_arr.append(ngram + ":" + str(out["idfs"][ngram]))
    index_file.write("\t".join(line_arr) + "\n")

    # Finally the actual index is stored

print "Idf saved"
with open("../files/index.data", "a") as index_file:
    for ngram in out["index"]:
        line_arr = []
        for docid in out["index"][ngram]:
            line_arr.append(str(docid) + ":" + str(out["index"][ngram][docid]))
        line = ngram + "\t" + "\t".join(line_arr) + "\n"
        index_file.write(line)


print "Index saved to disk"



















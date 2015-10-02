__author__ = 'Dani'


the_in = "../../../files/discogs_releases.xml"
the_out = "5000_lines_discogs_releases.xml"

n_lines = 50000
with open(the_in, "r") as thein:
    with open(the_out, "w") as theout:
        counter = 0
        for line in thein:
            counter += 1
            if counter % 100 == 0:
                print counter
            if counter > n_lines:
                break
            theout.write(line)




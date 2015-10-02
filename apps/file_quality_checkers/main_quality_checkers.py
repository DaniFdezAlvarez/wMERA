__author__ = 'Dani'



class AolQualityChecker(object):

    def run(self, file_path):
        report = ""
        good = 0
        bad = 0
        with open(file_path, "r") as file_io:
            file_io.readline()
            for line in file_io:
                sub_report = self.check_line(line)
                if sub_report is not None:
                    bad += 1
                    report += sub_report + "  -->  {" + line + "}\n"
                else:
                    good += 1
        report = "Good:: " + str(good) + "\n" + "Bad: " + str(bad)+ "\n" + report
        return report

    def check_line(self, line):
        line = line.replace("\n", "")
        if line == "":
            return None
        pieces = line.split("\t")
        if len(pieces) < 9:
            return "Not enough fields"
        #0 --> file
        if pieces[0] not in ["w", "k"]:
            return "Source file wrong specified[0]"
        #1 --> number of line
        try:
            int(pieces[1])
        except:
            return "Wrong number of line[1]"
        #2 --> number of artist
        try:
            int(pieces[2])
        except:
            return "Wrong number of artist[2]"
        if len(pieces) != 8 + int(pieces[2]):
            return "Not coherent number of fields[2]"
        #3 --> Original query
        #4 --> Song
        if pieces[4] == "":
            return "Song missing[4]"
        #5 + number of artists
        for i in range(5, int(pieces[2])):
            if pieces[i] == "":
                return "Artist missing[5]"
        #-1 ---> discogs if
        if "[" not in pieces[-1] or "]" not in pieces[-1] or pieces[-1].endswith("]"):
            return "Wrong or missing discogs identifier[-1]"
        #-2 --> Comment
        #-3 --> Found not found
        if pieces[-3] not in ["V", "X"]:
            return "Wrong found/not found[-3]"
        return None  # All OK


class MusicBrainzQualityChecker(object):

    def run(self, file_path):
        report = ""
        good = 0
        bad = 0
        with open(file_path, "r") as file_io:
            file_io.readline()
            for line in file_io:
                sub_report = self.check_line(line)
                if sub_report is not None:
                    bad += 1
                    report += sub_report + "  -->  {" + line + "}\n"
                else:
                    good += 1
        report = "Good:: " + str(good) + "\n" + "Bad: " + str(bad)+ "\n" + report
        return report

    def check_line(self, line):
        line = line.replace("\n", "")
        if line == "":
            return None
        pieces = line.split("\t")
        if len(pieces) != 6:
            return "Wrong number of fields"
        #0 --> discogs file index
        try:
            int(pieces[0])
        except:
            return "Wrong or missing index in file ID[0]"

        #1 --> discogs id
        if "[" not in pieces[1] or "]" not in pieces[1] or pieces[1].endswith("]") or pieces[1][1] != "r":
            return "Wrong or missing discogs identifier[1]"

        #2 --> number of artist
        try:
            int(pieces[2])
        except:
            return "Wrong or missing number of related people[2]"
        #3 --> Song
        if pieces[3] == "":
            return "Missing song[3]"
        #4 --> artists
        nArt = 0
        if not pieces[4] == "-":
            if pieces[4] == "":
                return "Missing artists[4]"
            else:
                artists = pieces[4].split("|")
                for artist in artists:
                    if artist == "":
                        return "Missin one of the artists[4]"
                nArt += len(artists)
        #5 --> writers
        nWri = 0
        if not pieces[5] == "-":
            if pieces[5] == "":
                return "Missing writers[5]"
            else:
                writers = pieces[5].split("|")
                for writer in writers:
                    if writer == "":
                        return "Missin one of the writers[5]"
                nWri += len(writers)
        # Coherence
        if int(pieces[2]) != nWri + nArt:
            return "Wrong number of artist+writers[2]"

        return None  # All OK



report_aol = AolQualityChecker().run("files/random_final_queries_without_discarded.txt")
print "AOL"
print report_aol
print "------------"
report_MB = MusicBrainzQualityChecker().run("files/random_musicbrainz.tsv")
print "MUSIC BRAINZ"
print report_MB
print "------------"

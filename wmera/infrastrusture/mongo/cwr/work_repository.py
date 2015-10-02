__author__ = 'Dani', 'borja'

from random import randint

from bson.code import Code

from wmera.infrastrusture.mongo.mongo_generic_repository import MongoGenericRepository


class WorkRepository(MongoGenericRepository):
    def __init__(self, url_root):
        super(WorkRepository, self).__init__(url_root, 'works')
        self._db[self.collection].ensure_index('title')

    def find_works_by_submitter(self, submitter_id):
        works = list(self._db[self.collection].find({'submitter_id': submitter_id}))

        if works is None:
            return "Work not found"

        return works

    def find_work_by_submitter_id(self, submitter_id, work_number):
        work = self._db[self.collection].find_one({'submitter_id': submitter_id, 'agreement_number': work_number})

        return work

    def find_works_by_title(self, work_title):
        works = list(self._db[self.collection].find({'title': work_title}))

        return works

    def find_works_by_titles(self, work_titles):
        works = list(self._db[self.collection].find({'title': {'$in': work_titles}}))

        return works

    def find_random_writer_names(self, num_of_writers=100):
        #TODO: quite far form being efficient
        result = []
        valid_count = 0
        while valid_count < num_of_writers:
            work = self._find_random_work()
            if self._is_work_with_complete_writer(work):
                result.append(self._get_writers_from_work(work, just_one=True))
                valid_count += 1
        return result

    def find_all_writer_names_generator(self):
        for work in self.find_all_works_generator():
            if self._is_work_with_complete_writer(work):
                for name in self._get_writers_from_work(work):
                    yield str(name)

    def find_all_works_generator(self):
        for work in self._db[self.collection].find():
            yield work


    @staticmethod
    def _get_writers_from_work(work, just_one=False):
        if just_one:
            return work["writers"][0]["first_name"].strip() + ' ' + work["writers"][0]["last_name"].strip()
        else:
            result =[]
            for writer in work["writers"]:
                if writer["first_name"] not in ["", None] and writer["last_name"] not in ["", None]:
                    result.append(writer["first_name"].strip() + ' ' + writer["last_name"].strip())
            return result

    @staticmethod
    def _is_work_with_complete_writer(work):
        if "writers" not in work:
            return False
        if len(work["writers"]) == 0:
            return False
        if "last_name" not in work["writers"][0] or "first_name" not in work["writers"][0]:
            return False
        if work["writers"][0]["last_name"] in ["", None] or work["writers"][0]["first_name"] in ["", None]:
            return False
        return True


    def _find_random_work(self):
        if "_total_works" not in self.__dict__:  # Potentially wrong
            self._total_works = self._db[self._collection].count()
        return self._db[self._collection].find().limit(1).\
            skip(randint(0, self._total_works)).\
            next()


    def create_idf_index_to_artist(self):
        function_map = Code('function (){'
                            'var pattern = /[ _\-]+/g;'
                            'var tokens = [];'
                            'var a_person;'
                            'var complete_name;'
                            'var tokens_name;'
                            'var writers = this.writers;'
                            'var performers = this.performers;'
                            'for (var j = 0; j < writers.length; j++){'
                            'a_person = writers[j];'
                            'complete_name = a_person["first_name"] + a_person["last_name"];'
                            'tokens_name = complete_name.replace(pattern, " ").split(" ");'
                            'for (var i =0; i < tokens_name.length; i++){'
                            'tokens.push(tokens_name[i]);'
                            '}'
                            '}'

                            'for (j = 0; j < performers.length; j++){'
                            'a_person = performers[j];'
                            'complete_name = a_person["first_name"] + a_person["last_name"];'
                            'tokens_name = complete_name.replace(pattern, " ").split(" ");'
                            'for (i =0; i < tokens_name.length; i++){'
                            'tokens.push(tokens_name[i]);'
                            '}'
                            '}'
                            'for (var k = 0; k < tokens.length; k++){'
                            'emit(tokens[k], 1);'
                            '}'
                            '}')
        function_reduce = Code("function(key, values){"
                               "return Array.sum(values);"
                               "}")
        self._db[self.collection].map_reduce(map=function_map,
                                             reduce=function_reduce,
                                             out="idf_artist")


    def create_idf_index_to_titles(self):
        function_map = Code('function (){'
                            'var pattern = /[ _\-]+/g;'
                            'var clean_title = this.title.replace(pattern, " ");'
                            'var tokens = clean_title.split(" ");'
                            'var alternatives = this.alternative_titles;'
                            'for (a_title in alternatives){'
                            'var new_tokens = alternatives[a_title]["title"].replace(pattern, " ").split(" ");'
                            'for (var k = 0; 0 < new_tokens.lenght; k++){'
                            'tokens.push(new_tokens[k]);'
                            '}'
                            '}'
                            'for (var i = 0; i < tokens.length; i++){'
                            'emit(tokens[i], 1);'
                            '}'
                            '}')
        function_reduce = Code("function(key, values){"
                               "return Array.sum(values);"
                               "}")
        self._db[self.collection].map_reduce(map=function_map,
                                             reduce=function_reduce,
                                             out="idf_songs")

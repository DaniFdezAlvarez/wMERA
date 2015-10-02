__author__ = 'Dani'


class Artist(object):
    def __init__(self, name, data_quality=None, real_name=None, name_variations=None, aliases=None):
        self.name = name
        self.data_quality = data_quality
        self.real_name = real_name if real_name is not None else []
        self.name_variations = name_variations if name_variations is not None else []
        self.aliases = aliases if aliases is not None else []

    def add_real_name(self, realname):
        self.real_name.append(realname)

    def add_name_variation(self, name_variation):
        self.name_variations.append(name_variation)

    def add_alias(self, alias):
        self.aliases.append(alias)

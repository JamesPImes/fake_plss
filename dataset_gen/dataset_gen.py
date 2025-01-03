
"""
Simulate PLSS land descriptions, optionally with intentional errors.
"""

import random

# All floats are weights (out of 1.0) of how common they should appear.
# (Approximates how commonly I see them in real data, or how I want to skew the dataset.)

PM = {
    'principal meridian': 0.8,
    'p.m.': 1.0,
    'pm': 0.2,
}
# Reference: https://en.wikipedia.org/wiki/List_of_principal_and_guide_meridians_and_base_lines_of_the_United_States
PM_IDS = [
    '1st',
    '1',
    'first',
    '2nd',
    '2',
    'second',
    '3rd',
    '3',
    'third',
    '4th',
    '4',
    'fourth',
    '5th',
    '5',
    'fifth',
    '6th',
    '6',
    'sixth',
    'black hills',
    'boise',
    'chickasaw',
    'choctaw',
    'cimarron',
    'copper river',
    'fairbanks',
    'gila and salt river',
    'humboldt',
    'huntsville',
    'mississippi',
    'indian',
    'kateel river',
    'louisiana',
    'michigan',
    'ohio',
    'montana',
    'mount diablo',
    'nevada',
    'navajo',
    'new mexico',
    'st. helena',
    'st. stephens',
    'mississippi',
    'salt lake',
    'san bernardino',
    'seward',
    'tallahassee',
    'uintah',
    'umiat',
    'ute',
    'washington',
    'willamette',
    'washington',
    'wind river',
]
TOWNSHIP = {
    'township': 1.0,
    'twp': 1.0,
    'twp.': 0.7,
    'tw.': 0.03,
    't': 0.7,
    't.': 0.4,
    '': 0.1,
}
RANGE = {
    'range': 1.0,
    'rnge': 0.02,
    'rng': 0.05,
    'rge': 0.5,
    'rge.': 0.3,
    'r': 0.7,
    'r.': 0.4,
    '': 0.1,
}
TWPRGE_REQUIRE_SPACE = [
    'township',
    'twp',
    'twp.',
    'tw.',
    'range',
    'rnge',
    'rng',
    'rge',
    'rge.'
]
SECTION = {
    'section': 1.0,
    'sec': 1.0,
    'sec.': 0.3,
    'sect': 0.02,
    'sect.': 0.01,
    '§': 0.02,
}
LOT = {
    'lot': 1.0,
    # 'governmental lot': 0.04,
    'l': 0.2,
    'l.': 0.03
}
SECTION_LOT_NOSPACE_OK = [
    '§',
    'l',
    'l.'
]
PLURAL_DISALLOWED = [
    # Lot abbreviations to disallow -- i.e., disallow 'ls' for "Lots"
    'l',
    'l.',
    # 'Section' abbreviations to disallow -- i.e., disallow '§s' for "Sections"
    '§',
    'sec.',
    'sect.',
]
NORTH_WORD = {
    'north': 1.0,
}
SOUTH_WORD = {
    'south': 1.0,
}
EAST_WORD = {
    'east': 1.0,
}
WEST_WORD = {
    'west': 1.0,
}
NORTH_ABBREV = {
    'n': 0.8,
}
SOUTH_ABBREV = {
    's': 0.8,
}
EAST_ABBREV = {
    'e': 0.8,
}
WEST_ABBREV = {
    'w': 0.8,
}

NORTH = {}
NORTH.update(NORTH_WORD)
NORTH.update(NORTH_ABBREV)
SOUTH = {}
SOUTH.update(SOUTH_WORD)
SOUTH.update(SOUTH_ABBREV)
EAST = {}
EAST.update(EAST_WORD)
EAST.update(EAST_ABBREV)
WEST = {}
WEST.update(WEST_WORD)
WEST.update(WEST_ABBREV)

NORTHEAST_WORD = {
    'northeast': 1.0,
    'north-east': 0.05,
    'north east': 1.0,
}
NORTHWEST_WORD = {
    'northwest': 1.0,
    'north-west': 0.05,
    'north west': 1.0,
}
SOUTHEAST_WORD = {
    'southeast': 1.0,
    'south-east': 0.05,
    'south east': 1.0,
}
SOUTHWEST_WORD = {
    'southwest': 1.0,
    'south-west': 0.05,
    'south west': 1.0,
}
NORTHEAST_ABBREV = {
    'ne': 1.0,
    'n.e.': 0.02,
}
NORTHWEST_ABBREV = {
    'nw': 1.0,
    'n.w.': 0.02,
}
SOUTHEAST_ABBREV = {
    'se': 1.0,
    's.e.': 0.02,
}
SOUTHWEST_ABBREV = {
    'sw': 1.0,
    's.w.': 0.02,
}
ALIQUOT_HALVES_WORD = [NORTH_WORD, SOUTH_WORD, EAST_WORD, WEST_WORD]
ALIQUOT_HALVES_ABBREV = [NORTH_ABBREV, SOUTH_ABBREV, EAST_ABBREV, WEST_ABBREV]
ALIQUOT_HALF_ELEMENTS = []
for d in ALIQUOT_HALVES_WORD:
    ALIQUOT_HALF_ELEMENTS.extend(d.keys())
for d in ALIQUOT_HALVES_ABBREV:
    ALIQUOT_HALF_ELEMENTS.extend(d.keys())

ALIQUOT_QUARTERS_WORD = [NORTHEAST_WORD, NORTHWEST_WORD, SOUTHEAST_WORD, SOUTHWEST_WORD]
ALIQUOT_QUARTERS_ABBREV = [NORTHEAST_ABBREV, NORTHWEST_ABBREV, SOUTHEAST_ABBREV, SOUTHWEST_ABBREV]
ALIQUOT_QUARTER_ELEMENTS = []
for d in ALIQUOT_QUARTERS_WORD:
    ALIQUOT_QUARTER_ELEMENTS.extend(d.keys())
for d in ALIQUOT_QUARTERS_ABBREV:
    ALIQUOT_QUARTER_ELEMENTS.extend(d.keys())

NS_COMPATIBLE_WORD = [NORTH_WORD, SOUTH_WORD]
NS_COMPATIBLE_ABBREV = [NORTH_ABBREV, SOUTH_ABBREV]
EW_COMPATIBLE_WORD = [EAST_WORD, WEST_WORD]
EW_COMPATIBLE_ABBREV = [EAST_ABBREV, WEST_ABBREV]

HALF_WORD = {
    'half': 1.0,
    '1/2': 0.4,  # compatible with unabbreviated halves (e.g., "north 1/2")
}
HALF_FRAC = {
    ' 1/2': 0.4,
    '1/2': 0.3,
    '/2': 0.8,
    '2': 0.8,
    '½': 0.8,
}
QUARTER_WORD = {
    'quarter': 1.0,
    'qrtr': 0.02,
    '1/4': 0.4,  # compatible with unabbreviated quarters (e.g., "northeast 1/4")
}
QUARTER_FRAC = {
    ' 1/4': 0.4,
    '1/4': 0.3,
    '/4': 0.8,
    '4': 0.8,
    '¼': 0.8,
    '': 0.1,
}
UNABBREVIATED_ILLEGAL_FRACS = [
    '2',
    '/2',
    '4',
    '/4',
]
# N/2 of the NE/4
OF_THE = {
    '': 0.9,
    ' ': 0.1,
    ' of ': 0.03,
    ' of the ': 0.08,
}
OF_THE_BLANK = [
    '', ' ',
]
OF_THE_BLANK_DISALLOWED = [
    'half', 'qrtr', 'quarter'
]
ALL = {
    'all': 1.0,
}
MB_MARKERS = [
    'of the',
    'in the',
    'thence',
    'bearing',
    'rr',
    'railroad',
    'river',
    'right of way',
    'row',
    'highway',
    'road',
    'street',
    'as',
    'feet',
    'ft',
    'chains',
    'rods',
    'arc',
    'fence',
    'point of beginning',
    'original',
    'from',
    'of',
    'that part',
    'all that',
    'all of the',
    'all in the',
    'of the said',
    'said',
    'excluding',
    'except',
    'outlot',
    'tract',
    'parcel',
    'of land',
    'strip',
    'formerly',
]
THROUGH = {
    'through': 0.4,
    'thru': 0.1,
    '-': 1.0,
    '–': 1.0,
    '—': 0.1,
}
AND = {
    'and': 1.0,
    '&': 0.2,
    '+': 0.003,
}
REQUIRE_SPACE = [
    'through',
    'thru',
    'and',
    '&',
    '+'
]
QQ_COMMA = {
    ', ': 1.0,
    '; ': 0.02,
    ' and ': 0.02,
    ' & ': 0.005,
}
MULTISEC_COMMA = {
    ', ': 0.2,
    '; ': 0.02,
    ' and ': 1.0,
    ' & ': 0.4,
}
DESC_STR_OF_THE = {
    'of': 1.0,
    'in': 0.8,
    'all in': 0.6,
    'all of': 0.8,
    'lying in': 0.06,
    'all lying in': 0.03,
    ',': 0.5,
    ';': 0.1,
}

# with open('./resources/lorem_ipsum.txt', 'r') as f:
#     LOREM_IPSUM = '\n'.join(f.readlines())
# LOREM_IPSUM = LOREM_IPSUM.split()


class DatasetGenerator:

    def __init__(
            self,
            drop_twp_wt=0.0,
            drop_rge_wt=0.0,
            drop_sec_wt=0.0,
            drop_ns_wt=0.01,
            drop_ew_wt=0.01,
            misspell_twp_wt=0.0,
            misspell_rge_wt=0.0,
            misspell_sec_wt=0.0,
            qq_continue_wt=0.25,
            desc_continue_wt=0.5,
            multi_sec_wt=0.02,
            desc_abbrev_wt=0.8,
            frac_abbrev_wt=0.95,
            pm_wt=0.8,
            avail_twp: list = None,
            avail_rge: list = None,
            avail_sec: list = None,
            avail_lots: list = None,
    ):
        self.drop_twp_wt = drop_twp_wt
        self.drop_rge_wt = drop_rge_wt
        self.drop_sec_wt = drop_sec_wt
        self.drop_ns_wt = drop_ns_wt
        self.drop_ew_wt = drop_ew_wt
        self.qq_continue_wt = qq_continue_wt
        self.desc_continue_wt = desc_continue_wt
        self.misspell_twp_wt = misspell_twp_wt
        self.misspell_rge_wt = misspell_rge_wt
        self.misspell_sec_wt = misspell_sec_wt
        self.multi_sec_wt = multi_sec_wt
        self.desc_abbrev_wt = desc_abbrev_wt
        self.frac_abbrev_wt = frac_abbrev_wt
        self.pm_wt = pm_wt
        if avail_twp is None:
            avail_twp = list(range(1, 160))
        if avail_rge is None:
            avail_rge = list(range(1, 104))
        if avail_sec is None:
            avail_sec = list(range(1, 37))
        if avail_lots is None:
            avail_lots = list(range(1, 17))
        self.avail_twp = avail_twp
        self.avail_rge = avail_rge
        self.avail_sec = avail_sec
        self.avail_lots = avail_lots
    
    @staticmethod
    def choose_weighted(weight_dict: dict):
        """
        Choose 1 element from a dictionary of strings and their weights.
        :param weight_dict: 
        :return: 
        """
        return random.choices(list(weight_dict.keys()), weights=list(weight_dict.values()), k=1)[0]
    
    @staticmethod
    def roll(weight):
        """Roll a probability between 0 and 1. Return a bool."""
        return random.uniform(0, 1) <= weight
    
    @classmethod
    def misspell(cls, word: str, a: int = 1, b: int = None, drop_chance=0.1):
        """
        Randomly shuffle and/or drop letters in the ``word``.

        :param word: Word to misspell.
        :param a: Min number of characters to shuffle.
        :param b:  Max number of characters to shuffle.
        :param drop_chance: Chance to drop each character.
        :return: Misspelled word.
        """
        if not word:
            return word
        n = len(word)
        if b is None:
            b = n
        orig_idxs = random.sample(range(n), random.randint(min(a, n), min(b, n)))
        shuffle_idxs = orig_idxs.copy()
        random.shuffle(shuffle_idxs)
        chars = list(word)
        for i, j in zip(orig_idxs, shuffle_idxs):
            chars[i], chars[j] = chars[j], chars[i]
        # Iterate over the indexes (last to first).
        for i in sorted(orig_idxs, reverse=True):
            if cls.roll(drop_chance):
                chars.pop(i)
        return ''.join(chars)

    def gen_trs_desc(self):
        """
        Generate a PLSS description in the ``TRS_DESC`` layout.
        """
        all_components = self.gen_all_description_components()
        descriptions = []
        for twprge, sec_desc in all_components.items():
            compiled_sec_descs = []
            for sec, desc in sec_desc.items():
                compiled_sec_descs.append(f"{sec}: {desc}")
            compiled = f"{twprge}, {', '.join(compiled_sec_descs)}"
            descriptions.append(compiled)
        return ', '.join(descriptions)

    def gen_tr_desc_s(self):
        """
        Generate a PLSS description in the ``TR_DESC_S`` layout.
        """
        all_components = self.gen_all_description_components()
        descriptions = []
        of_the = self.choose_weighted(DESC_STR_OF_THE)
        of_the = f" {of_the} "
        for twprge, sec_desc in all_components.items():
            compiled_sec_descs = []
            for sec, desc in sec_desc.items():
                compiled_sec_descs.append(f"{desc}{of_the}{sec}")
            compiled = f"{twprge}, {', '.join(compiled_sec_descs)}"
            descriptions.append(compiled)
        return ', '.join(descriptions)

    def gen_desc_str(self):
        """
        Generate a PLSS description in the ``DESC_STR`` layout.
        """
        all_components = self.gen_all_description_components()
        descriptions = []
        of_the1 = self.choose_weighted(DESC_STR_OF_THE)
        of_the1 = f" {of_the1} "
        of_the2 = self.choose_weighted(DESC_STR_OF_THE)
        of_the2 = f" {of_the2} "
        for twprge, sec_desc in all_components.items():
            compiled_sec_descs = []
            for sec, desc in sec_desc.items():
                compiled_sec_descs.append(f"{desc}{of_the1}{sec}")
            compiled = f"{', '.join(compiled_sec_descs)}{of_the2}{twprge}"
            descriptions.append(compiled)
        return ', '.join(descriptions)

    def gen_s_desc_tr(self):
        """
        Generate a PLSS description in the ``S_DESC_TR`` layout.
        (This is not a commonly seen layout in real data.)
        """
        all_components = self.gen_all_description_components()
        descriptions = []
        of_the = self.choose_weighted(DESC_STR_OF_THE)
        of_the = f" {of_the} "
        for twprge, sec_desc in all_components.items():
            compiled_sec_descs = []
            for sec, desc in sec_desc.items():
                compiled_sec_descs.append(f"{sec}: {desc}")
            compiled = f"{', '.join(compiled_sec_descs)}{of_the}{twprge}"
            descriptions.append(compiled)
        return ', '.join(descriptions)

    def gen_all_description_components(
            self,
            min_twprge_ct=1,
            max_twprge_ct=4,
            min_sec_ct=1,
            max_sec_ct=4,
            twprge_continue_wt=0.1,
            sec_continue_wt=0.3
    ):
        """
        Generate all components necessary for a PLSS description.
        :param min_twprge_ct: Min number of Twp/Rge to generate.
        :param max_twprge_ct: Max number of Twp/Rge to generate.
        :param min_sec_ct: Min number of sections to generate for
         each Twp/Rge.
        :param max_sec_ct: Max number of sections to generate for
         each Twp/Rge.
        :param twprge_continue_wt: Likelihood of generating each
         additional Twp/Rge beyond the minimum (up to the max).
        :param sec_continue_wt: Likelihood of generating each
         additional section beyond the minimum (up to the max).
        :return: A nested dict of components.
        """
        twprges = {}
        while (len(twprges) < max_twprge_ct) and ((len(twprges) < min_twprge_ct) or self.roll(twprge_continue_wt)):
            twprges[self.gen_twprge()] = {}
        for twprge, desc_dict in twprges.items():
            while (len(desc_dict) < max_sec_ct) and ((len(desc_dict) < min_sec_ct) or self.roll(sec_continue_wt)):
                sec = self.gen_sec_or_multisec()
                desc_dict[sec] = self.gen_desc()
        return twprges

    def gen_twp(self):
        """
        Generate a Township (not including its range).
        :return:
        """
        twp_wd = self.choose_weighted(TOWNSHIP)
        space_req = twp_wd in TWPRGE_REQUIRE_SPACE
        if self.roll(self.misspell_twp_wt):
            twp_wd = self.misspell(twp_wd, a=2, b=4, drop_chance=0.1)
        if space_req:
            twp_wd = f"{twp_wd} "
        twp_num = random.choice(self.avail_twp)
        draw_from = NORTH
        if random.choice([0, 1]) == 0:
            draw_from = SOUTH
        ns = self.choose_weighted(draw_from)
        space1 = ' '
        if self.roll(0.9):
            space1 = ''
        space2 = ' '
        if ns in ('n', 's') and self.roll(0.9):
            space2 = ''
        return f"{twp_wd}{space1}{twp_num}{space2}{ns}"

    def gen_rge(self):
        """
        Generate a Range.
        :return:
        """
        rge_wd = self.choose_weighted(RANGE)
        space_req = rge_wd in TWPRGE_REQUIRE_SPACE
        if self.roll(self.misspell_rge_wt):
            rge_wd = self.misspell(rge_wd, a=1, b=3, drop_chance=0.1)
        if space_req:
            rge_wd = f"{rge_wd} "
        rge_num = random.choice(list(self.avail_rge))
        draw_from = WEST
        if random.choice([0, 1]) == 0:
            draw_from = EAST
        ew = self.choose_weighted(draw_from)
        space1 = ' '
        if rge_wd == 'r' and self.roll(0.9):
            space1 = ''
        space2 = ' '
        if ew in ('e', 'w') and self.roll(0.9):
            space2 = ''
        return f"{rge_wd}{space1}{rge_num}{space2}{ew}"

    def gen_sec(self):
        """
        Generate a single section.
        Ex: ``'section 4'``
        """
        sec_wd = self.choose_weighted(SECTION)
        sec_num = random.choice(self.avail_sec)
        space = ' '
        if sec_wd == '§':
            space = ''
        return f"{sec_wd}{space}{sec_num}"

    def gen_sec_or_multisec(self):
        """
        Generate a Section or Multi-Section, as rolled per the
        probability ``.multi_sec_wt``.

        Ex1:    ``'section 4'``
        Ex2:    ``'sections 4 - 6'``
        """
        if self.roll(self.multi_sec_wt):
            return self.gen_multisec()
        return self.gen_sec()

    @classmethod
    def choose_multiple(cls, choose_from: list, min_count=2, repeat_wt=0.01, reverse=False):
        """
        Generate a sorted list of elements.

        :param choose_from: A list of elements to choose from.
        :param min_count: The minimum number to select.
        :param repeat_wt: The probability of choosing each additional
         element after ``min_count`` is reached.
        :param reverse: If ``True``, sort the selection in reverse order.
        """
        if len(choose_from) < min_count:
            raise ValueError("length of `choose_from` must be >= `min_count`")
        chosen = set()
        avail = set(choose_from)
        new_choice = random.sample(list(avail), min_count)
        chosen.update(new_choice)
        avail -= chosen
        while (len(chosen) < min_count or cls.roll(repeat_wt)) and avail:
            new_choice = random.choice(list(avail))
            chosen.add(new_choice)
            avail.remove(new_choice)
        return sorted(chosen, reverse=reverse)

    def gen_pm(self):
        "Generate a principal meridian."
        pm_wd = self.choose_weighted(PM)
        pm_selection = random.choice(list(PM_IDS))
        return f"{pm_selection} {pm_wd}"
    
    def gen_twprge(self):
        """
        Generate a Township and Range, including possibly the
        principal meridian.
        :return:
        """
        twp = ''
        rge = ''
        if not self.roll(self.drop_twp_wt):
            twp = self.gen_twp()
        if not self.roll(self.drop_rge_wt):
            rge = self.gen_rge()
        twprge_connector = ''
        if twp and rge:
            twprge_connector = random.choice([', ', ' - ', '-'])
        pm = ''
        if self.roll(self.pm_wt):
            pm = self.gen_pm()
        pm_connector = ''
        if (twp or rge) and pm:
            pm_connector = random.choice([', ', ' of the '])
        return f"{twp}{twprge_connector}{rge}{pm_connector}{pm}"
    
    def gen_desc_qq(self):
        """
        Generate a simple aliquot description.
        :return:
        """
        abbrev_words = self.roll(self.desc_abbrev_wt)
        abbrev_frac = False
        if abbrev_words and self.roll(self.frac_abbrev_wt):
            abbrev_frac = True

        quarter__ = QUARTER_WORD
        half__ = HALF_WORD
        ns_compatible__ = NS_COMPATIBLE_WORD
        ew_compatible__ = EW_COMPATIBLE_WORD
        aliquot_halves__ = ALIQUOT_HALVES_WORD
        aliquot_quarters__ = ALIQUOT_QUARTERS_WORD

        if abbrev_words:
            quarter__ = QUARTER_FRAC
            half__ = HALF_FRAC
            ns_compatible__ = NS_COMPATIBLE_ABBREV
            ew_compatible__ = EW_COMPATIBLE_ABBREV
        if abbrev_frac:
            aliquot_halves__ = ALIQUOT_HALVES_ABBREV
            aliquot_quarters__ = ALIQUOT_QUARTERS_ABBREV

        quarter_wd = self.choose_weighted(quarter__)
        half_wd = self.choose_weighted(half__)
        if not abbrev_words:
            quarter_wd = ' ' + quarter_wd
            half_wd = ' ' + half_wd

        while True:
            of_the = self.choose_weighted(OF_THE)
            if not (half_wd in OF_THE_BLANK_DISALLOWED
                    and quarter_wd in OF_THE_BLANK_DISALLOWED
                    and of_the in OF_THE_BLANK):
                # If not illegal combination, break out and use it.
                break
        if of_the == '' and not abbrev_words:
            of_the = ' '
        desc_list = []
        available_aliquot_groups = aliquot_halves__ + aliquot_quarters__ + [ALL]
        components = []
        while True:
            while True:
                chosen_group = random.choice(available_aliquot_groups)
                if chosen_group == ALL:
                    components = [self.choose_weighted(chosen_group)]
                    return components[0]
                if chosen_group in aliquot_quarters__:
                    # If we've encountered aliquot_quarters__, then aliquot_halves__ are no longer allowed.
                    available_aliquot_groups = aliquot_quarters__
                elif chosen_group in ns_compatible__:
                    # Do not cross "East/West Half" with "North/South Half"
                    available_aliquot_groups = ns_compatible__ + aliquot_quarters__
                elif chosen_group in ew_compatible__:
                    # Do not cross "East/West Half" with "North/South Half"
                    available_aliquot_groups = ew_compatible__ + aliquot_quarters__
                aliquot_component = self.choose_weighted(chosen_group)
                frac = ''  # Default "ALL"
                if aliquot_component in ALIQUOT_HALF_ELEMENTS:
                    frac = half_wd
                elif aliquot_component in ALIQUOT_QUARTER_ELEMENTS:
                    frac = quarter_wd
                components.append(aliquot_component + frac)
                # component_fracs.append(frac)
                if not self.roll(self.qq_continue_wt):
                    break
            desc_list.append(components)
            components = []
            if not self.roll(self.desc_continue_wt):
                break
            # Can't have "ALL" anymore.
            available_aliquot_groups = aliquot_halves__ + aliquot_quarters__
        joined_components = []
        for component_list in desc_list:
            joined_components.append(of_the.join(component_list))
        comma = self.choose_weighted(QQ_COMMA)
        return comma.join(joined_components)

    def gen_desc(self, lots_wt=0.2, both_wt=0.8):
        """
        :param lots_wt: Probability of generating at least one lot.
        :param both_wt: Probability of also generating aliquots
         if lots are also generated. (If lots are not generated,
         will definitely generate aliquots.)
        :return:
        """
        lots_needed = self.roll(lots_wt)
        desc_needed = (not lots_needed) or self.roll(both_wt)
        components = []
        if lots_needed:
            components.append(self.gen_lots())
        if desc_needed:
            components.append(self.gen_desc_qq())
        # Favor putting lots first, which happens more often than not in real data.
        if self.roll(0.8):
            components.reverse()
        return ', '.join(components)

    def gen_lots(self, lot_continue_wt=0.6):
        """
        :param lot_continue_wt: Probability of generating each
         additional lot. (Will always generate at least 1.)
        :return:
        """
        lot_wd = self.choose_weighted(LOT)
        lots = self.choose_multiple(self.avail_lots, min_count=1, repeat_wt=lot_continue_wt)
        and_wd = self.choose_weighted(QQ_COMMA)
        thru_wd = self.choose_weighted(THROUGH)
        return self._elements_to_str_list(
            elements=lots,
            thru_wd=thru_wd,
            and_wd=and_wd,
            thru_wt=0.4,
            type_word=lot_wd,
            plural_s_wt=0.9,
            allow_type_word_everytime=True
        )

    def gen_multisec(self, thru_wt=0.02, repeat_wt=0.01):
        """
        :param thru_wt: Likelihood of using ``'through'`` instead of ``'and'``
         (where possible).
        :param repeat_wt: Likelihood of adding a 3rd (or 4th, etc.) section.
        :return:
        """
        while True:
            out = self.choose_weighted(SECTION)
            # Disallow '§' symbol for multi-sec.
            if out != '§':
                break
        sections = self.choose_multiple(self.avail_sec, min_count=2, repeat_wt=repeat_wt)
        sec_wd = self.choose_weighted(SECTION)
        thru_wd = self.choose_weighted(THROUGH)
        and_wd = self.choose_weighted(MULTISEC_COMMA)
        return self._elements_to_str_list(
            elements=sections,
            thru_wd=thru_wd,
            and_wd=and_wd,
            thru_wt=thru_wt,
            type_word=sec_wd,
            plural_s_wt=0.5,
            allow_type_word_everytime=True
        )

    def _elements_to_str_list(
            self,
            elements: list,
            thru_wd: str,
            and_wd: str,
            thru_wt: float,
            type_word: str,
            plural_s_wt: float,
            allow_type_word_everytime: bool = True):
        """
        Convert a list of `elements` into an appropriate string,
        using the specified words/symbols for 'through' or 'and'.

        Intended use is to convert multiple section numbers or lot
        numbers into a "nice" output, such as:
            [1, 3, 5, 6] --> "sections 1 - 3, 5, 6"
            [9, 12, 13] --> "l.9, l.12, l.13"
        (Actual results are randomized somewhat.)

        :param elements: List of elements (integers) to convert.
        :param thru_wd: Word or symbol for ``'through'``.
        :param and_wd: Word or symbol for ``'and'``.
        :param thru_wt: Probability of using "through" instead of "and"
         (where possible)
        :param type_word: E.g., ``'section'``, ``'sec'``, ``'lot'``, etc.
        :param plural_s_wt: Probability of adding plural 's' to
         ``type_word`` (if allowed).
        :param allow_type_word_everytime: Whether to allow the function
         the chance to put the type word before all elements.
         (e.g., ``"lot 1, lot 2, lot 5"`` if the ``type_word`` is ``'lot'``).
        """
        plural_ok = False
        if type_word not in PLURAL_DISALLOWED and self.roll(plural_s_wt):
            plural_ok = True
        elements = sorted(elements)
        elems_str = [str(elem) for elem in elements]
        if thru_wd in REQUIRE_SPACE or self.roll(0.2):
            thru_wd = f" {thru_wd} "
        if and_wd in REQUIRE_SPACE:
            and_wd = f" {and_wd} "

        # Figure out what goes between each pair of [lots/sections]:
        # i.e., "[Lot/Sec] 1 - 3, 5, 6 - 12"  (Note that ',' might alternatively be ' and ' etc.)
        throughs_ands = []
        for i in range(len(elements) - 1):
            l_i = elements[i]
            l_j = elements[i + 1]
            # Can't have 2 consecutive "through" -- i.e., disallow "[Lots/Sections] 1 - 3 - 5".
            through_was_last = False
            if len(throughs_ands) > 0 and throughs_ands[-1] == thru_wd:
                through_was_last = True
            if l_j - l_i > 1 and not through_was_last and self.roll(thru_wt):
                # Avoid using "through" between consecutively numbered lots/sections.
                # i.e., "Lots 1 - 2" should only be "Lots 1, 2".
                throughs_ands.append(thru_wd)
            else:
                throughs_ands.append(and_wd)

        plural_s = ''
        if len(elements) > 1 and plural_ok:
            plural_s = 's'
        type_word_everytime = False
        if allow_type_word_everytime and (type_word in PLURAL_DISALLOWED or not plural_ok) and self.roll(0.9):
            # For example, to render "L.3, L.5-L.7" or "L3, L5-L7"
            type_word_everytime = True
        space = ' '
        if type_word in SECTION_LOT_NOSPACE_OK and self.roll(0.95):
            # 'L1' vs 'L 1', etc.
            space = ''
        if type_word_everytime:
            elems_str = [f"{type_word}{plural_s}{space}{elem}" for elem in elems_str]
        else:
            # Remember `elements` is in sorted order.
            elems_str[0] = f"{type_word}{plural_s}{space}{elems_str[0]}"
        out = elems_str.pop(0)  # Start with first element.
        for connector, elem in zip(throughs_ands, elems_str):
            out += f'{connector}{elem}'
        return out


import os
import pickle


class WordFilter:
    domain_set = (
        "ing-bio",
        "ing-recipedb",
        "foodname-recipedb",
        "commons",
    )

    def __init__(self, config, filter_exact=True, domains=list(domain_set)):
        self.config = config
        self.filter_exact = filter_exact
        self.data_dir = config.data_dir
        self.bio_data_path = self.data_dir + "/biomedical/"
        self.recipedb_data_path = self.data_dir + "/recipedb/"
        self.commons_path = self.data_dir + "/commons/"
        self.filter_dict = {d: self.get_domain_words(d) for d in domains}

    def _parse_txt(self, f, include_tab=True):
        res = []
        for l in f:
            if include_tab:
                lsp = l.split("\t")
                if len(lsp) == 2:
                    if len(lsp[0]) > 3:
                        res.append(lsp[0])
            else:
                res.append(l.strip())
        return set(res)

    def get_domain_words(self, d):
        if d == "ing-bio":
            with open(f"{self.bio_data_path}/ingredient_dic.pkl", "rb") as f:
                return pickle.load(f)

        elif d == "ing-recipedb":
            with open(os.path.join(self.recipedb_data_path, "ing.txt"), "r") as f:
                return self._parse_txt(f)

        elif d == "foodname-recipedb":
            with open(
                os.path.join(self.recipedb_data_path, "food_names.txt"), "r"
            ) as f:
                return self._parse_txt(f)

        elif d == "commons":
            with open(os.path.join(self.commons_path, "all_20230918.txt"), "r") as f:
                return self._parse_txt(f, include_tab=False)

    def set_domain(self, domain):
        self.current_domain = domain

    def is_in_filter_using_current_domain(self, sen):
        if self.current_domain is None:
            raise ValueError(f"current_domain is None / set_domain first")
        _in = False
        sen_sp = sen.split(" ")
        for fw in self.filter_dict[self.current_domain]:
            fw_sp = fw.split(" ")
            if len(fw_sp) > 1:
                if fw in sen:
                    _in = True
                    break
            elif len(fw_sp) == 1:
                for _token_in_sen in sen_sp:
                    if (fw_sp[0] == _token_in_sen and self.filter_exact) or (
                        fw_sp[0] in _token_in_sen and not self.filter_exact
                    ):
                        _in = True
                        break

            else:
                pass

        return _in

    def is_in_filter(self, sen):
        _res = False
        for domain_key, _ in self.filter_dict.items():
            self.set_domain(domain_key)
            _in = self.is_in_filter_using_current_domain(sen)
            if _in:
                _res = True
        return _res

    def __str__(self):
        return f"[ Filter : filter_dict keys = {self.filter_dict.keys()} ]"

    def __repr__(self):
        return self.__str__()

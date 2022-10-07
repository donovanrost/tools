import subprocess
from os.path import abspath, dirname
import yaml


class AnsibleModuleInstaller:
    __path_to_ansible = f"{dirname(abspath(__file__))}/ansible"
    __path_to_playbook = f"{__path_to_ansible}/site.yml"
    __path_to_inventory = f"{__path_to_ansible}/inventory/hosts.yml"
    __roles = []

    def __init__(self):
        self.__gather_roles()

    def get_modules(self):
        return self.__roles

    def install_modules(self, modules):
        base_cmd = f"ansible-playbook {self.__path_to_playbook} -i {self.__path_to_inventory}"

        if not modules:
            return
        for module in modules:
            base_cmd += f" --tags \"{module}\""
        subprocess.run(base_cmd, shell=True)

    def __gather_roles(self):
        # the playbook can have multiple plays
        # right now there's only one play, so I'm
        # just going to handle this special single play case
        playbook = None
        with open(self.__path_to_playbook, 'r') as file:
            playbook = yaml.safe_load(file)

        if not playbook:
            return []

        play = playbook[0]
        roles = []
        for entry in play.items():
            if entry[0] == "roles":
                roles = entry[1]

        self.__roles = roles
        return roles

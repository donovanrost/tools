import subprocess
from collections import namedtuple
from os.path import abspath, dirname

from ansible import context
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context


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

        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=[self.__path_to_inventory])
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        context.CLIARGS = ImmutableDict(
            connection='local',
            syntax=None,
            forks=10,
            become=None,
            become_method=None,
            become_user=None,
            check=False,
            diff=False,
            start_at_task=None,
            tags=modules
        )

        playbook = PlaybookExecutor(
            playbooks=[self.__path_to_playbook],
            inventory=inventory,
            loader=loader,
            passwords={},
            variable_manager=variable_manager,
        )

        playbook.run()

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

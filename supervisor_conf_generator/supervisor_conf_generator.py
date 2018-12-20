#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import xprint as xp


class Generator:
    def __init__(self,
                 name: str,
                 directory: str = None,
                 command: str = None,
                 user: str = None,
                 auto_start: bool = True,
                 auto_restart: bool = True,
                 start_retries: int = 5,
                 redirect_stderr: bool = True,
                 stdout_logfile: str or None = '',
                 ):
        self._name = name
        self._directory = directory
        self._command = command
        self._user = user
        self._auto_start = auto_start
        self._auto_restart = auto_restart
        self._start_retries = start_retries
        self._redirect_stderr = redirect_stderr
        self._stdout_logfile = stdout_logfile

    @property
    def __invalid_attributes(self):
        keys = [
            'name',
            'command',
        ]

        for key in keys:
            if not getattr(self, '_{}'.format(key)):
                xp.error('Attribute `{}` is invalid.'.format(key))
                return True
        return False

    @property
    def stdout_logfile(self):
        if self._stdout_logfile is None:
            return 'NONE'
        return self._stdout_logfile or '/var/log/supervisor_{name}.log'.format(name=self._name)

    def write(self, path_to_conf: str = None):
        if self.__invalid_attributes:
            return None

        file = path_to_conf or '/etc/supervisor/conf.d/{name}.conf'.format(name=self._name)

        xp.about_t('Generate', file, 'for supervisor')

        # name
        configs = list()
        configs.append('[program:{name}]'.format(name=self._name))
        if self._directory:
            configs.append('directory={directory}'.format(directory=self._directory))
        configs.append('command={command}'.format(command=self._command))
        if self._user:
            configs.append('user={user}'.format(user=self._user))
        if self._auto_start:
            configs.append('autostart=true')
        if self._auto_restart:
            configs.append('autorestart=true')
        if self._start_retries:
            configs.append('startretries={start_retries}'.format(start_retries=self._start_retries))
        if self._redirect_stderr:
            configs.append('redirect_stderr=true')
        configs.append('stdout_logfile={stdout_logfile}'.format(stdout_logfile=self.stdout_logfile))

        # write
        configs = '\n'.join(configs)
        with open(file, 'wb') as f:
            f.write(configs.encode('utf-8'))
        xp.success()
        xp.wr(xp.Fore.LIGHTBLACK_EX + configs)
        xp.fx()

        return file

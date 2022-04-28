#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Trading Agent Base Class

Defines general trading API functionalities.

Todo:
    * ...
"""

# Built-in modules

# Third-party modules

# Local modules


class TradingAgent():
    """Trading Agent Class.

    Defines generation infrastructures and provides related information.
    """

    def __init__(self, name: str = 'def_agent', settings: dict = {}):
        """Initialization Function.

        Args:
            name (str, optional): Agent's name. Defaults to 'def_agent'.
            settings (dict, optional): Agent's settings. Defaults to {}.
        """

        self.settings = self._define_and_sanitize_settings(settings)

    def __repr__(self):
        return 'Trading Agent'

    def apply_policy(*args, **kwargs):
        error_msg = "You need to implement your agent's apply_policy method."
        raise NotImplementedError(error_msg)

    def _define_and_sanitize_settings(self, settings: dict) -> dict:
        """Define and sanitize settings dictionary.

        Args:
            settings (dict): User inputed dictionaries.

        Raises:
            ValueError: If incorrect setting keys inputed.

        Returns:
            dict: Sanitized settings dictionary.
        """

        def_settings = self.get_default_settings()

        # Verify only authorized keys were inputed
        for k in settings.keys():
            if k not in def_settings.keys():
                error_msg = f"Unknown agent setting: {k}"
                raise ValueError(error_msg)

        sanitized_settings = def_settings
        sanitized_settings.update(settings)

        return sanitized_settings

    @staticmethod
    def get_default_settings() -> dict:
        """Returns the class' default settings dictionary.

        Returns:
            dict: Default settings dictionary.
        """

        def_config = {}

        return def_config

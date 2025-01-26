from dataclasses import dataclass, asdict

__all__ = [
    "Config"
]


@dataclass
class Config:
    """
    A supercharged dataclass for all config classes
    """
    @classmethod
    def load(cls, path, **kwargs):
        """
        Load a config from a yaml file and convert to the proper class.
        """
        from omegaconf import OmegaConf

        config_dict = OmegaConf.to_container(OmegaConf.load(path))

        config = cls.from_dict(config_dict, **kwargs)

        return config

    @classmethod
    def from_dict(cls, config_dict, **kwargs):
        """
        Load a config dataclass using an input dict
        """
        config_dict.update(kwargs)

        dict_config = {k: v for k, v in config_dict.items() if k in cls.fields() and cls.fields()[k].init}

        config = cls(**dict_config)  # noqa

        return config

    def dict(self):
        """
        Helper function to convert the dataclass to dict
        """
        return asdict(self)

    def __len__(self):
        """
        Get the size of the fields in the dataclass.
        """
        return len(self.dict())

    def __iter__(self):
        """
        Helper function to treat the dataclass as dict.
        """
        return iter(self.dict())

    @classmethod
    def fields(cls):
        """
        Get the dictionary of the fields of the dataclass
        """
        return cls.__dataclass_fields__  # noqa

    def keys(self):
        """
        Get dataclass field keys
        """
        return list(self.dict().keys())

    def get(self, key, default=None):
        """
        Get a value of the dataclass field
        """
        return getattr(self, key, default)

    def update(self, d: dict, **kwargs):
        """
        Update dataclass fields by passing dict or keyword arguments.
        """
        d.update(**kwargs)
        for k, v in d.items():
            if k not in self.fields():
                continue
            setattr(self, k, v)
        return self

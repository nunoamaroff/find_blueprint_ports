import os
import yaml
from pathlib import Path
from multiprocessing import Pool
from dotenv import load_dotenv

load_dotenv()


# https://stackoverflow.com/questions/25108581/python-yaml-dump-bad-indentation
class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


def read_ports(yaml_path: Path):
    """
    Reads YAML file looking for used ports and returns them.
    To be used in parallel for faster parsing of entire repository.

    Example YAML port mapping:

    ports:
        loadbalancer_ports:
            - XXXX
        service_ports:
            - XXXX

    :param yaml_path: absolute path to YAML file
    :return:
    """

    with open(yaml_path, 'r') as yaml_stream:
        try:
            yaml_dict = yaml.safe_load(yaml_stream)
            ports = yaml_dict.get("ports")
            return ports.get("service_ports", []) if ports else []
        except yaml.YAMLError:
            print(f"Failed to read {yaml_path.name}")


if __name__ == "__main__":

    pool = Pool()
    map_result = pool.map(read_ports, list(Path(os.getenv("BLUEPRINT_REPO")).rglob("*.yaml")))

    cleaned_result = {
        "free_ports": list(
            set(range(9000, 10000)) - set(sorted([port[0] for port in map_result if port]))
        )
    }

    # custom dumper for correct indentation
    with open('results.yaml', 'w') as result_stream:
        yaml.dump(data=cleaned_result, stream=result_stream, Dumper=IndentDumper, default_flow_style=False)

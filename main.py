import json
import os

import utils.scripts as scripts
from experiment import start_experiment
from store.text.logger import Logger
from utils.model_api import get_model_apis, get_toolkit_apis


def process_json(content: str):
    """
    处理json文件，生成实验文件夹，返回实验id
    :param content:
    :return:
    """
    json_data = json.loads(content)
    # 应该不需要检查id是否重复
    experiment_id = scripts.generate_experiment_id()
    json_data["experiment_id"] = experiment_id
    os.makedirs(os.path.join("experiments", experiment_id), exist_ok=True)

    json_data["agents_num"] = len(json_data["agent_list"])
    format_num_len = max(2, json_data["agents_num"])

    agnet_model_dict = dict()
    role_list = set()
    for idx, agent in enumerate(json_data["agent_list"]):
        agent["agent_id"] = idx
        agent_path = os.path.join("experiments", experiment_id, f"agent_{idx:0{format_num_len}}")
        os.makedirs(agent_path, exist_ok=True)
        with open(os.path.join(agent_path, "agnet_config.json"), "w") as f:
            json.dump(agent, f)
        agnet_model_dict[idx] = agent["model_settings"]
        role_list.add(agent["role"])

    json_data["agnet_model_dict"] = agnet_model_dict
    json_data["role_list"] = list(role_list)

    with open(os.path.join("experiments", experiment_id, "config.json"), "w") as f:
        json.dump(json_data, f)

    # 现在只返回了id
    return experiment_id


if __name__ == '__main__':
    with open("test/files4test/expe_config.json", "r") as f:
        content = f.read()
    experiment_id = process_json(content)

    # experiment_id = "20210417_1703_00"
    try:
        with open(os.path.join("experiments", experiment_id, "config.json"), "r") as f:
            expe_config_json = json.load(f)
    except:
        print("experiment id {} not found".format(experiment_id))
        assert False
    model_apis = get_model_apis(expe_config_json["agnet_model_dict"])
    external_toolkit_apis = get_toolkit_apis(expe_config_json["external_toolkit"])

    # start_experiment(expe_config_json, model_apis, external_toolkit_apis)

    # test_chat = model_apis[0].chat(
    #     "write a passage about the life of a person who has made a difference to the world,at least 5000 words")
    # print(test_chat)

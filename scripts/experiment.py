"""
@author: Guo Shiguang
@software: PyCharm
@file: experiment.py
@time: 2023/4/17 17:03
"""
import importlib
import inspect
import os

from src.exp.actions import BaseAction
from src.exp.agents.agent import Agent
from src.exp.expe_info import ExpeInfo
from src.store.text.logger import Logger


def register_action(expinfo: ExpeInfo, action_path='../src/exp/actions'):
    """
    遍历指定目录下所有文件，将所有action类注册到actions字典中
    :param action_path:
    :return:
    """
    actions = {}

    for root, dirs, files in os.walk(action_path):
        for file in files:
            if file.endswith('.py'):
                # TODO 更好的提取文件的方式
                module_name = root.replace('/', '.') + '.' + file[:-3]
                module_name = module_name.replace('...', '')
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, BaseAction):
                        actions[name] = obj(expinfo)

    return actions


def start_experiment(experiment_config, model_api, external_toolkit_api=None):
    """
    :param experiment_config:
    :param model_api:
    :param external_toolkit_api:
    :return:
    """
    logger = Logger()

    pipeline = ["Setup"]
    experiment_settings = experiment_config['experiment_settings']
    for step in experiment_settings["pipeline"]:
        pipeline.extend([step["action"]] * int(step["times"]))

    # TODO 完善执行逻辑
    agents_list = []
    for agent in experiment_config["agent_list"]:
        agents_list.append(Agent(agent_id=agent["agent_id"], role=agent["role"], profile=agent["profile"],
                                 agent_path=agent["agent_path"]))

    exp_info = ExpeInfo(agents=agents_list, models=model_api, toolkits=external_toolkit_api,
                        config=experiment_config)

    actions = register_action(exp_info, )

    for expe_round in range(experiment_settings["round_nums"]):
        for step in pipeline:
            actions[step].run()
            while True:
                logger.info("Round {} finished".format(expe_round), )
                user_input = input("press Enter to continue or check agnents' status")
                if user_input.strip() == "":
                    break
                elif user_input.strip().startswith("probe"):
                    # TODO check if  agent_id is valid
                    try:
                        agent_id = int(user_input.strip().split()[1])
                        probe_message = user_input.strip().split()[2]
                        if agent_id not in exp_info.get_agent_ids():
                            logger.warning("Invalid agent_id")
                            logger.info("Valid agent_id: {}".format(exp_info.get_agent_ids()))
                        actions["probe"].run(agent_id, probe_message)
                    except:
                        logger.warning("Invalid input, usage: probe [agent_id] [message]")
                elif user_input.strip().startswith("instuct"):
                    try:
                        agent_id = int(user_input.strip().split()[1])
                        instuct_message = user_input.strip().split()[2]
                        if agent_id not in exp_info.get_agent_ids():
                            logger.warning("Invalid agent_id")
                            logger.info("Valid agent_id: {}".format(exp_info.get_agent_ids()))
                        actions["instuct"].run(agent_id, instuct_message)
                    except:
                        logger.warning("Invalid input, usage: instuct [agent_id] [message]")
                else:
                    logger.warning("Invalid input")

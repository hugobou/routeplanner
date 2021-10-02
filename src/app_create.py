from configparser import ConfigParser
import logging
import mapreader as mr
import traffic as tf
from application import Application
from model.features import FeaturesEncoder
from model.model import Model
from model.modelbuilder import load_model


def app_create(config_file_name = '/routeplanner/config/routeplanner.cfg'):
    (gml_file_name, pm_dict_file_name, model_params_file_name) = read_config(config_file_name)

    logging.info("Reading map")
    graph = mr.ReadMap(gml_file_name)

    logging.info("Traffic info preparation")
    tf.reset_traffic_info(graph)
    tm_dict = tf.read_tm_dict(pm_dict_file_name)

    logging.info("Loading model")
    model = Model(load_model(model_params_file_name))

    feature_encoder = FeaturesEncoder()

    return Application(graph, tm_dict, model, feature_encoder)


def read_config(config_file_name):
    configparser = ConfigParser()
    configparser.read(config_file_name)
    gml_file_name = configparser.get('config_files', 'gml_file_name')
    pm_dict_file_name = configparser.get('config_files', 'pm_dict_file_name')
    model_params_file_name = configparser.get('config_files', 'model_params_file_name')
    return gml_file_name, pm_dict_file_name, model_params_file_name
